import copy

"""
Course ADT
"""
class Course:
    ''' Class for a Course '''
    def __init__(self, code, terms, prereqs, uoc):
        '''
        Constructor method for a Course
            code: course code (str) CCCCNNNN - stored in lowercase
            terms: term offerings (list of ints - 0 (summer), 1, 2, 3)
            prereqs: prerequisites (format described under prereqs_parser, from str input)
            uoc: units of credit (int)
            level: first digit in course code (int)
            exclusion: list of course codes (str) for exclusion courses
        '''
        self.code = code.lower()
        self.terms = terms
        self.prereqs = prereqs_parser(prereqs)
        self.uoc = uoc
        self.level = course_level(code)
        self.exclusion = [] # TODO

    def num_prerequisites(self):
        ''' Returns the number of unique prerequisite courses for a Course object '''
        prereqs = set()
        for comb in self.prereqs:
            prereqs |= set(comb)
        return len(prereqs)

    def priority(self, prereqs, **corrections):
        '''
        Returns the priority score tuple (dependency_score, course_rarity, course_level) calculated for a Course object
        '''
        # NOTE: higher tuple = more priority
        dependency_score = corrections.get('dependency_score', len(prereqs.total_dependencies(self.code, {})))
        course_rarity = corrections.get('course_rarity', -len(self.terms))
        course_level = corrections.get('course_level', -self.level)
        return dependency_score, course_rarity, course_level

    def copy(self, **corrections):
        ''' Returns a deep copy of the Course object with optional corrections '''
        new_course = Course(self.code, self.terms, '', self.uoc)
        new_course.code = corrections.get('code', self.code)
        new_course.terms = corrections.get('terms', copy.deepcopy(self.terms))
        new_course.prereqs = corrections.get('prereqs', copy.deepcopy(self.prereqs))
        new_course.uoc = corrections.get('uoc', self.uoc)
        return new_course

    def __repr__(self):
        ''' Representation of a Course object for debugging purposes '''
        return f'{self.code} - {prereqs_expression(self.prereqs)}'
    
    def __hash__(self):
        ''' Hash of a Course object for priority queue comparison purposes '''
        return hash(self.code)

    def __eq__(self, other):
        ''' Equality comparison between two Course objects for priority queue comparison purposes '''
        return self.code == other.code
    
    def __lt__(self, other):
        ''' Less than comparison between two Course objects for priority queue comparison purposes '''
        return self.code < other.code

    def __gt__(self, other):
        ''' Greater than comparison between two Course objects for priority queue comparison purposes '''
        return self.code > other.code


def course_level(course_code):
    return int(course_code[4])


"""
Directed Graph ADT
"""
class Graph:
    ''' Class for a Graph '''
    def __init__(self, courses):
        '''
        Constructor method for a Graph
            courses (list of Course objects)
            num_vertices (int)
            connections (adjacency list representation of outgoing connections)
            no_pre_courses (list of course_codes (str) without any prerequisites)
        '''
        self.num_vertices = len(courses)
        self.no_pre_courses = []
        self.connections = {course.code: [] for course in courses}
        self.connections_setup(courses)

    def connections_setup(self, courses):
        ''' Sets up prerequisite connections for the Graph, taking in courses (list of Course objects) '''
        for course in courses:
            if course.num_prerequisites() == 0:
                self.no_pre_courses.append(course.code)
            else:
                for comb in course.prereqs:
                    for prereq_code in comb:
                        if course.code not in self.connections[prereq_code]:
                            self.connections[prereq_code].append(course.code)

    def immediate_dependencies(self, course_code):
        '''
        Returns a list of codes (str) for courses that have the given course_code (str) as an immediate prerequisite
        '''
        return self.connections[course_code]

    def total_dependencies(self, course_code, memo):
        '''
        Returns a list of codes (str) for courses that depend on the given course_code (str)
        as a prerequisite at some point using a depth first search (dfs) algorithm
        '''
        dependencies = []
        # for each course that has the given course_code as a prerequisite 
        for dependency_code in self.immediate_dependencies(course_code):
            if dependency_code not in memo:
                # add itself as a dependency
                dependencies.append(dependency_code)
                memo[dependency_code] = True
                # as well as other courses that have it as a prerequisite (recursion)
                dependencies += self.total_dependencies(dependency_code, memo)
        return dependencies


"""
Queue ADT
"""
import queue
class PriorityQueue(queue.PriorityQueue):
    '''
    Custom wrapper for the PriorityQueue class provided by the queue module, adjusting inherited functionality
    so that the highest priority item/Course object has the highest priority score tuple, rather than the
    lowest tuple (as in the original class). Also has a shallow copy method.
    '''
    def __init__(self):
        ''' Constructor method '''
        super().__init__()

    def push(self, prereqs, course, **priority_corrections):
        '''
        Adds a Course object to the priority queue. Its priority is calculated using
        the given prereqs (Graph), and optional corrections may be provided
        '''
        dependency_score, course_rarity, course_level = course.priority(prereqs, **priority_corrections)
        new_tuple = (-dependency_score, -course_rarity, -course_level, course)
        super().put(new_tuple)

    def pop(self):
        '''
        Removes the Course object with the highest priority from the priority queue.
        '''
        _, _, _, course = super().get()
        return course


"""
Prerequisite Logic Parser
"""
import re

