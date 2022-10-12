from calendar import leapdays
from typing_extensions import Required
from wsgiref import validate
from rest_framework import serializers
from rift_dictionary.models import Word, WordDefinition, WordMeaning


class WordDefinitionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    definition = serializers.CharField(required=False)
    example = serializers.CharField(required=False)

    class Meta:
        model = WordDefinition
        fields = ['id', 'definition', 'example']


class WordMeaningSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    partOfSpeech = serializers.CharField(source='part_of_speech')
    definitions = WordDefinitionSerializer(many=True)

    def create(self, validated_data):
        return WordMeaning.objects.create(part_of_speech='sop')

    class Meta:
        model = WordMeaning
        fields = ['id', 'partOfSpeech', 'definitions']


class WordListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        first_word = validated_data[0]
        word_name = first_word['word']
        word_phonetic = first_word.get('phonetic')
        saved_word = Word.objects.create(
            word=word_name, phonetic=word_phonetic)
        data_length = len(validated_data)
        for index in range(data_length):
            meanings = validated_data[index]['meanings']
            for meaning in meanings:
                saved_meaning = WordMeaning.objects.create(
                    word=saved_word, part_of_speech=meaning['part_of_speech'])
                definitions = meaning['definitions']
                for definition in definitions:
                    WordDefinition.objects.create(
                        word_meaning=saved_meaning, **definition)

        return saved_word


class WordSerializer(serializers.ModelSerializer):
    phonetic = serializers.CharField(required=False)
    meanings = WordMeaningSerializer(many=True)

    class Meta:
        model = Word
        fields = ['word', 'phonetic', 'meanings']
        list_serializer_class = WordListSerializer
