from pathlib import Path
from typing import List, Optional

from tap import Tap


class MisspellingArgumentParser(Tap):
    """
    Argument parser with the options for the misspellings command
    """

    def __init__(self):
        super().__init__(underscores_to_dashes=True)

    file_list: Optional[Path] = None  # File containing list of files to check
    misspelling_file: Optional[Path] = None  # File containing list of misspelled words and corrections
    json_file: Optional[Path] = None  # Json file containing misspelled words and corrections
    script_output: Optional[
        Path
    ] = None  # Create a shell script to interactively correct the files - script saved to the given file
    export_file: Optional[Path] = None  # Export the list of misspelled words into a file
    dump_misspelling: bool = False  # Dump the list of misspelled words
    version: bool = False  # Version of the misspellings package
    files: Optional[List[Path]] = None  # Files to check

    def configure(self) -> None:
        self.add_argument(
            "files",
            nargs="*",
            help="Files to check",
        )
