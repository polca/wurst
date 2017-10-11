from constructive_geometries import ConstructiveGeometries
from copy import deepcopy
from wurst import geomatcher
from wurst.geo import Geomatcher
import pytest


def test_default_setup():
    cg = ConstructiveGeometries()

    assert geomatcher["RoW"] == set()
    assert geomatcher["GLO"] == set()
    assert geomatcher["AS"] == set(cg.data['AS'])
    assert geomatcher[('ecoinvent', 'Russia (Europe)')] == set(cg.data['Russia (Europe)'])
    assert geomatcher["Japan"] == set(cg.data['JP'])

    with pytest.raises(KeyError):
        geomatcher["Nope"]

def test_image_added():
    g = Geomatcher()
    with pytest.raises(KeyError):
        g["Oceania"]

    assert len(geomatcher[("IMAGE", "Oceania")])

def test_provide_topology():
    given = {
        'A': {1, 2, 3},
        'B': {2, 3, 4},
    }
    g = Geomatcher(given.copy())
    assert g.topology == given

def test_split_faces():
    given = {
        'A': {1, 2, 3},
        'B': {2, 3, 4},
    }
    expected = {
        'A': {1, 2, 5, 6},
        'B': {2, 5, 6, 4},
    }
    g = Geomatcher(given)
    g.split_face(3)
    assert g.topology == expected
    assert 3 not in g.faces
    assert 5 in g.faces

    given = {
        'A': {1, 2, 3},
        'B': {2, 3, 4},
    }
    expected = {
        'A': {1, 2, 5, 6, 7},
        'B': {2, 5, 6, 7, 4},
    }
    g = Geomatcher(given)
    g.split_face(3, number=3)
    assert g.topology == expected

    given = {
        'A': {1, 2, 3},
        'B': {2, 3, 4},
    }
    expected = {
        'A': {1, 2, 10, 11},
        'B': {2, 10, 11, 4},
    }
    g = Geomatcher(given)
    g.split_face(3, ids={10, 11})
    assert g.topology == expected

    given = {
        'A': {1, 2, 3},
        'B': {2, 3, 4},
    }
    expected = {
        'A': {1, 2, 10, 11},
        'B': {2, 10, 11, 4},
    }
    g = Geomatcher(given)
    g.split_face(3, number=5, ids={10, 11})
    assert g.topology == expected

def test_empty_topology():
    g = Geomatcher({})
    assert g.topology == {}
    assert g.faces == set()

def test_add_definitions():
    g = Geomatcher({})
    given = {
        'A': {1, 2, 3},
        'B': {2, 3, 4},
    }
    g.add_definitions(given, "foo", False)
    assert ("foo", "A") in g.topology
    assert g.faces == {1, 2, 3, 4}

def test_add_definitions_relative():
    given = {
        'A': {1, 2, 3},
        'B': {2, 3, 4},
    }
    extra = {
        'C': ['A', 'B']
    }
    g = Geomatcher(given)
    g.add_definitions(extra, "foo")
    assert g.topology[("foo", "C")] == {1, 2, 3, 4}
    assert 'A' in g.topology

def test_actual_key():
    given = {
        'A': {1, 2, 3},
        ('silly', 'B'): {2, 3, 4},
    }
    g = Geomatcher(given, 'silly')
    assert g['A']
    assert g['B']
    assert g['B']
    assert g[('silly', 'B')]

    with pytest.raises(KeyError):
        g[('silly', 'A')]

    assert g._actual_key('RoW') == 'RoW'
    assert g._actual_key('GLO') == 'GLO'

def test_actual_key_coco():
    given = {
        'AT': {1, 2},
    }
    g = Geomatcher(given, 'silly')

    assert g['AT']
    assert g['Austria']

    g = Geomatcher(given, 'silly', use_coco=False)
    assert g['AT']
    with pytest.raises(KeyError):
        g['Austria']

