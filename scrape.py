import re
import json
import requests
URL = 'https://www.handbook.unsw.edu.au'
API = 'https://www.handbook.unsw.edu.au/api/es/search'

# degrees - 243 total degrees
# filtered to remove UNSW Canberra, Global and DVC - 211 degrees
with open('query_degree.json') as f:
    degree_body = json.load(f)

resp = requests.get(API, json=degree_body)
payload = json.loads(resp.content)['contentlets']


courses = [(deg['code'], deg['name']) for deg in payload]
for code, course in courses[:10]:
    print(URL + '/undergraduate/programs/2021/' + code)

exit()
