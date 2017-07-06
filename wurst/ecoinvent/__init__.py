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


def get_ordered_geo_relationships():
    """"""
    _ = lambda x: [y[1] for y in x] + ['RoW', 'GLO']

    res = {region: [region] + _(sorted([(len(b), a)
        for a, b in ecoinvent_faces.items()
        if a not in (region, '__all__')
        and not faces.difference(b)
    ])) for region, faces in ecoinvent_faces.items()}
    res['RoW'] = ['RoW', 'GLO']
    res['GLO'] = ['GLO', 'RoW']
    return res


ECOINVENT_ORDERED_GEO = get_ordered_geo_relationships()
