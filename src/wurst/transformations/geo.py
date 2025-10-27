from .. import log
from ..errors import InvalidLink
from ..geo import geomatcher
from ..searching import reference_product, get_many, equals, get_one
from .uncertainty import rescale_exchange
from .utils import copy_dataset
from constructive_geometries import resolved_row
from copy import deepcopy


def copy_to_new_location(ds, location):
    """Copy dataset and substitute new ``location``.

    Doesn't change exchange locations, except for production exchanges.

    Returns the new dataset."""
    MESSAGE = "Copied activity from '{old}' location to '{new}'."
    log(
        {
            "function": "copy_to_new_location",
            "message": MESSAGE.format(old=ds["location"], new=location),
        },
        ds,
    )

    cp = copy_dataset(ds)
    cp["location"] = location
    for exc in cp["exchanges"]:
        if exc["type"] == "production":
            exc["location"] = location

    return cp


def relink_technosphere_exchanges(
    ds, data, exclusive=True, drop_invalid=False, biggest_first=False, contained=True
):
    """Find new technosphere providers based on the location of the dataset.

    Designed to be used when the dataset's location changes, or when new datasets are added.

    Uses the name, reference product, and unit of the exchange to filter possible inputs. These must match exactly. Searches in the list of datasets ``data``.

    Will only search for providers contained within the location of ``ds``, unless ``contained`` is set to ``False``, all providers whose location intersects the location of ``ds`` will be used.

    A ``RoW`` provider will be added if there is a single topological face in the location of ``ds`` which isn't covered by the location of any providing activity.

    If no providers can be found, `relink_technosphere_exchanes` will try to add a `RoW` or `GLO` providers, in that order, if available. If there are still no valid providers, a ``InvalidLink`` exception is raised, unless ``drop_invalid`` is ``True``, in which case the exchange will be deleted.

    Allocation between providers is done using ``allocate_inputs``; results seem strange if ``contained=False``, as production volumes for large regions would be used as allocation factors.

    Input arguments:

        * ``ds``: The dataset whose technosphere exchanges will be modified.
        * ``data``: The list of datasets to search for technosphere product providers.
        * ``exclusive``: Bool, default is ``True``. Don't allow overlapping locations in input providers.
        * ``drop_invalid``: Bool, default is ``False``. Delete exchanges for which no valid provider is available.
        * ``biggest_first``: Bool, default is ``False``. Determines search order when selecting provider locations. Only relevant is ``exclusive`` is ``True``.
        * ``contained``: Bool, default is ``True``. If ture, only use providers whose location is completely within the ``ds`` location; otherwise use all intersecting locations.

    Modifies the dataset in place; returns the modified dataset."""
    MESSAGE = "Relinked technosphere exchange of {}/{}/{} from {}/{} to {}/{}."
    DROPPED = "Dropped technosphere exchange of {}/{}/{}; no valid providers."
    new_exchanges = []
    technosphere = lambda x: x["type"] == "technosphere"

    for exc in filter(technosphere, ds["exchanges"]):
        possible_datasets = list(get_possibles(exc, data))
        possible_locations = [obj["location"] for obj in possible_datasets]
        with resolved_row(possible_locations, geomatcher) as g:
            func = g.contained if contained else g.intersects
            gis_match = func(
                ds["location"],
                include_self=True,
                exclusive=exclusive,
                biggest_first=biggest_first,
                only=possible_locations,
            )

        kept = [
            ds for loc in gis_match for ds in possible_datasets if ds["location"] == loc
        ]

        if kept:
            missing_faces = geomatcher[ds["location"]].difference(
                set.union(*[geomatcher[obj["location"]] for obj in kept])
            )
            if missing_faces and "RoW" in possible_locations:
                kept.extend(
                    [obj for obj in possible_datasets if obj["location"] == "RoW"]
                )
        elif "RoW" in possible_locations:
            kept = [obj for obj in possible_datasets if obj["location"] == "RoW"]

        if not kept and "GLO" in possible_locations:
            kept = [obj for obj in possible_datasets if obj["location"] == "GLO"]

        if not kept:
            if drop_invalid:
                log(
                    {
                        "function": "relink_technosphere_exchanges",
                        "message": DROPPED.format(
                            exc["name"], exc["product"], exc["unit"]
                        ),
                    },
                    ds,
                )
                continue
            else:
                raise InvalidLink

        allocated = allocate_inputs(exc, kept)

        for obj in allocated:
            log(
                {
                    "function": "relink_technosphere_exchanges",
                    "message": MESSAGE.format(
                        exc["name"],
                        exc["product"],
                        exc["unit"],
                        exc["amount"],
                        ds["location"],
                        obj["amount"],
                        obj["location"],
                    ),
                },
                ds,
            )

        new_exchanges.extend(allocated)

    ds["exchanges"] = [
        exc for exc in ds["exchanges"] if exc["type"] != "technosphere"
    ] + new_exchanges
    return ds


def allocate_inputs(exc, lst):
    """Allocate the input exchanges in ``lst`` to ``exc``, using production volumes where possible, and equal splitting otherwise.

    Always uses equal splitting if ``RoW`` is present."""
    has_row = any((x["location"] in ("RoW", "GLO") for x in lst))
    pvs = [reference_product(o).get("production volume") or 0 for o in lst]
    if all((x > 0 for x in pvs)) and not has_row:
        # Allocate using production volume
        total = sum(pvs)
    else:
        # Allocate evenly
        total = len(lst)
        pvs = [1 for _ in range(total)]

    def new_exchange(exc, location, factor):
        cp = deepcopy(exc)
        cp["location"] = location
        return rescale_exchange(cp, factor)

    return [
        new_exchange(exc, obj["location"], factor / total)
        for obj, factor in zip(lst, pvs)
    ]


def get_possibles(exchange, data):
    """FIlter a list of datasets ``data``, returning those with the save name, reference product, and unit as in ``exchange``.

    Returns a generator."""
    key = (exchange["name"], exchange["product"], exchange["unit"])
    for ds in data:
        if (ds["name"], ds["reference product"], ds["unit"]) == key:
            yield ds


def default_global_location(database):
    """Set missing locations to ```GLO``` for datasets in ``database``.

    Changes location if ``location`` is missing or ``None``. Will add key ``location`` if missing."""
    for ds in get_many(database, *[equals("location", None)]):
        ds["location"] = "GLO"
    return database
