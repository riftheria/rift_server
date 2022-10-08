from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rift_dictionary import models
import requests
import io
from rest_framework.parsers import JSONParser
from rift_dictionary.serializers import WordSerializer
from rift_dictionary.models import Word
from rest_framework.decorators import api_view
import json


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


def save_word_from_free_api(word):
    free_api_word_url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}'
    free_api_response = requests.get(url=free_api_word_url)
    word_bytes = io.BytesIO(free_api_response.content)
    json_data = JSONParser().parse(word_bytes)
    word_serializer = WordSerializer(data=json_data, many=True)
    if word_serializer.is_valid():
        word_serializer.save()
    else:
        return word_serializer.errors


@api_view(['GET'])
def get_word_list(request):
    requested_words = list(request.GET.values())
    words_already_in_database = Word.objects.filter(word__in=requested_words)
    words_already_in_database_count = words_already_in_database.count()
    if words_already_in_database_count == len(requested_words):
        word_serializer = WordSerializer(words_already_in_database, many=True)
        return Response(word_serializer.data)
    words_names_in_database = words_already_in_database.values_list(
        'word', flat=True)
    words_not_in_database = list(
        set(requested_words)-set(words_names_in_database))
    for requested_word in words_not_in_database:
        save_word_from_free_api(requested_word)
    word_list_response = Word.objects.filter(word__in=requested_words)
    word_serializer = WordSerializer(word_list_response, many=True)
    return Response(word_serializer.data)
