from src.models import Course, PlanType
from src.utils.requirements import Requirement


# TODO: args as *args instead


class CompositeLogic(Requirement):
    def __init__(self, args: list[Requirement]) -> None:
        self.args = args

    def filter_relevant_courses(self, courses: list[Course]) -> list[Course]:
        relevant_courses = set()
        for arg in self.args:
            relevant_courses |= set(arg.filter_relevant_courses(courses))
        return list(relevant_courses)


class And(CompositeLogic):
    """And Condition"""

    def __init__(self, args: list[Requirement]) -> None:
        super().__init__(args)

    def is_satisfied(self, plan_details: PlanType, term_place: int) -> bool:
        return all(arg.is_satisfied(plan_details, term_place) for arg in self.args)


class Or(CompositeLogic):
    """Or Condition"""

    def __init__(self, args: list[Requirement]) -> None:
        super().__init__(args)

    def is_satisfied(self, plan_details: PlanType, term_place: int) -> bool:
        return any(arg.is_satisfied(plan_details, term_place) for arg in self.args)


class Not(Requirement):
    """Not Condition"""

    # NOTE: is this even necessary?

    def __init__(self, requirement: Requirement) -> None:
        self.requirement = requirement

    def is_satisfied(self, plan_details: PlanType, term_place: int) -> bool:
        return not self.requirement.is_satisfied(plan_details, term_place)

    # def filter_relevant_courses(self, courses: list[Course]) -> list[Course]:
    #     raise NotImplementedError
