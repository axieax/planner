import re
import json
from dataclasses import dataclass, field

CODE_PATTERN = re.compile(r'\w{4}\d{4}')
VALID_TERMS = set(range(4))
with open('data/faculties.json') as f:
    FACULTIES = set(json.load(f))


# @dataclass(frozen=True, eq=True, order=True, repr=True)
@dataclass(frozen=True, repr=True)
class Course:
    code: str = ''
    terms: list[int] = field(default_factory=lambda: [])
    raw_requirements: str = ''
    faculty: str = ''
    uoc: int = 0

    def __post_init__(self):
        ''' Field Validation '''
        # check code format
        if not CODE_PATTERN.match(self.code):
            raise ValueError(f'Invalid Course Code: {self.code}')
        # check terms
        if set(self.terms) - VALID_TERMS:
            raise ValueError(f'Invalid Terms: {self.terms}')
        # check faculty
        if self.faculty not in FACULTIES:
            raise ValueError(f'Invalid Faculty: {self.faculty}')

    @property
    def requirements(self) ->  list:
        # parse
        return []

    @property
    def level(self) -> int:
        return int(self.code[4])



