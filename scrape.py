import re
import json
import requests
URL = 'https://www.handbook.unsw.edu.au'
API = 'https://www.handbook.unsw.edu.au/api/es/search'



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
# filtered to remove UNSW Canberra, Global and DVC - 211 degrees
with open('query_degrees.json') as f:
    degree_body = json.load(f)

resp = requests.get(API, json=degree_body)
payload = json.loads(resp.content)['contentlets']


courses = [(deg['code'], deg['name']) for deg in payload]
for code, course in courses[:10]:
    print(URL + '/undergraduate/programs/2021/' + code)

exit()
