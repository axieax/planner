from copy import deepcopy
from numpy import average, var as variance
from util import Course, Graph, PriorityQueue, course_level, relevant_prereqs_filter
from data import courses, plan, plan_specs, all_courses

NUM_TERMS = 4

'''
Key definitions:
    course - Course object
    course_code: course.code - str
    plan - 2D list of course_codes (list of terms where each term is a list of course_codes)
        plan_index: index for the plan list - int
    plan_specs: plan specifications - dict
    *_index - int
'''

"""
Plan info functions
"""

def plan_balance(plan):
    '''
    Calculates how balanced the plan is based on:
        term density variance (number of courses per term)
        difficulty variance (change in average level per term)
    '''
    # separate summer and standard terms
    summer_terms = []
    standard_terms = []
    for plan_index, term in enumerate(plan):
        if plan_index % 4 == 0:
            summer_terms.append(term)
        else:
            standard_terms.append(term)

    # calculate term density variance
    summer_term_density_variance = variance([len(term) for term in summer_terms])
    standard_term_density_variance = variance([len(term) for term in standard_terms])

    # calculate difficulty variance
    # ideally, the change in difficulty for the plan (level delta) should be constant -> minimise variance in change in level delta
    info = plan_info(plan)
    study_plan = plan[info['start_index']: info['finish_index'] + 1]
    average_term_levels = [average([course_level(course_code) for course_code in term]) for term in plan if len(term) != 0]
    term_level_delta = [average_term_levels[i + 1] - average_term_levels[i] for i in range(len(average_term_levels) - 1)]    
    difficulty_variance = variance(term_level_delta)

    return 2 * standard_term_density_variance + summer_term_density_variance + difficulty_variance


def plan_info(plan):
    ''' Returns a dictionary of info regarding the plan '''
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

    return {
        'start_index': start_index,
        'finish_index': finish_index,
        'total_study_terms': total_study_terms,
        'total_duration': finish_index - start_index + 1,
    }


def print_plan(plan):
    ''' Debugging: plan print '''
    info = plan_info(plan)
    start_index = info['start_index']
    finish_index = info['finish_index']
    total_study_terms = info['total_study_terms']
    for plan_index, term_courses in enumerate(plan[:finish_index + 1]):
        print(f'Year {plan_index//NUM_TERMS + 1} Term {plan_index % NUM_TERMS}: {term_courses}')
    print(f'Start: Year {start_index//NUM_TERMS + 1} Term {start_index % NUM_TERMS}')
    print(f'Finish: Year {finish_index//NUM_TERMS + 1} Term {finish_index % NUM_TERMS}')
    print(f'Terms of study: {total_study_terms} terms')
    print(f'Total duration: {(finish_index - start_index + 1) // NUM_TERMS} years and {(finish_index - start_index + 1) % NUM_TERMS} terms; or {finish_index - start_index + 1} total terms')


"""
Algorithm functions
"""

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
    earliest_placement = plan_specs['starting_term']
    possible_placement = True if course.num_prerequisites() == 0 else False
    for comb in course.prereqs:
        # find indices where its prereqs have been placed
        prereqs_placement = [placed_index(plan, prereq_code) for prereq_code in comb]
        # ignore if not all prereqs placed for this combination - try next combination
        if -1 in prereqs_placement:
            continue
        last_satisfied = max(prereqs_placement)
        if possible_placement:
            # minimise earliest_placement if already calculated before
            earliest_placement = min(earliest_placement, last_satisfied + 1)
        else:
            # first calculation for earliest_placement
            earliest_placement = last_satisfied + 1
            possible_placement = True

    # no prerequisite combinations can be satisfied
    if not possible_placement:
        raise ValueError(f'{course.code}: unable to satisfy prerequisites')

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
    return True


def place_course(plan, plan_specs, selected_courses, course):
    '''
    Places a Course object into the plan. Returns a list of plans with the course placed for each of the course's term offerings.
    '''
    possible_plans = []

    # determine first possible index for placement
    first_possible_index = first_possible_placement(plan, plan_specs, course)

    # find possible plans for each term
    possible_terms = course.terms.copy()
    plan_index = first_possible_index
    while True:
        plan_term = plan_index % NUM_TERMS
        # combinations for each term offering exhausted
        if len(possible_terms) == 0:
            break
        # course has not been added yet for a term offering, and able to be placed in that term
        if plan_term in possible_terms and possible_insertion(plan, plan_specs, plan_index, selected_courses, course):
            # create a copy of the plan and place the course in the term
            new_plan = deepcopy(plan)
            new_plan[plan_index].append(course.code)
            # append to possible plans and remove the term once found (find plans for remaining terms)
            possible_plans.append(new_plan)
            possible_terms.remove(plan_term)
        plan_index += 1

    return possible_plans


