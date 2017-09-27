def delete_zero_amount_exchanges(data, drop_types=None):
    """Drop all zero value exchanges from a list of datasets.

    ``drop_types`` is an optional list of strings, giving the type of exchanges to drop; default is to drop all types.

    Returns the modified data."""
    if drop_types:
        dont_delete = lambda x: x['type'] not in drop_types or x['amount']
    else:
        dont_delete = lambda x: x['amount']
    for ds in data:
        ds['exchanges'] = list(filter(dont_delete, ds['exchanges']))
    return data


def empty_market_dataset(ds, exclude=None):
    """Remove input exchanges from a market dataset, in preparation for input exchanges defined by an external data source.

    Removes all exchanges which have the same flow as the reference product of the exchange. ``exclude`` is an iterable of activity names to exclude."""
    ds['exchanges'] = [
        exc
        for exc in ds['exchanges']
        if exc['type'] != 'technosphere'
        or exc['product'] != ds['reference product']
        or exc['name'] in (exclude or [])
    ]
    return ds
