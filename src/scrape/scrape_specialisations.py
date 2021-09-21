import re
import json
import requests
from plan.models.specialisation import Specialisation

URL = 'https://www.handbook.unsw.edu.au'
API = 'https://www.handbook.unsw.edu.au/api/es/search'

SCRAPE_LIMIT = 2


def parse_specialisation(specialisation_json: dict) -> Specialisation:
    print(specialisation_json)


def scrape_specialisations():
    # prepare query for scraping all specialisations
    with open('scrape/query_specialisations_all.json') as f:
        query = json.load(f)
    query['size'] = SCRAPE_LIMIT
    # scrape from handbook api
    response = requests.get(API, json=query)
    payload = json.loads(response.content)
    # extract data from each specialisation
    specialisation_objects = []
    for specialisation_json in payload['contentlets']:
        specialisation_object = parse_specialisation(specialisation_json)
        specialisation_objects.append(specialisation_object)
    # save data (pickle, json, sql?) to data directory


if __name__ == '__main__':
    scrape_specialisations()
