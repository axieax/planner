
"""
Queue ADT - slightly more convenient than the default
"""
import queue

from src.models.course import Course
class PriorityQueue(queue.PriorityQueue):
    '''
    Custom wrapper for the PriorityQueue class provided by the queue module, adjusting inherited functionality
    so that the highest priority item/Course object has the highest priority score tuple, rather than the
    lowest tuple (as in the original class). Also has a shallow copy method.
    '''
    def __init__(self):
        ''' Constructor method '''
        super().__init__()

    def push(self, prereqs, course):
        '''
        Adds a Course object to the priority queue. Its priority is calculated using
        the given prereqs (Graph), and optional corrections may be provided
        '''
        dependency_score, course_rarity, course_level = course.priority(prereqs)
        new_tuple = (-dependency_score, -course_rarity, -course_level, course)
        super().put(new_tuple)

    def pop(self) -> Course:
        '''
        Removes the Course object with the highest priority from the priority queue.
        '''
        _, _, _, course = super().get()
        return course
