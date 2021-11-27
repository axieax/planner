from data.get_course import get_course
from src.models import Course, PlanType, Requirement
from src.utils.logic import And, Or


class CourseReq(Requirement):
    """Course Requirement abstract class"""

    def __init__(self, code: str) -> None:
        self._code = code
        self._course = get_course(code)

    def filter_relevant_courses(self, courses: list[Course]) -> list[Course]:
        return [course for course in courses if course.code == self._code]


class PreReq(CourseReq):
    """Prerequisites"""

    def __init__(self, code: str) -> None:
        super().__init__(code)

    def is_satisfied(self, plan_details: PlanType, term_place: int) -> bool:
        """
        Predicate for checking whether a prerequisite is satisfied for a plan up to term_place
        """
        terms = plan_details["plan"]["terms"]
        for term in terms[:term_place]:
            if self._code in term["courses"]:
                return True
        return False


class CoReq(CourseReq):
    """Corequisites"""

    def __init__(self, code) -> None:
        super().__init__(code)

    def is_satisfied(self, plan_details: PlanType, term_place: int) -> bool:
        """
        Predicate for checking whether a corequisite is satisfied for a plan up to term_place
        """
        terms = plan_details["plan"]["terms"]
        for term in terms[: term_place + 1]:
            if self._code in term["courses"]:
                return True
        return False


class UocReq(Requirement):
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

    def is_beneficial(self, course: Course) -> bool:
        return False


class DegreeReq:
    """Degree Requirement"""

    def __init__(self, program) -> None:
        self._program = program

    # TODO: currently not passed, will implement
    def is_satisfied(self, plan, _) -> bool:
        return False


def parse_requirement(prereq_str: str) -> Requirement:
    # find ors and ands and split along them
    # assume ands supersede or's - bad assumption, but is what lots of courses use
    if prereq_str == "":
        return None
    poss_strings = prereq_str.split("\n")
    for string in poss_strings:
        if string.count("Pre") > 0:
            string = " ".join(string.split()[1:])
            # assume these are prerequisites
            # TODO: expand to more
            ands = string.split("and")
            ands_and_ors = [
                Or(PreReq(code.strip()) for code in a.split("or")) for a in ands
            ]
            return And(ands_and_ors)
