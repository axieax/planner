from __future__ import annotations
from src.utils.constants import NUM_TERMS, TERMS
from src.models import PriorityQueue, Graph, Course, PlanType, Plan, Term


def greedy_per_term(plan_details: PlanType, selected_courses: list[Course]):
    """
    Algorithm for placing courses greedily by filling each term with available courses

    Args:
        - plan_details
        - courses
    """
    plan: Plan = plan_details["plan"]
    requirements = Graph(selected_courses)

    # PLACEMENT PART 1: Place all unplaced courses into the priority
    pq = PriorityQueue()
    for course in selected_courses:
        pq.push(requirements, course)

    # TODO: allocate more terms

    # place courses
    for term_index, term in enumerate(plan["terms"]):
        unsatisfied = []
        while not pq.empty():
            # try to place courses from the PriorityQueue
            course = pq.pop()
            if (
                # course can be placed
                term["term"] in course.terms
                # requirements satisfied
                and course.requirements.is_satisfied(plan_details, term_index)
                # uoc won't exceed maximum
                and course.uoc + term["current_uoc"] <= term["max_uoc"]
                # NOTE: walrus operator can be used for the above LHS
            ):
                term["courses"].append(course.code)
                term["current_uoc"] += course.uoc
            else:
                unsatisfied.append(course)

        # return unsatisfied courses back to PriorityQueue
        for course in unsatisfied:
            pq.push(requirements, course)

    # update plan details
    return plan_details
