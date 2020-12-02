from .errors import InvalidLink, NonuniqueCode
from .searching import reference_product
from pprint import pformat


get_input_databases = lambda data: {ds["database"] for ds in data}


def link_internal(data, fields=("name", "product", "location", "unit")):
    """Link internal exchanges by ``fields``. Creates ``input`` field in newly-linked exchanges."""
    input_databases = get_input_databases(data)
    get_tuple = lambda exc: tuple([exc[f] for f in fields])
    products = {
        get_tuple(reference_product(ds)): (ds["database"], ds["code"]) for ds in data
    }

    for ds in data:
        for exc in ds["exchanges"]:
            if exc.get("input"):
                continue

            if exc["type"] == "biosphere":
                raise ValueError(
                    "Unlinked biosphere exchange:\n{}".format(pformat(exc))
                )

            try:
                exc["input"] = products[get_tuple(exc)]
            except KeyError:
                raise KeyError(
                    "Can't find linking activity for exchange:\n{}".format(pformat(exc))
                )
    return data


def check_internal_linking(data):
    """Check that each internal link is to an actual activity"""
    names = get_input_databases(data)
    keys = {(ds["database"], ds["code"]) for ds in data}
    for ds in data:
        for exc in ds["exchanges"]:
            if exc.get("input") and exc["input"][0] in names:
                if exc["input"] not in keys:
                    raise InvalidLink(
                        "Exchange links to non-existent activity:\n{}".format(
                            pformat(exc)
                        )
                    )


def change_db_name(data, name):
    """Change the database of all datasets in ``data`` to ``name``.

    Raises errors if each dataset does not have exactly one reference production exchange."""
    old_names = get_input_databases(data)
    for ds in data:
        ds["database"] = name
        for exc in ds["exchanges"]:
            if exc.get("input") and exc["input"][0] in old_names:
                exc["input"] = (name, exc["input"][1])
    return data


def check_duplicate_codes(data):
    """Check that there won't be duplicate codes when activities are merged to new, common database"""
    seen = set()
    for ds in data:
        if ds["code"] in seen:
            raise NonuniqueCode("Code {} seen at least twice".format(ds["code"]))
        seen.add(ds["code"])
