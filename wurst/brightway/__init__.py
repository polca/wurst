try:
    from .extract_database import extract_brightway2_databases
    from .write_database import write_brightway2_database
except ImportError:
    print("Brightway2 not present")
    extract_brightway2_database = write_brightway2_database = None
