import unittest

from data_importer.csv_importer import CSVImporter
from data_importer.json_importer import JsonImporter
from data_importer.xml_importer import XMLImporter


class DataImporterTestCaseAbs:
    importer = None
    user_data = None

    def test_imported_data_types(self):
        """
        Class imports data into Python list format composed of dicts.
        """
        self.assertIs(type(self.user_data), list)
        self.assertIs(type(self.user_data[0]), dict)

    def test_import_length(self):
        """
        Test data contains two entries.
        """
        self.assertEqual(len(self.user_data), 2)

    def test_example_data(self):
        expected_output = {
            "firstname": "Justin",
            "telephone_number": "678762794",
            "email": "opoole@example.org",
            "password": "+3t)mSM6xX",
            "role": "admin",
            "created_at": "2022-11-25 02:19:37",
            "children": [
                {
                    "name": "Anna",
                    "age": 18
                },
                {
                    "name": "James",
                    "age": 17
                }
            ]
        }
        self.assertDictEqual(expected_output, self.user_data[0])


class JsonImporterTestCase(unittest.TestCase, DataImporterTestCaseAbs):
    @classmethod
    def setUpClass(cls):
        cls.importer = JsonImporter("./test_data/users.json")
        cls.user_data = cls.importer.get_data()


class XMLImporterTestCase(unittest.TestCase, DataImporterTestCaseAbs):
    @classmethod
    def setUpClass(cls):
        cls.importer = XMLImporter("./test_data/users.xml")
        cls.user_data = cls.importer.get_data()


class CSVImporterTestCase(unittest.TestCase, DataImporterTestCaseAbs):
    @classmethod
    def setUpClass(cls):
        cls.importer = CSVImporter("./test_data/users.csv")
        cls.user_data = cls.importer.get_data()


if __name__ == '__main__':
    unittest.main()
