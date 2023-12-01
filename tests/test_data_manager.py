import unittest
from unittest import mock

from database.data_manager import DataManager
from database.models import User, Child


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
        session = self.data_manager.session
        user_justin = session.query(User).filter_by(
            telephone_number=justin_phone).first()
        expected_output = ['George, 8', 'Marie, 17', 'Susan, 14']
        children = self.data_manager.get_children(user_justin)
        result = [str(child) for child in children]
        self.assertListEqual(expected_output, result)

    def test_similar_age_children(self):
        patricia = self.data_manager.session.get(
            User, "woodsjerry@example.com")
        users = self.data_manager.users_w_similar_aged_children(patricia)

        # roughly testing the desired behaviour
        self.assertEqual(1, len(users))
        self.assertEqual("opoole@example.org", users[0].email)


if __name__ == '__main__':
    unittest.main()
