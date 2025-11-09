from typing import List, Optional

from bw2data import Database, ProcessedDataStore, databases, labels
from bw2io.importers.base_lci import LCIImporter

from wurst import logger
from wurst.linking import (
    change_db_name,
    check_duplicate_codes,
    check_internal_linking,
    link_internal,
)


class WurstImporter(LCIImporter):
    def __init__(self, db_name, data):
        self.db_name = db_name
        self.data = data
        for act in self.data:
            act["database"] = self.db_name

    def write_database(self, metadata: Optional[dict] = None) -> ProcessedDataStore:
        if metadata is None:
            metadata = {}

        self.metadata.update(metadata or {})

        assert not self.statistics()[2], "Not all exchanges are linked"
        assert self.db_name not in databases, "This database already exists"
        super().write_database()
        return Database(self.db_name)


def link_internal_products_processes(
    data: list[dict],
    biosphere_fields: list[str] = ["name", "unit", "categories"],
    technosphere_fields: list[str] = ["name", "unit", "location"],
) -> int:
    """Do internal linking for both technosphere and biosphere edges"""
    count = 0

    products = [ds for ds in data if ds["type"] in labels.product_node_types]
    flows = [
        ds
        for ds in data
        if ds["type"]
        in [labels.biosphere_node_default, "natural resource", "resource", "social"]
    ]
    processes = [ds for ds in data if ds["type"] in labels.process_node_types]

    product_mapping = {
        tuple([ds.get(field) for field in technosphere_fields]): (
            ds["database"],
            ds["code"],
        )
        for ds in products
    }
    flow_mapping = {
        tuple([ds.get(field) for field in biosphere_fields]): (
            ds["database"],
            ds["code"],
        )
        for ds in flows
    }

    technosphere_labels = (
        labels.technosphere_negative_edge_types
        + labels.technosphere_positive_edge_types
    )

    for ds in processes:
        for edge in ds["exchanges"]:
            if edge.get("input"):
                continue
            elif edge["type"] in labels.biosphere_edge_types:
                if (
                    key := tuple([edge.get(field) for field in biosphere_fields])
                ) in flow_mapping:
                    edge["input"] = flow_mapping[key]
                    count += 1
            elif edge["type"] in technosphere_labels:
                if (
                    key := tuple([edge.get(field) for field in technosphere_fields])
                ) in product_mapping:
                    edge["input"] = product_mapping[key]
                    count += 1

    missing = sum(
        [
            1
            for ds in processes
            for edge in ds.get("exchanges", [])
            if not edge.get("input")
        ]
    )

    logger.info(
        f"link_internal_products_processes added {count} edges; {missing} edges still unlinked"
    )
    return count


def write_brightway2_database(
    data: List[dict],
    name: str,
    metadata: Optional[dict] = None,
    products_and_processes: bool = False,
) -> None:
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
    if products_and_processes:
        link_internal_products_processes(data)
    else:
        link_internal(data)
    check_internal_linking(data)
    check_duplicate_codes(data)
    WurstImporter(name, data).write_database(metadata)


def write_brightway2_array_database(data: List[dict], name: str) -> None:
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
