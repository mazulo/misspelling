import collections
import io
import json
import os
import pathlib
import sys
from codecs import StreamWriter
from typing import Iterable, TextIO

from tap.tap import TapType

from utils import Suggestion, esc_file, esc_sed, same_case, split_words


class Misspellings:
    """
    Detects misspelled words in files.
    """

    def __init__(
        self, misspelling_file: str = None, misspelling_json_file: str = None
    ) -> None:
        """Initialises a Misspellings instance.

        Args:
          misspelling_file: Filename with a list of misspelled words and their corrections.
          misspelling_json_file: JSON filename of misspelled words and their corrections.

        Raises:
          IOError: Raised if misspelling_file can't be found.
          ValueError: Raised if misspelling_file isn't correctly formatted.

        """
        self.suggestion = Suggestion()
        if misspelling_file:
            self._misspelling_dict = collections.defaultdict(list)
            with io.open(misspelling_file, 'r') as f:
                for line in f:
                    bad_word, correction = line.strip().split(' ', 1)
                    self._misspelling_dict[bad_word].append(correction)
        elif misspelling_json_file:
            self._misspelling_dict = collections.defaultdict(list)
            with io.open(misspelling_json_file, 'r') as custom_json_file:
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
                with io.open(
                    os.path.join(os.path.dirname(__file__), dictionary)
                ) as input_file:
                    self._misspelling_dict.update(json.load(input_file))

    @staticmethod
    def _get_default_json_files() -> list[str]:
        assets_dir = pathlib.Path(__file__).parents[1] / 'assets'
        # file_paths = [path.as_posix() for path in assets_dir.iterdir()]
        file_paths = [
            assets_dir.joinpath(file).as_posix()
            for file in os.listdir(assets_dir.as_posix())
            if os.path.isfile(assets_dir.joinpath(file))
        ]
        return file_paths

    def check(
        self, filename: str
    ) -> tuple[list[Exception], list[[str, int, str]]]:
        """Checks the files for misspellings.

        Returns:
          (errors, results)
          errors: List of system errors, usually file access errors.
          results: List of spelling errors - each tuple is filename,
                   line number and misspelled word.

        """
        errors = []
        results = []
        if not os.path.isdir(filename):
            try:
                with io.open(filename, 'r') as f:
                    line_ct = 1
                    for line in f:
                        for word in split_words(line):
                            if (
                                word in self._misspelling_dict
                                or word.lower() in self._misspelling_dict
                            ):
                                results.append([filename, line_ct, word])
                        line_ct += 1
            except UnicodeDecodeError:
                pass
            except IOError as exception:
                errors.append(exception)
        return errors, results

    def suggestions(self, word: str) -> list[str]:
        """Returns a list of suggestions for a misspelled word.

        Args:
          word: The word to check.

        Returns:
          List of zero or more suggested replacements for word.

        """
        suggestions = set(self._misspelling_dict.get(word, set())).union(
            set(self._misspelling_dict.get(word.lower(), set()))
        )
        return sorted(
            same_case(source=word, destination=w) for w in suggestions
        )

    def dump_misspelling_list(self):
        """Returns a list of misspelled words and corrections."""
        results = []
        for bad_word in sorted(self._misspelling_dict.keys()):
            for correction in self._misspelling_dict[bad_word]:
                results.append([bad_word, correction])
        return results

    def output_normal(
        self,
        filenames: list[str] | Iterable[str],
        output: StreamWriter,
    ) -> bool:
        """
        Print a list of misspelled words and their corrections.

        Return True if misspellings are found.

        """
        found = False

        for filename in filenames:
            errors, results = self.check(filename)
            for res in results:
                suggestions = ','.join(
                    ['"%s"' % w for w in self.suggestions(res[2])]
                )
                output.write(f'{res[0]}:{res[1]}: {res[2]} -> {suggestions}\n')
                found = True

            for err in errors:
                sys.stderr.write('ERROR: %s\n' % err)
            output.flush()

        return found

    def export_result_to_file(
        self, filenames: list[str] | Iterable[str], output: TextIO
    ) -> None:
        """
        Save the list of misspelled words and their corrections into a file.
        """

        for filename in filenames:
            _, results = self.check(filename)
            for res in results:
                output.write(
                    '{}:{}: {} -> {}\n'.format(
                        res[0],
                        res[1],
                        res[2],
                        ','.join(
                            ['"%s"' % w for w in self.suggestions(res[2])]
                        ),
                    )
                )

    def output_sed_script(
        self,
        parser: TapType,
        args: TapType,
        filenames: list[str] | Iterable[str],
    ) -> None:
        """
        Output a series of portable sed commands to change the file.
        """
        if os.path.exists(args.script_output):
            # Emit an error is the file already exists in case the user
            # forgets to give the file - but does give source files.
            parser.error(
                'The sed script file "%s" must not exist.' % args.script_output
            )

        with io.open(args.script_output, 'w') as sed_script:
            for filename in filenames:
                errors, results = self.check(filename)
                for res in results:
                    suggestions = self.suggestions(res[2])
                    if len(suggestions) == 1:
                        suggestion = suggestions[0]
                    else:
                        suggestion = self.suggestion.get_suggestion(
                            res[0], res[1], res[2], suggestions
                        )
                    if suggestion != res[2]:
                        sed_script.write(
                            f'cp "{esc_file(res[0])}" "{esc_file(res[0])},"\n'
                            f'sed "{res[1]}s/{esc_sed(res[2])}/{esc_sed(suggestion)}/" "{esc_file(res[0])}" > "{esc_file(res[0])},"\n'
                            f'mv "{esc_file(res[0])}," "{esc_file(res[0])}"\n'
                        )
                for err in errors:
                    sys.stderr.write(f'ERROR: {err}\n' % err)
