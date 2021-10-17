from __future__ import annotations
from src.models.course import Course
from src.utils.constants import NUM_TERMS, LIGHT_TERMS
from src.models.priority_queue import PriorityQueue
from src.models.graph import Graph
'''
implement new algos here and import them in algo.py to slot in
'''

def greedy_per_term(courses: list[Course], originalPlan: list[list[Course]]):
    # assuming the original plan is validated
    plan = originalPlan.copy()
    pq = PriorityQueue()
    # PLACEMENT PART 1: Place all unplaced courses into the priority 
    dependancies = Graph(courses)
    for course in courses:
        pq.push(dependancies, course)
    for index, term in enumerate(plan):
        term_number = index % NUM_TERMS
        refused = []
        unsatisfied = courses.copy()
        while len(term) != 3 and not pq.empty():
            course = pq.pop()
            # check dependancies satisfied
            if course.requirements.is_satisfied(plan, term_number) and term_number in course.terms:
                term.append(course.code)
            else:
                refused.append(course)
        #print("refused list")
        for x in refused:
            # print(x)
            pq.push(dependancies, x)