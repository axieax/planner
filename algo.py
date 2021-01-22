import json
from util import Course, Graph, PriorityQueue, relevant_prereqs_filter
from data import courses, plan, plan_specs, all_courses

DEBUG = False
NUM_TERMS = 4 # MOVE TO PLAN_SPECS?
# default specs

'''
Key definitions:
    course - Course object
    course_code: course.code - str
    plan - 2D list of course_codes (list of terms where each term is a list of course_codes)
        plan_index: index for the plan list - int
    plan_specs: plan specifications - dict
    _index - int
'''

def plan_stats(plan):
    ''' Returns a dictionary of stats related to the plan '''
    # find finishing term - first term from end that is non-empty
    finish_index = len(plan) - 1
    while not plan[finish_index]:
        finish_index -= 1
    # find starting term and study duration
    total_study_terms = 0
    start_index = finish_index
    for term_index, term_courses in enumerate(plan[:finish_index + 1]):
        if term_courses:
            start_index = min(start_index, term_index)
            total_study_terms += 1
    
    # TEMPORARY:
    # for plan_index, term_courses in enumerate(plan[:finish_index + 1]):
    #     print(f'Year {plan_index//NUM_TERMS + 1} Term {plan_index % NUM_TERMS}: {term_courses}')
    # print(f'Start: Year {start_index//NUM_TERMS + 1} Term {start_index % NUM_TERMS}')
    # print(f'Finish: Year {finish_index//NUM_TERMS + 1} Term {finish_index % NUM_TERMS}')
    # print(f'Terms of study: {total_study_terms} terms')
    # print(f'Total duration: {(finish_index - start_index + 1) // NUM_TERMS} years and {(finish_index - start_index + 1) % NUM_TERMS} terms; or {finish_index - start_index + 1} total terms')
    
    return {
        'start_index': start_index,
        'finish_index': finish_index,
        'num_study_terms': total_study_terms,
        'total_duration': finish_index - start_index + 1,
    }


def placed_index(plan, course_code):
    '''
    Returns the plan index where a course_code has been placed in the plan.
    Returns -1 if course is not placed in the plan.
    '''
    for plan_index, term_courses in enumerate(plan):
        if course_code in term_courses:
            return plan_index
    return -1


def first_possible_placement(plan, plan_specs, course):
    '''
    Returns the first possible term index in the given plan where a Course object can be placed.
    Returns -1 if its prerequisites cannot be satisfied.
    '''
    # TODO: co-requisite (first_possible_index could be earlier)

    # courses without prerequisites can be placed anytime
    if course.num_prerequisites() == 0:
        return plan_specs['starting_term']

    # find earliest placement
    earliest_placement = -1
    for comb in course.prereqs:
        # find the last term index where all the prerequisites are satisfied
        last_satisfied = -1
        all_placed = True
        for prereq_code in comb:
            # retrieve information about prerequisite
            prereq_index = placed_index(plan, prereq_code)
            if prereq_index == -1:
                # ignore combinations where not all prereqs have been placed
                all_placed = False
                break
            else:
                # make last_satisfied the last term index for all prereqs
                last_satisfied = max(last_satisfied, prereq_index)

        if all_placed:
            # earliest placement is the term after the term where all the prereqs are satisfied
            earliest_placement = last_satisfied + 1 if earliest_placement == -1 else min(earliest_placement, last_satisfied + 1)

    # earliest placement should be one of the course term offerings
    if earliest_placement == -1:
        return -1
    # keep increasing the earliest placement until it is one of the course term offerings
    while earliest_placement % NUM_TERMS not in course.terms:
        earliest_placement += 1
    return earliest_placement


