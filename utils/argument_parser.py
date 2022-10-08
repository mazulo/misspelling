from pathlib import Path
from typing import Optional, Union

from tap import Tap

from .version import get_version


def to_path(files: list[Path] | list[str]) -> Union[list[str], list[str]]:
    if isinstance(files, list):
        return [path.as_posix() for path in files]
    else:
        return files


class MisspellingArgumentParser(Tap):
    """Checks files against a list of commonly misspelled words.

    Wikipedia contains a large number of proper nouns and technical
    terms. Traditional spell-checking in this case is problematic.
    Instead, it has a page that people can use to list commonly misspelled
    words and to then use that to find misspellings.

    A similar approach can be taken to spell-checking (or misspell-checking)
    the files in a body of source code.

    This tool uses the English wordlist from Wikipedia in order to scan
    source code and identify misspelled words.
    """

    def __init__(self):
        super().__init__(underscores_to_dashes=True)

    file_list: Optional[Path] = None   # file containing list of files to check
    misspelling_file: Optional[
        Path
    ] = None   # file containing list of misspelled words and corrections
    json_file: Optional[
        Path
    ] = None   # Json file containing misspelled words and corrections
    script_output: Optional[
        Path
    ] = None   # Create a shell script to interactively correct the files - script saved to the given file
    export_file: Optional[
        Path
    ] = None   # Export the list of misspelled words into a file
    dump_misspelling: bool = False   # Dump the list of misspelled words
    version: Optional[str] = f'misspellings: {get_version()}'
    files: Optional[list[Path] | list[str]] = None   # Files to check

    def configure(self) -> None:
        self.add_argument(
            'files',
            nargs='*',
            help='Files to check',
            type=to_path,
        )
