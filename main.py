from adt import Course, lookup, Vertex, Graph, queue
from data import courses, plan, planSize
import json


# Counts the total number of courses that are dependent on specified course - not just immediate
def totalDependencies(prereqs, counted, course):
    connections = prereqs.returnConnections(course)
    for connection in connections:
        if len(connection) != 0 and connection not in counted:
            counted.append(connection)
            totalDependencies(prereqs, counted, connection)
    return len(counted)


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


def main(courses, plan, planSize):
    # Create a graph representing course prerequisites
    prereqs = Graph(courses)
    for course in courses:
        prereqs.addVertex(course)

    # Creates a priority queue for placement
    pq = queue.PriorityQueue()
    # Courses are represented and sorted by a tuple (totalDependencies, courseYearCode, course)
    # totalDependencies are negative since the pq function sorts by least priority

    # Place courses with no prerequisites in priority queue
    for course in prereqs.noPreCourses:
        pq.put((-totalDependencies(prereqs, [], course), int(course[4]), course))

    ## Alternative: place all courses in pq first

    # Place courses
    while not pq.empty():
        # print(f"PQ: {pq.queue}")
        # Dequeue and place course
        course = pq.get()[2]
        place(prereqs, plan, planSize, courses, pq, course)
        # Add unplaced dependencies to priority queue
        for connection in prereqs.connections[course]:
            if checkPlaced(plan, connection) is False:
                pq.put((-totalDependencies(prereqs, [], connection), int(connection[4]), connection))

    # Generate dictionary to store plan
    output = {}

    # Determine last-placed term
    lastTerm = 0
    for term in range(len(plan)):
        lastTerm = term if len(plan[term]) != 0 else lastTerm

    # Write to dictionary
    for term in range(0, lastTerm + 1):
        termText = "Summer" if (term + 1) % 4 == 0 else term % 4 + 1
        output[f"Year {term // 4 + 1} Term {termText}"] = plan[term]

    # Display output
    for term in output.items():
        print(term)

    print(len(courses) * 6)

    return output


main(courses, plan, planSize)

### Notes:
# Maybe try to place courses with no-pres earlier in plan - easier, such as SCIF1131?
# Consider both term offerings not just the first available option
# Find last placed course and don't write terms after it
