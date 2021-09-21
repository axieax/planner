import re
from dataclasses import dataclass

CODE_PATTERN = re.compile(r"\w{4}\d{2}")


@dataclass
class Degree:
    code: str = ""
    faculty: str = ""
