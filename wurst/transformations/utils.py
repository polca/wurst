from copy import deepcopy
from ..filesystem import get_uuid


def copy_dataset(ds):
    """Copy dataset and generate new codes."""
    cp = deepcopy(ds)
    cp["code"] = get_uuid()
    return cp
