from wurst import rescale_exchange
import pytest


def test_rescale_exchange_wrong_inputs():
    with pytest.raises(AssertionError):
        rescale_exchange([], 4)
    with pytest.raises(AssertionError):
        rescale_exchange({}, "four")


def test_rescale_exchange():
    given = {"amount": 2, "foo": "bar", "minimum": 7, "uncertainty type": -1}
    expected = {"amount": 1, "loc": 1, "foo": "bar", "uncertainty type": 0}
    assert rescale_exchange(given, 0.5) == expected
