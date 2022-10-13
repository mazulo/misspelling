import re
import string
from pathlib import Path
from typing import List

_NORM_REGEX = re.compile(r"(?<=[a-z])(?=[A-Z])")
_WORD_REGEX = re.compile(r"[\s_0-9\W]+", flags=re.UNICODE)


def normalize(word: str) -> str:
    """Return word with symbols stripped from its ends."""
    return word.strip(string.punctuation)


def split_words(line: str) -> List[str]:
    """Return the list of words contained in a line."""
    # Normalize any camel cased words first.
    line = " ".join(w for w in _NORM_REGEX.split(line) if w)

    return [normalize(w) for w in _WORD_REGEX.split(line)]


def same_case(source: str, destination: str) -> str:
    """Return destination with same case as source."""
    if source and source[:1].isupper():
        return destination.capitalize()
    return destination


def get_a_line(filename: str, lineno: int) -> str:
    """Read a specific line from a file."""
    # Perhaps caching this would be nice, but assuming not an insane
    # number of misspellings.
    return open(filename, "r", encoding="utf-8").readlines()[lineno - 1].rstrip()


def esc_sed(raw_text: str) -> str:
    """Escape chars for a sed command on a shell command line."""
    return raw_text.replace('"', '\\"').replace("/", "\\/")


def esc_file(path_text: Path) -> str:
    """Escape chars for a file name on a shell command line."""
    raw_text = path_text.as_posix()
    return raw_text.replace("'", "'\"'\"'")
