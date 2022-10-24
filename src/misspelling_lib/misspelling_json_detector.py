import collections
import json
import pathlib
from typing import List, Union

from .misspelling_checker import MisspellingChecker


class MisspellingJSONDetector(MisspellingChecker):
    """
    Detects misspelled words in files based on a JSON file.
    """

    def __init__(
        self,
        filenames: List[pathlib.Path],
        misspelling_file: Union[pathlib.Path, str],
    ) -> None:
        """
        Initialises a MisspellingJSONDetector instance.

        Args:
          misspelling_file: JSON filename of misspelled words and their corrections.

        Raises:
          IOError: Raised if misspelling_file can't be found.
          ValueError: Raised if misspelling_file isn't correctly formatted.

        """
        super().__init__(filenames)
        self._misspelling_dict = collections.defaultdict(list)
        with open(misspelling_file, "r", encoding="utf-8") as custom_json_file:
            custom_dict_with_misspelled_words = json.load(custom_json_file)
            for (
                bad_word,
                correction,
            ) in custom_dict_with_misspelled_words.items():
                self._misspelling_dict[bad_word].append(correction[0])
