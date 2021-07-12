from wurst import change_exchanges_by_constant_factor, equals
import pytest


def test_change_exchanges_by_constant_factor_errors():
    with pytest.raises(AssertionError):
        change_exchanges_by_constant_factor({}, "four")
    with pytest.raises(AssertionError):
        change_exchanges_by_constant_factor(None, 4)


def test_change_exchanges_by_constant_factor():
    given = {
        "foo": "bar",
        "exchanges": [
            {"filter me": "found", "foo": "baz", "amount": 6, "type": "technosphere"},
            {"filter me": "found", "amount": 5, "type": "biosphere"},
            {"foo": "baz", "amount": 4, "type": "technosphere"},
            {"amount": 3, "type": None},
        ],
    }
    expected = {
        "foo": "bar",
        "exchanges": [
            {
                "filter me": "found",
                "uncertainty type": 0,
                "loc": 3,
                "foo": "baz",
                "amount": 3,
                "type": "technosphere",
            },
            {
                "filter me": "found",
                "uncertainty type": 0,
                "loc": 2.5,
                "amount": 2.5,
                "type": "biosphere",
            },
            {"foo": "baz", "amount": 4, "type": "technosphere"},
            {"amount": 3, "type": None},
        ],
    }
    filters = [equals("filter me", "found")]
    assert change_exchanges_by_constant_factor(given, 0.5, filters, filters) == expected
