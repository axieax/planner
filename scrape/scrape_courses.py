import re
import json
import requests
from plan.models.course import Course

URL = 'https://www.handbook.unsw.edu.au'
API = 'https://www.handbook.unsw.edu.au/api/es/search'

SCRAPE_LIMIT = 2
VALID_TERMS = ['Summer Term', 'Term 1', 'Term 2', 'Term 3']


def parse_course(course_json: dict) -> Course:
    '''
    Parses course data from the handbook and
    returns a Course object from extracted data
    '''
    # course data
    course_data = json.loads(course_json['data'])
    course_code = course_data['code']
    print(course_code)

    # extract course requirements
    enrolment_rules = course_data['enrolment_rules']
    if enrolment_rules:
        requirement_string = enrolment_rules[0]['description']
    else:
        requirement_string = ''

    faculty = course_data['faculty_detail'][0]['name']
    terms = course_data['offering_detail']['offering_terms'].split(', ')
    terms = [VALID_TERMS.index(term) for term in terms]
    uoc = int(course_data['credit_points'])
    print(requirement_string)
    print(faculty)
    print(terms)
    print(uoc)


def scrape_courses():
    # prepare query for scraping all courses
    with open('scrape/query_courses_all.json') as f:
        query = json.load(f)
    query['size'] = SCRAPE_LIMIT
    # scrape from handbook api
    response = requests.get(API, json=query)
    payload = json.loads(response.content)
    # extract data from each course
    course_objects = []
    for course_json in payload['contentlets']:
        course_object = parse_course(course_json)
        course_objects.append(course_object)
    # save data (pickle, json, sql?) to data directory
    # with open('data/courses.json', 'w') as f:
    #     json.dump(course_objects, f, indent=2)
    # each model will have a to_json method as well


if __name__ == '__main__':
    scrape_courses()
