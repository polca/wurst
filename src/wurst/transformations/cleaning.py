def delete_zero_amount_exchanges(data, drop_types=None):
    """Drop all zero value exchanges from a list of datasets.

    ``drop_types`` is an optional list of strings, giving the type of exchanges to drop; default is to drop all types.

    Returns the modified data."""
    if drop_types:
        dont_delete = lambda x: x["type"] not in drop_types or x["amount"]
    else:
        dont_delete = lambda x: x["amount"]
    for ds in data:
        ds["exchanges"] = list(filter(dont_delete, ds["exchanges"]))
    return data


def empty_market_dataset(ds, exclude=None):
    """Remove input exchanges from a market dataset, in preparation for input exchanges defined by an external data source.

    Removes all exchanges which have the same flow as the reference product of the exchange. ``exclude`` is an iterable of activity names to exclude."""
    ds["exchanges"] = [
        exc
        for exc in ds["exchanges"]
        if exc["type"] != "technosphere"
        or exc["product"] != ds["reference product"]
        or exc["name"] in (exclude or [])
    ]
    return ds


def add_metadata_to_production_exchanges(
    data, fields=("location", "unit"), matching_fields=("name", "unit", "location")
):
    """Add metadata to exchanges based on linked activities"""
    get_key = lambda x: tuple([x.get(f) for f in matching_fields])
    mapping = {get_key(ds): ds for ds in data}

    for ds in data:
        for exc in ds["exchanges"]:
            if all([field in exc for field in fields]):
                continue
            try:
                if exc.get("type") == "production":
                    partner = ds
                else:
                    partner = mapping[get_key(exc)]
            except KeyError:
                continue
            for field in fields:
                if field not in exc and field in partner:
                    exc[field] = partner[field]
    return data


def remove_exchange_fields_with_nones(data):
    """Remove all keys from exchanges if their value is ``None``"""
    clean = lambda dct: {k: v for k, v in dct.items() if v is not None}
    for ds in data:
        ds["exchanges"] = [clean(exc) for exc in ds["exchanges"]]
    return data
