from copy import deepcopy
from numpy import average, var as variance
from itertools import combinations
from util import Course, Graph, PriorityQueue, course_level, relevant_prereqs_filter
from data import NUM_TERMS, courses, plan, plan_specs, all_courses

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
    long = 0
    # create a priority queue for course placement
    pq = PriorityQueue()

    # PLACEMENT PART 1: Place all unplaced courses into the priority queue
    for course_code in unplaced_course_codes:
        pq.push(prereqs, selected_courses[course_code])
    
    if long == 1:
        # create a backtracking queue based on the possible courses, and allow for an iterating search 
        backpq = []
        while not pq.empty():
            backpq.append(pq.pop())
        
        for i in range(20):
            plan = [[] for _ in range(i)] # we will have to change this into a nicer object possibly, to accomodate preferences and stuff
            recursive_check(backpq, 0, 0, plan)


                
    else:


        plan = [[] for _ in range(20)]
        for index, term in enumerate(plan):
            term_number = index % NUM_TERMS
            if term_number == 0:
                continue
            #print(f'Term: {term_number}')
            refused = []
            unsatisfied = set([x[3].code for x in pq.queue])

            while len(term) != 3:
                if pq.empty():
                    break
                    
                course = pq.pop()
                # check prereqs satisfied
                if term_number in course.terms and (all(not x for x in course.prereqs) or any(unsatisfied & set(comb) == set() for comb in course.prereqs)):
                    term.append(course.code)
                else:
                    refused.append(course)
            #print("refused list")
            for x in refused:
                # print(x)
                pq.push(prereqs, x)
    print(plan)
    return
    
def recursive_check(backpq, index, term, plan):
    rejected = []
    possible = []
    term_number = index % 4
    # anything in the ordered course list minus the stuff in the plan
    unsatisfied = set([x[3].code for x in backpq])
    for t in plan:
        for c in t:
            unsatisfied.remove(c)
    if term_number == 0:
        return # we avoid summer for now, we can bring it back in. Notice - we need to make this more flexible by defining some "avoid" terms and "normal" terms. This nicely generalises.
    for course in backpq:
        # check prereqs satisfied
        if term_number in course.terms and (all(not x for x in course.prereqs) or any(unsatisfied & set(comb) == set() for comb in course.prereqs)):
            possible.append(course)
        else:
            rejected.append(course)
    # now i have a list of all the possible courses i can have this term, in a prioritised order. I can now make a combination list of all the possible arrangements for the term
    poss_term = combinations(possible, 3)


    # check how we went in this term
    if possible.empty() and rejected.empty():
        # valid plan found
        print(plan)
        exit()
    for comb in poss_term:
        plan[index] = list(comb)
        for c in comb:
            for string in comb:
                backpq.remove(string)
            recursive_check(backpq, index + 1, term + 1, plan)
            for string in comb:
                backpq.append(string)
    return

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
