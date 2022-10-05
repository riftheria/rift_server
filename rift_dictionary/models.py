from unittest.util import _MAX_LENGTH
from django.db import models


class Word(models.Model):
    word = models.CharField(max_length=100, primary_key=True)
    phonetic = models.CharField(max_length=100, null=True, blank=True)


class WordMeaning(models.Model):
    word = models.ForeignKey(
        Word, related_name='meanings', on_delete=models.CASCADE)
    part_of_speech = models.CharField(max_length=100)


class WordDefinition(models.Model):
    word_meaning = models.ForeignKey(
        WordMeaning, related_name='definitions', on_delete=models.CASCADE)
    definition = models.CharField(max_length=1000)
    example = models.CharField(max_length=1000)
