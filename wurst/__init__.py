__all__ = (
    "best_geo_match",
    "biosphere",
    "change_exchanges_by_constant_factor",
    "contains",
    "copy_to_new_location",
    "create_dir",
    "create_log",
    "default_global_location",
    "delete_zero_amount_exchanges",
    "doesnt_contain_any",
    "either",
    "empty_market_dataset",
    "equals",
    "extract_brightway2_databases",
    "geomatcher",
    "get_many",
    "get_one",
    "log",
    "production",
    "reference_product",
    "relink_technosphere_exchanges",
    "rescale_exchange",
    "resolved_row",
    "startswith",
    "technosphere",
    "toolz",
    "write_brightway2_database",
)


import logging

logger = logging.getLogger("wurst")


def log(message, ds):
    FIELDS = ("database", "code", "name", "reference product", "unit", "location")
    message.update({key: ds.get(key) for key in FIELDS})
    logger.info(message)


try:
    import cytoolz as toolz
except ImportError:
    import toolz

from .version import version as __version__

try:
    from .brightway import extract_brightway2_databases, write_brightway2_database
except ImportError:
    extract_brightway2_databases = write_brightway2_database = None
from .filesystem import create_log, create_dir
from .searching import (
    best_geo_match,
    biosphere,
    contains,
    doesnt_contain_any,
    either,
    equals,
    get_many,
    get_one,
    production,
    reference_product,
    startswith,
    technosphere,
)
from .transformations import (
    change_exchanges_by_constant_factor,
    copy_to_new_location,
    default_global_location,
    delete_zero_amount_exchanges,
    empty_market_dataset,
    relink_technosphere_exchanges,
    rescale_exchange,
)
from .geo import geomatcher
from constructive_geometries import resolved_row
