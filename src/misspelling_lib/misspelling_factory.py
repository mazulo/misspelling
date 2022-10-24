from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from .misspelling_detector import MisspellingDetector
from .misspelling_file_detector import MisspellingFileDetector
from .misspelling_json_detector import MisspellingJSONDetector

MisspellingDetectorType = Union[MisspellingDetector, MisspellingFileDetector, MisspellingJSONDetector]


class MisspellingFactory:
    @classmethod
    def factory(
        cls, misspelling_detector_name: str, filenames: List[Path], misspelling_file: Optional[Union[Path, None]] = None
    ) -> MisspellingDetectorType:
        class_map = cls.get_misspelling_class_map()
        if misspelling_detector_name == "misspelling_detector":
            return class_map.get(misspelling_detector_name)(filenames=filenames)
        return class_map.get(misspelling_detector_name)(filenames=filenames, misspelling_file=misspelling_file)

    @staticmethod
    def get_misspelling_class_map() -> Dict[str, Any]:
        return {
            "misspelling_detector": MisspellingDetector,
            "misspelling_file_detector": MisspellingFileDetector,
            "misspelling_json_detector": MisspellingJSONDetector,
        }
