import re
import sys
from glob import iglob
from pathlib import Path
from typing import Iterator, List, NoReturn, Union

EXCLUDED_FILES_RE = re.compile(r"\.(pyc|s?o|a|sh|txt|coverage|gitignore|python-version)|LICENSE$")
EXCLUDED_DIRS_RE = re.compile(
    r"\.(git|github|mypy_cache|pytest_cache|idea|vscode)|"
    r"(\*egg|\*egg-info|CVS|bin|node_modules|__pycache__|json_sources|test_assets)"
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


def expand_directories(path_list: List[Path]) -> Iterator[Path]:
    """Return list with directories replaced their contained files."""
    for path in path_list:
        if path.is_dir() and not EXCLUDED_DIRS_RE.search(path.as_posix()):
            for filename in iglob(f"{path}/**/*.*", recursive=True):
                if not EXCLUDED_DIRS_RE.search(filename) and not EXCLUDED_FILES_RE.search(filename):
                    yield Path(filename)
        else:
            yield path