def test_finish_filter():
    g = Geomatcher({'A': {1, 2}})
    given = [('A', 4), ('B', 6), ('C', 3)]
    assert g._finish_filter(deepcopy(given), 'A', True, False, True) == ['B', 'A', 'C']
    assert g._finish_filter(deepcopy(given), 'A', True, False, False) == ['C', 'A', 'B']
    assert g._finish_filter(deepcopy(given), 'A', False, False, True) == ['B', 'C']
    assert g._finish_filter(deepcopy(given), 'A', False, False, False) == ['C', 'B']

def test_finish_filter_exclusive():
    given = {
        'A': {1, 2, 3},
        'B': {2, 3, 4},
        'C': {3, 4, 5},
        'D': {10, 11},
        'E': {5, 6, 10},
    }
    g = Geomatcher(given)
    lst = [('A', 5), ('B', 6), ('C', 7), ('D', 8), ('E', 9)]
    result = g._finish_filter(lst, 'A', True, True, True)
    # Start with E (biggest), then B (next possible)
    assert result == ["E", "B"]
    result = g._finish_filter(lst, 'A', True, True, False)
    # Start with A (smallest), then D (next possible)
    assert result == ['A', 'D']

def test_intersects():
    g = Geomatcher()
    expected = [
        ('ecoinvent', 'UN-AMERICAS'),
        ('ecoinvent', 'RLA'),
        ('ecoinvent', 'UN-CARIBBEAN'),
    ]
    assert geomatcher.intersects("CU") == expected
    assert geomatcher.intersects("CU", exclusive=True) == [('ecoinvent', 'UN-AMERICAS')]
    expected = [
        ('ecoinvent', 'UN-CARIBBEAN'),
        ('ecoinvent', 'RLA'),
        ('ecoinvent', 'UN-AMERICAS'),
    ]
    assert geomatcher.intersects("CU", biggest_first=False) == expected

def test_contained():
    g = Geomatcher()
    expected = [
        'US',
        ('ecoinvent', 'US-ASCC'),
        ('ecoinvent', 'US-NPCC'),
        ('ecoinvent', 'US-HICC'),
        ('ecoinvent', 'US-WECC'),
        ('ecoinvent', 'US-SERC'),
        ('ecoinvent', 'US-RFC'),
        ('ecoinvent', 'US-FRCC'),
        ('ecoinvent', 'US-MRO'),
        ('ecoinvent', 'US-SPP')
    ]
    assert g.contained("US")[:5] == expected[:5]
    expected.pop(0)
    assert g.contained("US", include_self=False)[:5] == expected[:5]
    assert g.contained("US", include_self=False, exclusive=True)[:5] == expected[:5]
    assert g.contained("US", biggest_first=False, include_self=False)[-1] == ('ecoinvent', 'US-ASCC')

def test_within():
    g = Geomatcher()
    expected = [
        ('ecoinvent', 'UN-EUROPE'),
        ('ecoinvent', 'FSU'),
        ('ecoinvent', 'UN-EEUROPE'),
        ('ecoinvent', 'IAI Area, Europe outside EU & EFTA'),
        'RU',
    ]
    assert g.within("RU") == expected
    expected.pop(-1)
    assert g.within("RU", include_self=False) == expected
    assert g.within("RU", exclusive=True) == [('ecoinvent', 'UN-EUROPE')]
    expected = [
        'RU',
        ('ecoinvent', 'IAI Area, Europe outside EU & EFTA'),
        ('ecoinvent', 'UN-EEUROPE'),
        ('ecoinvent', 'FSU'),
        ('ecoinvent', 'UN-EUROPE'),
    ]
    assert g.within("RU", biggest_first=False) == expected

def test_intersects_glo_row():
    g = Geomatcher()
    assert len(geomatcher.intersects("GLO")) > 400
    assert geomatcher.intersects("RoW") == []

def test_contained_glo_row():
    g = Geomatcher()
    assert len(geomatcher.contained("GLO")) > 400
    assert geomatcher.contained("RoW") == []

def test_within_glo_row():
    g = Geomatcher()
    assert geomatcher.within("GLO") == []
    assert geomatcher.within("RoW") == []
