from util import Course, lookup, Vertex, Graph, queue
from data import courses, plan, planSize, all_courses
from util import relevant_prereqs_filter
import json

# TODO: need to rewrite logic due to changing of Course structure

# Determines whether a course has already been placed in the plan
def checkPlaced(plan, course):
    for term in plan:
        if course in term:
            return True
    return False


# Returns the index corresponding to when the last prerequisite is
def lastPlaced(plan, course):
    courseObject = lookup(courses, course)
    latestIndex = -1
    allPlaced = True
    for prereq in courseObject.pre:
        placed = False
        # Check if prereq has been placed
        for term in plan:
            if prereq in term:
                placed = True
                latestIndex = plan.index(term) if plan.index(term) > latestIndex else latestIndex
        # If prereq has not been placed yet
        if placed is False:
            allPlaced = False
            break
    return latestIndex if allPlaced is True else -1


# Places a course
def place(prereqs, plan, planSize, courses, pq, course):
    # Place after last prereq, if prereq unplaced - return to pq - may have infinite loop
    # priority by prereqs placed?

    # Check to see if already placed
    if checkPlaced(plan, course):
        return
    print(f"Placing {course}", end=' ')
    courseObject = lookup(courses, course)

    # Extract information about last-placed prerequisite
    lastIndex = lastPlaced(plan, course)
    lastYear = lastIndex // 4 + 1
    lastTerm = lastIndex % 4 + 1

    # Course has no prequisites
    if len(courseObject.pre) == 0:
        lastYear = 1
        lastTerm = -1
    # Not all prerequisites placed
    elif lastIndex == -1:
        # Return to priority queue with less priority?
        pq.put((-totalDependencies(prereqs, [], course) + 1, int(course[4]), course))
        return

    # Determine Year
    for year in range(lastYear, 6):
        # Determine Term
        for offering in courseObject.term:
            # Update logic below for co-requisites < instead of <=
            if year == lastYear and offering <= lastTerm:
                continue
            # Check full
            index = 4 * (year - 1) + (offering - 1)
            if len(plan[index]) < planSize[index]:
                print(f"into year {year + 1} term {offering}")
                plan[index].append(course)
                return


def main(selected_course_codes, plan, plan_specs):
    '''
    selected_courses (list of Course objects)
    plan (arr)
    plan_specs (dict containing info about each term in plan)
        e.g. max_uoc, term 0/1/2/3, 
    '''
    # filter relevant prerequisites
    selected_courses = {}
    for course_code in selected_course_codes:
        # retrieve course data
        original_course = all_courses[course_code]
        # filter prerequisites, keeping those relevant to the selected courses
        new_course = Course(course_code, original_course.terms, '', original_course.uoc)
        new_course.prereqs = relevant_prereqs_filter(selected_course_codes, original_course) # getter and setter
        selected_courses[course_code] = new_course
    
    # set up a graph representing course prerequisites
    prereqs = Graph(selected_courses.values())


    # calculate courses available in each term??
    summer_courses = [course for course in selected_courses.values() if 0 in course.terms]
    term_1_course = [course for course in selected_courses.values() if 1 in course.terms]
    term_2_course = [course for course in selected_courses.values() if 2 in course.terms]
    term_3_course = [course for course in selected_courses.values() if 3 in course.terms]



    # create a priority queue for course placement
    # courses are represented and sorted by a tuple (total_dependencies, course_level, course_name)
    # since the priority queue sorts by least priority, lower valued tuples have higher priority
    pq = queue.PriorityQueue()

    # place courses with no prerequisites in priority queue first if other courses depend on it
    for course_code in prereqs.no_pre_courses:
        course = selected_courses[course_code]
        total_dependencies = prereqs.total_dependencies(course_code, {})
        if len(total_dependencies) > 0:
            pq.put((-len(total_dependencies), course.level, course))  

    # place courses
    while not pq.empty():
        course = pq.get()[2]
        place()
        for dependency_code in prereqs.immediate_dependencies(course.code):
            dependency = selected_courses[dependency_code]
            if not already_placed(plan, dependency): # course code or object??
                total_dependencies = prereqs.total_dependencies(dependency_code, {})
                pq.put((-len(total_dependencies), dependency.level, dependency))

    print(plan)
    # calculate finishing term and total length
    return {}


if __name__ == '__main__':
    main([course.code for course in courses], plan, planSize)

### Notes:
# Maybe try to place courses with no-pres earlier in plan - easier, such as SCIF1131?
# Consider both term offerings not just the first available option TODO
# Find last placed course and don't write terms after it