def prereqs_parser(prereqs_string):
    '''
    Returns a 2D list representation for the given prerequisites string in the PREREQS FORMAT.
    PREREQS FORMAT:
    A list of all possible combinations (topmost OR), where each combination is also
    represented by a list (pairwise AND) of prerequisite courses.
    e.g. [['a', 'b'], ['c']] represents '(a and b) or c'
    '''

    def logic_parser(prereqs):
        '''
        Simplifies the list representation of the prerequisite string into the PREREQS FORMAT
        Input: prereqs (list with prerequisite courses as a 2D list in the PREREQS FORMAT, and may include keywords)
                   e.g. ['(', [['a']], 'or', [['b']], ')', 'and', [['c']]]
        Output: 2D list in the PREREQS FORMAT
        '''
        # evaluate brackets first
        while '(' in prereqs:
            # find last opening bracket (first occurence in reversed string)
            last_open = len(prereqs) - prereqs[::-1].index('(') - 1
            # try to evaluate to first closing bracket
            try:
                first_close = last_open + prereqs[last_open:].index(')')
            except ValueError:
                raise ValueError('Bad logic')
            # simply prereq logic in brackets
            before = prereqs[:last_open]
            inside = prereqs[last_open + 1: first_close]
            after = prereqs[first_close + 1:]
            # update prereqs by replacing bracket logic
            prereqs = before + [logic_parser_simple(inside)] + after

        return logic_parser_simple(prereqs)


    def logic_parser_simple(prereqs):
        '''
        Simple parser that assumes there are no brackets in the input. Joins a list of PREREQS FORMAT 2D lists,
        separated by logic operational keywords (AND, OR), into a single 2D list in the PREREQS format.
        Input: prereqs (list with prerequisite courses as a 2D list in the PREREQS FORMAT, and may include keywords)
        Output: 2D list in the PREREQS FORMAT
        e.g. [[['a']], 'and', [['b']], 'and', [['c']]] => [['a', 'b', 'c']]
        e.g. [[['a', 'b']], 'or', [['c']]] => [['a', 'b'], ['c']]
        '''
        if not prereqs:
            # no prereqs provided
            return []
        elif 'and' in prereqs and 'or' in prereqs:
            # e.g. cannot understand 'a and b or c' (without brackets)
            raise ValueError('Bad logic')
        elif 'and' in prereqs:
            # remove 'and' keyword and compute new prereqs accordingly
            return prereqs_and_join([x for x in prereqs if x != 'and'])
        else:
            # remove 'or' keyword and compute new prereqs accordingly
            return flatten_lists([x for x in prereqs if x != 'or'])


    def flatten_lists(lists):
        '''
        Flattens a list of lists (e.g. 3D to 2D)
        e.g. [[['a']], [['b']]] => [['a'], ['b']]
        '''
        return [x for l in lists for x in l]


    def prereqs_and_join(prereqs_list):
        '''
        Joins a list of prereqs with pairwise AND logic into a single 2D list in the PREREQS FORMAT
        Input: 3D list (topmost AND, then prereqs in the PREREQS FORMAT)
        Output: 2D list in the PREREQS FORMAT
        '''
        # check for prereqs with multiple options (OR logic)
        linear = True
        combinations = []
        for prereqs_index, prereqs in enumerate(prereqs_list):
            # prereqs is in the PREREQS FORMAT (2D list)
            if len(prereqs) > 1:
                # length greater than 1 indicates that there are multiple options
                prereqs_before_list = prereqs_list[:prereqs_index]
                prereqs_after_list = prereqs_list[prereqs_index + 1:]
                # use distributive logic law to separate each option out
                for option in prereqs:
                    # recursively compute each option separately
                    recursive_prereqs_list = prereqs_before_list + [[option]] + prereqs_after_list
                    combination = prereqs_and_join(recursive_prereqs_list)
                    if combination not in combinations:
                        # NOTE: unnecessary check
                        combinations.append(combination)
                # not all prereqs have one option anymore
                linear = False
                break

        if linear:
            # all prereqs in prereqs_list have a single option (no OR logic)
            # join all the prerequisite courses in the prereqs by AND logic - associative logic law
            return [[prereq for prereqs in prereqs_list for prereq in prereqs[0]]]
        else:
            # prereqs_list provided contains prereqs with multiple options
            return flatten_lists(combinations)


    # create list representation for the prerequisite string
    const_symbols = ['and', 'or', '(', ')']
    prereqs_string = re.sub(r'\(', ' ( ', prereqs_string)
    prereqs_string = re.sub(r'\)', ' ) ', prereqs_string)
    # represent each prerequisite course within a single 2D list in the PREREQS FORMAT
    prereqs = [[[x]] if x not in const_symbols else x for x in prereqs_string.lower().split()]
    return logic_parser(prereqs)


def relevant_prereqs_filter(original_prereqs, selected_course_codes):
    ''' Returns a list of relevant prereqs to the selected courses (list of strings) '''
    return [comb for comb in original_prereqs if all(prereq in selected_course_codes for prereq in comb)]


def prereqs_expression(prereqs):
    ''' Debugging logic '''
    return ' OR '.join(f"({' AND '.join(prereq for prereq in comb)})" for comb in prereqs)


if __name__ == '__main__':
    # run prereq parser
    ans = prereqs_parser(input())
    print(ans)
    print(prereqs_expression(ans))
