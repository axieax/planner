import re
import json
import requests
from data import all_degrees, all_courses
URL = 'https://www.handbook.unsw.edu.au'
API = 'https://www.handbook.unsw.edu.au/api/es/search'


def scrape_degrees():
    # Retrieve all degrees (p_course) - TODO: ALL YEARS
    # filtered to remove UNSW Canberra, Global and DVC - 211 degrees
    with open('query_degrees.json') as f:
        degrees_body = json.load(f)
    resp = requests.get(API, json=degrees_body)
    payload = json.loads(resp.content)['contentlets']

    # Retrieve data for each degree
    with open('query_degree.json') as f:
        degree_body = json.load(f)
    for degree in payload:
        # retrieve data for each degree
        degree_body['query']['bool']['must'][0]['query_string']['query'] = f'unsw_pcourse.code: {degree['code']}'
        resp = requests.get(API, json=degree_body)
        payload = json.loads(resp.content)['contentlets']

        all_degrees[degree['code']] = {
            'name': degree['name']
        }
    print(all_degrees)
    

def scrape_specialisations():
    pass

def scrape_courses():
    pass




# extract term offerings: strip 'Term' from offering terms
# sub summmer -> 0
# list

# course
# with open('course_degree.json') as f:
#     course_body = json.load(f)
# resp = requests.get(API, json=course_body)
# payload = json.loads(resp.content)['contentlets']
# print(len(payload))
# exit()


# degrees - 243 total degrees



if __name__ == '__main__':
    scrape_degrees()
    scrape_courses()
