from wurst import logger

try:
    from .extract_database import extract_brightway2_databases
    from .write_database import (
        write_brightway2_array_database,
        write_brightway2_database,
    )
except ImportError:
    logger.warning("Brightway not installed; Brightway IO functionality disabled")
    extract_brightway2_databases = (
        write_brightway2_database
    ) = write_brightway2_array_database = None
