from .errors import MultipleResults, NoResults


def equals(field, value):
    """Return function where input ``field`` value is equal to ``value``"""
    return lambda x: x[field] == value


def contains(field, value):
    return lambda x: value in x[field]


def startswith(field, value):
    return lambda x: x[field].startswith(value)


def get_many(data, funcs):
    for fltr in funcs:
        data = filter(fltr, data)
    return data


def get_one(data, funcs):
    """Apply filter functions ``funcs`` to ``data``, and return exactly one result.

    Raises ``wurst.errors.NoResults`` or ``wurst.errors.MultipleResults`` if zero or multiple results are returned.
    """
    results = list(get_many(data, funcs))
    if not results:
        raise NoResults
    if not len(results) == 1:
        raise MultipleResults
    return results[0]
