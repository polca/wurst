from bw2io.base_lci import LCIImporter
from bw2data import databases


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
    WurstImporter(data, name).write_database()
