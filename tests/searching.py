from wurst.searching import *
from wurst.errors import MultipleResults, NoResults
import pytest


def test_contains():
    func = contains('n', 'foo')
    assert func({'n': 'foobar'})
    assert not func({'n': 'bar'})
    with pytest.raises(KeyError):
        func({'m': 'foobar'})
