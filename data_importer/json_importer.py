import json

from data_importer.data_importer import DataImporter


class JsonImporter(DataImporter):
    def convert_data(self):
        self.converted_data = json.loads(self.filedata)
