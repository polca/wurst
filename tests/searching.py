from wurst.searching import *
from wurst.errors import MultipleResults, NoResults
import pytest


def test_contains():
    func = contains('n', 'foo')
    assert func({'n': 'foobar'})
    assert not func({'n': 'bar'})
    with pytest.raises(KeyError):
        func({'m': 'foobar'})

def test_equals():
    func = equals('n', 'foo')
    assert func({'n': 'foo'})
    assert not func({'n': 'foobar'})
    with pytest.raises(KeyError):
        func({'m': 'foo'})

def test_startswith():
    func = startswith('n', 'foo')
    assert func({'n': 'foobar'})
    assert not func({'n': 'barfoo'})
    with pytest.raises(KeyError):
        func({'m': 'foo'})

def test_get_one():
    func = equals('n', 'foo')
    assert get_one([{'n': 'foo'}], [func]) == {'n': 'foo'}
    with pytest.raises(MultipleResults):
        get_one([{'n': 'foo'}, {'n': 'foo'}], [func])
    with pytest.raises(NoResults):
        get_one([{'n': 'bar'}, {'n': 'bar'}], [func])

def test_get_many():
    func = equals('n', 'foo')
    assert list(get_many([{'n': 'foo'}, {'n': 'foo'}], [func])) == [{'n': 'foo'}, {'n': 'foo'}]
    assert list(get_many([{'n': 'bar'}], [func])) == []
