class And:
    """And Condition"""

    def __init__(self, lhs, rhs) -> None:
        self.lhs = lhs
        self.rhs = rhs

    def is_satisfied(self, plan, term_place) -> bool:
        return self.lhs.is_satisfied(plan, term_place) and self.rhs.satisfied(
            plan, term_place
        )


class Or:
    """Or Condition"""

    def __init__(self, lhs, rhs) -> None:
        self.lhs = lhs
        self.rhs = rhs

    def is_satisfied(self, plan, term_place) -> bool:
        return self.lhs.is_satisfied(plan, term_place) or self.rhs.is_satisfied(
            plan, term_place
        )
