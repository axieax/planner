""" Imports """
import re
import json
import requests
from src.models import Degree
from src.scrape.scrape_utils import URL, API

""" Constants """
SCRAPE_LIMIT = 2


def parse_degree(program_json: dict) -> Degree:
    print(program_json)


def scrape_degrees():
    # prepare query for scraping all degrees
    with open("scrape/query_degrees_all.json") as f:
        query = json.load(f)
    query["size"] = SCRAPE_LIMIT
    # scrape from handbook api
    response = requests.get(API, json=query)
    payload = json.loads(response.content)
    # extract data from each program
    degree_objects = []
    for program_json in payload["contentlets"]:
        degree_object = parse_degree(program_json)
        degree_objects.append(degree_object)
    # save data (pickle, json, sql?) to data directory


if __name__ == "__main__":
    scrape_degrees()
