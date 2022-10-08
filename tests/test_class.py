import os
from pathlib import Path

import pytest

from misspellings_lib.misspelling_detector import MisspellingDetector
from misspellings_lib.misspelling_file_detector import MisspellingFileDetector
from misspellings_lib.misspelling_json_detector import MisspellingJSONDetector
from utils import normalize, same_case, split_words

BASE_PATH = Path(__file__).parents[0]


class TestMisspellingDetector:
    def test_missing_ms_list(self):
        with pytest.raises(IOError):
            MisspellingFileDetector(os.path.join(BASE_PATH, 'missing_msl.txt'))

    def test_broken_ms_list(self):
        with pytest.raises(ValueError):
            MisspellingFileDetector(os.path.join(BASE_PATH, 'assets/broken_msl.txt'))

    def test_missing_ms_list_for_json_detector(self):
        with pytest.raises(IOError):
            MisspellingJSONDetector(os.path.join(BASE_PATH, 'missing_msl.json'))

    def test_broken_ms_list_for_json_detector(self):
        with pytest.raises(ValueError):
            MisspellingJSONDetector(os.path.join(BASE_PATH, 'assets/broken_msl.json'))

    def test_missing_file(self):
        ms = MisspellingDetector()
        errors, results = ms.check(os.path.join(BASE_PATH, 'missing_source.c'))
        assert errors

    def test_good_file(self):
        ms = MisspellingDetector()
        errors, results = ms.check(
            os.path.join(BASE_PATH, 'assets/nine_misspellings.json')
        )
        assert len(errors) == 0
        assert len(results) == 9

    def test_more_complex_file(self):
        ms = MisspellingDetector()
        errors, results = ms.check(
            os.path.join(BASE_PATH, 'assets/various_spellings.c')
        )
        assert len(errors) == 0
        assert len(results) == 7


class TestUtilityFunction:
    def test_same_case(self):
        assert 'Apple' == same_case(source='Apple', destination='apple')

        # Do not make lowercase as "Apple" may be the first word in a sentence.
        assert 'Apple' == same_case(source='apple', destination='Apple')

    def test_same_case_with_empty_destination(self):
        assert '' == same_case(source='apple', destination='')
        assert '' == same_case(source='Apple', destination='')

    def test_same_case_with_empty_source(self):
        assert 'apple' == same_case(source='', destination='apple')
        assert 'Apple' == same_case(source='', destination='Apple')

    def test_split_words(self):
        assert ['one', 'two', 'three'] == split_words('one two three')

    def test_split_words_with_underscores(self):
        assert ['one', 'two', 'three'] == split_words('one_two_three')
        assert ['one', 'two', 'three'] == split_words('one__two__three')
        assert ['one', 'two', 'three', 'four'] == split_words(
            'one_two_three four'
        )

    def test_split_words_with_punctuation(self):
        assert ['one', 'two'] == split_words('one, two')
        assert ['a', 'sentence', ''] == split_words('a sentence.')

    def test_split_words_with_numbers(self):
        assert ['upper', 'lower'] == split_words('upper2lower')

    def test_split_words_with_camel_case(self):
        assert ['one', 'Two', 'Three'] == split_words('oneTwoThree')
        assert ['one', 'Two', 'Three', 'Four'] == split_words(
            'oneTwoThreeFour'
        )
        assert ['one', 'Two', 'Three', 'four'] == split_words(
            'oneTwoThree_four'
        )
        assert ['one', 'Two', 'Three', 'four', 'five'] == split_words(
            'oneTwoThree_four five'
        )
        assert ['foo', 'Up', 'To', 'Bar'] == split_words('fooUpToBar')

    def test_split_words_with_other_characters(self):
        assert ['the', 'big', 'cat'] == split_words('the%big$cat')

    def test_normalize(self):
        assert 'alpha' == normalize('"alpha".')
