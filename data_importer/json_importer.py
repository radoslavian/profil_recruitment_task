import json

from data_importer.data_importer import DataImporter


class JsonImporter(DataImporter):
    def import_from_file(self, file):
        return json.load(file)
