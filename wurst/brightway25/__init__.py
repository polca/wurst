"""Export inventories compatible with the dev release of Brightway 2.5. The functions in ``brightway/extract_database.py`` will work without modification."""
from ..linking import check_duplicate_codes, check_internal_linking, link_internal
from bw2data.backends import ActivityDataset
from bw2io.importers.base_lci import LCIImporter
from copy import copy
from fs.zipfs import ZipFS
import bw2data as bd
import bw_processing as bwp
import datetime


class DeltaImporter(LCIImporter):
    def __init__(self, db_name, data):
        self.db_name = db_name
        self.data = data

    def write_database(self):
        super().write_database(process=False)


def strip_exchanges(ds):
    o = copy(ds)
    o["exchanges"] = []
    return o


PRODUCTION = ("production", "substitution", "generic production")


def write_brightway25_database(data, name):
    """Write a new database compatible with Brightway 2.5 functionality.

    Instead of aggregating everything into a new database, we take a new approach. New activities are stored as a new database (``name``), but for exchanges that are modified, we use the 2.5 functionality to write processed arrays which override values in the original database. In other words, the previous approach was to write as much as possible; here we write as little as possible. The end calculation results are the same either way.

    * New or modified data (both entire activities, and individual exchanges) must be marked with ``"modified"=True``.
    * Exchange data won't be accessible in the database, and hence also missing in programs like the activity browser. You can still use ``write_brightway2_database`` to get a complete database.

    You should be in the correct project already.

    In contrast with the ``write_brightway2_array_database`` function, this function preserves links to the original datasets. New activities are only written if they were added during the Wurst run. We use the functionality added in Brightway 2.5 to dynamically modify the original data on-demand.

    Inputs:

    * ``data``: list. Datasets in the standard Wurst format
    * ``name``: str. Name of the new database. Will raise an ``AssertionError`` is ``name`` already exists.

    Returns:

        ``None``

    This function will also do the following:

    * Change the database name for new activities to ``name``.
    * Relink exchanges using the default fields: ``('name', 'product', 'location', 'unit')``.
    * Check that all internal links resolve to actual activities, If the ``input`` value is ``('name', 'bar')``, there must be an activity with the code ``bar``.
    * Check to make sure that all activity codes in the new activities are unique

    """
    assert name not in bd.databases, "This database already exists"

    new_activities = [x for x in data if x.get("modified")]

    for ds in new_activities:
        ds["database"] = name
        if "parameters" in ds:
            ds["parameters"] = {
                name: {"amount": amount} for name, amount in ds["parameters"].items()
            }

    # Links to external databases (i.e. those not imported in their entirety)
    # are maintained; the exchanges have ``input`` keys. This will link
    # the exchanges against activities in ``data``.
    link_internal(data)

    check_internal_linking(data)
    check_duplicate_codes(new_activities)

    new_activities = [strip_exchanges(x) for x in data if x.get("modified")]
    DeltaImporter(name, new_activities).write_database()

    # Exchanges in new activities don't have to have database yet
    dependents = (
        {obj.get("database") for obj in data}
        .union({exc["database"] for ds in data for exc in ds.get("exchanges", [])})
        .difference({None})
    )

    id_mapping = {
        (t[0], t[1]): t[2]
        for t in ActivityDataset.select(
            ActivityDataset.database, ActivityDataset.code, ActivityDataset.id
        )
        .where(ActivityDataset.database << dependents)
        .tuples()
    }

    # Construct processed array manually
    tech_exchanges = []
    bio_exchanges = []
    for ds in data:
        for exc in ds["exchanges"]:
            if ds.get("modified") or exc.get("modified"):
                if exc["type"] == "biosphere":
                    print(
                        "Bio exchange:",
                        {
                            "row": exc["input"],
                            "col": (ds["database"], ds["code"]),
                            "amount": exc["amount"],
                        },
                    )
                    bio_exchanges.append(
                        {
                            "row": id_mapping[exc["input"]],
                            "col": id_mapping[(ds["database"], ds["code"])],
                            "amount": exc["amount"],
                            "flip": False,
                        }
                    )
                else:
                    print(
                        "Tech exchange:",
                        {
                            "row": exc["input"],
                            "col": (ds["database"], ds["code"]),
                            "amount": exc["amount"],
                        },
                    )
                    flip = exc["type"] not in PRODUCTION
                    tech_exchanges.append(
                        {
                            "row": id_mapping[exc["input"]],
                            "col": id_mapping[(ds["database"], ds["code"])],
                            "amount": exc["amount"],
                            "flip": flip,
                        }
                    )

        # We currently assume that all activities have a production exchange
        # if add_implicit_production and ds.get("modified"):
        #     if not any(
        #         exc.get("type") in PRODUCTION for exc in ds.get("exchanges", [])
        #     ):
        #         tech_exchanges.append(
        #             {
        #                 "row": id_mapping[(ds["database"], ds["code"])],
        #                 "col": id_mapping[(ds["database"], ds["code"])],
        #                 "amount": 1,
        #                 "flip": False,
        #             }
        #         )

    process_delta_database(name, tech_exchanges, bio_exchanges, dependents)


def process_delta_database(name, tech, bio, dependents):
    """A modification of ``bw2data.backends.base.SQLiteBackend.process`` to skip retrieving data from the database."""
    print("Tech:", tech)
    print("Bio:", bio)

    db = bd.Database(name)
    db.metadata["processed"] = datetime.datetime.now().isoformat()

    # Create geomapping array, from dataset interger ids to locations
    inv_mapping_qs = ActivityDataset.select(
        ActivityDataset.id, ActivityDataset.location
    ).where(ActivityDataset.database == name, ActivityDataset.type == "process")

    # self.filepath_processed checks if data is dirty,
    # and processes if it is. This causes an infinite loop.
    # So we construct the filepath ourselves.
    fp = str(db.dirpath_processed() / db.filename_processed())

    dp = bwp.create_datapackage(
        fs=ZipFS(fp, write=True),
        name=bwp.clean_datapackage_name(name),
        sum_intra_duplicates=True,
        sum_inter_duplicates=False,
    )
    dp.add_persistent_vector_from_iterator(
        matrix="inv_geomapping_matrix",
        name=bwp.clean_datapackage_name(name + " inventory geomapping matrix"),
        dict_iterator=(
            {
                "row": row[0],
                "col": bd.geomapping[
                    bd.backends.utils.retupleize_geo_strings(row[1])
                    or bd.config.global_location
                ],
                "amount": 1,
            }
            for row in inv_mapping_qs.tuples()
        ),
        nrows=inv_mapping_qs.count(),
    )

    dp.add_persistent_vector_from_iterator(
        matrix="biosphere_matrix",
        name=bwp.clean_datapackage_name(name + " biosphere matrix"),
        dict_iterator=bio,
    )
    dp.add_persistent_vector_from_iterator(
        matrix="technosphere_matrix",
        name=bwp.clean_datapackage_name(name + " technosphere matrix"),
        dict_iterator=tech,
    )
    dp.finalize_serialization()

    db.metadata["depends"] = sorted(dependents.difference({name}))
    db.metadata["dirty"] = False
    db._metadata.flush()
