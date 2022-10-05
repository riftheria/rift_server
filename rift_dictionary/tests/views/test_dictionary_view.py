from rest_framework.test import APITestCase
from rest_framework import status
from httmock import HTTMock, urlmatch, response
from rift_dictionary.models import Word


@urlmatch(netloc='https://api.dictionaryapi.dev/api/v2/entries/en/invalid_word')
def word_not_found_mock(url, request):
    return response(404, """{"title":"No Definitions Found","message":"Sorry pal, we couldn't find definitions for the word you were looking for.","resolution":"You can try the search again at later time or head to the web instead."}""")


@urlmatch(netloc='https://api.dictionaryapi.dev/api/v2/entries/en/rift')
def word_response(url, request):
    return """[{"word":"rift","phonetic":"/ɹɪft/","phonetics":[{"text":"/ɹɪft/","audio":""}],"meanings":[{"partOfSpeech":"noun","definitions":[{"definition":"A chasm or fissure.","synonyms":[],"antonyms":[],"example":"My marriage is in trouble: the fight created a rift between us and we can't reconnect."},{"definition":"A break in the clouds, fog, mist etc., which allows light through.","synonyms":[],"antonyms":[]},{"definition":"A shallow place in a stream; a ford.","synonyms":[],"antonyms":[]}],"synonyms":[],"antonyms":[]},{"partOfSpeech":"verb","definitions":[{"definition":"To form a rift; to split open.","synonyms":[],"antonyms":[]},{"definition":"To cleave; to rive; to split.","synonyms":[],"antonyms":[],"example":"to rift an oak"}],"synonyms":[],"antonyms":[]}],"license":{"name":"CC BY-SA 3.0","url":"https://creativecommons.org/licenses/by-sa/3.0"},"sourceUrls":["https://en.wiktionary.org/wiki/rift"]},{"word":"rift","phonetic":"/ɹɪft/","phonetics":[{"text":"/ɹɪft/","audio":""}],"meanings":[{"partOfSpeech":"verb","definitions":[{"definition":"(obsolete outside Scotland and northern Britain) To belch.","synonyms":[],"antonyms":[]}],"synonyms":[],"antonyms":[]}],"license":{"name":"CC BY-SA 3.0","url":"https://creativecommons.org/licenses/by-sa/3.0"},"sourceUrls":["https://en.wiktionary.org/wiki/rift"]}]"""


class TestDictionaryView(APITestCase):

    def test_dictionary_response_is_ok(self):
        response = self.client.get('/dictionary/rift/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_dictionary_response_is_not_found_for_invalid_word(self):
        with HTTMock(word_not_found_mock):
            response = self.client.get('/dictionary/invalid_word/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_word_is_saved_on_database(self):
        with HTTMock(word_response):
            self.client.get('/dictionary/rift/')
        words_count = Word.objects.count()
        self.assertEquals(words_count, 1)

    def test_word_is_retrieved_from_database_the_second_time(self):
        with HTTMock(word_response):
            self.client.get('/dictionary/rift/')
            second_response = self.client.get('/dictionary/rift/')
        words_count = Word.objects.count()
        self.assertEquals(words_count, 1)
        self.assertEquals(second_response.status_code, status.HTTP_200_OK)
