import unittest
from datetime import datetime
from unittest.mock import patch, call

from modules.data_printer import print_longest_existing_account, \
    print_children_by_age, print_children, print_users_children_same_age


class Child:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"{self.name}, {self.age}"


class DataPrinterTestCase(unittest.TestCase):
    class User:
        firstname = "Boris"
        email = "boris@gmail.com"
        created_at = datetime.fromisoformat("1990-12-12 13:20:00")
        telephone_number = "123456789"
        children = [
            Child("Archibald", 2),
            Child("Tim", 15)
        ]

        def __str__(self):
            return f"{self.firstname}, {self.telephone_number}"

    ages_distribution = [
        {
            "age": 8,
            "count": 1
        }
    ]

    @patch("builtins.print")
    def test_printing_longest_existing_account(self, mocked_print):
        print_longest_existing_account(self.User)
        expected_output = ("name: Boris\n"
                           "email_address: boris@gmail.com\n"
                           "created_at: 1990-12-12 13:20:00\n")
        mocked_print.assert_called_with(expected_output)

    @patch("builtins.print")
    def test_printing_children_by_age(self, mocked_print):
        print_children_by_age(self.ages_distribution)
        expected_output = "age: 8, count: 1\n"
        mocked_print.assert_called_with(expected_output)

    @patch("builtins.print")
    def test_print_children(self, mocked_print):
        print_children(self.User)
        expected_output = [
            call("Archibald, 2\n"),
            call("Tim, 15\n")
        ]
        self.assertEqual(expected_output, mocked_print.mock_calls)

    @patch("builtins.print")
    def test_print_users_with_children_of_same_age(self, mocked_print):
        input_data = {
            self.User(): self.User.children
        }
        print_users_children_same_age(input_data)
        expected_output = [
            call('Boris, 123456789: ', end=''),
            call('Archibald, 2', end=''),
            call('; ', end=''),
            call('Tim, 15', end=''),
            call()
        ]
        self.assertEqual(expected_output, mocked_print.mock_calls)


if __name__ == '__main__':
    unittest.main()
