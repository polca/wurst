from wurst.transformations.geo import *
import pytest


def test_copy_to_new_location():
    given = {
        "foo": "bar",
        "location": "here",
        "exchanges": [{"type": "technosphere"}, {"type": "production"}],
    }
    expected = {
        "foo": "bar",
        "location": "here",
        "exchanges": [
            {"type": "technosphere"},
            {"type": "production", "location": "here"},
        ],
    }
    result = copy_to_new_location(given, "here")
    expected["code"] = result["code"]
    assert result == expected


def test_allocate_inputs_equal():
    given = [
        {"location": "here", "exchanges": [{"type": "production", "amount": 1}]},
        {
            "location": "there",
            "exchanges": [{"type": "production", "production volume": 7, "amount": 1}],
        },
    ]
    exc = {"amount": 1}
    expected = [
        {"location": "here", "amount": 0.5, "loc": 0.5, "uncertainty type": 0},
        {"location": "there", "amount": 0.5, "loc": 0.5, "uncertainty type": 0},
    ]
    assert allocate_inputs(exc, given) == expected
    assert exc == {"amount": 1}


def test_allocate_inputs_equal_row():
    given = [
        {
            "location": "RoW",
            "exchanges": [{"type": "production", "production volume": 20, "amount": 1}],
        },
        {
            "location": "there",
            "exchanges": [{"type": "production", "production volume": 10, "amount": 1}],
        },
    ]
    exc = {"amount": 3}
    expected = [
        {"location": "RoW", "amount": 1.5, "loc": 1.5, "uncertainty type": 0},
        {"location": "there", "amount": 1.5, "loc": 1.5, "uncertainty type": 0},
    ]
    assert allocate_inputs(exc, given) == expected
    assert exc == {"amount": 3}


def test_allocate_inputs_pv():
    given = [
        {
            "location": "there",
            "exchanges": [{"type": "production", "production volume": 30, "amount": 1}],
        },
        {
            "location": "there",
            "exchanges": [{"type": "production", "production volume": 10, "amount": 1}],
        },
    ]
    exc = {"amount": 2}
    expected = [
        {"location": "there", "amount": 1.5, "loc": 1.5, "uncertainty type": 0},
        {"location": "there", "amount": 0.5, "loc": 0.5, "uncertainty type": 0},
    ]
    assert allocate_inputs(exc, given) == expected
    assert exc == {"amount": 2}


def test_get_possibles():
    exc = {"name": "one", "product": "two", "unit": "three"}
    given = [
        {"name": "one", "reference product": "two", "unit": "three", "code": 1},
        {"name": "one", "reference product": "2", "unit": "three", "code": 2},
        {"name": "one", "reference product": "two", "unit": "3", "code": 3},
        {"name": "one", "reference product": "two", "unit": "three", "code": 4},
        {"name": "1", "reference product": "two", "unit": "three", "code": 5},
    ]
    expected = [
        {"name": "one", "reference product": "two", "unit": "three", "code": 1},
        {"name": "one", "reference product": "two", "unit": "three", "code": 4},
    ]
    assert list(get_possibles(exc, given)) == expected


def test_default_global_location():
    given = [{"location": "something"}, {"location": None}, {"foo": "bar"}]
    expected = [
        {"location": "something"},
        {"location": "GLO"},
        {"foo": "bar", "location": "GLO"},
    ]
    problem = [{"foo": "bar"}]
    assert default_global_location(given) == expected
