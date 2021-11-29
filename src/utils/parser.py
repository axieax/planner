from src.models import Requirement, And, Or

# case insensitive, optional plural s
COURSE_REQUIREMENT_MAP = {
    "prereq",
    "prerequisite",
    "pre-requisite",
    "must have completed",
}

BINARY_OPERATORS = {"and", "or"}
# TODO: not


def parse_requirement(requirement_str: str) -> Requirement:
    # highlight operators and expand outwards
    tokens = requirement_str.split()
    regions = requirement_str.split(", ")
    return parse_expression([token.lower() for token in tokens], 0, -1)


def parse_expression(tokens: list, start: int, end: int) -> Requirement:

    # find first operator
    first_operator_index, first_operator = (0, "")
    for index, token in enumerate(tokens):
        if token in BINARY_OPERATORS:
            first_operator_index = index
            first_operator = token
            break

    # find end of useless?

    # Resolve commas, right to left
    last_operator_index, last_operator = ("idk", "and")
    # find last operator on same level

    # split around operator
    lhs = parse_expression(tokens, 0, first_operator_index)
    rhs = parse_expression(tokens, first_operator_index + 1, -1)
    # TODO: normal
    if first_operator == "and":
        return And([lhs, rhs])
    elif first_operator == "or":
        return Or([lhs, rhs])
    else:
        raise ValueError("invalid composite operator")


# EXTENSION: https://tree-sitter.github.io/tree-sitter parsing
def parse_requirements_treesitter(requirement_str: str) -> Requirement:
    pass
