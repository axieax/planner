class And:
    """And Condition"""

    def __init__(self, args) -> None:
        self.args = args

    def is_satisfied(self, plan, term_place) -> bool:
        return all([arg.is_satisfied(plan, term_place) for arg in self.args])


class Or:
    """Or Condition"""

    def __init__(self, lhs, rhs) -> None:
        self.lhs = lhs
        self.rhs = rhs

    def is_satisfied(self, plan, term_place) -> bool:
        return any([arg.is_satisfied(plan, term_place) for arg in self.args])
