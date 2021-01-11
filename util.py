"""
Course ADT
"""
class Course:
    ''' Class for a Course '''
    def __init__(self, code, terms, prereqs, uoc):
        '''
        Constructor method for a Course
            code: course code (str) CCCCNNNN
            terms: term offerings (list of ints - 0 (summer), 1, 2, 3)
            prereqs: prerequisites (format described under prereqs_parser, from str input)
            uoc: units of credit (int)
            level: first digit in course code (int)
            exclusion: list of course codes (str) for exclusion courses
        '''
        self.code = code.lower()
        # name: course name (str)
        # self.name = name
        self.terms = terms
        self.prereqs = prereqs_parser(prereqs)
        self.uoc = uoc
        self.level = int(code[4])
        self.exclusion = [] # TODO

    def __repr__(self):
        return f'{self.code} - {prereqs_expression(self.prereqs)}'
    
    def __hash__(self):
        return hash(self.code)

    def __eq__(self, other):
        return (self.__class__ == other.__class__) and (self.code == other.code)
    
    def __lt__(self, other):
        return (self.__class__ == other.__class__) and (self.code < other.code)

    def __gt__(self, other):
        return (self.__class__ == other.__class__) and (self.code > other.code)
    
    def num_prerequisites(self):
        return sum(map(len, self.prereqs))
    
    def prereq_complexity(self):
        # max depth
        # FILTER
        return max(map(len, self.prereqs))
        return len(self.prereqs)


def lookup(courses, check):
    '''
    Course name lookup - returns Course object given course code (str) if it exists
    '''
    # TODO: COURSES: MY COURSES OR ALL COURSES?
    for course in courses:
        if course.code.lower() == check.lower(): # lower case
            return course
    return None


"""
Directed Graph ADT
"""
class Vertex:
    ''' Class for a Vertex '''
    def __init__(self, course):
        '''
        Constructor method for a Vertex
            course (Course object)
            num_pres: number of prereqs
        '''
        self.course = course
        self.num_pres = course.num_prerequisites()


# Graph Class
class Graph:
    ''' Class for a Graph '''
    def __init__(self, courses):
        '''
        Constructor method for a Directed Graph
            courses (list of Course objects)
            num_vertices (int)
            connections (adjacency list representation of outgoing connections)
            no_pre_courses (list of Course objects without any prerequisites)
        '''
        self.num_vertices = len(courses)
        # Adjacency list representation of outgoing connections
        self.no_pre_courses = []
        self.connections = {course.code: [] for course in courses}
        self.connections_setup(courses)

    def connections_setup(self, courses):
        ''' Set up prerequisite connections '''
        for course in courses:
            node = Vertex(course)
            if node.num_pres == 0:
                self.no_pre_courses.append(course.code)
            else:
                for comb in course.prereqs:
                    for prereq_code in comb:
                        if course.code not in self.connections[prereq_code]:
                            self.connections[prereq_code].append(course.code)

    def immediate_dependencies(self, course_code):
        '''
        Returns the courses that have the given course_code as an immediate prerequisite
        '''
        return self.connections[course_code]

    def total_dependencies(self, course_code, memo):
        '''
        Returns all the course_codes that depend on the given course_code as a prerequisite at some point
        using a depth first search (dfs) algorithm
        '''
        dependencies = []
        for dependency_code in self.immediate_dependencies(course_code):
            if dependency_code not in memo:
                dependencies.append(dependency_code)
                memo[dependency_code] = True
                dependencies += self.total_dependencies(dependency_code, memo)
        return dependencies


"""
Queue ADT
"""
import queue


"""
Prerequisite Logic Parser
"""
import re
const_symbols = ['and', 'or', '(', ')']

def prereqs_parser(prereqs_string):
    '''
    Returns a 2D list of all possible combinations (topmost OR) for a prereqs_string
    where each combination is represented by a list (AND) of prerequisite courses
    e.g. [['a', 'b'], 'c'] represents '(a and b) or c'
    '''
    prereqs = prereqs_str_to_list(prereqs_string)

    # evaluate brackets first
    while '(' in prereqs:
        # find last opening bracket (first occurence in reversed string)
        last_open = len(prereqs) - prereqs[::-1].index('(') - 1
        # evaluate to first closing bracket
        # could raise ValueError if ')' does not exist - bad logic
        first_close = last_open + prereqs[last_open:].index(')')
        # simply prereq logic in brackets
        bracket_prereqs = prereqs[last_open + 1: first_close]
        bracket_prereqs = prereqs_parser_simple(bracket_prereqs)
        # update prereqs by replacing bracket logic
        for _ in range(first_close - last_open + 1):
            prereqs.pop(last_open)
        prereqs.insert(last_open, bracket_prereqs)

    return prereqs_parser_simple(prereqs)


def prereqs_str_to_list(prereqs_string):
    '''
    Converts the prereq string input to list format (with prerequisite courses as a 2d list)
    e.g. 'a and (b or c)' => [[['a']], 'and', '(', [['b']], 'or', [['c']], ')']
    '''
    prereqs_string = prereqs_string.lower()
    prereqs_string = re.sub(r'\(', ' ( ', prereqs_string)
    prereqs_string = re.sub(r'\)', ' ) ', prereqs_string)
    return [[[x]] if x not in const_symbols else x for x in prereqs_string.strip().split()]


def prereqs_parser_simple(prereqs):
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
        # memoization for list_and_join to ensure unique combinations
        ans = list_and_join([x for x in prereqs if x != 'and'], {})
        return ans
    else:
        return flatten_lists([x for x in prereqs if x != 'or'])


def list_and_join(prereqs_list, memo):
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
                new_lists = flatten_lists(new)
                # only include unique combinations
                if str(new_lists) not in memo:
                    ans.append(list_and_join(new_lists, memo))

            linear = False

    memo[str(prereqs_list)] = True
    if linear:
        # no combinations present (simple) - use associative logic law
        # [[['b']], [['c']] ] => [['b', 'c']]
        # [[['a', 'b']], [['c']] ] => [['a', 'b', 'c']]
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


def relevant_prereqs_filter(selected_course_codes, course):
    ''' Returns a list of relevant prereqs for the selected courses (list of strings) '''
    return [comb for comb in course.prereqs if all([prereq in selected_course_codes for prereq in comb])]

def prereqs_expression(prereqs):
    ''' Debugging logic '''
    return ' OR '.join(f"({' AND '.join(prereq for prereq in comb)})" for comb in prereqs)


if __name__ == '__main__':
    # run prereq parser
    ans = prereqs_parser(input())
    print(ans)
    print(prereqs_expression(ans))
