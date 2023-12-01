import unittest
from datetime import datetime

from utils.helpers import normalize_telephone_num, list_files_for_import, \
    get_file_extension


class TelephoneNumberConverterTestCase(unittest.TestCase):
    expected_output = "123456789"

    def test_remove_plus_country_code(self):
        """
        Should remove leading +48 country code.
        """
        input_num = "+48123456789"
        result = normalize_telephone_num(input_num)
        self.assertEqual(self.expected_output, result)

    def test_remove_leading_zeros(self):
        input_num = "00123456789"
        result = normalize_telephone_num(input_num)
        self.assertEqual(self.expected_output, result)

    def test_remove_parentheses(self):
        """
        Should remove parentheses around country code and drop
        subsequent space.
        """
        input_num = "(48) 123456789"
        result = normalize_telephone_num(input_num)
        self.assertEqual(self.expected_output, result)

    def test_remove_spaces(self):
        input_num = "123 456 789"
        result = normalize_telephone_num(input_num)
        self.assertEqual(self.expected_output, result)


class FileUtilsTestCase(unittest.TestCase):
    def test_getting_file_extension(self):
        file = "/home/user/filename.txt"
        result = get_file_extension(file)

        self.assertEqual(".txt", result)
        self.assertEqual(".png", get_file_extension("file.png"))

    def test_listing_files(self):
        """
        Listing files for import.
        """
        expected_output = {
            "test_data/a/c/file3.json",
            "test_data/a/b/file2.csv",
            "test_data/a/file1.xml"
        }
        file_extensions = [".csv", ".xml", ".json"]
        output = list_files_for_import("test_data/a", file_extensions)

        self.assertEqual(len(output), 3)
        self.assertSetEqual(expected_output, set(output))


if __name__ == '__main__':
    unittest.main()
