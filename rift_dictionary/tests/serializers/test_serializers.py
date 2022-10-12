import io
from django.test import TestCase
from rest_framework.parsers import JSONParser
from rift_dictionary.serializers import WordSerializer
from rift_dictionary.models import Word, WordDefinition, WordMeaning
import django

RESPONSE = """[{"word":"rift","phonetic":"/ɹɪft/","phonetics":[{"text":"/ɹɪft/","audio":""}],"meanings":[{"partOfSpeech":"noun","definitions":[{"definition":"A chasm or fissure.","synonyms":[],"antonyms":[],"example":"My marriage is in trouble: the fight created a rift between us and we can't reconnect."},{"definition":"A break in the clouds, fog, mist etc., which allows light through.","synonyms":[],"antonyms":[]},{"definition":"A shallow place in a stream; a ford.","synonyms":[],"antonyms":[]}],"synonyms":[],"antonyms":[]},{"partOfSpeech":"verb","definitions":[{"definition":"To form a rift; to split open.","synonyms":[],"antonyms":[]},{"definition":"To cleave; to rive; to split.","synonyms":[],"antonyms":[],"example":"to rift an oak"}],"synonyms":[],"antonyms":[]}],"license":{"name":"CC BY-SA 3.0","url":"https://creativecommons.org/licenses/by-sa/3.0"},"sourceUrls":["https://en.wiktionary.org/wiki/rift"]},{"word":"rift","phonetic":"/ɹɪft/","phonetics":[{"text":"/ɹɪft/","audio":""}],"meanings":[{"partOfSpeech":"verb","definitions":[{"definition":"(obsolete outside Scotland and northern Britain) To belch.","synonyms":[],"antonyms":[]}],"synonyms":[],"antonyms":[]}],"license":{"name":"CC BY-SA 3.0","url":"https://creativecommons.org/licenses/by-sa/3.0"},"sourceUrls":["https://en.wiktionary.org/wiki/rift"]}]"""

django.setup()


class WordSerializerTest(TestCase):
    def test_word_id_is_correctly_serialized(self):
        data = io.BytesIO(RESPONSE.encode('utf-8'))
        json_data = JSONParser().parse(data)
        serializer = WordSerializer(data=json_data, many=True)
        is_valid = serializer.is_valid()
        self.assertTrue(is_valid)

    def test_word_has_three_meanings(self):
        data = io.BytesIO(RESPONSE.encode('utf-8'))
        json_data = JSONParser().parse(data)
        serializer = WordSerializer(data=json_data, many=True)
        is_valid = serializer.is_valid()
        self.assertTrue(serializer.save())
        self.assertEqual(len(WordMeaning.objects.all()), 3)

    def test_word_has_six_definitions(self):
        data = io.BytesIO(RESPONSE.encode('utf-8'))
        json_data = JSONParser().parse(data)
        serializer = WordSerializer(data=json_data, many=True)
        is_valid = serializer.is_valid()
        self.assertTrue(serializer.save())
        self.assertEqual(len(WordDefinition.objects.all()), 6)

    def test_retrieved_words_contains_id_in_all_their_objects(self):
        word = Word.objects.create(word='word', phonetic='phonetic')
        meaning = WordMeaning.objects.create(word=word, part_of_speech='Verb')
        definition = WordDefinition.objects.create(
            word_meaning=meaning, definition='Def', example='Example')

        word_serializer = WordSerializer(word)
        data = word_serializer.data
        self.assertEqual(data['meanings'][0]['id'], 1)
        self.assertEqual(data['meanings'][0]['definitions'][0]['id'], 1)
