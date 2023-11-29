from data_importer.data_importer import DataImporter
import xml.etree.ElementTree as ET


class XMLImporter(DataImporter):
    @staticmethod
    def read_children(children):
        output = []
        for child in children:
            child_data = {
                "name": child.find("name").text,
                "age": int(child.find("age").text)
            }
            output.append(child_data)
        return output

    def import_from_file(self, file):
        tree = ET.parse(file)
        users = tree.getroot()
        output = []
        for user in users:
            data = {}
            for prop in user:
                if prop.tag == "children":
                    data[prop.tag] = self.read_children(prop)
                else:
                    data[prop.tag] = prop.text

            output.append(data)

        self.converted_data = output
