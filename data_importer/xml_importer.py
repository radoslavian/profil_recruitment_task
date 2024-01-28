from data_importer.data_importer import DataImporter
from lxml import etree


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
        parser = etree.XMLParser(recover=True)
        tree = etree.parse(file, parser=parser)
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

        return output
