
"""
Queue ADT - slightly more convenient than the default
"""
import queue

from src.models.course import Course
from src.models.graph import Graph
class PriorityQueue(queue.PriorityQueue):
    '''
    Custom wrapper for the PriorityQueue class provided by the queue module, adjusting inherited functionality
    so that the highest priority item/Course object has the highest priority score tuple, rather than the
    lowest tuple (as in the original class). Also has a shallow copy method.
    '''
    def __init__(self):
        ''' Constructor method '''
        super().__init__()

    def push(self, prereqs: Graph, course: Course):
        '''
        Adds a Course object to the priority queue. Its priority is calculated using
        the given prereqs (Graph), and optional corrections may be provided
        '''
        dependency_score = len(prereqs.total_dependencies(course.code))
        course_rarity = len(course.terms)
        course_level = int(course.code[4])
        super().put((-dependency_score, -course_rarity, -course_level, course))

    def pop(self) -> Course:
        '''
        Removes the Course object with the highest priority from the priority queue.
        '''
        _, _, _, course = super().get()
        return course
