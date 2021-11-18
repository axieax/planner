from src.models.course import Course


class And:
    """And Condition"""

    def __init__(self, args: list) -> None:
        self.args = args

    def is_satisfied(self, plan, term_place) -> bool:
        return all([arg.is_satisfied(plan, term_place) for arg in self.args])

    def is_beneficial(self, course: Course) -> bool:
        return any([arg.is_beneficial(course) for arg in self.args])

    def get_beneficial_courses(self, courses: list[Course]) -> list[Course]:
        return [*filter(self.is_beneficial, courses)]



class Or:
    """Or Condition"""

    def __init__(self, args : list) -> None:
        self.args = args

    def is_satisfied(self, plan, term_place) -> bool:
        return any([arg.is_satisfied(plan, term_place) for arg in self.args])

    def is_beneficial(self, course: Course) -> bool:
        return any([arg.is_beneficial(course) for arg in self.args])

    def get_beneficial_courses(self, courses: list[Course]) -> list[Course]:
        return [*filter(self.is_beneficial, courses)]