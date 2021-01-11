import pytest
from util import prereqs_parser

def test_null():
    assert prereqs_parser('') == []

def test_invalid():
    with pytest.raises(Exception):
        prereqs_parser('a and b or c')
    with pytest.raises(Exception):
        prereqs_parser('a or b and c')

def test_single():
    # use Hypothesis testing
    assert prereqs_parser('a') == [['a']]
    assert prereqs_parser('b') == [['b']]

def test_simple_or():
    assert prereqs_parser('a or b') == [['a'], ['b']]
    assert prereqs_parser('a or b or c') == [['a'], ['b'], ['c']]

def test_simple_and():
    assert prereqs_parser('a and b') == [['a', 'b']]
    assert prereqs_parser('a and b and c') == [['a', 'b', 'c']]

def test_unnecessary_bracket():
    assert prereqs_parser('(a and b) and c') == [['a', 'b', 'c']]
    assert prereqs_parser('a and (b and c)') == [['a', 'b', 'c']]
    assert prereqs_parser('(a or b) or c') == [['a'], ['b'], ['c']]
    assert prereqs_parser('a or (b or c)') == [['a'], ['b'], ['c']]

def test_simple_combination():
    assert prereqs_parser('(a and b) or c') == [['a', 'b'], ['c']]
    assert prereqs_parser('a and (b or c)') == [['a', 'b'], ['a', 'c']]
    # assert prereqs_parser('a and (b or c)') == prereqs_parser('(a and b) or (a and c)') == [['a', 'b'], ['a', 'c']]
    assert prereqs_parser('(a and b) or (c and d)') == [['a', 'b'], ['c', 'd']]

def test_complex_combination():
    assert len(prereqs_parser('(a or b or c or d) and (e or f)')) == 4 * 2

def test_courses():
    # comp1511
    cs1511 = prereqs_parser('COMP1511 or DPST1091 or COMP1911 or COMP1917')
    assert cs1511 == [['comp1511'], ['dpst1091'], ['comp1911'], ['comp1917']]
    # with my courses filter => [['comp1511']]

    cs9417 = prereqs_parser('(comp2521 and comp1531) or comp2521') == [['comp2521', 'comp1531'], ['comp2521']]

def test_relevant_filter():
    pass


