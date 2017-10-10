from wurst import geomatcher
from constructive_geometries import ConstructiveGeometries
import pytest


def test_get_faces():
    cg = ConstructiveGeometries()

    assert geomatcher["RoW"] == set()
    assert geomatcher["GLO"] == set()
    assert geomatcher["AS"] == set(cg.data['AS'])
    assert geomatcher["Japan"] == set(cg.data['JP'])

    with pytest.raises(KeyError):
        geomatcher["Nope"]
