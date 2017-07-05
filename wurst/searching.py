from .errors import MultipleResults, NoResults


def equals(field, value):
    """Return function where input ``field`` value is equal to ``value``"""
    return lambda x: x[field] == value


def contains(field, value):
    return lambda x: value in x[field]


def startswith(field, value):
    return lambda x: x[field].startswith(value)


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
    return get_many(
        filter(lambda x: x['type'] == kind, ds['exchanges']),
        *funcs
    )


def technosphere(ds, *funcs):
    """Get all technosphere exchanges in ``ds`` that pass filtering functions ``funcs``"""
    return _exchanges(ds, 'technosphere', *funcs)


def biosphere(ds, *funcs):
    """Get all biosphere exchanges in ``ds`` that pass filtering functions ``funcs``"""
    return _exchanges(ds, 'biosphere', *funcs)
