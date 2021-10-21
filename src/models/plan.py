from typing import Dict, List, TypedDict


class Term(TypedDict):
    year: int
    term: int
    max_uoc: int
    current_uoc: int
    courses: List[str]


class Plan(TypedDict):
    terms: List[Term]


class PlanType(TypedDict):
    start: Dict
    end: Dict
    num_terms: int
    program: str
    current_uoc: int
    selected_courses: List[str]
    plan: Plan
