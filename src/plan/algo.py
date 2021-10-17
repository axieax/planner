""" Main Algorithm """
from dataclasses import replace
from data.get_course import get_courses
from src.plan.algos import greedy_per_term

# lookup from data


def place_courses(degree_details: dict, plan_details: dict, plan: list, generate_plan: function = greedy_per_term) -> list:
    """
    Pushy

    Args:
        - Current Plan (plan)
        - Degree Information (your stream, program name)
        - Selected Courses that are not in plan (plan_details)
        - Course Overrides (inside plan_details) (server side validation)
    """
    # here, we want to do preamble processing
    courses = get_courses(plan_details['courses_list'])
    
    # TODO: verify that the current plan is sane
    
    generate_plan(courses, degree_details, plan)


if __name__ == '__main__':
    place_courses({}, {'courses_list': ['COMP1511', 'COMP2521', 'COMP2521', 'MATH1141', 'MATH1241']}, [])