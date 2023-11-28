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


if __name__ == '__main__':
    unittest.main()
