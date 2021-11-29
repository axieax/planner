from src.models.course import Course
from src.models.plan import PlanType


class Requirement:
    """Requirement interface"""

    def is_satisfied(self, plan_details: PlanType, term_place: int) -> bool:
        """
        Checks whether a Requirement is satisfied for a given plan

        :param plan_details PlanType: details for a plan
        :param term_place int: index of term to place the course
        :rtype bool: true if Requirement is satisfied for the given plan at term_place, false otherwise
        """
        raise NotImplementedError

    def filter_relevant_courses(self, courses: list[Course]) -> list[Course]:
        """
        Filters a given list of courses which are relevant to satisfying the Requirement

        :param courses list[Course]: courses to check
        :rtype list[Course]: filtered list of courses
        """
        raise NotImplementedError
