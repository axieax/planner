from data import get_course
from src.utils.logic import And, Or


def parse_requirement(prereq_str: str) -> Requirement:
    pass


class Requirement:
    def __init__(self, requirement) -> None:
        self._requirement = requirement

    def is_satisfied(self, plan, term_place) -> bool:
        return self._requirement.is_satisfied(plan, term_place)


class PreReq:
    """Prerequisites"""

    def __init__(self, code) -> None:
        self._code = code
        self._course = get_course(code)

    def is_satisfied(self, plan, term_place) -> bool:
        """
        Predicate for checking whether a prerequisite is satisfied for a plan up to term_place
        """
        for term in plan[:term_place]:
            if self._code in term["courses"]:
                return True
        return False


class CoReq:
    """Corequisites"""

    def __init__(self, code) -> None:
        self._code = code

    def is_satisfied(self, plan, term_place) -> bool:
        """
        Predicate for checking whether a corequisite is satisfied for a plan up to term_place
        """
        for term in plan[: term_place + 1]:
            if self._code in term["courses"]:
                return True
        return False


class UocReq:
    """UOC Requirement"""

    # also #courses

    def __init__(self, uoc, level, faculty) -> None:
        self._uoc = int(uoc)
        self._year = 0

    def is_satisfied(self, plan, term_place) -> bool:
        """
        Predicate for checking whether a UOC requirement is satisfied for a plan up to term_place
        """
        count = 0
        for term in plan[:term_place]:
            for course_code in term["courses"]:
                course = get_course(course_code)
                count += course.get_uoc()
        return count >= self._uoc


class DegreeReq:
    """Degree Requirement"""

    def __init__(self, program) -> None:
        self._program = program

    def is_satisfied(self, plan, _) -> bool:
        return False