def plan_placement(plan, plan_specs, selected_courses, unplaced_course_codes, pq):
    '''
    Places all the courses in the PriorityQueue pq into the provided plan.
    '''
    # base case
    if pq.empty():
        return plan

    # retrieve the course with the highest priority for placement
    course = pq.pop()
    # place the course into its first available term offering
    new_plan = place_course(plan, plan_specs, selected_courses, course)[0]
    unplaced_course_codes.remove(course.code)

    # recursively place remaining courses from the priority queue
    return plan_placement(new_plan, plan_specs, selected_courses, unplaced_course_codes, pq)


def generate_plans(plans, plan_specs, selected_courses, pq):
    '''
    Generates all possible plans for placing the courses from pq into the provided plan
    (based on first available term offerings).
    '''
    # base case
    if pq.empty():
        return plans

    # retrieve the course with the highest priority for placement
    course = pq.pop()
    # compute new list of plans with the course placed in each plan
    new_plans = []
    for plan in plans:
        # list of plans with course placed in each of its first available term offerings
        possible_plans = place_course(plan, plan_specs, selected_courses, course)
        new_plans += possible_plans

    # recursively place remaining courses from the priority queue
    return generate_plans(new_plans, plan_specs, selected_courses, pq)


def main(plan, plan_specs, selected_course_codes, find_optimal):
    '''
    Main algorithm for creating a plan for the provided courses.
    Returns a list of plans sorted by how balanced it is.
    Input:
        plan (2D list of course codes)
        plan_specs (dict containing plan info)
            starting_term (int)
            max_uoc: maximum uoc for each term (list of int)
        selected_courses_codes: list of all course codes for the courses selected (list of str)
        find_optimal: find optimal placement (bool)
    Output dict containing plans:
        plan (2D list of course codes - input with unplaced courses placed)
        info (dict containing plan info)
            start_index: index in plan where the first term starts (int)
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

    # set up a graph modelling course prerequisites and dependencies for the selected courses
    prereqs = Graph(selected_courses.values())

    # create a priority queue for course placement
    pq = PriorityQueue()

    # PLACEMENT PART 1: Place unplaced courses with dependencies into the priority queue
    for course_code in unplaced_course_codes:
        if len(prereqs.immediate_dependencies(course_code)) > 0:
            pq.push(prereqs, selected_courses[course_code])

    # place courses from priority queue
    plan = plan_placement(plan, plan_specs, selected_courses, unplaced_course_codes, pq)

    # PLACEMENT PART 2: Find optimal placement for remaining courses
    # Place remaining unplaced courses into the priority queue
    print(plan)
    for course_code in unplaced_course_codes:
        print(course_code, end=' ')
        print(selected_courses[course_code].terms)
        pq.push(prereqs, selected_courses[course_code])

    if find_optimal:
        # find all possible plan permutations
        plans = generate_plans([plan], plan_specs, selected_courses, pq)
        # keep the shortest plans
        shortest_plan_length = min(plan_info(plan)['total_duration'] for plan in plans)
        plans = [plan for plan in plans if plan_info(plan)['total_duration'] == shortest_plan_length]
        # sort plans by its balance score (to find optimal)
        plans.sort(key=plan_balance, reverse=False)
    else:
        # place remaining unplaced courses using the same approach as before
        plans = [plan_placement(plan, plan_specs, selected_courses, unplaced_course_codes, pq)]

    # TEMP: prune plan length
    plans = [plan[:plan_info(plan)['finish_index'] + 1] for plan in plans]

    # sort each term alphabetically
    for plan in plans:
        for term in plan:
            term.sort()

    # remove duplicate plans if they exist
    memo = set(str(plan) for plan in plans)
    new_plans = []
    for plan in plans:
        memo.remove(str(plan))
        if str(plan) not in memo:
            # ignore plan if its duplicates exist
            new_plans.append(plan)
    plans = new_plans

    # TEMP: debugging
    # for p in plans:
    #     print_plan(p)
    #     print(plan_balance(p))
    #     print('')

    # for p in plans:
        # print_plan(p)
        # print('')
    print_plan(plans[0])

    return {
        'plans': [
            {
                'plan': p,
                'info': plan_info(p),
            }
            for p in plans
        ],
    }


if __name__ == '__main__':
    main(plan, plan_specs,[course.code for course in courses], find_optimal=False)

# TODO: add dynamic list size increase (can remove finish_index)
# plans: array of {
#   'courses': [],
#   'max_uoc': 20,
# } ??
# term index instead of plan index - e.g. term_index, term in enumerate(plan)
