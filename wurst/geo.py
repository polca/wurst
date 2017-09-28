from constructive_geometries import ConstructiveGeometries
import country_converter as coco


class Geomatcher:
    def __init__(self, topology='ecoinvent'):
        if topology == 'ecoinvent':
            cg = ConstructiveGeometries()
            self.topology = {x: set(y) for x, y in cg.data.items()
                             if x != "__all__"}
        else:
            self.topology = topology
        self.faces = set.union(set(x) for x in self.topology.values())

    def as_valid_key(self, key):
        key = coco.convert(names=[key], to='ISO2', not_found=None)[0]
        if key in self.topology:
            return key
        else:
            raise KeyError("Can't find this location")

    def intersects(self, key, include_self=True):
        """Get all locations that intersect this location, in order of number of faces (highest first)"""
        def _(answer):
            if not include_self:
                answer.pop(answer.index(key))
            return answer

        if key in ('RoW', 'GLO'):
            return _(['GLO', 'RoW'])

        faces = self.topology(self.as_valid_key(key))
        return  _([x
            for x, y in sorted([
                    k, len(v.intersection(faces))
                    for k, v in self.topology.items()
                    if v.intersection(faces)
                ], reverse=True, key=lambda x: x[1])
        ])

    def contains(self, key, include_self=True):
        """Get all locations that contain this location, in order of number of faces (lowest first)"""
        def _(answer):
            if not include_self:
                answer.pop(answer.index(key))
            return answer

        if key in ('RoW', 'GLO'):
            return _(['GLO', 'RoW'])

        faces = self.topology(self.as_valid_key(key))
        return  _([x
            for x, y in sorted([
                    k, len(v.intersection(faces))
                    for k, v in self.topology.items()
                    if v.intersection(faces)
                ], reverse=True, key=lambda x: x[1])
        ])

    def within(self, key, include_self=True):
        """Get all locations that are contained by this location, in order of number of faces (highest first)"""
        def _(answer):
            if not include_self:
                answer.pop(answer.index(key))
            return answer

        if key in ('RoW', 'GLO'):
            return _(['GLO', 'RoW'])

        faces = self.topology(self.as_valid_key(key))
        return  _([x
            for x, y in sorted([
                    k, len(v.intersection(faces))
                    for k, v in self.topology.items()
                    if v.intersection(faces)
                ], reverse=True, key=lambda x: x[1])
        ])

    def split_face(self, face, number=None, ids=None):
        """Split a topological face into a number of small faces.

    * ``face``: The face to split. Must be in the topology.
    * ``number``: Number of new faces to create. Optional, can be inferred from ``ids``. Default is 2 new faces.
    * ``ids``: Iterable of new face ids. Optional, default is the maximum integer in the existing topology plus one. ``ids`` don't have to be integers. If ``ids`` is specified, ``number`` is ignored.

    Returns the new face ids.

        """
        assert face in self.faces

        if ids:
            ids = set(ids)
        else:
            max_int = max(x for x in self.faces if isinstance(x, int))
            ids = set(range(max_int + 1, max_int + 2 + (number or 2)))

        for obj in self.topology.values():
            if face in obj:
                obj.discard(face)
                obj.update(ids)

        self.faces.discard(face)
        self.faces.update(ids)

        return ids



geomatcher = Geomatcher()
geomatcher.add_definitions(IMAGE, relative=True)
