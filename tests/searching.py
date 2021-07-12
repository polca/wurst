from wurst.searching import *
from wurst.errors import MultipleResults, NoResults
import pytest


def test_contains():
    func = contains("n", "foo")
    assert func({"n": "foobar"})
    assert not func({"n": "bar"})


def test_equals():
    func = equals("n", "foo")
    assert func({"n": "foo"})
    assert not func({"n": "foobar"})


def test_startswith():
    func = startswith("n", "foo")
    assert func({"n": "foobar"})
    assert not func({"n": "barfoo"})


def test_exclude():
    func = equals("n", "foo")
    assert func({"n": "foo"})
    func = exclude(equals("n", "foo"))
    assert not func({"n": "foo"})


def test_either():
    func1 = equals("n", "foo")
    func2 = equals("n", "bar")
    assert either(func1, func2)({"n": "bar"})
    assert not either(func1, func2)({"n": "foobar"})


def test_get_one():
    func = equals("n", "foo")
    assert get_one([{"n": "foo"}], func) == {"n": "foo"}
    with pytest.raises(MultipleResults):
        get_one([{"n": "foo"}, {"n": "foo"}], func)
    with pytest.raises(NoResults):
        get_one([{"n": "bar"}, {"n": "bar"}], func)


def test_get_many():
    func = equals("n", "foo")
    assert list(get_many([{"n": "foo"}, {"n": "foo"}], func)) == [
        {"n": "foo"},
        {"n": "foo"},
    ]
    assert list(get_many([{"n": "bar"}], func)) == []


def test_doesnt_contain_any():
    func = doesnt_contain_any("n", ["foo", "bar"])
    assert func({"n": "chicken"})
    assert not func({"n": "barfoo"})
    assert not func({"n": "ffffooooo"})


def test_technosphere():
    given = {
        "exchanges": [
            {"type": "nope", "n": "foo"},
            {"type": "technosphere", "n": "bar"},
        ]
    }
    expected = [{"type": "technosphere", "n": "bar"}]
    assert list(technosphere(given)) == expected

    given = {
        "exchanges": [
            {"type": "nope", "n": "foo"},
            {"type": "technosphere", "n": "bar"},
        ]
    }
    expected = [{"type": "technosphere", "n": "bar"}]
    assert list(technosphere(given, None)) == expected

    given = {
        "exchanges": [
            {"type": "nope", "n": "foo"},
            {"type": "technosphere", "n": "bar"},
            {"type": "technosphere", "n": "foo"},
        ]
    }
    expected = [{"type": "technosphere", "n": "bar"}]
    assert list(technosphere(given, equals("n", "bar"))) == expected


def test_biosphere():
    given = {
        "exchanges": [{"type": "nope", "n": "foo"}, {"type": "biosphere", "n": "bar"}]
    }
    expected = [{"type": "biosphere", "n": "bar"}]
    assert list(biosphere(given)) == expected

    given = {
        "exchanges": [
            {"type": "nope", "n": "foo"},
            {"type": "biosphere", "n": "bar"},
            {"type": "biosphere", "n": "foo"},
        ]
    }
    expected = [{"type": "biosphere", "n": "bar"}]
    assert list(biosphere(given, equals("n", "bar"))) == expected


def test_production():
    given = {
        "exchanges": [{"type": "nope", "n": "foo"}, {"type": "production", "n": "bar"}]
    }
    expected = [{"type": "production", "n": "bar"}]
    assert list(production(given)) == expected

    given = {
        "exchanges": [
            {"type": "nope", "n": "foo"},
            {"type": "production", "n": "bar"},
            {"type": "production", "n": "foo"},
        ]
    }
    expected = [{"type": "production", "n": "bar"}]
    assert list(production(given, equals("n", "bar"))) == expected


def test_reference_product():
    given = {
        "exchanges": [
            {"type": "production", "n": "foo", "amount": 1},
            {"type": "production", "n": "bar", "amount": 0},
            {"type": "not production", "n": "foobar", "amount": 1},
        ]
    }
    expected = {"type": "production", "n": "foo", "amount": 1}
    assert reference_product(given) == expected

    given = {
        "exchanges": [
            {"type": "production", "n": "bar", "amount": 0},
            {"type": "not production", "n": "foobar", "amount": 1},
        ]
    }
    with pytest.raises(NoResults):
        reference_product(given)

    given = {
        "exchanges": [
            {"type": "production", "n": "foo", "amount": 1},
            {"type": "production", "n": "bar", "amount": 1},
            {"type": "not production", "n": "foobar", "amount": 1},
        ]
    }
    with pytest.raises(MultipleResults):
        reference_product(given)


def test_best_geo_match():
    given = [
        {"location": "one"},
        {"location": "two"},
        {"location": "three"},
        {"location": "four"},
        {"location": "five"},
        {"location": "six"},
        {"location": "seven"},
    ]
    order = ["foo", "bar", "four", "seven", "one", "july"]
    assert best_geo_match(given, order) == {"location": "four"}

    order = ["foo", "bar", "july"]
    assert best_geo_match(given, order) is None
