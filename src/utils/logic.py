class And:
    """And Condition"""

    def __init__(self, *args) -> None:
        self._args = args

    def is_satisfied(self, plan, term_place) -> bool:
        return all(x.is_satisfied(plan, term_place) for x in self._args)


class Or:
    """Or Condition"""

    def __init__(self, *args) -> None:
        self._args = args

    def is_satisfied(self, plan, term_place) -> bool:
        return any(x.is_satisfied(plan, term_place) for x in self._args)
