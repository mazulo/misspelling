from __future__ import annotations

from pathlib import Path
from typing import Any, Union

from .misspelling_detector import MisspellingDetector
from .misspelling_file_detector import MisspellingFileDetector
from .misspelling_json_detector import MisspellingJSONDetector

MisspellingDetectorType = Union[MisspellingDetector, MisspellingFileDetector, MisspellingJSONDetector]


class MisspellingFactory:
    @classmethod
    def factory(cls, misspelling_detector_name: str, misspelling_file: Path | None = None) -> MisspellingDetectorType:
        class_map = cls.get_misspelling_class_map()
        if misspelling_detector_name == "misspelling_detector":
            return class_map.get(misspelling_detector_name)()
        return class_map.get(misspelling_detector_name)(misspelling_file)

    @staticmethod
    def get_misspelling_class_map() -> dict[str, Any]:
        return {
            "misspelling_detector": MisspellingDetector,
            "misspelling_file_detector": MisspellingFileDetector,
            "misspelling_json_detector": MisspellingJSONDetector,
        }
