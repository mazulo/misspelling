from __future__ import annotations

import collections
import os
import re
import sys
from pathlib import Path
from typing import NoReturn

EXCLUDED_RE = re.compile(r"\.(py[co]|s?o|a|sh|txt|pylintrc|coverage|gitignore|python-version)|LICENSE$")
EXCLUDED_DIRS_RE = re.compile(
    r"^(.*\..*egg|.*\..*egg-info|\.bzr|\.git|\.hg|\.svn|\.github|CVS|"
    r"\.pytest_cache|bin|\.idea|assets|tests/assets|)$"
)


def parse_file_list(filename: Path) -> list[str] | NoReturn:
    """Show a line from a file in context."""
    f = sys.stdin
    try:
        if filename.as_posix() != "-":
            f = open(filename, "r", encoding="utf-8")
        file_list = [line.strip() for line in f]
        if f != sys.stdin:
            f.close()
        return file_list
    except IOError as err:
        print(f"ERRO NO ARQUIVO: {err}")
        raise err


def expand_directories(path_list: list[Path]) -> collections.Iterable[str]:
    """Return list with directories replaced their contained files."""
    for path in path_list:
        if os.path.isdir(path):
            for root, dirnames, filenames in os.walk(path):
                for name in filenames:
                    if not EXCLUDED_RE.search(name):
                        yield os.path.join(root, name)

                dirnames[:] = [d for d in dirnames if not EXCLUDED_DIRS_RE.match(d)]
        else:
            yield path