def possible_insertion(plan, plan_specs, plan_index, selected_courses, course):
    '''
    Determines whether a Course object can be inserted for a given plan_index.
    '''
    # uoc check
    current_uoc = sum(selected_courses[course_code].uoc for course_code in plan[plan_index])
    if current_uoc + course.uoc > plan_specs['max_uoc'][plan_index]:
        return False
    # term offering check
    plan_term = plan_index % NUM_TERMS
    if plan_term not in course.terms:
        return False
    return True


def place_course(plan, plan_specs, selected_courses, course):
    '''
    Places a Course object into the plan.
    Returns True if able to successfully place the course, False otherwise.
    '''
    if DEBUG:
        print(f'Placing {course.code}', end=' ')

    # determine first possible index for placement
    first_possible_index = first_possible_placement(plan, plan_specs, course)
    if first_possible_index == -1:
        if DEBUG:
            print('.. failed')
        return False
    # ELSE IF GREATER THAN PLAN - INCREASE PLAN SIZE
    first_possible_year = first_possible_index // NUM_TERMS # 0-indexed
    first_possible_term = first_possible_index % NUM_TERMS

    # course placement
    year = first_possible_year
    while True:
        # find first possible year for placement
        for term in range(NUM_TERMS):
            # find first possible term for placement
            if year == first_possible_year and term < first_possible_term:
                continue
            plan_index = NUM_TERMS * year + term
            # NOTE: separate place into plan as a separate function
            # allocate more terms to plan if need be (same for possible insertion)
            # years_filled as a separate function - always have one year extra just in case (fill with default for specs)
            if possible_insertion(plan, plan_specs, plan_index, selected_courses, course):
                if DEBUG:
                    print(f'into year {year + 1} term {term}')
                plan[plan_index].append(course.code)
                return True
        year += 1


# place_course returns plans - normally just take first one

from copy import deepcopy

def generate_plans(plans, plan_specs, selected_courses, pq):
    ''' return a list of all possible combinations '''
    # base case
    if pq.empty():
        return plans

    # recursive case
    # original_plans = deepcopy(plans)
    new_plans = []
    course, _ = pq.pop()
    print(course.code)

    for offering_term in course.terms:
        new_plans_for_term = deepcopy(plans)
        mod_course = course.copy(terms=[offering_term])
        for plan in new_plans_for_term:
            place_course(plan, plan_specs, selected_courses, mod_course)
        new_plans += new_plans_for_term

    return generate_plans(new_plans, plan_specs, selected_courses, pq)


    # # base case
    # if not unplaced_course_codes:
    #     return [plan]
    # # recursive case
    # combinations = []
    # for course_code in unplaced_course_codes:
    #     # deep copy
    #     new_plan = deepcopy(plan)
    #     place_course(new_plan, plan_specs, selected_courses, selected_courses[course_code])
    #     combinations += backtrack_placement(plan, plan_specs, selected_courses, unplaced_course_codes - {course_code})
    # return combinations


