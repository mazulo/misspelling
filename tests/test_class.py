import os
from pathlib import Path

import pytest

from src.misspelling_lib import MisspellingDetector, MisspellingFileDetector, MisspellingJSONDetector
from src.misspelling_lib.utils import normalize, same_case, split_words

BASE_PATH = Path(__file__).parents[0]


class TestMisspellingDetector:
    def test_missing_ms_list(self):
        with pytest.raises(IOError):
            MisspellingFileDetector(
                filenames=[BASE_PATH / "missing_msl.txt"],
                misspelling_file=BASE_PATH / "test_assets/nine_misspellings.cc",
            )

    def test_broken_ms_list(self):
        with pytest.raises(ValueError):
            MisspellingFileDetector(
                filenames=[BASE_PATH / "broken_msl.txt"],
                misspelling_file=BASE_PATH / "test_assets/broken_nine_misspellings.c",
            )

    def test_missing_ms_list_for_json_detector(self):
        with pytest.raises(IOError):
            MisspellingJSONDetector(
                filenames=[BASE_PATH / "missing_msl.json"],
                misspelling_file=BASE_PATH / "test_assets/missing_nine_misspellings.json",
            )

    def test_broken_ms_list_for_json_detector(self):
        with pytest.raises(ValueError):
            MisspellingJSONDetector(
                filenames=[BASE_PATH / "broken_msl.json"],
                misspelling_file=BASE_PATH / "test_assets/broken_nine_misspellings.json",
            )

    def test_missing_file(self):
        ms = MisspellingDetector(filenames=[BASE_PATH / "test_assets/missing_source.c"])
        file_dto = ms.files_dto[0]
        errors, _ = ms.check(file_dto)
        assert errors

    def test_good_file(self):
        ms = MisspellingDetector(filenames=[BASE_PATH / "test_assets/nine_misspellings.json"])
        file_dto = ms.files_dto[0]
        errors, results = ms.check(file_dto)
        assert len(errors) == 0
        assert len(results) == 9

    def test_more_complex_file(self):
        ms = MisspellingDetector(filenames=[BASE_PATH / "test_assets/various_spellings.c"])
        file_dto = ms.files_dto[0]
        errors, results = ms.check(file_dto)
        assert len(errors) == 0
        assert len(results) == 7


class TestUtilityFunction:
    def test_same_case(self):
        assert same_case(source="Apple", destination="apple") == "Apple"

        # Do not make lowercase as "Apple" may be the first word in a sentence.
        assert same_case(source="apple", destination="Apple") == "Apple"

    def test_same_case_with_empty_destination(self):
        assert same_case(source="apple", destination="") == ""
        assert same_case(source="Apple", destination="") == ""

    def test_same_case_with_empty_source(self):
        assert same_case(source="", destination="apple") == "apple"
        assert same_case(source="", destination="Apple") == "Apple"

    def test_split_words(self):
        assert split_words("one two three") == ["one", "two", "three"]

    def test_split_words_with_underscores(self):
        assert split_words("one_two_three") == ["one", "two", "three"]
        assert split_words("one__two__three") == ["one", "two", "three"]
        assert split_words("one_two_three four") == ["one", "two", "three", "four"]

    def test_split_words_with_punctuation(self):
        assert split_words("one, two") == ["one", "two"]
        assert split_words("a sentence.") == ["a", "sentence", ""]

    def test_split_words_with_numbers(self):
        assert split_words("upper2lower") == ["upper", "lower"]

    def test_split_words_with_camel_case(self):
        assert split_words("oneTwoThree") == ["one", "Two", "Three"]
        assert split_words("oneTwoThreeFour") == ["one", "Two", "Three", "Four"]
        assert split_words("oneTwoThree_four") == ["one", "Two", "Three", "four"]
        assert split_words("oneTwoThree_four five") == ["one", "Two", "Three", "four", "five"]
        assert split_words("fooUpToBar") == ["foo", "Up", "To", "Bar"]

    def test_split_words_with_other_characters(self):
        assert split_words("the%big$cat") == ["the", "big", "cat"]

    def test_normalize(self):
        assert normalize('"alpha".') == "alpha"
