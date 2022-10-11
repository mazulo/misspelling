import collections
import json
import pathlib
from typing import Union

from .misspelling_checker import MisspellingChecker


class MisspellingJSONDetector(MisspellingChecker):
    """
    Detects misspelled words in files based on a JSON file.
    """

    def __init__(
        self,
        misspelling_json_file: Union[pathlib.Path, str],
    ) -> None:
        """
        Initialises a MisspellingJSONDetector instance.

        Args:
          misspelling_json_file: JSON filename of misspelled words and their corrections.

        Raises:
          IOError: Raised if misspelling_json_file can't be found.
          ValueError: Raised if misspelling_json_file isn't correctly formatted.

        """
        self._misspelling_dict = collections.defaultdict(list)
        with open(misspelling_json_file, "r", encoding="utf-8") as custom_json_file:
            custom_dict_with_misspelled_words = json.load(custom_json_file)
            for (
                bad_word,
                correction,
            ) in custom_dict_with_misspelled_words.items():
                self._misspelling_dict[bad_word].append(correction[0])
