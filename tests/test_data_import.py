import unittest

from data_importer.csv_importer import CSVImporter
from data_importer.json_importer import JsonImporter
from data_importer.xml_importer import XMLImporter


class DataImporterTestCaseAbs:
    Importer = None
    importer = None
    user_data = None

    @classmethod
    def setup_importer(cls, test_data_path):
        cls.importer = cls.Importer(test_data_path)
        if cls.importer.is_loaded:
            cls.user_data = list(cls.importer)

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

    def test_successful_import(self):
        self.assertTrue(self.importer.is_loaded)

    def test_import_fail(self):
        importer = self.Importer("/wrong/path/to/file")
        self.assertFalse(importer.is_loaded)
        self.assertIn("No such file or directory", importer.fail_reason)

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
    Importer = JsonImporter

    @classmethod
    def setUpClass(cls):
        cls.setup_importer("./test_data/users.json")


class XMLImporterTestCase(unittest.TestCase, DataImporterTestCaseAbs):
    Importer = XMLImporter

    @classmethod
    def setUpClass(cls):
        cls.setup_importer("./test_data/users.xml")


class CSVImporterTestCase(unittest.TestCase, DataImporterTestCaseAbs):
    Importer = CSVImporter

    @classmethod
    def setUpClass(cls):
        cls.setup_importer("./test_data/users.csv")


if __name__ == '__main__':
    unittest.main()
