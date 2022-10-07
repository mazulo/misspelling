import io
import os
import re
import sys
from pathlib import Path
from typing import Union, NoReturn, Iterable


EXCLUDED_RE = re.compile('\.(py[co]|s?o|a)$')
EXCLUDED_DIRS_RE = re.compile(
    r'^(.*\..*egg|.*\..*egg-info|\.bzr|\.git|\.hg|\.svn|\.github|CVS|\.pytest_cache|\.bin|)$'
)


def parse_file_list(filename: Path) -> Union[list[str], NoReturn]:
    """Show a line from a file in context."""
    f = sys.stdin
    try:
        if filename.as_posix() != '-':
            f = io.open(filename.as_posix(), 'r')
        file_list = [line.strip() for line in f]
        if f != sys.stdin:
            f.close()
        return file_list
    except IOError as err:
        print(f"ERRO NO ARQUIVO: {err}")
        raise err


def expand_directories(path_list: list[Path]) -> Iterable[str]:
    """Return list with directories replaced their contained files."""
    for path in path_list:
        if os.path.isdir(path):
            for root, dirnames, filenames in os.walk(path):
                for name in filenames:
                    if not EXCLUDED_RE.search(name):
                        yield os.path.join(root, name)

                dirnames[:] = [
                    d for d in dirnames if not EXCLUDED_DIRS_RE.match(d)
                ]
        else:
            yield path
