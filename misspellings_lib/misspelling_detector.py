import collections
import json
import os
import pathlib
from typing import List, Union

from .misspelling_checker import MisspellingChecker

class MisspellingDetector(MisspellingChecker):
    """
    Detects misspelled words in files.
    """

    def __init__(
        self,
        misspelling_file: Union[pathlib.Path, str] = None,
        misspelling_json_file: Union[pathlib.Path, str] = None,
    ) -> None:
        """
        Initialises a Misspellings instance.

        Args:
          misspelling_file: Filename with a list of misspelled words and their corrections.
          misspelling_json_file: JSON filename of misspelled words and their corrections.

        Raises:
          IOError: Raised if misspelling_file can't be found.
          ValueError: Raised if misspelling_file isn't correctly formatted.

        """
        if misspelling_file:
            self._misspelling_dict = collections.defaultdict(list)
            with open(misspelling_file, 'r') as f:
                for line in f:
                    bad_word, correction = line.strip().split(' ', 1)
                    self._misspelling_dict[bad_word].append(correction)
        elif misspelling_json_file:
            self._misspelling_dict = collections.defaultdict(list)
            with open(misspelling_json_file, 'r') as custom_json_file:
                custom_dict_with_misspelled_words = json.load(custom_json_file)
                for (
                    bad_word,
                    correction,
                ) in custom_dict_with_misspelled_words.items():
                    self._misspelling_dict[bad_word].append(correction[0])
        else:
            self._misspelling_dict = {}
            file_paths = self._get_default_json_files()
            for dictionary in file_paths:
                with open(
                    os.path.join(os.path.dirname(__file__), dictionary)
                ) as input_file:
                    self._misspelling_dict.update(json.load(input_file))

    @staticmethod
    def _get_default_json_files() -> List[pathlib.Path]:
        assets_dir = pathlib.Path(__file__).parents[1] / 'assets'
        file_paths = [
            assets_dir.joinpath(file)
            for file in os.listdir(assets_dir.as_posix())
            if os.path.isfile(assets_dir.joinpath(file))
        ]
        return file_paths
