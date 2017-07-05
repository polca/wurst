import os
import json

faces_filepath = os.path.join(os.path.dirname(__file__), "metadata", "faces.json")
ecoinvent_faces = {x: set(y) for x, y in json.load(open(faces_filepath))['data']}


def ecoinvent_within(data, location):
    try:
        faces = ecoinvent_faces[location]
    except KeyError:
        raise ValueError("Unknown location")
    return (ds for ds in data if False)
