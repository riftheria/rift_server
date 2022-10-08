import gzip
from typing import OrderedDict
from unittest import mock
from rest_framework.test import APITestCase
from rest_framework import status
from httmock import HTTMock, urlmatch, response, all_requests
from rift_dictionary.models import Word


@all_requests
def word_not_found_mock(url, request):
    return {'status_code': 404, 'content': """{"title":"No Definitions Found","message":"Sorry pal, we couldn't find definitions for the word you were looking for.","resolution":"You can try the search again at later time or head to the web instead."}"""}


@all_requests
def word_response_mock(url, request):
    response = None
    if request.url == 'https://api.dictionaryapi.dev/api/v2/entries/en/rift':
        response = """[{"word":"rift","phonetic":"/ɹɪft/","phonetics":[{"text":"/ɹɪft/","audio":""}],"meanings":[{"partOfSpeech":"noun","definitions":[{"definition":"A chasm or fissure.","synonyms":[],"antonyms":[],"example":"My marriage is in trouble: the fight created a rift between us and we can't reconnect."},{"definition":"A break in the clouds, fog, mist etc., which allows light through.","synonyms":[],"antonyms":[]},{"definition":"A shallow place in a stream; a ford.","synonyms":[],"antonyms":[]}],"synonyms":[],"antonyms":[]},{"partOfSpeech":"verb","definitions":[{"definition":"To form a rift; to split open.","synonyms":[],"antonyms":[]},{"definition":"To cleave; to rive; to split.","synonyms":[],"antonyms":[],"example":"to rift an oak"}],"synonyms":[],"antonyms":[]}],"license":{"name":"CC BY-SA 3.0","url":"https://creativecommons.org/licenses/by-sa/3.0"},"sourceUrls":["https://en.wiktionary.org/wiki/rift"]},{"word":"rift","phonetic":"/ɹɪft/","phonetics":[{"text":"/ɹɪft/","audio":""}],"meanings":[{"partOfSpeech":"verb","definitions":[{"definition":"(obsolete outside Scotland and northern Britain) To belch.","synonyms":[],"antonyms":[]}],"synonyms":[],"antonyms":[]}],"license":{"name":"CC BY-SA 3.0","url":"https://creativecommons.org/licenses/by-sa/3.0"},"sourceUrls":["https://en.wiktionary.org/wiki/rift"]}]"""
    elif request.url == 'https://api.dictionaryapi.dev/api/v2/entries/en/something':
        response = """[{"word":"something","phonetic":"/ˈsamθɪŋ/","phonetics":[{"text":"/ˈsamθɪŋ/","audio":""},{"text":"/ˈsʌmθɪŋ/","audio":""},{"text":"/ˈsʌmθɪŋ/","audio":"https://api.dictionaryapi.dev/media/pronunciations/en/something-us.mp3","sourceUrl":"https://commons.wikimedia.org/w/index.php?curid=471130","license":{"name":"BY-SA 3.0","url":"https://creativecommons.org/licenses/by-sa/3.0"}}],"meanings":[{"partOfSpeech":"noun","definitions":[{"definition":"An object whose nature is yet to be defined.","synonyms":[],"antonyms":[]},{"definition":"An object whose name is forgotten by, unknown or unimportant to the user, e.g., from words of a song. Also used to refer to an object earlier indefinitely referred to as 'something' (pronoun sense).","synonyms":[],"antonyms":[]}],"synonyms":[],"antonyms":[]},{"partOfSpeech":"verb","definitions":[{"definition":"Applied to an action whose name is forgotten by, unknown or unimportant to the user, e.g. from words of a song.","synonyms":[],"antonyms":[]}],"synonyms":[],"antonyms":[]},{"partOfSpeech":"adjective","definitions":[{"definition":"Having a characteristic that the speaker cannot specify.","synonyms":[],"antonyms":[]}],"synonyms":[],"antonyms":[]},{"partOfSpeech":"adverb","definitions":[{"definition":"(degree) Somewhat; to a degree.","synonyms":[],"antonyms":[],"example":"The baby looks something like his father."},{"definition":"(degree) To a high degree.","synonyms":[],"antonyms":[]}],"synonyms":[],"antonyms":[]},{"partOfSpeech":"pronoun","definitions":[{"definition":"An uncertain or unspecified thing; one thing.","synonyms":[],"antonyms":[],"example":"I have a feeling something good is going to happen today."},{"definition":"(of someone or something) A quality to a moderate degree.","synonyms":[],"antonyms":[],"example":"That child is something of a genius."},{"definition":"(of a person) A talent or quality that is difficult to specify.","synonyms":[],"antonyms":[],"example":"She has a certain something."},{"definition":"(often with really or quite) Somebody who or something that is superlative or notable in some way.","synonyms":[],"antonyms":[],"example":"- Some marmosets are less than six inches tall.\n- Well, isn't that something?"}],"synonyms":["je ne sais quoi","sth"],"antonyms":[]}],"license":{"name":"CC BY-SA 3.0","url":"https://creativecommons.org/licenses/by-sa/3.0"},"sourceUrls":["https://en.wiktionary.org/wiki/something"]}]"""
    elif request.url == 'https://api.dictionaryapi.dev/api/v2/entries/en/everywhere':
        response = """[{"word":"everywhere","phonetic":"/ɛv.ɹi.(h)weə(ɹ)/","phonetics":[{"text":"/ɛv.ɹi.(h)weə(ɹ)/","audio":""},{"text":"/ɛv.ɹi.(h)wɛɹ/","audio":"https://api.dictionaryapi.dev/media/pronunciations/en/everywhere-us.mp3","sourceUrl":"https://commons.wikimedia.org/w/index.php?curid=1676757","license":{"name":"BY-SA 3.0","url":"https://creativecommons.org/licenses/by-sa/3.0"}}],"meanings":[{"partOfSpeech":"adverb","definitions":[{"definition":"In or to all locations under discussion.","synonyms":[],"antonyms":[],"example":"He delivers the mail everywhere on this street."},{"definition":"In or to a few or more locations.","synonyms":[],"antonyms":[],"example":"I've looked everywhere in the house and still can't find my glasses."}],"synonyms":[],"antonyms":["nowhere"]}],"license":{"name":"CC BY-SA 3.0","url":"https://creativecommons.org/licenses/by-sa/3.0"},"sourceUrls":["https://en.wiktionary.org/wiki/everywhere"]}]"""

    return {'status_code': 200, 'content': response.replace("'", "\'").replace("\n", "")}


