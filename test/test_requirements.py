import pytest
from data import get_course, get_all_courses
from src.models import NullReq, PreReq, CoReq, UocReq, DegreeReq, And, Or

# TODO: fixtures for different plans


def test_prereq():
    requirement = PreReq("COMP1511")
    comp1511 = get_course("COMP1511")
    comp1521 = get_course("COMP1521")
    comp1531 = get_course("COMP1531")
    comp2521 = get_course("COMP2521")
    assert requirement.filter_relevant_courses([]) == []
    assert requirement.filter_relevant_courses([comp1511]) == [comp1511]
    assert requirement.filter_relevant_courses([comp1511, comp1521]) == [comp1511]
    assert requirement.filter_relevant_courses([comp1511, comp1521, comp1531]) == [
        comp1511
    ]
    assert requirement.filter_relevant_courses(
        [comp1511, comp1521, comp1531, comp2521]
    ) == [comp1511]


def test_no_req():
    requirement = NullReq()
    assert requirement.filter_relevant_courses([]) == []
    for course in get_all_courses():
        assert requirement.filter_relevant_courses([course]) == []


def test_coreq():
    pass


def test_and_simple():
    requirement = And([])


def test_or_simple():
    requirement = Or([])
