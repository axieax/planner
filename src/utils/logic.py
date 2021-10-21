class And:
    """And Condition"""

    def __init__(self, args: list) -> None:
        self.args = args

    def is_satisfied(self, plan, term_place) -> bool:
        return all([arg.is_satisfied(plan, term_place) for arg in self.args])


class Or:
    """Or Condition"""

    def __init__(self, args : list) -> None:
        self.args = args

    def is_satisfied(self, plan, term_place) -> bool:
        return any([arg.is_satisfied(plan, term_place) for arg in self.args])
