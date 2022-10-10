import sys
from typing import List

from .words import get_a_line


class SuggestionGenerator:
    """Class to query which correction should be used."""

    def __init__(self):
        self.last_suggestions = {}

    def get_suggestion(self, filename: str, lineno: int, word: str, suggestions: List[str]) -> str:
        """Show line from file, a misspelled word and request replacement."""
        if word not in self.last_suggestions:
            self.last_suggestions[word] = suggestions[0]

        line = get_a_line(filename, lineno)
        list_suggestions = ",".join(suggestions)
        last_suggestion = self.last_suggestions[word]
        sys.stdout.write(f'> {line}\nReplace "{word}" with one of {list_suggestions}\nChoose [{last_suggestion}]:')

        suggestion = sys.stdin.readline().strip()
        if not suggestion:
            suggestion = self.last_suggestions[word]
        else:
            self.last_suggestions[word] = suggestion

        return suggestion
