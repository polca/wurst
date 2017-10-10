from .IMAGE import IMAGE_TOPOLOGY
from constructive_geometries import ConstructiveGeometries
import country_converter as coco


class Geomatcher:
    __seen = set()

    def __init__(self, topology='ecoinvent', default_namespace=None):
        if topology == 'ecoinvent':
            def ns(x):
                if len(x) == 2 or x in {'RoW', 'GLO'}:
                    return x
                else:
                    return ('ecoinvent', x)

            cg = ConstructiveGeometries()
            self.topology = {ns(x): set(y) for x, y in cg.data.items()
                             if x != "__all__"}
            self.default_namespace = 'ecoinvent'
        else:
            self.topology = topology
            self.default_namespace = default_namespace
        self.faces = set.union(*[set(x) for x in self.topology.values()])

    def __getitem__(self, key):
        if key in {"RoW", "GLO"}:
            return set()
        return self.topology[self._actual_key(key)]

    def _actual_key(self, key):
        if key in {"RoW", "GLO"}:
            return key
        elif key in self.topology:
            return key
        elif (self.default_namespace, key) in self.topology:
            return (self.default_namespace, key)

        if isinstance(key, str):
            new = coco.convert(names=[key], to='ISO2', not_found=None)
            if new in self.topology:
                if new not in self.__seen:
                    self.__seen.add(key)
                    print("Geomatcher: Used '{}' for '{}'".format(new, key))
                return new

        raise KeyError("Can't find this location")

    def _finish_filter(self, lst, key, include_self, exclusive, biggest_first):
        key = self._actual_key(key)
        if not include_self:
            lst.pop(lst.index(key))
        lst.sort(key=lambda x: x[1], reverse=biggest_first)
        lst = [x for x, y in lst]
        if exclusive:
            removed, remaining = set(), []
            while lst:
                current = lst.pop(0)
                faces = self[current]
                if not faces.intersection(removed):
                    removed.update(faces)
                    remaining.append(current)
            lst = remaining
        return lst

    def intersects(self, key, include_self=False, exclusive=False, biggest_first=True):
        """Get all locations that intersect this location."""
        if key in ('RoW', 'GLO'):
            return self._finish_filter(
                [("GLO", 2), ("RoW", 1)],
                key, include_self, exclusive, biggest_first
            )

        faces = self[key]
        lst = [
            (k, len(v.intersection(faces)))
            for k, v in self.topology.items()
            if faces.intersection(v)
        ]
        return self._finish_filter(lst, key, include_self, exclusive, biggest_first)

    def contained(self, key, include_self=True, exclusive=False, biggest_first=True):
        """Get all locations contained by this location."""
        if key in ('RoW', 'GLO'):
            return self._finish_filter(
                [("GLO", 2), ("RoW", 1)],
                key, include_self, exclusive, biggest_first
            )

        faces = self[key]
        lst = [
            (k, len(v))
            for k, v in self.topology.items()
            if faces.issuperset(v)
        ]
        return self._finish_filter(lst, key, include_self, exclusive, biggest_first)

    def within(self, key, include_self=True, exclusive=False):
        """Get all locations that are contained by this location."""
        if key in ('RoW', 'GLO'):
            return self._finish_filter(
                [("GLO", 2), ("RoW", 1)],
                key, include_self, exclusive, biggest_first
            )

        faces = self[key]
        lst = [
            (k, len(v))
            for k, v in self.topology.items()
            if faces.issubset(v)
        ]
        return self._finish_filter(lst, key, include_self, exclusive, biggest_first)

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

    def add_definitions(self, data, namespace, relative=True):
        """Add new topological definitions to ``self.topology``.

        If ``relative`` is true, then ``data`` is defined relative to the existing locations already in ``self.topology``, e.g. IMAGE:

        .. code-block:: python

            {"Russia Region": [
                "AM",
                "AZ",
                "GE",
                "RU"
            ]}

        Otherwise, ``data`` is a dictionary with integer topology face ids.

        """
        if not relative:
            self.topology.update({(namespace, k): v for k, v in data.items()})
        else:
            self.topology.update({
                (namespace, k): set.union(*[self[o] for o in v])
                for k, v in data.items()
            })


geomatcher = Geomatcher()
geomatcher.add_definitions(IMAGE_TOPOLOGY, "IMAGE", relative=True)
