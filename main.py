from courses import Course, courses, lookup
import queue

# Planner
plan = [[] for i in range(len(courses))]
# plan = [["COMP1511", "MATH1081", "MATH1141"], ["COMP2521", "DATA1001", "MATH1241"],
#         ["COMP1521", "COMP1531", "MATH2621"], [], []]

# Sort by prerequisites - directed graph
class Vertex:
    def __init__(self, course):
        self.course = course
        self.num_pres = len(course.pre)


class Graph:
    def __init__(self):
        self.num_vertices = 0
        self.connections = {course.code: [] for course in courses}
        self.no_pre = []

    def addVertex(self, course):
        self.num_vertices += 1
        node = Vertex(course)
        if node.num_pres == 0:
            self.no_pre.append(course.code)
        else:
            for prereq in course.pre:
                self.connections[prereq].append(course.code)
        return node

    def numConnections(self, course):
        return len(self.connections[course])

    def returnConnections(self, course):
        return self.connections[course]


def totalDependencies(prereqs, counted, course):
    connections = prereqs.returnConnections(course)
    for connection in connections:
        if len(connection) != 0 and connection not in counted:
            counted.append(connection)
            totalDependencies(prereqs, counted, connection)
    # print(counted)
    return len(counted)

def checkPlaced(course):
    for term in plan:
        if course in term:
            return True
    return False


def lastPlace(course):
    current = lookup(course)
    latestIndex = -1
    allPlaced = True
    for prereq in current.pre:
        placed = False
        # Check if exists
        for term in plan:
            if prereq in term:
                placed = True
                latestIndex = plan.index(term) if plan.index(term) > latestIndex else latestIndex
        if placed is False:
            allPlaced = False
            break
    return latestIndex if allPlaced is True else -1


def place(pq, course):
    # Place after last prereq, if prereq unplaced - return to pq - may have infinite loop
    # priority by prereqs placed?
    # Need check to see if already placed
    for term in plan:
        if course in term:
            return
    print(f"Placing {course}", end=' ')
    lastIndex = lastPlace(course)
    lastYear = lastIndex // 4 + 1
    lastTerm = lastIndex % 4 + 1
    obj = lookup(course)
    if len(obj.pre) == 0:
        lastYear = 1
        lastTerm = -1
    elif lastIndex == -1:
        # Check prerequisites placed
        # allPlaced = True
        # for prereq in obj.pre:
        #     allPlaced = checkPlaced(prereq) if allPlaced is True else False
        # if allPlaced is True:

        # Return to priority queue with less priority
        pq.put((-totalDependencies(prereqs, [], course) + 1, course))
        return

    for year in range(lastYear, 5):
        for offering in obj.term:
            # Co-requisite logic
            if year == lastYear and offering <= lastTerm:
                continue
            if len(plan[4 * (year - 1) + (offering - 1)]) < 3:
                print(f"into year {year + 1} term {offering}")
                print(f"Last index: {lastIndex}")
                plan[4 * (year - 1) + (offering - 1)].append(course)
                return



def main(courses):
    prereqs = Graph()

    for course in courses:
        prereqs.addVertex(course)

    prereqs.no_pre.sort(key=lambda course: totalDependencies(prereqs, [], course), reverse=True)
    # courses.sort(key=lambda course: totalDependencies(prereqs, [], course.code), reverse=True)

    # Sort by priority - number of connections
    # negative priority since the module sorts by least priority
    # NEED PRIORITY TO BE BY CONNECTIONS OF CONNECTIONS - NOT JUST IMMEDIATE CONNECTION - RECURSIVE FUNCTION
    # in this case, ensure prereqs met
    # not all no-pres should be placed first - e.g. scif1131 - ignore 0 actual dependencies/connections?
    # ALSO consider summer term - split year into 4 instead of 3

    # Consider both term offerings instead of just the first ###
    pq = queue.PriorityQueue()

    for course in prereqs.no_pre:
        pq.put((-totalDependencies(prereqs, [], course), course))

    while not pq.empty():
        print(f"PQ: {pq.queue}")
        # Dequeue
        course = pq.get()[1]
        # print(f"Dequeued: {course}")
        place(pq, course)
        for connection in prereqs.connections[course]:
            if checkPlaced(connection) is False:
                pq.put((-totalDependencies(prereqs, [], connection), connection))

    # print(plan)
    returnString = ""

    for term in range(len(plan)):
        t = "Summer" if (term + 1) % 4 == 0 else term % 4 + 1
        returnString += f"Year {term // 4 + 1} Term {t}: {plan[term]}\n"

    print(returnString)
    return returnString


    # for course in courses:
    #     c = course.code
    #     #print(f"{c} : {prereqs.numConnections(c)}")

main(courses)