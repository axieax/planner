import json
from src.models.course import Course


def make_course_from_dict(dict) -> Course:
    return Course(
        dict["code"],
        dict["terms"],
        dict["raw_requirements"],
        dict["faculty"],
        dict["uoc"],
    )


def get_courses(coursesOutput) -> list[Course]:
    """ get all courses you need using this function """
    with open("data/courses.json", "r") as f:
        courses = json.loads(f.read())
        return [make_course_from_dict(courses[course]) for course in coursesOutput]


def get_course(course) -> Course:
    """ if you need a course on the fly, avoid using in loops or recursion """
    with open("data/courses.json", "r") as f:
        courses = json.loads(f.read())
        try:
            return make_course_from_dict(courses[course])
        except KeyError:
            print("not found! Returning COMP1511 instead. You should do COMP1511") #TODO: bad
            return courses['COMP1511']
