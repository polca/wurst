from ..ecoinvent import ecoinvent_faces
import json
import os

dirpath = os.path.dirname(__file__)

REGIONS = json.load(open(os.path.join(dirpath, "metadata", "regions.json")))
REGION_TOPOLOGY = json.load(open(os.path.join(dirpath, "metadata", "region-topolgy.json")))
LOCATION_MAPPING = json.load(open(os.path.join(dirpath, "metadata", "location-mapping.json")))

IMAGE_REGION_FACES = {k: set.union(*[set(ecoinvent_faces[code]) for code in v])
                      for k, v in REGION_TOPOLOGY.items()}


def ecoinvent_to_image_locations(location):
    if location in ('RoW', 'GLO'):
        return ['World']
    if location not in ecoinvent_faces:
        raise KeyError("Can't find topo data for this location: {}".format(location))
    covered = [
        key for key, value in IMAGE_REGION_FACES.items()
        if not ecoinvent_faces[location].difference(value)
    ]
    partial = [
        key for key, value in IMAGE_REGION_FACES.items()
        if ecoinvent_faces[location].intersection(value)
    ]
    if len(covered) == 1:
        return covered
    else:
        return partial
