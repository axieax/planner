import re
import json
import requests

VALID_TERMS = ['Summer Term', 'Term 1', 'Term 2', 'Term 3']

URL = 'https://www.handbook.unsw.edu.au'
API = 'https://www.handbook.unsw.edu.au/api/es/search'

with open('data/courses/query.json') as f:
    query = json.load(f)

def scrape_course(course_code: str):
    # prepare query
    query['query']['bool']['must'][0]['query_string']['query'] = 'unsw_psubject.code: ' + course_code
    response = requests.get(API, json=query)
    payload = json.loads(response.content)
    payload = json.loads(payload['contentlets'][0]['data'])
    print(payload)
    # extract and parse data
    # NOTE: multiple enrolment rules?
    requirement_string = payload['enrolment_rules'][0]['description']
    faculty = payload['faculty_detail'][0]['name']
    terms = payload['offering_detail']['offering_terms'].split(', ')
    terms = [VALID_TERMS.index(term) for term in terms]
    uoc = int(payload['credit_points'])
    print(requirement_string)
    print(faculty)
    print(terms)
    print(uoc)
    


if __name__ == '__main__':
    scrape_course('COMP9417')

