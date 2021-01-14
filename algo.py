import json
from util import Course, Graph, PriorityQueue
from data import courses, plan, plan_specs, all_courses
from util import relevant_prereqs_filter

DEBUG = False
NUM_TERMS = 4
# default specs

def course_lookup(selected_courses, course_code):
    '''
    Returns the Course object in selected_courses (list) with the given course_code (str).
    Returns None if unable to find the course.
    '''
    for course in selected_courses:
        if course.code == course_code:
            return course
    return None


def placed_index(plan, course):
    '''
    Returns the plan index (int) where a Course object has been placed in the plan (list of lists).
    Returns -1 if course is not placed in the plan.
    '''
    for plan_index, term_courses in enumerate(plan):
        if course in term_courses:
            return plan_index
    return -1


def first_possible_placement(plan, plan_specs, selected_courses, course):
    '''
    Returns the first possible term index (int) in the given plan (list of lists) with plan_specs (dict)
    where a Course object can be placed. Returns -1 if its prerequisites cannot be satisfied.
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
            prereq = course_lookup(selected_courses, prereq_code)
            prereq_index = placed_index(plan, prereq)
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


def possible_insertion(plan, plan_specs, plan_index, course):
    '''
    Determines whether a Course object can be inserted for a given plan_index (int)
    in the plan (list of lists) with plan_specs (dict).
    '''
    # uoc check
    current_uoc = sum(x.uoc for x in plan[plan_index])
    if current_uoc + course.uoc > plan_specs['max_uoc'][plan_index]:
        return False
    # term offering check
    plan_term = plan_index % NUM_TERMS
    if plan_term not in course.terms:
        return False
    return True


def place_course(plan, plan_specs, selected_courses, course):
    '''
    Places a Course object into the plan (list of lists) with plan_specs (dict).
    selected_courses (list of Course objects) is passed onto first_possible_placement.
    Returns True if able to successfully place the course, False otherwise.
    '''
    if DEBUG:
        print(f'Placing {course.code}', end=' ')

    # determine first possible index for placement
    first_possible_index = first_possible_placement(plan, plan_specs, selected_courses, course)
    if first_possible_index == -1:
        if DEBUG:
            print('.. failed')
        return False
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
            if possible_insertion(plan, plan_specs, plan_index, course):
                if DEBUG:
                    print(f'into year {year + 1} term {term}')
                plan[plan_index].append(course)
                return True
        year += 1


def main(selected_course_codes, plan, plan_specs):
    '''
    Main algorithm for creating a plan for the provided courses
    Input:
        selected_courses_codes (list of str)
        plan (list)
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
    selected_courses = []
    for course_code in selected_course_codes:
        # retrieve course data
        original_course = all_courses[course_code]
        # filter prerequisites, keeping those relevant to the selected courses
        filter_course = Course(course_code, original_course.terms, '', original_course.uoc)
        filter_course.prereqs = relevant_prereqs_filter(selected_course_codes, original_course) # use getter and setter, or this function returns new Course object?
        selected_courses.append(filter_course)
    
    # set up a graph representing course prerequisites
    prereqs = Graph(selected_courses)

    # create a priority queue for course placement
    # level of importance for course priority: dependency_score, course_rarity and course_level
    pq = PriorityQueue()
    placed_courses = set()

    # place courses into priority queue
    for course in selected_courses:
        pq.push(prereqs, course)

    # place courses from priority queue
    while not pq.empty():
        # retrieve the course with the highest priority for placement
        course, priority_summary = pq.pop()
        # course already placed
        if course in placed_courses:
            continue
        # course unable to be placed
        if not place_course(plan, plan_specs, selected_courses, course):
            # place it back in the priority queue with less priority if not placed (to prevent infinite loop)
            new_dependency_score = priority_summary['dependency_score'] - 1
            pq.push(prereqs, course, dependency_score=new_dependency_score)
            continue
        # course placed
        placed_courses.add(course)


    # information about plan
    # finishing term - first term from end that is non-empty
    finish_index = len(plan) - 1
    while not plan[finish_index]:
        finish_index -= 1
    # study duration
    total_study_terms = 0
    start_index = finish_index
    for term_index, term_courses in enumerate(plan[:finish_index + 1]):
        if term_courses:
            start_index = min(start_index, term_index)
            total_study_terms += 1

    # TEMPORARY:
    plan = plan[:finish_index + 1]
    for plan_index, term_courses in enumerate(plan):
        print(f'Year {plan_index//NUM_TERMS + 1} Term {plan_index % NUM_TERMS}: {[course.code for course in term_courses]}')
    print(f'Start: Year {start_index//NUM_TERMS + 1} Term {start_index % NUM_TERMS}')
    print(f'Finish: Year {finish_index//NUM_TERMS + 1} Term {finish_index % NUM_TERMS}')
    print(f'Terms of study: {total_study_terms} terms')
    print(f'Total duration: {(finish_index - start_index + 1) // NUM_TERMS} years and {(finish_index - start_index + 1) % NUM_TERMS} terms; or {finish_index - start_index + 1} total terms')

    return {
        'start_index': start_index,
        'finish_index': finish_index,
        'num_study_terms': total_study_terms,
        'total_duration': finish_index - start_index + 1,
        'plan': [[course.code for course in term_courses] for term_courses in plan],
    }


if __name__ == '__main__':
    main([course.code for course in courses], plan, plan_specs)

### Notes:
# Consider both term offerings not just the first available option TODO
# Find last placed course and don't write terms after it

# A BACKTRACKING ALGORITHM MIGHT BE BETTER (sort by effiency, then practicality - level)
# TERM PLACEMENT BASED ON TERM OFFERINGS OF OTHER COURSES (TERM RARITY? FROM OTHER COURSES?)