def main(selected_course_codes, plan, plan_specs):
    '''
    Main algorithm for creating a plan for the provided courses
    Input:
        selected_courses_codes: list of all course codes for the courses selected (list of str)
        plan (2D list of course codes)
        plan_specs (dict containing plan info)
            starting_term (int)
            max_uoc: maximum uoc for each term (list of int)
    Output dict:
        plan: filled in with course codes (list)
        start_index: index in plan where the first term start (int)
        finish_index: index in plan where the last term ends (int)
        num_study_terms: number of terms in the plan with classes (int),
        total_duration: number of terms in the plan (int)
    '''
    # filter relevant prerequisites
    selected_courses = {}
    for course_code in selected_course_codes:
        # retrieve course data
        original_course = all_courses[course_code]
        # filter prerequisites, keeping those relevant to the selected courses
        filtered_prereqs = relevant_prereqs_filter(original_course.prereqs, selected_course_codes)
        filtered_course = original_course.copy(prereqs=filtered_prereqs)
        selected_courses[course_code] = filtered_course

    # find unplaced courses
    placed_course_codes = set(course_code for term in plan for course_code in term)
    unplaced_course_codes = set(selected_courses.keys()) - placed_course_codes

    # set up a graph representing course prerequisites for the selected courses
    prereqs = Graph(selected_courses.values())

    # create a priority queue for course placement
    # level of importance for course priority: dependency_score, course_rarity and course_level
    pq = PriorityQueue()

    # PART 1: Place unplaced courses with dependencies into priority queue
    for course_code in unplaced_course_codes:
        if len(prereqs.immediate_dependencies(course_code)) > 0:
            pq.push(prereqs, selected_courses[course_code])

    # place courses from priority queue
    while not pq.empty():
        # retrieve the course with the highest priority for placement
        course, priority_summary = pq.pop()

        # place course
        if not place_course(plan, plan_specs, selected_courses, course):
            # place it back in the priority queue with less priority if not placed (to prevent infinite loop)
            new_dependency_score = priority_summary['dependency_score'] - 1
            pq.push(prereqs, course, dependency_score=new_dependency_score)
            continue
        # course placed
        unplaced_course_codes.remove(course.code)

    # PART 2: Place remaining unplaced courses using backtracking to find optimal placement
    print(len(unplaced_course_codes))

    for course_code in unplaced_course_codes:
        pq.push(prereqs, selected_courses[course_code])

    print(pq.queue)
    # place courses from priority queue
    # while not pq.empty():
    #     # retrieve the course with the highest priority for placement
    #     course, priority_summary = pq.pop()

    #     #
    #     for _ in range(len(course.terms)):
    #         deepcopy(plans)
        
    #     # may be easier if place_course returned the new plan (immutable plans)
    #     for term in 

    plans = [plan]
    plans = generate_plans(plans, plan_specs, selected_courses, pq)
    # print(plans)

    shortest_length = min(plan_stats(p)['total_duration'] for p in plans)
    shortest = [p for p in plans if plan_stats(p)['total_duration'] == shortest_length]
    # print(shortest)
    for p in shortest:
        ''' Returns a dictionary of stats related to the plan '''
        # find finishing term - first term from end that is non-empty
        finish_index = len(p) - 1
        while not p[finish_index]:
            finish_index -= 1
        # find starting term and study duration
        total_study_terms = 0
        start_index = finish_index
        for term_index, term_courses in enumerate(p[:finish_index + 1]):
            if term_courses:
                start_index = min(start_index, term_index)
                total_study_terms += 1
        
        # TEMPORARY:
        for plan_index, term_courses in enumerate(p[:finish_index + 1]):
            print(f'Year {plan_index//NUM_TERMS + 1} Term {plan_index % NUM_TERMS}: {term_courses}')
        print(f'Start: Year {start_index//NUM_TERMS + 1} Term {start_index % NUM_TERMS}')
        print(f'Finish: Year {finish_index//NUM_TERMS + 1} Term {finish_index % NUM_TERMS}')
        print(f'Terms of study: {total_study_terms} terms')
        print(f'Total duration: {(finish_index - start_index + 1) // NUM_TERMS} years and {(finish_index - start_index + 1) % NUM_TERMS} terms; or {finish_index - start_index + 1} total terms')


    # backtrack_placement(plan, plan_specs, selected_courses, unplaced_course_codes)

    # place in same priority order - but try different offering terms

    # calculate plan stats
    stats = plan_stats(plan)
    # print(plans[0])
    return {
        'plan': plan[:stats['finish_index'] + 1],
        'stats': stats,
    }


if __name__ == '__main__':
    main([course.code for course in courses], plan, plan_specs)

### Notes:
# Consider both term offerings not just the first available option TODO
# Find last placed course and don't write terms after it

# A BACKTRACKING ALGORITHM MIGHT BE BETTER (sort by effiency, then practicality - level)
# TERM PLACEMENT BASED ON TERM OFFERINGS OF OTHER COURSES (TERM RARITY? FROM OTHER COURSES?)