@all_requests
def word_empty_response(url, request):
    return ''


@all_requests
def word_partial_response_mock(url, request):
    response = None
    if request.url == 'https://api.dictionaryapi.dev/api/v2/entries/en/rift':
        response = ''
    elif request.url == 'https://api.dictionaryapi.dev/api/v2/entries/en/something':
        response = ''
    elif request.url == 'https://api.dictionaryapi.dev/api/v2/entries/en/everywhere':
        response = """[{"word":"everywhere","phonetic":"/ɛv.ɹi.(h)weə(ɹ)/","phonetics":[{"text":"/ɛv.ɹi.(h)weə(ɹ)/","audio":""},{"text":"/ɛv.ɹi.(h)wɛɹ/","audio":"https://api.dictionaryapi.dev/media/pronunciations/en/everywhere-us.mp3","sourceUrl":"https://commons.wikimedia.org/w/index.php?curid=1676757","license":{"name":"BY-SA 3.0","url":"https://creativecommons.org/licenses/by-sa/3.0"}}],"meanings":[{"partOfSpeech":"adverb","definitions":[{"definition":"In or to all locations under discussion.","synonyms":[],"antonyms":[],"example":"He delivers the mail everywhere on this street."},{"definition":"In or to a few or more locations.","synonyms":[],"antonyms":[],"example":"I've looked everywhere in the house and still can't find my glasses."}],"synonyms":[],"antonyms":["nowhere"]}],"license":{"name":"CC BY-SA 3.0","url":"https://creativecommons.org/licenses/by-sa/3.0"},"sourceUrls":["https://en.wiktionary.org/wiki/everywhere"]}]"""

    return {'status_code': 200, 'content': response.replace("'", "\'").replace("\n", "")}


class TestDictionaryView(APITestCase):

    def test_dictionary_response_is_ok(self):
        with HTTMock(word_response_mock):
            response = self.client.get('/dictionary/rift/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_dictionary_response_is_not_found_for_invalid_word(self):
        with HTTMock(word_not_found_mock):
            response = self.client.get('/dictionary/invalid_word/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_word_is_saved_on_database(self):
        with HTTMock(word_response_mock):
            self.client.get('/dictionary/rift/')
        words_count = Word.objects.count()
        self.assertEquals(words_count, 1)

    def test_word_is_retrieved_from_database_the_second_time(self):
        with HTTMock(word_response_mock):
            self.client.get('/dictionary/rift/')
            second_response = self.client.get('/dictionary/rift/')
        words_count = Word.objects.count()
        self.assertEquals(words_count, 1)
        self.assertEquals(second_response.status_code, status.HTTP_200_OK)

    def test_word_list_adds_a_word_to_database(self):
        with HTTMock(word_response_mock):
            response = self.client.get('/dictionary/?words[0]=everywhere')
        words_count = Word.objects.count()
        self.assertEquals(words_count, 1)

    def test_word_list_return_a_list(self):
        with HTTMock(word_response_mock):
            response = self.client.get('/dictionary/?words[0]=everywhere')
        self.assertIsInstance(response.data, list)

    def test_word_list_saves_three_words_to_database(self):
        with HTTMock(word_response_mock):
            response = self.client.get(
                '/dictionary/?words[0]=rift&words[1]=something&words[2]=everywhere')
        words_count = Word.objects.count()
        self.assertEqual(words_count, 3)

    def test_response_contains_three_words(self):
        with HTTMock(word_response_mock):
            response = self.client.get(
                '/dictionary/?words[0]=rift&words[1]=something&words[2]=everywhere')
        self.assertEquals(len(response.data), 3)

    def test_retrieve_existing_data_from_database(self):
        Word.objects.create(word='rift', phonetic='')
        Word.objects.create(word='something', phonetic='')
        Word.objects.create(word='everywhere', phonetic='')
        with HTTMock(word_empty_response):
            response = self.client.get(
                '/dictionary/?words[0]=rift&words[1]=something&words[2]=everywhere')
        self.assertEquals(len(response.data), 3)

    def test_retrieve_words_from_database_and_remote(self):
        Word.objects.create(word='rift', phonetic='')
        Word.objects.create(word='something', phonetic='')
        with HTTMock(word_partial_response_mock):
            response = self.client.get(
                '/dictionary/?words[0]=rift&words[1]=something&words[2]=everywhere')
        self.assertEquals(len(response.data), 3)
