from ..linking import link_internal, change_db_name, check_internal_linking
from bw2data import databases
from bw2io.importers.base_lci import LCIImporter


class WurstImporter(LCIImporter):
    def __init__(self, db_name, data):
        self.db_name = db_name
        self.data = data
        for act in self.data:
            act['database'] = self.db_name

    def write_database(self):
        assert not self.statistics[2], "Not all exchanges are linked"
        assert self.db_name not in databases, "This database already exists"
        super(WurstImporter).write_database()


def write_brightway2_database(data, name):
    data = change_db_name(data, name)
    data = link_internal(data)
    data = check_internal_linking(data)
    WurstImporter(data, name).write_database()
