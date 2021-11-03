import re
import json
from dataclasses import dataclass, field

from src.utils.requirements import Requirement, parse_requirement
from src.utils.constants import VALID_TERMS

CODE_PATTERN = re.compile(r"\w{4}\d{4}")
with open("data/faculties.json") as f:
    FACULTIES = set(json.load(f))


# @dataclass(frozen=True, eq=True, order=True, repr=True)
@dataclass(frozen=True, repr=True)
class Course:
    code: str = ""
    terms: list = field(default_factory=list)
    raw_requirements: str = ""
    faculty: str = ""
    uoc: int = 0

    def __post_init__(self):
        """Field Validation"""
        # check code format
        if not CODE_PATTERN.match(self.code):
            raise ValueError(f"Invalid Course Code: {self.code}")
        # check terms
        if set(self.terms) - VALID_TERMS:
            raise ValueError(f"Invalid Terms: {self.terms}")
        # check faculty
        if self.faculty not in FACULTIES:
            raise ValueError(f"Invalid Faculty: {self.faculty}")

    @property
    def requirements(self) -> Requirement:
        return parse_requirement(self.raw_requirements)

    @property
    def level(self) -> int:
        return int(self.code[4])

    def to_dict(self):
        return {
            "code": self.code,
            "terms": self.terms,
            "raw_requirements": self.raw_requirements,
            "faculty": self.faculty,
            "uoc": self.uoc,
        }
