from __future__ import annotations
"""
Directed Graph ADT
"""
from src.models.course import Course
class Graph:
    ''' Class for a Graph '''
    def __init__(self, courses: list[Course]):
        '''
        Constructor method for a Graph
            courses (list of Course objects)
            num_vertices (int)
            connections (adjacency list representation of outgoing connections)
            no_pre_courses (list of course_codes (str) without any prerequisites)
        '''
        self.num_vertices = len(courses)
        self.no_pre_courses = []
        self.connections = {course: [] for course in courses}
        self.connections_setup(courses)

    def connections_setup(self, courses: list[Course]):
        ''' Sets up prerequisite connections for the Graph, taking in courses (list of Course objects) '''
        for course in courses:
            if course.requirements.has_no_prereqs():
                self.no_pre_courses.append(course.code)
            else:
                for requirement in course.requirements.get_beneficial_courses(courses):
                    if requirement not in self.connections[requirement]:
                        self.connections[requirement].append(course.code)

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

