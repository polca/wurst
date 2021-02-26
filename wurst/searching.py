from .errors import MultipleResults, NoResults


def equals(field, value):
    """Return function where input ``field`` value is equal to ``value``"""
    return lambda x: x.get(field) == value


def contains(field, value):
    return lambda x: value in x.get(field)


def startswith(field, value):
    return lambda x: x.get(field, "").startswith(value)


def either(*funcs):
    """Return ``True`` is any of the function evaluate true"""
    return lambda x: any(f(x) for f in funcs)


def exclude(func):
    """Return the opposite of ``func`` (i.e. ``False`` instead of ``True``)"""
    return lambda x: not func(x)


def doesnt_contain_any(field, values):
    """Exclude all dataset whose ``field`` contains any of ``values``"""
    return lambda x: all(exclude(contains(field, value))(x) for value in values)


def get_many(data, *funcs):
    """Apply all filter functions ``funcs`` to ``data``"""
    for fltr in funcs:
        data = filter(fltr, data)
    return data


def get_one(data, *funcs):
    """Apply filter functions ``funcs`` to ``data``, and return exactly one result.

    Raises ``wurst.errors.NoResults`` or ``wurst.errors.MultipleResults`` if zero or multiple results are returned.
    """
    results = list(get_many(data, *funcs))
    if not results:
        raise NoResults
    if not len(results) == 1:
        raise MultipleResults
    return results[0]


def _exchanges(ds, kind, *funcs):
    if funcs == [None]:
        funcs = []
    return get_many(filter(lambda x: x["type"] == kind, ds["exchanges"]), *funcs)


def technosphere(ds, *funcs):
    """Get all technosphere exchanges in ``ds`` that pass filtering functions ``funcs``"""
    return _exchanges(ds, "technosphere", *funcs)


def biosphere(ds, *funcs):
    """Get all biosphere exchanges in ``ds`` that pass filtering functions ``funcs``"""
    return _exchanges(ds, "biosphere", *funcs)


def production(ds, *funcs):
    """Get all production exchanges in ``ds`` that pass filtering functions ``funcs``"""
    return _exchanges(ds, "production", *funcs)


def reference_product(ds):
    """Get single reference product exchange from a dataset.

    Raises ``wurst.errors.NoResults`` or ``wurst.errors.MultipleResults`` if zero or multiple results are returned."""
    excs = [
        exc for exc in ds["exchanges"] if exc["amount"] and exc["type"] == "production"
    ]
    if not excs:
        raise NoResults("No suitable production exchanges found")
    elif len(excs) > 1:
        raise MultipleResults("Multiple production exchanges found")
    return excs[0]


def best_geo_match(possibles, ordered_locations):
    """Pick the dataset from ``possibles`` whose location is first in ``ordered_locations``.

    ``possibles`` is an interable with the field ``location``.

    ``ordered_locations`` is a list of locations in sorting order.

    Returns an element from ``possibles``, or ``None``.
    """
    weights = {y: x for x, y in enumerate(ordered_locations)}
    filtered = (obj for obj in possibles if obj["location"] in weights)
    ordered = sorted(filtered, key=lambda x: weights[x["location"]])
    if ordered:
        return ordered[0]
