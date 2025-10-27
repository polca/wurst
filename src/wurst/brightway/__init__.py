try:
    from .extract_database import extract_brightway2_databases
    from .write_database import (
        write_brightway2_database,
        write_brightway2_array_database,
    )
except ImportError:
    print("Brightway2 not present")
    extract_brightway2_databases = (
        write_brightway2_database
    ) = write_brightway2_array_database = None
