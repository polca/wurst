from .errors import MultipleResults, NoResults


def equals(field, value):
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
    results = list(get_many(data, funcs))
    if not len(results) == 1:
        raise MultipleResults
    return results[0]
