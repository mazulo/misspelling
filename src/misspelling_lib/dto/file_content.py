from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional


@dataclass(kw_only=True)
class FileContentDTO:
    filename: str
    filepath: Path
    filecontent: Optional[List[str]] = field(default=None)
    has_error: Optional[bool] = field(default=False)
    error: Optional[str] = field(default=None)
