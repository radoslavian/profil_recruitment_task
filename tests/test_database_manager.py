import unittest

from data_importer.csv_importer import CSVImporter
from data_importer.json_importer import JsonImporter
from data_importer.xml_importer import XMLImporter
from database.database_manager import DatabaseManager
from database.models import User, Child, Role
from utils.helpers import convert_datetime
from utils.security import check_password_hash


class DatabaseManagerSetup:
    def setUp(self):
        self.database_manager = DatabaseManager("sqlite:///:memory:")
        # this is needed for the greater good
        self.session = self.database_manager.session

    def tearDown(self):
        self.database_manager.drop_all()


class DatabaseManagerTestCase(DatabaseManagerSetup, unittest.TestCase):
    class TestData:
        user_with_children = [
            {
                "firstname": "Tiffany",
                "telephone_number": "00804241616",
                "email": "kyle63@example.org",
                "password": "ywq%6FzI_o",
                "role": "user",
                "created_at": "2023-04-08 12:26:15",
                "children": [
                    {
                        "name": "Alan",
                        "age": 5
                    },
                    {
                        "name": "Sara",
                        "age": 8
                    }
                ]
            }
        ]
        user_without_children = [
            {
                "firstname": "Cathy",
                "telephone_number": "(48)094885352",
                "email": "rubengriffin@example.com",
                "password": "Dw2Bf(Dd!q",
                "role": "admin",
                "created_at": "2023-08-27 16:39:04",
                "children": []
            }
        ]
        duplicate_users = [
            {
                "firstname": "Amy",
                "telephone_number": "+48361568741",
                "email": "brenda74@example.org",
                "password": "+vJCXfFLe0",
                "role": "admin",
                "created_at": "2023-03-01 04:14:24",
                "children": [
                    {
                        "name": "Sara",
                        "age": 8
                    }
                ]
            },
            {
                "firstname": "Amy",
                "telephone_number": "+48361568741",
                "email": "brenda74@example.org",
                "password": "+vJCXfFLe0",
                "role": "admin",
                "created_at": "2023-03-05 04:14:24",

                # different child!
                "children": [
                    {
                        "name": "Justin",
                        "age": 15
                    }
                ]
            }
        ]

    def test_adding_user_with_children(self):
        self.database_manager.feed_data(self.TestData.user_with_children)
        user_email = self.TestData.user_with_children[0]["email"]
        user = self.session.query(User).filter_by(email=user_email).first()
        child = self.session.query(Child).filter_by(name="Alan").first()

        self.assertEqual(user.email, user_email)
        self.assertEqual(user.children.count(), 2)
        self.assertEqual(child.parent.email, user.email)

    def test_normalized_phone_number(self):
        self.database_manager.feed_data(self.TestData.user_without_children)
        user = self.session.get(
            User, self.TestData.user_without_children[0]["email"])
        self.assertEqual("094885352", user.telephone_number)

    def test_add_user_with_malformed_email(self):
        """
        Shouldn't add user with malformed email.
        """
        user_data = [
            {
                **self.TestData.user_without_children[0],
                "email": "@cutHead.com"
            }
        ]
        self.database_manager.feed_data(user_data)
        user = self.session.query(User).first()
        self.assertFalse(user)

    def test_adding_user_without_children(self):
        self.database_manager.feed_data(self.TestData.user_without_children)
        user_email = self.TestData.user_without_children[0]["email"]
        user = self.session.query(User).filter_by(email=user_email).first()

        self.assertEqual(user.email, user_email)
        self.assertEqual(user.children.count(), 0)

    def test_adding_duplicate_record_newer_on_list(self):
        """
        Should add newer record (the one from the queue).
        """
        self.database_manager.feed_data(self.TestData.duplicate_users)
        user = self.session.query(User).first()
        child = self.session.query(Child).first()
        # below equals to:
        # created at = self.TestData.duplicate_users[1]["created_at"]
        created_at = convert_datetime("2023-03-05 04:14:24")

        self.assertEqual(1, self.session.query(User).count())
        self.assertEqual(1, self.session.query(Child).count())
        self.assertEqual(child.name, "Justin")
        self.assertEqual(user.created_at, created_at)

    def test_adding_duplicate_record_newer_in_db(self):
        """
        Should keep newer record (already present in the database).
        """
        # reverse the list without mutating the original
        duplicate_users = self.TestData.duplicate_users[::-1]
        # newer record will be added to the db as the first one
        self.database_manager.feed_data(duplicate_users)
        created_at = convert_datetime("2023-03-05 04:14:24")
        user = self.session.query(User).first()

        self.assertEqual(self.session.query(User).count(), 1)
        self.assertEqual(user.created_at, created_at)

    def test_adding_user_without_telephone(self):
        """
        An attempt to add user entry without telephone number should
        raise InvalidPhoneNumberError exception.
        """
        user_entry = [
            {
                **self.TestData.user_without_children[0],
                "telephone_number": ""
            }
        ]
        self.database_manager.feed_data(user_entry)
        user = self.session.get(User, user_entry[0]["email"])
        self.assertFalse(user)

    def test_password_hash(self):
        self.database_manager.feed_data(self.TestData.user_without_children)
        user = self.session.query(User).first()
        password = self.TestData.user_without_children[0]["password"]
        self.assertTrue(check_password_hash(user.password_hash, password))

    def test_user_with_admin_role(self):
        user_data = self.TestData.user_without_children[0]
        self.database_manager.feed_data(self.TestData.user_without_children)
        admin_user = self.session.get(User, user_data["email"])

        self.assertTrue("admin", admin_user.role.name)

    def test_user_with_user_role(self):
        user_data = [
            {
                **self.TestData.user_without_children[0],
                "role": "user"
            }
        ]
        self.database_manager.feed_data(user_data)
        user = self.session.get(User, user_data[0]["email"])

        self.assertEqual("user", user.role.name)


