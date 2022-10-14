import os
import re
import sys
from pathlib import Path
from typing import Iterator, List, NoReturn, Optional, Union

EXCLUDED_FILES_RE = re.compile(r"\.(pyc|s?o|a|sh|txt|coverage|gitignore|python-version)|LICENSE$")
DOT_EXCLUDED_DIRS_RE = re.compile(r"\.(git|github|mypy_cache|pytest_cache|idea|vscode|.local)")
EXCLUDED_DIRS_RE = re.compile(
    r"(\*egg|\*egg-info|CVS|bin|node_modules|__pycache__|json_sources|test_assets|_local|build|dist)"
)


def parse_file_list(filename: Path) -> Union[List[Path], NoReturn]:
    """Show a line from a file in context."""
    f = sys.stdin
    try:
        if filename.as_posix() != "-":
            f = open(filename, "r", encoding="utf-8")
        file_list = [Path(line.strip()) for line in f]
        if f != sys.stdin:
            f.close()
        return file_list
    except IOError as err:
        raise err


def expand_directories(path_list: List[Path], result_files: Optional[List[Path]] = None) -> Iterator[Path]:
    """Return list with directories replaced their contained files."""

    if result_files is None:
        result_files = []

    for path in path_list:
        if path.is_dir():
            for entry in os.scandir(path):
                if (
                    not entry.path.find(".local") > -1
                    and not entry.path.find("_local") > -1
                    and not DOT_EXCLUDED_DIRS_RE.search(entry.path)
                    and not EXCLUDED_DIRS_RE.search(entry.path)
                    and entry.is_dir()
                ):
                    expand_directories(path_list=[Path(entry.path)], result_files=result_files)
                if entry.is_file() and not EXCLUDED_FILES_RE.search(entry.name):
                    result_files.append(Path(entry.path))
        else:
            result_files.append(path)
    return result_files
