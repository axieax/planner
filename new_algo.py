from copy import deepcopy
from util import Course, Graph, PriorityQueue, relevant_prereqs_filter
from data import courses, plan, plan_specs, all_courses

DEBUG = False
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

def print_plan(plan):
    stats = plan_stats(plan)
    start_index = stats['start_index']
    finish_index = stats['finish_index']
    total_study_terms = stats['total_study_terms']
    for plan_index, term_courses in enumerate(plan[:finish_index + 1]):
        print(f'Year {plan_index//NUM_TERMS + 1} Term {plan_index % NUM_TERMS}: {term_courses}')
    print(f'Start: Year {start_index//NUM_TERMS + 1} Term {start_index % NUM_TERMS}')
    print(f'Finish: Year {finish_index//NUM_TERMS + 1} Term {finish_index % NUM_TERMS}')
    print(f'Terms of study: {total_study_terms} terms')
    print(f'Total duration: {(finish_index - start_index + 1) // NUM_TERMS} years and {(finish_index - start_index + 1) % NUM_TERMS} terms; or {finish_index - start_index + 1} total terms')


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

    return {
        'start_index': start_index,
        'finish_index': finish_index,
        'total_study_terms': total_study_terms,
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
    Places a Course object into the plan. Returns a list of plans with the course placed in each plan
    for each of the course's term offerings.
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


def average(x):
    return sum(x) / len(x)

def evaluate_plan(plan):
    '''
    Evalutation based on how balanced the plan is
        average term course density (number of courses per term)
        level difference (average level per term)
    '''
    term_density = {}
    level_difference = 0
    for term_index, term in plan:
        if term:
            # term density
            num_courses = len(terms)
            term_density[num_courses] = term_density.get(num_courses, 0) + 1
            # level difference
            year = term_index // 4 + 1
            term_levels = [int(c[4]) for c in term]
            level_difference += abs(year - average(term_levels))
    
    
    
    # multiple courses in same summer bad
    # average term level density
    total_course_density = 0
    total_level_density = 0
    for term in plan:
        if term:
            course_density = len(term)
            level_density = sum(int(c[4]) for c in term) / course_density
    
    total_study_terms = plan_stats(plan)['total_study_terms']
    average_course_density = total_course_density / total_study_terms
    average_level_density = total_level_density / total_study_terms
    pass



def main(plan, plan_specs, selected_course_codes, find_optimal):

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
    for course_code in unplaced_course_codes:
        pq.push(prereqs, selected_courses[course_code])

    if find_optimal:
        # find all possible plan permutations
        plans = generate_plans([plan], plan_specs, selected_courses, pq)
        shortest_plan_length = min(plan_stats(p)['total_duration'] for p in plans)
        plans = [p for p in plans if plan_stats(p)['total_duration'] == shortest_plan_length]
        # sort by difficulty, lowest average num courses per term
    else:
        plans = [plan_placement(plan, plan_specs, selected_courses, unplaced_course_codes, pq)]
    
    for p in plans:
        print_plan(p)
        print('')

    return {
        'plans': [
            {
                'plan': p,
                'specs': plan_stats(p),
            }
            for p in plans
        ],
    }
    
    # plans: array of {
    #   'courses': [],
    #   'max_uoc': 20,
    # }


def plan_placement(plan, plan_specs, selected_courses, unplaced_course_codes, pq):
    if pq.empty():
        return plan
    
    course, _ = pq.pop()
    new_plan = place_course(plan, plan_specs, selected_courses, course)[0]
    unplaced_course_codes.remove(course.code)
    return plan_placement(new_plan, plan_specs, selected_courses, unplaced_course_codes, pq)



def generate_plans(plans, plan_specs, selected_courses, pq):
    if pq.empty():
        return plans
    
    course, _ = pq.pop()
    new_plans = []
    for plan in plans:
        possible_plans = place_course(plan, plan_specs, selected_courses, course)
        new_plans += possible_plans
    return generate_plans(new_plans, plan_specs, selected_courses, pq)




if __name__ == '__main__':
    main(plan, plan_specs,[course.code for course in courses], True)
    # option for fast placement - chuck everything in pq
