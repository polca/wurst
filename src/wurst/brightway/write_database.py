from ..linking import (
    change_db_name,
    check_duplicate_codes,
    check_internal_linking,
    link_internal,
)
from bw2data import databases, Database
from bw2io.importers.base_lci import LCIImporter


class WurstImporter(LCIImporter):
    def __init__(self, db_name, data):
        self.db_name = db_name
        self.data = data
        for act in self.data:
            act["database"] = self.db_name

    def write_database(self):
        assert not self.statistics()[2], "Not all exchanges are linked"
        assert self.db_name not in databases, "This database already exists"
        super().write_database()


def write_brightway2_database(data, name):
    """Write a new database as a new Brightway2 database named ``name``.

    You should be in the correct project already.

    This function will do the following:

    * Change the database name for all activities and internal exchanges to ``name``. All activities will have the new database ``name``, even if the original data came from multiple databases.
    * Relink exchanges using the default fields: ``('name', 'product', 'location', 'unit')``.
    * Check that all internal links resolve to actual activities, If the ``input`` value is ``('name', 'bar')``, there must be an activity with the code ``bar``.
    * Check to make sure that all activity codes are unique
    * Write the data to a new Brightway2 SQLite database

    Will raise an assertion error is ``name`` already exists.

    Doesn't return anything."""
    assert name not in databases, "This database already exists"

    # Restore parameters to Brightway2 format which allows for uncertainty and comments
    for ds in data:
        if "parameters" in ds:
            ds["parameters"] = {
                name: {"amount": amount} for name, amount in ds["parameters"].items()
            }

    change_db_name(data, name)
    link_internal(data)
    check_internal_linking(data)
    check_duplicate_codes(data)
    WurstImporter(name, data).write_database()


def write_brightway2_array_database(data, name):
    """Write a new database using the ``IOTable`` backend that saves exchange values only as processed arrays.

    You should be in the correct project already.

    This function will do the following:

    * Change the database name for all activities and internal exchanges to ``name``. All activities will have the new database ``name``, even if the original data came from multiple databases.
    * Relink exchanges using the default fields: ``('name', 'product', 'location', 'unit')``.
    * Check that all internal links resolve to actual activities, If the ``input`` value is ``('name', 'bar')``, there must be an activity with the code ``bar``.
    * Check to make sure that all activity codes are unique
    * Write the data to a new Brightway2 IOTable

    Will raise an assertion error is ``name`` already exists.

    Doesn't return anything."""
    assert name not in databases, "This database already exists"

    # Restore parameters to Brightway2 format which allows for uncertainty and comments
    for ds in data:
        if "parameters" in ds:
            ds["parameters"] = {
                name: {"amount": amount} for name, amount in ds["parameters"].items()
            }

    change_db_name(data, name)
    link_internal(data)
    check_internal_linking(data)
    check_duplicate_codes(data)

    exchanges = []

    for ds in data:
        ds["key"] = (name, ds["code"])
        for exc in ds["exchanges"]:
            exc["output"] = ds["key"]
            exchanges.append(exc)
        ds["exchanges"] = []

    Database(name, "iotable").write(
        {ds["key"]: ds for ds in data}, exchanges, includes_production=True
    )
