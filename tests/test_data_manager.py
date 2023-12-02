import unittest
from unittest import mock

from database.data_manager import DataManager
from database.models import User, Child
from utils.exceptions import AuthenticationError


class TestData:
    users = [
        {
            "firstname": "Patricia",
            "telephone_number": "823816375",
            "email": "woodsjerry@example.com",
            "password": "z2Y%0Hbcsi",
            "role": "user",
            "created_at": "2023-04-02 15:57:34",
            "children": [
                {
                    "name": "Michael",
                    "age": 17
                },
                {
                    "name": "Angela",
                    "age": 14
                }
            ]
        },
        {
            "firstname": "Justin",
            "telephone_number": "678762794",
            "email": "opoole@example.org",
            "password": "+3t)mSM6xX",
            "role": "admin",
            "created_at": "2022-11-25 02:19:37",
            "children": [
                {
                    "name": "Marie",
                    "age": 17
                },
                {
                    "name": "George",
                    "age": 8
                },
                {
                    "name": "Susan",
                    "age": 14
                }
            ]
        },
        # phone num duplicated from Patricia
        {
            "firstname": "Donna",
            "telephone_number": "823816375",
            "email": "ngreen@example.org",
            "password": "z2Y%0Hbcsi",
            "role": "user",
            "created_at": "2023-04-02 15:57:34",
            "children": []
        }
    ]


class CreateDatabaseTestCase(unittest.TestCase):
    def setUp(self):
        self.data_manager = DataManager("sqlite:///:memory:")
        self.data_manager.database_creator = mock.MagicMock()

    def test_feeding_files(self):
        """
        Create database from files in a top-level directory.
        """
        path = "./test_data/a"
        files = [
            "./test_data/a/file1.xml",
            "./test_data/a/c/file3.json",
            "./test_data/a/b/file2.csv"
        ]
        feed_files = mock.MagicMock()
        self.data_manager.database_creator.feed_files = feed_files
        self.data_manager.create_database(path)

        self.assertTrue(feed_files.called)
        feed_files.assert_called_with(files)


class TasksTestCase(unittest.TestCase):
    def setUp(self):
        self.data_manager = DataManager("sqlite:///:memory:")
        self.data_manager.database_creator.feed_data(TestData.users)
        self.data_manager.log_in("opoole@example.org",
                                 "+3t)mSM6xX")

    def tearDown(self):
        self.data_manager.drop_database()

    def test_get_number_of_valid_accounts(self):
        """
        Return the total number of valid accounts.
        """
        expected_output = 2
        result = self.data_manager.accounts_total_number()
        self.assertEqual(expected_output, result)

    def test_oldest_account(self):
        """
        Information about the account with the longest existence.
        """
        expected_user_data = {
            "firstname": "Justin",
            "email": "opoole@example.org",
            "created_at": "2022-11-25 02:19:37"
        }
        oldest_user_account = self.data_manager.get_oldest_account()

        self.assertEqual(expected_user_data["firstname"],
                         oldest_user_account.firstname)
        self.assertEqual(expected_user_data["email"],
                         oldest_user_account.email)
        self.assertEqual(expected_user_data["created_at"],
                         str(oldest_user_account.created_at))

    def test_group_children_by_age(self):
        expected_output = [
            {
                "age": 8,
                "count": 1
            },
            {
                "age": 14,
                "count": 2
            },
            {
                "age": 17,
                "count": 2
            }
        ]
        result = self.data_manager.group_children_by_age()
        self.assertListEqual(expected_output, result)

    def test_get_children(self):
        """
        Getting user's children. Children must be sorted alphabetically.
        """
        justin_phone = "678762794"
        expected_output = ['George, 8', 'Marie, 17', 'Susan, 14']
        children = self.data_manager.get_children()
        result = [str(child) for child in children]
        self.assertListEqual(expected_output, result)

    def test_similar_age_children(self):
        self.data_manager.log_out()
        self.data_manager.log_in("woodsjerry@example.com",
                                 "z2Y%0Hbcsi")
        users = self.data_manager.users_w_similar_aged_children()
        user_key = list(users.keys())[0]

        # roughly testing the desired behaviour
        self.assertEqual(user_key.firstname, "Justin")
        self.assertEqual(1, len(users.keys()))
        self.assertEqual(2, len(users[user_key]))
        self.assertEqual(str(users[user_key][0]), "Marie, 17")
        self.assertEqual(str(users[user_key][1]), "Susan, 14")


class AuthenticationAuthorizationTestCase(unittest.TestCase):
    def setUp(self):
        self.data_manager = DataManager("sqlite:///:memory:")
        self.session = self.data_manager.session
        self.data_manager.database_creator.feed_data(TestData.users)
        self.email = "woodsjerry@example.com"
        self.password = "z2Y%0Hbcsi"
        self.phone_num = "823816375"
        self.user_patricia = self.session.query(User).filter_by(
            email=self.email).first()

    def test_logging_in_by_email_success(self):
        self.data_manager.log_in(self.email, self.password)
        self.assertEqual(self.user_patricia,
                         self.data_manager._authenticated_user)

    def test_logging_in_by_email_fail(self):
        def fail_logging_in():
            self.data_manager.log_in(self.email, "wrong_password")

        self.assertRaises(AuthenticationError, fail_logging_in)

    def test_logging_in_by_telephone_success(self):
        self.data_manager.log_in(self.phone_num, self.password)
        self.assertEqual(self.user_patricia,
                         self.data_manager._authenticated_user)

    def test_logging_in_by_telephone_fail(self):
        def fail_logging_in():
            self.data_manager.log_in(self.phone_num,
                                     "wrong_password")

        self.assertRaises(AuthenticationError, fail_logging_in)

    def test_invalid_login(self):
        """
        Attempt to pass login that is neither an email nor phone number.
        """
        def fail_logging_in():
            self.data_manager.log_in("##$zdfva54854855154",
                                     self.password)

        self.assertRaises(AuthenticationError, fail_logging_in)


if __name__ == '__main__':
    unittest.main()
