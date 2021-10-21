""" Main Algorithm """
from typing import Callable
from data import get_courses
from src.plan.greedy import greedy_per_term
from src.models import PlanType


def place_courses(
    plan_details: PlanType,
    generate_plan: Callable = greedy_per_term,
) -> PlanType:
    """
    Places courses for a plan

    Args:
        - plan_details
    """
    # get Course objects for a user's selected courses
    selected_courses = get_courses(plan_details["selected_courses"])

    # TODO: verify that the current plan is sane
    # 1. validate PlanType

    return generate_plan(plan_details, selected_courses)


if __name__ == "__main__":
    place_courses(
        {
            "start": {
                "year": "2020",
                "term": "1",
            },
            "end": {
                "year": "2020",
                "term": "1",
            },
            "num_terms": 4,
            "program": "3789",
            "selected_courses": [
                "COMP1511",  # t1
                "COMP1521",  # t3
                "COMP1531",  # t3
                "COMP2511",  # t3
                "COMP2521",  # t2
                "MATH1081",  # t1
                "MATH1141",  # t1
                "MATH1241",  # t2
                "DATA1001",  # t2
            ],
            "plan": {
                "terms": []
            },  # term dict: year, term, max_uoc, courses, current_uoc
        },
    )
