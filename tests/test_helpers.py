import unittest

from utils.helpers import convert_datetime, normalize_telephone_num, \
    list_files_for_import, get_file_extension


class DateTimeConverterTestCase(unittest.TestCase):
    def test_datetime_conversion(self):
        """
        Converts datetime string in the format YYYY-MM-DD HH:MM:SS
        into datetime object.
        """
        date_time = "2023-06-25 06:56:34"
        converted_date_time = convert_datetime(date_time)

        self.assertEqual(2023, converted_date_time.year)
        self.assertEqual(6, converted_date_time.month)
        self.assertEqual(25, converted_date_time.day)
        self.assertEqual(6, converted_date_time.hour)
        self.assertEqual(56, converted_date_time.minute)
        self.assertEqual(34, converted_date_time.second)

    def test_malformed_argument(self):
        """
        Should raise ValueError when called with malformed input.
        """
        date_time = "2023/06/25 06:56:34"
        self.assertRaises(ValueError, lambda: convert_datetime(date_time))


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
            "test_data/a/b/file2.cvs",
            "test_data/a/file1.xml"
        }
        file_extensions = [".cvs", ".xml", ".json"]
        output = list_files_for_import("test_data/a", file_extensions)

        self.assertEqual(len(output), 3)
        self.assertSetEqual(expected_output, set(output))


if __name__ == '__main__':
    unittest.main()
