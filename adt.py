"""
Course ADT
"""
# Course Class
class Course:
    def __init__(self, code, term, pre, uoc):
        # Course code (string)
        self.code = code
        # Term offerings (list of numbers)
        self.term = term
        # Prerequisites (list of strings)
        self.pre = pre
        # Units of credit (int)
        self.uoc = uoc


# Course name lookup - returns Course object given course code if it exists
def lookup(courses, check):
    for course in courses:
        if course.code == check:
            return course
    return None


"""
Directed Graph ADT
"""
# Vertex Class
class Vertex:
    def __init__(self, course):
        self.course = course
        self.numPres = len(course.pre)


# Graph Class
class Graph:
    def __init__(self, courses):
        self.numVertices = 0
        # Adjacency list representation of outgoing connections
        self.connections = {course.code: [] for course in courses}
        self.noPreCourses = []

    # Add a vertex to graph
    def addVertex(self, course):
        self.numVertices += 1
        node = Vertex(course)
        if node.numPres == 0:
            # Append to list of no-prerequisites
            self.noPreCourses.append(course.code)
        else:
            # Connect each prerequisite to current course
            for prereq in course.pre:
                self.connections[prereq].append(course.code)
        return node

    # Returns the number of immediate connections a course has
    def numConnections(self, course):
        return len(self.connections[course])

    # Returns the immediate connections a course has
    def returnConnections(self, course):
        return self.connections[course]


"""
Queue ADT
"""
import queue
