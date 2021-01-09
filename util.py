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


"""
Prerequisite Logic Parser
"""
import re
const_symbols = ['and', 'or', '(', ')']

def prereq_parser(prereq_string):
    '''
    Returns a 2D list of all possible combinations (topmost OR) for a prereq_string
    where each combination is represented by a list (AND) of prerequisite courses
    e.g. [['a', 'b'], 'c'] represents '(a and b) or c'
    '''
    prereqs = prereq_str_to_list(prereq_string)

    # evaluate brackets first
    while '(' in prereqs:
        # find last opening bracket (first occurence in reversed string)
        last_open = len(prereqs) - prereqs[::-1].index('(') - 1
        # evaluate to first closing bracket
        first_close = last_open + prereqs[last_open:].index(')') # could raise ValueError if ')' does not exist - bad logic
        # simply prereq logic in brackets
        bracket_prereqs = prereqs[last_open + 1: first_close]
        bracket_prereqs = prereq_parser_simple(bracket_prereqs)
        # update prereqs by replacing bracket logic
        for _ in range(first_close - last_open + 1):
            prereqs.pop(last_open)
        prereqs.insert(last_open, bracket_prereqs)
    
    return prereq_parser_simple(prereqs)


def prereq_str_to_list(prereq_string):
    '''
    Converts the prereq string input to list format (with prerequisite courses as a 2d list)
    e.g. 'a and (b or c)' => [[['a']], 'and', '(', [['b']], 'or', [['c']], ')']
    '''
    prereq_string = prereq_string.lower()
    prereq_string = re.sub(r'\(', ' ( ', prereq_string)
    prereq_string = re.sub(r'\)', ' ) ', prereq_string)
    return [[[x]] if x not in const_symbols else x for x in prereq_string.strip().split()]


def prereq_parser_simple(prereqs):
    '''
    Simple parser that assumes no brackets (but could have multiple same operations)
    Input: list of base prereqs logic - could include 'and' or 'or' keywords which need to be filtered
    Output: 2D list of prereqs - parsed (with 'and' or 'or' keywords removed)
    e.g. [[['a']], 'and', [['b']]] => [['a', 'b']]
    e.g. [[['a', 'b']], 'or', [['c']]] => [['a', 'b'], ['c']]
    '''
    # base cases
    if not prereqs:
        # empty prereqs
        return []
    elif 'and' in prereqs and 'or' in prereqs:
        # cannot understand 'a and b or c' (without brackets)
        raise ValueError('Bad logic')

    # parse simple prereqs - removing keywords
    if 'and' in prereqs:
        return list_and_join([x for x in prereqs if x != 'and'])
    else:
        return flatten_lists([x for x in prereqs if x != 'or'])


def list_and_join(prereqs_list):
    '''
    Joins a list of prereqs with pairwise AND logic
    Input: 3D list (top level AND, then prereqs, then prereq)
    Output: 2D list
    '''
    # check for combinations in prereqs (OR logic) - "linear" otherwise
    ans = []
    linear = True
    for prereqs_index, prereqs in enumerate(prereqs_list):
        # combinations are represented by [['a'], ['b']] in prereqs (multiple options)
        if len(prereqs) > 1:
            # compute OR logic separately for each option
            for option in prereqs:
                # use distributive logic law to separate each option out
                before = prereqs_list[:prereqs_index]
                curr = [[option]]
                after = prereqs_list[prereqs_index + 1:]
                
                # [[['a'], ['b']], [['c', 'd']]] => [[['a']], [['c', 'd']]] OR [[['b']], [['c', 'd']]]
                new = []
                if prereqs_index > 0:
                    # include prereqs before the prereqs with multiple options if they exist
                    new.append(before)
                new.append(curr)
                if prereqs_index < len(prereqs_list) - 1:
                    # include prereqs after the prereqs with multiple options if they exist
                    new.append(after)
                
                ans.append(list_and_join(flatten_lists(new)))
            linear = False

    # no combinations present (simple) - use associative logic law
    # [[['b']], [['c']] ] => [['b', 'c']]
    # [[['a', 'b']], [['c']] ] => [['a', 'b', 'c']]
    if linear:
        # flattening process (ignore level ordering):
        # [[['a', 'b']], [['c']]] => [['a', 'b'], ['c']] => ['a', 'b', 'c']
        # then we want [['a', 'b', 'c']]
        return [flatten_lists(flatten_lists(prereqs_list))]
        # or the bottom-most prereq's extracted with [[prereq for prereqs in prereqs_list for prereq in prereqs[0]]]
    else:
        # 3D list ans => 2D list
        return flatten_lists(ans)


def flatten_lists(lists):
    return sum(lists, [])

