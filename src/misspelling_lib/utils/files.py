import re
import sys
from glob import iglob
from pathlib import Path
from typing import Iterator, List, NoReturn, Union

EXCLUDED_FILES_RE = re.compile(r"\.(pyc|s?o|a|sh|txt|coverage|gitignore|python-version)|LICENSE$")
EXCLUDED_DIRS_RE = re.compile(
    r"\.(git|github|mypy_cache|pytest_cache|idea|vscode)|"
    r"^(\*egg|\*egg-info|CVS|bin|node_modules|json_sources|tests/sources)$"
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
        if path.is_dir() and not EXCLUDED_DIRS_RE.match(path.as_posix()):
            for filenames in iglob(path.as_posix()):
                for name in filenames:
                    if not EXCLUDED_FILES_RE.search(name):
                        yield Path(name)
        else:
            yield path
