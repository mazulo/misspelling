from __future__ import annotations

import collections
import os
import sys
from codecs import StreamWriter
from typing import TextIO

from tap.tap import TapType

from utils import esc_file, esc_sed, same_case, split_words

from .misspelling_interface import IMisspellingChecker


class MisspellingChecker(IMisspellingChecker):
    def check(self, filename: str) -> tuple[list[Exception], list[list[str | int | str]]]:
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
        if not os.path.isdir(filename):
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    line_ct = 1
                    for line in f:
                        for word in split_words(line):
                            if word in self._misspelling_dict or word.lower() in self._misspelling_dict:
                                results.append([filename, line_ct, word])
                        line_ct += 1
            except UnicodeDecodeError:
                pass
            except IOError as exception:
                errors.append(exception)
        return errors, results

    def get_suggestions(self, word: str) -> list[str]:
        """
        Returns a list of suggestions for a misspelled word.
        Args:
          word: The word to check.

        Returns:
          List of zero or more suggested replacements for word.

        """
        suggestions = set(self._misspelling_dict.get(word, set())).union(
            set(self._misspelling_dict.get(word.lower(), set()))
        )
        return sorted(same_case(source=word, destination=w) for w in suggestions)

    def dump_corrections(self) -> list[list[str]]:
        """Returns a list of misspelled words and corrections."""
        results = []
        for bad_word in sorted(self._misspelling_dict.keys()):
            for correction in self._misspelling_dict[bad_word]:
                results.append([bad_word, correction])
        return results

    def print_result(self, filenames: list[str] | collections.Iterable[str], output: StreamWriter) -> bool:
        """
        Print a list of misspelled words and their corrections.

        Return True if misspellings are found.

        """
        found = False

        for filename in filenames:
            errors, results = self.check(filename)
            for res in results:
                suggestions = ",".join(['"%s"' % w for w in self.get_suggestions(res[2])])
                output.write(f"{res[0]}:{res[1]}: {res[2]} -> {suggestions}\n")
                found = True

            for err in errors:
                sys.stderr.write("ERROR: %s\n" % err)
            output.flush()

        return found

    def export_result_to_file(self, filenames: list[str] | collections.Iterable[str], output: TextIO) -> None:
        """
        Save the list of misspelled words and their corrections into a file.
        """

        for filename in filenames:
            _, results = self.check(filename)
            for res in results:
                output.write(
                    "{}:{}: {} -> {}\n".format(
                        res[0],
                        res[1],
                        res[2],
                        ",".join(['"%s"' % w for w in self.get_suggestions(res[2])]),
                    )
                )

    def output_sed_commands(
        self, parser: TapType, args: TapType, filenames: list[str] | collections.Iterable[str]
    ) -> None:
        """
        Output a series of portable sed commands to change the file.
        """
        if os.path.exists(args.script_output):
            # Emit an error is the file already exists in case the user
            # forgets to give the file - but does give source files.
            parser.error('The sed script file "%s" must not exist.' % args.script_output)

        with open(args.script_output, "w", encoding="utf-8") as sed_script:
            for filename in filenames:
                errors, results = self.check(filename)
                for res in results:
                    suggestions = self.get_suggestions(res[2])
                    if len(suggestions) == 1:
                        suggestion = suggestions[0]
                    else:
                        suggestion = self.suggestion_generator.get_suggestion(res[0], res[1], res[2], suggestions)
                    if suggestion != res[2]:
                        sed_script.write(
                            f'cp "{esc_file(res[0])}" "{esc_file(res[0])},"\n'
                            f'sed "{res[1]}s/{esc_sed(res[2])}/{esc_sed(suggestion)}/"'
                            f' "{esc_file(res[0])}" > "{esc_file(res[0])},"\n'
                            f'mv "{esc_file(res[0])}," "{esc_file(res[0])}"\n'
                        )
                for err in errors:
                    sys.stderr.write(f"ERROR: {err}\n" % err)
