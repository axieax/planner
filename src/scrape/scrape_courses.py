""" Imports  """
import re
import json
import requests
from src.models import Course
from src.scrape.scrape_utils import URL, API
from functools import reduce

""" Constants """
SCRAPE_LIMIT = 8000
VALID_TERMS = ["Summer Term", "Term 1", "Term 2", "Term 3"]


def parse_course(course_json: dict) -> Course:
    """
    Parses course data from the handbook and
    returns a Course object from extracted data
    """
    # course data
    course_data = json.loads(course_json["data"])
    try:
        uoc = int(course_json['creditPoints'])
    except:
        uoc = 0
    course_code = course_data["code"]

    # extract course requirements
    enrolment_rules = course_data["enrolment_rules"]
    if enrolment_rules:
        requirement_string = enrolment_rules[0]["description"].replace("<br/>", "")
    else:
        requirement_string = ""

    faculty = course_data["faculty_detail"][0]["name"]
    terms = course_data["offering_detail"]["offering_terms"].split(", ")
    try:
        terms = [VALID_TERMS.index(term) for term in terms]
    except:
        terms = []
    return Course(course_code, terms, requirement_string, faculty, uoc)


def scrape_courses():
    # prepare query for scraping all courses
    with open("src/scrape/query_courses_all.json") as f:
        query = json.load(f)
    query["size"] = SCRAPE_LIMIT
    # scrape from handbook api
    response = requests.get(API, json=query)
    payload = json.loads(response.content)
    # extract data from each course
    course_objects = {}
    for course_json in payload["contentlets"]:
        course_object = parse_course(course_json)
        course_objects[course_object.code] = course_object.to_dict()

    print(json.dumps(course_objects))

if __name__ == "__main__":
    '''run this script and rerout your output to somewhere you want to get a clean json of courses'''
    scrape_courses()