class RolesTestCase(DatabaseManagerSetup, unittest.TestCase):
    def test_adding_roles(self):
        """
        Adding basic roles: admin and user.
        """
        self.database_manager.insert_roles()
        admin_role = self.session.query(Role).filter_by(name="admin").first()
        user_role = self.session.query(Role).filter_by(name="user").first()

        self.assertIsNotNone(admin_role)
        self.assertIsNotNone(user_role)


class SelectingImporterTestCase(DatabaseManagerSetup, unittest.TestCase):
    def test_selecting_csv_importer(self):
        """
        Should return importer for a csv file.
        """
        fake_file = "/path/to/the/file.csv"
        Importer = self.database_manager.get_importer_for_file(fake_file)
        self.assertIs(Importer, CSVImporter)

    def test_selecting_json_importer(self):
        """
        Should return importer for a json file.
        """
        fake_file = "/path/to/the/file.json"
        Importer = self.database_manager.get_importer_for_file(fake_file)
        self.assertIs(Importer, JsonImporter)

    def test_selecting_xml_importer(self):
        """
        Should return importer for a json file.
        """
        fake_file = "/path/to/the/file.xml"
        Importer = self.database_manager.get_importer_for_file(fake_file)
        self.assertIs(Importer, XMLImporter)

    def test_selecting_importer_wrong_file_type(self):
        """
        Should raise ValueError on an attempt to import data from a file
        of a different (from xml, csv, json) type.
        """
        fake_file = "/path/to/the/file.bin"

        def import_wrong_file():
            self.database_manager.get_importer_for_file(fake_file)

        self.assertRaises(ValueError, import_wrong_file)


class ImportingDataFromFiles(DatabaseManagerSetup, unittest.TestCase):
    def test_importing_from_csv(self):
        test_data_file = "./test_data/a/b/file2.csv"
        self.database_manager.import_data_from_file(test_data_file)
        user_jamie = self.session.get(User, "kcampbell@yahve.com")
        user_carol = self.session.query(User).filter_by(
            firstname="Carol").first()

        self.assertIsNotNone(user_jamie)
        self.assertIsNone(user_carol)
        self.assertEqual("Jamie", user_jamie.firstname)
        self.assertEqual(2, self.session.query(User).count())

    def test_importing_from_xml(self):
        test_data_file = "./test_data/a/file1.xml"
        self.database_manager.import_data_from_file(test_data_file)
        user_justin = self.session.get(User, "opoole@example.org")
        user_felicia = self.session.query(User).filter_by(
            firstname="Felicia").first()

        self.assertIsNotNone(user_justin)
        self.assertIsNone(user_felicia)
        self.assertEqual("Justin", user_justin.firstname)
        self.assertEqual(1, self.session.query(User).count())

    def test_importing_from_json(self):
        test_data_file = "./test_data/a/c/file3.json"
        self.database_manager.import_data_from_file(test_data_file)
        user_patricia = self.session.get(User, "woodsjerry@example.com")
        user_michael = self.session.query(User).filter_by(
            firstname="Michael").first()

        self.assertIsNotNone(user_patricia)
        self.assertIsNone(user_michael)
        self.assertEqual("Patricia", user_patricia.firstname)
        self.assertEqual(1, self.session.query(User).count())



if __name__ == '__main__':
    unittest.main()
