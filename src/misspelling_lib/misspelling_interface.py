import abc
import pathlib
from codecs import StreamWriter
from typing import DefaultDict, Dict, List, TextIO, Tuple, Union

from tap.tap import TapType

from .utils import SuggestionGenerator


class IMisspellingChecker(metaclass=abc.ABCMeta):
    _misspelling_dict: Union[DefaultDict, Dict]
    suggestion_generator = SuggestionGenerator()

    @abc.abstractmethod
    def check(self, filename: str) -> Tuple[List[Exception], List[List[Union[str, int, str]]]]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_suggestions(self, word: str) -> List[str]:
        raise NotImplementedError

    @abc.abstractmethod
    def dump_corrections(self) -> List[List[str]]:
        raise NotImplementedError

    @abc.abstractmethod
    def print_result(
        self,
        filenames: List[pathlib.Path],
        output: StreamWriter,
    ) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def export_result_to_file(self, filenames: List[pathlib.Path], output: TextIO) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def output_sed_commands(
        self,
        parser: TapType,
        args: TapType,
        filenames: List[pathlib.Path],
    ) -> None:
        raise NotImplementedError
