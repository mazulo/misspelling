from __future__ import annotations

import abc
import collections
from codecs import StreamWriter
from collections import abc as colllection_abc
from typing import TextIO

from tap.tap import TapType

from src.utils import SuggestionGenerator


class IMisspellingChecker(metaclass=abc.ABCMeta):
    _misspelling_dict: collections.defaultdict | dict
    suggestion_generator = SuggestionGenerator()

    @abc.abstractmethod
    def check(self, filename: str) -> tuple[list[Exception], list[list[str | int | str]]]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_suggestions(self, word: str) -> list[str]:
        raise NotImplementedError

    @abc.abstractmethod
    def dump_corrections(self) -> list[list[str]]:
        raise NotImplementedError

    @abc.abstractmethod
    def print_result(
        self,
        filenames: list[str] | colllection_abc.Iterable[str],
        output: StreamWriter,
    ) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def export_result_to_file(self, filenames: list[str] | colllection_abc.Iterable[str], output: TextIO) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def output_sed_commands(
        self,
        parser: TapType,
        args: TapType,
        filenames: list[str] | colllection_abc.Iterable[str],
    ) -> None:
        raise NotImplementedError
