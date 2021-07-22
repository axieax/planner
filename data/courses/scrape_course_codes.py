import re
import json
import requests

URL = 'https://www.handbook.unsw.edu.au'
API = 'https://www.handbook.unsw.edu.au/api/es/search'

with open('data/courses/query_course_codes.json') as f:
    query = json.load(f)

def scrape_course_codes():
    course_codes = []
    # prepare query
    response = requests.get(API, json=query)
    payload = json.loads(response.content)
    for data in payload['contentlets']:
        course_data = json.loads(data['data'])
        course_codes.append(course_data['code'])
    with open('data/courses/course_codes.json', 'w') as f:
        json.dump(course_codes, f, indent=2)


if __name__ == '__main__':
    scrape_course_codes()

