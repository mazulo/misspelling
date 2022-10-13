import json
import os
import pathlib
from typing import List

from .misspelling_checker import MisspellingChecker


class MisspellingDetector(MisspellingChecker):
    """
    Detects misspelled words in files.
    """

    def __init__(self) -> None:
        """
        Initialises a MisspellingDetector instance using the default json files.
        """
        self._misspelling_dict = {}
        file_paths = self._get_default_json_files()
        for dictionary in file_paths:
            with open(os.path.join(os.path.dirname(__file__), dictionary), encoding="utf-8") as input_file:
                self._misspelling_dict.update(json.load(input_file))

    @staticmethod
    def _get_default_json_files() -> List[pathlib.Path]:
        assets_dir = pathlib.Path(__file__).parents[0] / "json_sources"
        file_paths = [
            assets_dir.joinpath(file)
            for file in os.listdir(assets_dir.as_posix())
            if os.path.isfile(assets_dir.joinpath(file))
        ]
        return file_paths
