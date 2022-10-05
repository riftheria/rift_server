import json
from os import stat
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rift_dictionary import models
import requests
import io
from rest_framework.parsers import JSONParser
from rift_dictionary.serializers import WordSerializer


class DictionaryView(APIView):
    def get(self, request, word):
        word_data = models.Word.objects.filter(word=word).first()
        if (word_data is None):
            response = Response(status=status.HTTP_404_NOT_FOUND)
            external_dictionary_response = requests.get(
                url=f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}')
            if external_dictionary_response.status_code == status.HTTP_200_OK:
                word_content = external_dictionary_response.content
                external_response_bytes = io.BytesIO(word_content)
                json_data = JSONParser().parse(external_response_bytes)
                word_serializer = WordSerializer(data=json_data, many=True)
                if word_serializer.is_valid():
                    word_serializer.save()
                    response = Response(word_serializer.validated_data[0])
                else:
                    response = Response(
                        data=word_serializer.errors, status=404)
        else:
            word_serializer = WordSerializer(word_data, )
            response = Response(word_serializer.data)

        return response
