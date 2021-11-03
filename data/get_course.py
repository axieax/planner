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


""" get all courses you need using this function """


def get_courses(coursesOutput) -> Course:
    with open("data/courses.json", "r") as f:
        courses = json.loads(f.read())
        return map(lambda course: make_course_from_dict(courses[course]), coursesOutput)


""" if you need a course on the fly, avoid using in loops or recursion """


def get_course(course) -> Course:
    with open("data/courses.json", "r") as f:
        courses = json.loads(f.read())
        return make_course_from_dict(courses[course])
