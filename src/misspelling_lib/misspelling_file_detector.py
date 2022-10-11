import collections
import pathlib
from typing import Union

from .misspelling_checker import MisspellingChecker


class MisspellingFileDetector(MisspellingChecker):
    """
    Detects misspelled words in files.
    """

    def __init__(
        self,
        misspelling_file: Union[pathlib.Path, str],
    ) -> None:
        """
        Initialises a MisspellingFileDetector instance.

        Args:
          misspelling_file: Filename with a list of misspelled words and their corrections.

        Raises:
          IOError: Raised if misspelling_file can't be found.
          ValueError: Raised if misspelling_file isn't correctly formatted.
        """
        self._misspelling_dict = collections.defaultdict(list)
        with open(misspelling_file, "r", encoding="utf-8") as f:
            for line in f:
                bad_word, correction = line.strip().split(" ", 1)
                self._misspelling_dict[bad_word].append(correction)
