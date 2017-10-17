from .IMAGE import IMAGE_TOPOLOGY
from collections.abc import MutableMapping
from constructive_geometries import ConstructiveGeometries
from contextlib import contextmanager
from functools import reduce
import country_converter as coco


class Geomatcher(MutableMapping):
    """Object managing spatial relationships using the a world topology.

    ``Geomatcher`` takes as its base data a definition of the world split into topological faces. This definition is provided by the `constructive_geometries <>`__ library. A toplogical face is a polygon which does not overlap any other topological face. In ``constructive_geometries``, these faces are defined by integer ids, so e.g. Ireland is:

    .. code-block:: python

        >>> from constructive_geometries import ConstructiveGeometries
        >>> cg = ConstructiveGeometries()
        >>> cg.data['IE']
        [325, 327, 328, 334, 336, 337, 338, 345, 346, 347, 348, 350, 374, 2045]

    By default, Geomatcher is populated with all world countries, and all ecoinvent regions. The instance of Geomatcher created in this file also includes the IMAGE world regions.

    Geospatial definitions are namespaced, except for countries. Countries are therefore defined by their ISO two-letter codes, but other data should be referenced by a tuple of its namespace and identifier, e.g. ``('ecoinvent', 'NAFTA')``. You can also set a default namespace, either in instantiation (``Geomatcher(default_namespace="foo")``) or afterwards (``geomatcher_instance.default_namespace = 'foo'``). The default namespace is ``'ecoinvent'``.

    Geomatcher supports the following operations:

        * Retrieving face ids for a given location, acting as a dictionary (``geomatcher['foo']``)
        * Adding new geospatial definitions, either directly with face ids or relative to existing definitions
        * Splitting faces to allow for finer-scale regionalization
        * Intersection, contained, and within calculations with several configuration options.

    Initialization arguments:

        * ``topology``: A dictionary of ``{str: set}`` labels to faces ids. Default is ``ecoinvent``, which loads the world and ecoinvent definitions from ``constructive_geometries``.
        * ``default_namespace``: String defining the default search namespace. Default is ``'ecoinvent'``.
        * ``use_coco``: Boolean, default ``True``. Use the `country_converter <>`__ library to fuzzy match country identifiers, e.g. "Austria" instead of "AT".

    """
    __seen = set()

    def __init__(self, topology='ecoinvent', default_namespace=None, use_coco=True):
        self.coco = use_coco
        if topology == 'ecoinvent':
            self.default_namespace = 'ecoinvent'
            def ns(x):
                if len(x) == 2 or x == 'RoW':
                    return x
                else:
                    return ('ecoinvent', x)

            cg = ConstructiveGeometries()
            self.topology = {ns(x): set(y) for x, y in cg.data.items()
                             if x != "__all__"}
            self['GLO'] = reduce(set.union, self.topology.values())
        else:
            self.default_namespace = default_namespace
            self.topology = topology
        if not self.topology:
            self.topology = {}
            self.faces = set()
        else:
            self.faces = reduce(set.union, self.topology.values())

    def __contains__(self, key):
        return key in self.topology

    def __getitem__(self, key):
        if key == 'RoW' and 'RoW' not in self.topology:
            return set()
        return self.topology[self._actual_key(key)]

    def __setitem__(self, key, value):
        try:
            key = self._actual_key(key)
        except KeyError:
            pass
        self.topology[key] = value

    def __delitem__(self, key):
        del self.topology[key]

    def __len__(self):
        return len(self.topology)

    def __iter__(self):
        return iter(self.topology)

    def _actual_key(self, key):
        """Translate provided key into the key used in the topology. Tries the unmodified key, the key with the default namespace, and the country converter. Raises a ``KeyError`` if none of these finds a suitable definition in ``self.topology``."""
        if key == "RoW":
            return key
        elif key in self:
            return key
        elif (self.default_namespace, key) in self:
            return (self.default_namespace, key)

        if isinstance(key, str) and self.coco:
            new = coco.convert(names=[key], to='ISO2', not_found=None)
            if new in self:
                if new not in self.__seen:
                    self.__seen.add(key)
                    print("Geomatcher: Used '{}' for '{}'".format(new, key))
                return new

        raise KeyError("Can't find this location")

    def _finish_filter(self, lst, key, include_self, exclusive, biggest_first):
        """Finish filtering a GIS operation. Can optionally exclude the input key, sort results, and exclude overlapping results. Internal function, not normally called directly."""
        key = self._actual_key(key)
        locations = [x[0] for x in lst]

        if not include_self and key in locations:
            lst.pop(locations.index(key))

        lst.sort(key=lambda x: x[1], reverse=biggest_first)
        lst = [x for x, y in lst]

        # RoW in both key and lst, but not defined; only RoW remains if exclusive
        if key == 'RoW' and 'RoW' not in self and exclusive:
            return ['RoW'] if 'RoW' in lst else []
        elif exclusive:
            removed, remaining = set(), []
            while lst:
                current = lst.pop(0)
                faces = self[current]
                if not faces.intersection(removed):
                    removed.update(faces)
                    remaining.append(current)
            lst = remaining

            # Remove RoW when there are no topo faces for it to occupy
            if ('RoW' not in self and 'RoW' in lst
                and not self[key].difference(removed)):
                lst.pop(lst.index('RoW'))

        # If RoW not resolved, make it the smallest
        if 'RoW' not in self and 'RoW' in lst:
            lst[-1 if biggest_first else 0] = lst.pop(lst.index('RoW'))

        return lst

    def intersects(self, key, include_self=False, exclusive=False, biggest_first=True, only=None):
        """Get all locations that intersect this location.

        Note that sorting is done by first by number of faces intersecting ``key``; the total number of faces in the intersected region is only used to break sorting ties.

        If the ``resolved_row`` context manager is not used, ``RoW`` doesn't have a spatial definition. Therefore, ``.intersects("RoW")`` returns a list with with ``RoW`` or nothing.

        """
        if key == 'RoW' and 'RoW' not in self:
            return ['RoW'] if 'RoW' in possibles else []

        possibles = self.topology if only is None else {k: self[k] for k in only}

        faces = self[key]
        lst = [
            (k, (len(v.intersection(faces)), len(v)))
            for k, v in possibles.items()
            if (faces.intersection(v))
        ]
        return self._finish_filter(lst, key, include_self, exclusive, biggest_first)

    def contained(self, key, include_self=True, exclusive=False, biggest_first=True, only=None):
        """Get all locations that are completely within this location.

        If the ``resolved_row`` context manager is not used, ``RoW`` doesn't have a spatial definition. Therefore, ``.contained("RoW")`` returns a list with either ``RoW`` or nothing.

        """
        if 'RoW' not in self:
            if key == 'RoW':
                return ['RoW'] if 'RoW' in (only or []) else []
            elif only and 'RoW' in only:
                only.pop(only.index('RoW'))

        possibles = self.topology if only is None else {k: self[k] for k in only}

        faces = self[key]
        lst = [
            (k, len(v))
            for k, v in possibles.items()
            if faces.issuperset(v)
        ]
        return self._finish_filter(lst, key, include_self, exclusive, biggest_first)

    def within(self, key, include_self=True, exclusive=False, biggest_first=True, only=None):
        """Get all locations that completely contain this location.

        If the ``resolved_row`` context manager is not used, ``RoW`` doesn't have a spatial definition. Therefore, ``RoW`` can only be contained by ``GLO`` and ``RoW``.

        """
        _ = lambda key: [key] if key in (only or []) else []
        if 'RoW' not in self and key == 'RoW':
            answer = [] + _('RoW') + _('GLO')
            return list(reversed(answer)) if biggest_first else answer

        possibles = self.topology if only is None else {k: self[k] for k in only}

        faces = self[key]
        lst = [
            (k, len(v))
            for k, v in possibles.items()
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
            ids = set(range(max_int + 1, max_int + 1 + (number or 2)))

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

        Otherwise, ``data`` is a dictionary with string keys and values of integer topology face id sets:

        .. code-block:: python

            {
                'A': {1, 2, 3},
                'B': {2, 3, 4},
            }

        """
        if not relative:
            self.topology.update({(namespace, k): v for k, v in data.items()})
            self.faces.update(set.union(*data.values()))
        else:
            self.topology.update({
                (namespace, k): set.union(*[self[o] for o in v])
                for k, v in data.items()
            })


geomatcher = Geomatcher()
geomatcher.add_definitions(IMAGE_TOPOLOGY, "IMAGE", relative=True)


@contextmanager
def resolved_row(objs, geomatcher=geomatcher):
    """Temporarily insert ``RoW`` into ``geomatcher.topology``, defined by the topo faces not used in ``objs``.

    Will overwrite any existing ``RoW``.

    On exiting the context manager, ``RoW`` is deleted."""
    def get_locations(lst):
        for elem in lst:
            try:
                yield elem['location']
            except TypeError:
                yield elem

    geomatcher['RoW'] = geomatcher.faces.difference(
        reduce(
            set.union,
            [geomatcher[obj] for obj in get_locations(objs)]
        )
    )
    yield geomatcher
    del geomatcher['RoW']
