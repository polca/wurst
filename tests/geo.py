from constructive_geometries import Geomatcher, ConstructiveGeometries
from wurst import geomatcher
import pytest


def test_default_setup():
    cg = ConstructiveGeometries()

    assert 'GLO' in geomatcher
    assert 'RoW' not in geomatcher
    assert geomatcher["RoW"] == set()
    assert len(geomatcher["GLO"]) > 400
    assert geomatcher["AS"] == set(cg.data['AS'])
    assert geomatcher[('ecoinvent', 'Russia (Europe)')] == set(cg.data['Russia (Europe)'])
    assert geomatcher["Japan"] == set(cg.data['JP'])

    with pytest.raises(KeyError):
        geomatcher["Nope"]

def test_image_added():
    assert ("IMAGE", "Oceania") in geomatcher
    g = Geomatcher()
    assert ("IMAGE", "Oceania") not in g
