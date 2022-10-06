# -*- coding: utf-8 -*-

"""Misspellings module.

Take a list of files, check them against a list of misspelled words.
"""

import collections
import io
import json
import os
import re
import string


__version__ = '1.0.7'


_NORM_REGEX = re.compile(r'(?<=[a-z])(?=[A-Z])')
_WORD_REGEX = re.compile(r'[\s_0-9\W]+', flags=re.UNICODE)


def normalize(word):
    """Return word with symbols stripped from its ends."""
    return word.strip(string.punctuation)


def split_words(line):
    """Return the list of words contained in a line."""
    # Normalize any camel cased words first.
    line = ' '.join(w for w in _NORM_REGEX.split(line) if w)

    return [normalize(w) for w in _WORD_REGEX.split(line)]


def same_case(source, destination):
    """Return destination with same case as source."""
    if source and source[:1].isupper():
        return destination.capitalize()
    else:
        return destination


class Misspellings(object):

    """Detects misspelled words in files."""

    def __init__(self, misspelling_file=None, misspelling_json_file=None):
        """Initialises a Misspellings instance.

        Args:
          misspelling_file: Filename with a list of misspelled words and their corrections.
          misspelling_json_file: JSON filename of misspelled words and their corrections.

        Raises:
          IOError: Raised if misspelling_file can't be found.
          ValueError: Raised if misspelling_file isn't correctly formatted.

        """
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
            for dictionary in ['wikipedia.json', 'custom.json']:
                with io.open(
                    os.path.join(os.path.dirname(__file__), dictionary)
                ) as input_file:
                    self._misspelling_dict.update(json.load(input_file))

    def check(self, filename):
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

    def suggestions(self, word):
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
