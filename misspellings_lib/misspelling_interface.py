import abc
from codecs import StreamWriter
from typing import DefaultDict, Tuple, List, Union, Iterable, TextIO, Dict

from tap.tap import TapType

from utils import SuggestionGenerator


class IMisspellingChecker(metaclass=abc.ABCMeta):
    _misspelling_dict: Union[DefaultDict, Dict]
    suggestion_generator = SuggestionGenerator()

    @abc.abstractmethod
    def check(
            self, filename: str
    ) -> Tuple[List[Exception], List[List[Union[str, int, str]]]]:
        raise NotImplemented

    @abc.abstractmethod
    def get_suggestions(self, word: str) -> List[str]:
        raise NotImplemented


    @abc.abstractmethod
    def dump_corrections(self) -> List[List[str]]:
        raise NotImplemented


    @abc.abstractmethod
    def print_result(
            self,
            filenames: Union[List[str], Iterable[str]],
            output: StreamWriter,
    ) -> bool:
        raise NotImplemented


    @abc.abstractmethod
    def export_result_to_file(
            self, filenames: Union[List[str], Iterable[str]], output: TextIO
    ) -> None:
        raise NotImplemented


    @abc.abstractmethod
    def output_sed_commands(
            self,
            parser: TapType,
            args: TapType,
            filenames: Union[List[str], Iterable[str]],
    ) -> None:
        raise NotImplemented
