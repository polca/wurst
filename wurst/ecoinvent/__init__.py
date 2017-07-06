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
    """Construct a dictionary with ecoinvent location codes as keys, and a list of ecoinvent location codes which contain that key in order of increasing size as values.

    Size is approximated using the number of topological faces in each location.

    Example output:

    .. code-block:: python

        'UZ': ['UZ', 'Central Asia', 'FSU', 'Asia without China', 'UN-ASIA', 'RAS', 'RoW', 'GLO']

    """
    _ = lambda x: [y[1] for y in x] + ['RoW', 'GLO']

    res = {region: [region] + _(sorted([(len(b), a)
        for a, b in ecoinvent_faces.items()
        if a not in (region, '__all__')
        and not faces.difference(b)]))
    for region, faces in ecoinvent_faces.items()
    if region != "__all__"}

    res['RoW'] = ['RoW', 'GLO']
    res['GLO'] = ['GLO', 'RoW']
    return res


ECOINVENT_ORDERED_GEO = get_ordered_geo_relationships()
