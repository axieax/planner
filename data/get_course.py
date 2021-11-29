import json
from typing import Union
from src.models import Course


def make_course_from_dict(course_dict: dict) -> Course:
    return Course(
        course_dict["code"],
        course_dict["terms"],
        course_dict["raw_requirements"],
        course_dict["faculty"],
        course_dict["uoc"],
    )


def load_courses_data() -> dict[str, dict]:
    with open("data/courses.json", "r") as f:
        return json.load(f)


def get_courses(courses_output: list[str]) -> list[Course]:
    """get all courses you need using this function"""
    courses_data = load_courses_data()
    return [make_course_from_dict(courses_data[course]) for course in courses_output]


def get_all_courses() -> list[Course]:
    courses_data = load_courses_data()
    return [make_course_from_dict(course_dict) for course_dict in courses_data.values()]


def get_course(course_code: str) -> Union[Course, None]:
    """if you need a course on the fly, avoid using in loops or recursion"""
    courses_data = load_courses_data()
    try:
        return make_course_from_dict(courses_data[course_code])
    except KeyError:
        print(
            "not found! Returning COMP1511 instead. You should do COMP1511"
        )  # TODO: bad
        return get_course("COMP1511") if course_code != "COMP1511" else None
