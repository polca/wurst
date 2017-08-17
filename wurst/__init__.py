__version__ = (0, 1, "dev")


from .brightway import extract_brightway2_databases, write_brightway2_database
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
from .ecoinvent import ECOINVENT_ORDERED_GEO
from .transformations import (
    change_exchanges_by_constant_factor,
    delete_zero_amount_exchanges,
    rescale_exchange,
)


import logging
logger = logging.getLogger('wurst')

def log(message, ds):
    FIELDS = ('database', 'code', 'name', 'reference product',
              'unit', 'location')
    message.update({key: ds.get(key) for key in FIELDS})
    logger.info(message)
