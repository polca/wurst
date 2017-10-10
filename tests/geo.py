from wurst import geomatcher
from wurst.geo import Geomatcher
from constructive_geometries import ConstructiveGeometries
import pytest


def test_get_faces():
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
        g[("IMAGE", "Oceania")]

    assert len(geomatcher[("IMAGE", "Oceania")])

def test_split_faces():
    g = Geomatcher()

