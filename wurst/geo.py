from .IMAGE import IMAGE_TOPOLOGY
from constructive_geometries import ConstructiveGeometries
import country_converter as coco


class Geomatcher:
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
        if self.topology:
            self.faces = set.union(*[set(x) for x in self.topology.values()])
        else:
            self.faces = set()

    def __getitem__(self, key):
        if key in {"RoW", "GLO"}:
            return set()
        return self.topology[self._actual_key(key)]

    def _actual_key(self, key):
        """Translate provided key into the key used in the topology. Tries the unmodified key, the key with the default namespace, and the country converter. Raises a ``KeyError`` if none of these finds a suitable definition in ``self.topology``."""
        if key in {"RoW", "GLO"}:
            return key
        elif key in self.topology:
            return key
        elif (self.default_namespace, key) in self.topology:
            return (self.default_namespace, key)

        if isinstance(key, str) and self.coco:
            new = coco.convert(names=[key], to='ISO2', not_found=None)
            if new in self.topology:
                if new not in self.__seen:
                    self.__seen.add(key)
                    print("Geomatcher: Used '{}' for '{}'".format(new, key))
                return new

        raise KeyError("Can't find this location")

    def _finish_filter(self, lst, key, include_self, exclusive, biggest_first):
        """Finish filtering a GIS operation. Can optionally exclude the input key, sort results, and exclude overlapping results. Internal function, not normally called directly."""
        key = self._actual_key(key)
        given = [x[0] for x in lst]

        has_row = "RoW" in given
        if has_row:
            lst.pop(given.index("RoW"))
            given.pop(given.index("RoW"))
        has_glo = "GLO" in given
        if has_glo:
            lst.pop(given.index("GLO"))
            given.pop(given.index("GLO"))

        if not include_self and key in given:
            lst.pop(given.index(key))
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

            # No faces left to be covered by global datasets
            if not self[key].difference(removed):
                has_row = has_glo = False

        if has_row and (key != 'RoW' or include_self):
            if biggest_first:
                lst.insert(0, "RoW")
            else:
                lst.insert(-1, "RoW")
        if has_glo and (key != 'GLO' or include_self):
            if biggest_first:
                lst.insert(0, "GLO")
            else:
                lst.insert(-1, "GLO")
        return lst

    def intersects(self, key, include_self=False, exclusive=False, biggest_first=True, only=None):
        """Get all locations that intersect this location.

        Note that sorting is done by first by number of faces intersecting ``key``; the total number of faces in the intersected region is only used to break sorting ties.

        ``.intersects("GLO")`` return all regions. ``.intersects("RoW")`` returns a list with with ``RoW`` or nothing.

        """
        possibles = {k: self[k] for k in (only or [])} or self.topology

        if key == 'GLO':
            return self._finish_filter(
                [(k, len(v)) for k, v in possibles.items()],
                "GLO", include_self, exclusive, biggest_first
            )
        if key == 'RoW':
            return ['RoW'] if 'RoW' in possibles else []

        faces = self[key]
        lst = [
            (k, (len(v.intersection(faces)), len(v)))
            for k, v in possibles.items()
            if (faces.intersection(v) or k in ("GLO", "RoW"))
        ]
        return self._finish_filter(lst, key, include_self, exclusive, biggest_first)

    def contained(self, key, include_self=True, exclusive=False, biggest_first=True, only=None):
        """Get all locations that are completely within this location.

        ``.contained("GLO")`` return all regions. ``.contained("RoW")`` returns a list with with ``RoW`` or nothing.

        "RoW" and "GLO" are not normally in ``self.topology``, but if they are, or are passed in ``only``, here are the rules for handling them:

            * GLO contains RoW and GLO
            * RoW contains RoW

        Note that both ``GLO`` and ``RoW`` could be removed if ``exclusive`` is true.

        """
        # GLO and RoW make my head hurt
        ALLOWED = {("RoW", "GLO"), ("GLO", "GLO"), ("RoW", "RoW")}
        row_filter = lambda x: x not in ("GLO", "RoW") or (x, key) in ALLOWED
        possibles = {
            k: self[k] for k in (only or []) if row_filter(k)
        } or self.topology

        if key == 'GLO':
            return self._finish_filter(
                [(k, len(v)) for k, v in possibles.items()],
                "GLO", include_self, exclusive, biggest_first
            )
        if key == 'RoW':
            return ['RoW'] if 'RoW' in possibles else []

        faces = self[key]
        lst = [
            (k, len(v))
            for k, v in possibles.items()
            if faces.issuperset(v)
        ]
        return self._finish_filter(lst, key, include_self, exclusive, biggest_first)

    def within(self, key, include_self=True, exclusive=False, biggest_first=True, only=None):
        """Get all locations that completely contain this location.

        When called with GLO or RoW, returns a list which can only have GLO or RoW inside, if either are passed in ``only`` or added to ``self.topology``. Otherwise returns an empty list.

        """
        possibles = {k: self[k] for k in (only or [])} or self.topology

        if key == 'GLO':
            return [x for x in possibles if x in ("GLO",)]
        if key == 'RoW':
            return [x for x in possibles if x in ("RoW", "GLO")]

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
