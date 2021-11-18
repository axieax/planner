from data.get_course import get_course
from src.models.course import Course
from src.utils.logic import And, Or

# NOTE: if _requirement == true, then no requirements are needed to sit the course
class Requirement:
    def __init__(self, requirement) -> None:
        self._requirement = requirement

    def is_satisfied(self, plan, term_place) -> bool:
        if self.has_no_prereqs():
            return True
        return self._requirement.is_satisfied(plan, term_place)

    def has_no_prereqs(self) -> None:
        return self._requirement == True

    def is_beneficial(self, course: Course) -> bool:
        return self._requirement.is_beneficial(course)

    def get_beneficial_courses(self, courses: list[Course]) -> list[Course]:
        return [*filter(self.is_beneficial, courses)]

class PreReq:
    """Prerequisites"""
    def __init__(self, code: str) -> None:
        self._code = code
        self._course = get_course(code)

    def is_satisfied(self, plan, term_place: int) -> bool:
        """
        Predicate for checking whether a prerequisite is satisfied for a plan up to term_place
        """
        for term in plan[:term_place]:
            if self._code in term["courses"]:
                return True
        return False

    def is_beneficial(self, course) -> bool:
        return course.code == self._code


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

    def is_beneficial(self, course) -> bool:
        return course.code == self._course.code


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

    # this one is wierd, may lead to wierd behaviour
    def is_beneficial(self, course) -> bool:
        return course.uoc > 0


class DegreeReq:
    """Degree Requirement"""

    def __init__(self, program) -> None:
        self._program = program

    # TODO: currently not passed, will implement
    def is_satisfied(self, plan, _) -> bool:
        return False


def parse_requirement(prereq_str: str):
    # find ors and ands and split along them
    # assume ands supersede or's - bad assumption, but is what lots of courses use
    if prereq_str == "":
        return Requirement(True)
    poss_strings = prereq_str.split("\n")
    for string in poss_strings:
        if string.count("Pre") > 0:
            string = " ".join(string.split()[1:])
            # assume these are prerequisites
            # TODO: expand to more
            ands = string.split("and")
            ands_and_ors = [Or(PreReq(code.strip()) for code in a.split("or")) for a in ands]
            return Requirement(And(ands_and_ors))
