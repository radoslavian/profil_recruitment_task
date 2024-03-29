import re
import csv

from data_importer.data_importer import DataImporter


class CSVImporter(DataImporter):
    child_regex = "(\w+)\s\((\d{1,2})\)"

    def _read_children(self, children):
        if not children:
            return []
        individual_children = children.split(",")
        children_output = []
        for child in individual_children:
            _child = self._parse_child(child)
            children_output.append(_child)
        return children_output

    def _parse_child(self, child):
        child_data = dict()
        child_match = re.match(self.child_regex, child)
        child_data["name"] = child_match.group(1)
        child_data["age"] = int(child_match.group(2))
        return child_data

    def _read_rows(self, reader):
        rows = []
        children_fieldnames = ("name", "age")
        for row in reader:
            children = self._read_children(row["children"])
            rows.append({**row, "children": children})
        return rows

    def import_from_file(self, file):
        reader = csv.DictReader(file, delimiter=";")
        return self._read_rows(reader)
