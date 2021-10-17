""" Imports """
from src.scrape.scrape_courses import scrape_courses
from src.scrape.scrape_degrees import scrape_degrees
from src.scrape.scrape_specialisations import scrape_specialisations


def scrape_all() -> None:
    print("Scraping Courses")
    scrape_courses()
    print("Scraping Degrees")
    scrape_degrees()
    print("Scraping Specialisations")
    scrape_specialisations()


if __name__ == "__main__":
    scrape_all()
