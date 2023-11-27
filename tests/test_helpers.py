import unittest

from utils.helpers import convert_datetime


class DateTimeConverterTestCase(unittest.TestCase):
    def test_datetime_conversion(self):
        """
        Converts datetime string in the format YYYY-MM-DD HH:MM:SS
        into datetime object.
        """
        date_time = "2023-06-25 06:56:34"
        converted_date_time = convert_datetime(date_time)

        self.assertEqual(converted_date_time.year, 2023)
        self.assertEqual(converted_date_time.month, 6)
        self.assertEqual(converted_date_time.day, 25)
        self.assertEqual(converted_date_time.hour, 6)
        self.assertEqual(converted_date_time.minute, 56)
        self.assertEqual(converted_date_time.second, 34)

    def test_malformed_argument(self):
        """
        Should raise ValueError when called with malformed input.
        """
        date_time = "2023/06/25 06:56:34"
        self.assertRaises(ValueError, lambda: convert_datetime(date_time))


if __name__ == '__main__':
    unittest.main()
