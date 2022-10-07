import sys

from .words import get_a_line


class Suggestions:
    """Class to query user on which correction should be used."""

    def __init__(self):
        self.last_suggestions = {}

    def get_suggestion(
        self, filename: str, lineno: int, word: str, suggestions: list[str]
    ) -> str:
        """Show line from file, a misspelled word and request replacement."""
        if word not in self.last_suggestions:
            self.last_suggestions[word] = suggestions[0]
        line = get_a_line(filename, lineno)
        sys.stdout.write(
            '> %s\nReplace "%s" with one of %s\nChoose [%s]:'
            % (line, word, ','.join(suggestions), self.last_suggestions[word])
        )
        suggestion = sys.stdin.readline().strip()
        if not suggestion:
            suggestion = self.last_suggestions[word]
        else:
            self.last_suggestions[word] = suggestion
        return suggestion
