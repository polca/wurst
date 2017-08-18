from .. import log
from ..ecoinvent import ecoinvent_faces
from ..IMAGE.metadata import IMAGE_REGION_FACES
from ..searching import reference_product
from .uncertainty import rescale_exchange
from .utils import copy_dataset
from copy import deepcopy


def copy_to_new_location(ds, location):
    """Copy dataset and substitute new ``location``.

    Doesn't change exchange locations, except for production exchanges.

    Returns the new dataset."""
    MESSAGE = "Copied activity from '{old}' location to '{new}'."
    log({
        'function': 'copy_to_new_location',
        'message': MESSAGE.format(old=ds['location'], new=location)
    }, ds)

    cp = copy_dataset(ds)
    cp['location'] = location
    for exc in cp['exchanges']:
        if exc['type'] == 'production':
            exc['location'] = location

    return cp


def relink_technosphere_exchanges(ds, data, include_row_cutoff=3):
    """Find new exchange(s) based on the location of the dataset.

    Designed to be used when the dataset's location changes.

    Uses the name, reference product, and unit of the exchange to filter possible inputs. These must match exactly. Searches in the list of datasets ``data``.

    This function will search for the input with the largest area which lies within the dataset location; it will then iteratively add additional inputs if they are contained in the remaining area (i.e. the dataset location minus the area of the largest input).

    Input choice algorithm logic:

    * If only a global (``GLO``) or Rest-of-World (``RoW``) input is available, use this input.
    * Otherwise, sort available inputs by their size, from largest to smallest. ``GLO`` and ``RoW`` are at the end of this list.
    * Iteratively take inputs, removing their areas from the remaining available area. Each subsequent input must fit completely inside the available area.
    * Only include ``GLO`` or ``RoW`` inputs if the number of region-specific inputs is less than ``include_row_cutoff`` (default is 3).
    * Allocate inputs using normalized production volumes, if a) all inputs have positive production volumes, and b) ``RoW`` or ``GLO`` are not in the list of inputs. Otherwise, use equal allocation among inputs.

    Modifies the dataset in place; returns the modified dataset."""
    faces = get_faces(ds['location'])
    inside = lambda x: not get_faces(x['location']).difference(faces)
    drop_row_global = lambda lst: [o for o in lst if o['location'] not in ('RoW', 'GLO')]
    MESSAGE = "Relinked technosphere exchange of {}/{}/{} from {}/{} to {}/{}."
    new_exchanges = []
    technosphere = lambda x: x['type'] == 'technosphere'

    for exc in filter(technosphere, ds['exchanges']):
        possibles = sorted(
            [obj for obj in get_possibles(exc, data) if inside(obj)],
            key=len(get_faces(obj['location'])),
            reverse=True
        )

        usable = iteratively_choose_inputs(possibles, faces.copy())
        if len(usable) >= include_row_cutoff:
            usable = drop_row_global(usable)
        allocated = allocate_inputs(exc, usable)

        for obj in allocated:
            log({
                'function': 'relink_technosphere_exchanges',
                'message': MESSAGE.format(
                    exc['name'], exc['product'], exc['unit'], exc['amount'],
                    ds['location'], obj['amount'], obj['location']
                )
            }, ds)

        new_exchanges.extend(allocated)

    ds['exchanges'] = [
        exc for exc in ds['exchanges']
        if exc['type'] != 'technosphere'
    ] + new_exchanges
    return ds


def allocate_inputs(exc, lst):
    """Allocate the input exchanges in ``lst`` to ``exc``, using production volumes where possible, and equal splitting otherwise."""
    has_row = any((x['location'] in ('RoW', 'GLO') for x in lst))
    pvs = [reference_product(o).get('production volume') or 0 for o in lst]
    if all((x > 0 for x in pvs)) and not has_row:
        # Allocate using production volume
        total = sum(pvs)
    else:
        # Allocate evenly
        total = len(lst)
        pvs = [1 for _ in range(total)]

    def new_exchange(exc, location, factor):
        cp = deepcopy(exc)
        cp['location'] = location
        return rescale_exchange(cp, factor)

    return [
        new_exchange(exc, obj['location'], factor / total)
        for obj, factor in zip(lst, pvs)
    ]


def iteratively_choose_inputs(lst, remaining_faces):
    """Return a list of inputs which are inside ``remaining_faces`` but don't overlap."""
    new = []
    while lst:
        possible = lst.pop(0)
        if not get_faces(possible['location']).difference(remaining_faces):
            new.append(deepcopy(possible))
            remaining_faces = remaining_faces.difference(get_faces(possible['location']))
            if not remaining_faces:
                # Don't include RoW, etc. if nothing is left
                break
    return new


def get_possibles(exchange, data):
    """FIlter a list of datasets ``data``, returning those with the save name, reference product, and unit as in ``exchange``.

    Returns a generator."""
    key = (exchange['name'], exchange['product'], exchange['unit'])
    for ds in data:
        if (ds['name'], ds['reference product'], ds['unit']) == key:
            yield ds


def get_faces(location):
    """Return a set of integers identifying the topological faces defining ``location``.

    Works with both ecoinvent and IMAGE locations."""
    if location in ('RoW', 'GLO'):
        return set()
    elif location in ecoinvent_faces:
        return ecoinvent_faces[location]
    elif location in IMAGE_REGION_FACES:
        return IMAGE_REGION_FACES[location]
    else:
        raise KeyError("Can't find location {} in ecoinvent or IMAGE".format(location))
