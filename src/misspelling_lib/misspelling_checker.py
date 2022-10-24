import multiprocessing
import os
import pathlib
import sys
from codecs import StreamWriter
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from typing import Iterator, List, Optional, TextIO, Tuple, Union

from tap.tap import TapType

from .dto import FileContentDTO
from .misspelling_interface import IMisspellingChecker
from .utils import esc_file, esc_sed, same_case, split_words


class MisspellingChecker(IMisspellingChecker):
    def __init__(self, filenames: List[pathlib.Path]) -> None:
        self.files_dto = self.initialize_files_content(filenames)

    def initialize_files_content(self, filenames: List[pathlib.Path]) -> List[FileContentDTO]:
        number_of_workers = int(multiprocessing.cpu_count() * 0.5)
        chunk_size = round(len(filenames) / number_of_workers) or 1
        list_file_content_dto = []

        # Create the process pool
        with ProcessPoolExecutor(number_of_workers) as executor:
            futures = []
            # Split the load operations into chunks
            for i in range(0, len(filenames), chunk_size):
                # select a chunk of filenames
                filepaths = filenames[i : (i + chunk_size)]
                # submit the task
                future = executor.submit(self.load_files, filepaths)
                futures.append(future)

            # Process all results
            for future in as_completed(futures):
                # Retrieve the list of FileContentDTOs
                list_file_content_dto.extend(future.result())

        return list_file_content_dto

    def read_file(self, filename: pathlib.Path) -> FileContentDTO:
        try:
            with open(filename, "r", encoding="utf-8") as file:
                file_content_dto = FileContentDTO(
                    filename=filename.name,
                    filepath=filename,
                    filecontent=file.readlines(),
                )
        except (IOError, UnicodeDecodeError) as exception:
            return FileContentDTO(filename=filename.name, filepath=filename, has_error=True, error=str(exception))
        else:
            return file_content_dto

    def load_files(self, filenames: List[pathlib.Path]) -> List[FileContentDTO]:
        with ThreadPoolExecutor(int(multiprocessing.cpu_count() * 0.5)) as exe:
            # Load files
            futures = [exe.submit(self.read_file, filename) for filename in filenames]
            # Collect data
            list_file_content_dto = [future.result() for future in futures]
            return list_file_content_dto

    def check(self, file_dto: FileContentDTO) -> Tuple[List[FileContentDTO], List[List[Union[pathlib.Path, int, str]]]]:
        """
        Checks the files for misspellings.
        Returns:
          (errors, results)
          errors: List of system errors, usually file access errors.
          results: List of spelling errors - each tuple is filename,
                   line number and misspelled word.
        """
        errors = []
        results = []
        if file_dto.has_error:
            errors.append(file_dto)
        else:
            line_number = 1
            for line in file_dto.filecontent:
                if "# ignore-misspelling" in line:
                    continue
                for word in split_words(line):
                    if word in self._misspelling_dict or word.lower() in self._misspelling_dict:
                        results.append([file_dto.filepath, line_number, word])
                line_number += 1

        return errors, results

    def get_suggestions(self, word: str) -> List[str]:
        """
        Returns a list of suggestions for a misspelled word.
        Args:
          word: The word to check.

        Returns:
          List of zero or more suggested replacements for word.

        """
        suggestions = set(self._misspelling_dict.get(word, [])).union(set(self._misspelling_dict.get(word.lower(), [])))
        return sorted(same_case(source=word, destination=w) for w in suggestions)

    def dump_corrections(self) -> List[List[str]]:
        """Returns a list of misspelled words and corrections."""
        results = []
        for bad_word in sorted(self._misspelling_dict.keys()):
            for correction in self._misspelling_dict[bad_word]:
                results.append([bad_word, correction])
        return results

    def print_result(self, filenames: Iterator[pathlib.Path], output: StreamWriter) -> bool:
        """
        Print a list of misspelled words and their corrections.
        Return True if misspellings are found.
        """
        found = False
        for file_dto in self.files_dto:
            errors, results = self.check(file_dto)
            for result in results:
                suggestions = ",".join([f'"{w}"' for w in self.get_suggestions(result[2])])
                output.write(f"{result[0]}:{result[1]}: {result[2]} -> {suggestions}\n")
                found = True

            for error in errors:
                sys.stderr.write(f"ERROR: {error.error}\n")
            output.flush()

        return found

    def export_result_to_file(self, filenames: Iterator[pathlib.Path], output: TextIO) -> None:
        """
        Save the list of misspelled words and their corrections into a file.
        """

        for file_dto in self.files_dto:
            _, results = self.check(file_dto)
            for result in results:
                suggestions = ",".join([f'"{w}"' for w in self.get_suggestions(result[2])])
                output.write(f"{result[0]}:{result[1]}: {result[2]} -> {suggestions}\n")

    def output_sed_commands(self, parser: TapType, args: TapType, filenames: Iterator[pathlib.Path]) -> None:
        """
        Output a series of portable sed commands to change the file.
        """
        if os.path.exists(args.script_output):
            # Emit an error if the file already exists in case the user
            # forgets to give the file - but does give source files.
            parser.error(f'The sed script file "{args.script_output}" must not exist.')

        with open(args.script_output, "w", encoding="utf-8") as sed_script:
            for file_dto in self.files_dto:
                errors, results = self.check(file_dto)
                for result in results:
                    suggestions = self.get_suggestions(result[2])
                    if len(suggestions) == 1:
                        suggestion = suggestions[0]
                    else:
                        suggestion = self.suggestion_generator.get_suggestion(
                            result[0], result[1], result[2], suggestions
                        )
                    if suggestion != result[2]:
                        sed_script.write(
                            f'cp "{esc_file(result[0])}" "{esc_file(result[0])},"\n'
                            f'sed "{result[1]}s/{esc_sed(result[2])}/{esc_sed(suggestion)}/"'
                            f' "{esc_file(result[0])}" > "{esc_file(result[0])},"\n'
                            f'mv "{esc_file(result[0])}," "{esc_file(result[0])}"\n'
                        )
                for error in errors:
                    sys.stderr.write(f"ERROR: {error.error}\n")
