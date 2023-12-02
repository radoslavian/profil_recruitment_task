import unittest
from datetime import datetime

from sqlalchemy.exc import IntegrityError

from database.models import User, start_engine, drop_all, Role, Child
from utils.exceptions import InvalidEmailError


class DatabaseTestCaseAbs(unittest.TestCase):
    def setUp(self):
        self.engine, self.session = start_engine("sqlite:///:memory:")
        self.setup_test_data()

    def tearDown(self):
        drop_all(self.engine)

    def setup_test_data(self):
        pass


class UserRoleTestCase(DatabaseTestCaseAbs):
    def setup_test_data(self):
        self.admin_role = Role(
            name="admin"
        )
        self.session.add(self.admin_role)
        self.session.commit()

        self.created_at = datetime.fromisoformat("2023-03-02 16:37:42")
        user = User(
            email="esexton@example.net",
            firstname="Patricia",
            role=self.admin_role,
            telephone_number="636162531",
            created_at=self.created_at
        )
        self.session.add(user)
        self.session.commit()

    def test_user_email_validation(self):
        """
        User instance shouldn't accept invalid email address.
        """
        invalid_email = "@host.com"

        def raise_error():
            user = User(
                email=invalid_email,
                firstname="Patricia",
                telephone_number="013112467",
                created_at=self.created_at
            )
            self.session.add(user)
            self.session.commit()

        self.assertRaises(InvalidEmailError, raise_error)

    def test_no_email(self):
        """
        Creating a user instance should fail if no email is given.
        """

        def raise_error():
            user = User(
                firstname="Patricia",
                telephone_number="013112467",
                created_at=self.created_at
            )
            self.session.add(user)
            self.session.commit()

        self.assertRaises(IntegrityError, raise_error)

    def test_user_valid_data(self):
        """
        Querying for the 'User' instance.
        """
        user = self.session.query(User).filter_by(
            email="esexton@example.net"
        ).first()

        self.assertEqual("Patricia", user.firstname)
        self.assertEqual("636162531", user.telephone_number)
        self.assertEqual(user.created_at, self.created_at)
        self.assertEqual("admin", user.role.name)

    def test_role_backref(self):
        """
        Role back-reference should point to the user.
        """
        role = self.session.query(Role).filter_by(
            name="admin"
        ).first()

        self.assertEqual("Patricia", role.users[0].firstname)
        self.assertEqual(1, role.users.count())

    def test_drop_user_keep_role(self):
        """
        Dropping user doesn't cause dropping role.
        """
        self.session.query(User).filter_by(
            email="esexton@example.net"
        ).delete()
        self.session.commit()
        role = self.session.query(Role).filter_by(name="admin").first()

        self.assertTrue(role)

    def test_drop_role_keep_user(self):
        """
        Dropping role doesn't cause dropping attached users.
        """
        self.session.delete(self.admin_role)
        self.session.commit()
        user = self.session.query(User).filter_by(
            email="esexton@example.net"
        ).first()

        self.assertTrue(user)


class UserChildrenTestCase(DatabaseTestCaseAbs):
    def setup_test_data(self):
        child1 = Child(
            name="Andrew",
            age=4
        )
        child2 = Child(
            name="James",
            age=13
        )
        self.children = [child1, child2]
        self.user = User(
            telephone_number="700851384",
            email="cherrera@example.com",
            firstname="Gregory",
            children=self.children,
            created_at=datetime.fromisoformat("2023-09-19 02:36:39")
        )
        self.session.add(self.user)
        self.session.commit()

    def test_child_valid_data(self):
        child = self.children[0]
        self.assertEqual("Andrew", child.name)
        self.assertEqual(4, child.age)

    def test_child_to_parent_backref(self):
        """
        Children indicate their parent.
        """
        child = self.children[0]
        self.assertEqual(child.parent.firstname, self.user.firstname)

    def test_children_count(self):
        """
        User has two children.
        """
        self.assertEqual(2, self.user.children.count())

    def test_removing_parent(self):
        """
        Removing parent should result in dropping children.
        """
        self.session.delete(self.user)
        self.session.commit()
        self.assertEqual(0, self.session.query(Child).count())

    def test_removing_children(self):
        """
        Removing children doesn't result in dropping parent.
        """
        self.session.query(Child).delete()
        self.session.commit()
        self.session.refresh(self.user)
        self.assertTrue(self.user)

    def test_child_serialization(self):
        """
        Output of the Child.__str__ method should look like this:
        Alan, 12
        """
        child = self.children[0]
        self.assertEqual(f"{child.name}, {child.age}", str(child))


class UserCredentialsTestCase(DatabaseTestCaseAbs):
    def setup_test_data(self):
        self.created_at = datetime.fromisoformat("2023-03-02 16:37:42")
        self.user = User(
            firstname="Patricia",
            telephone_number="013112467",
            created_at=self.created_at,
            password="very_odd_password"
        )

    def test_verify_password_success(self):
        self.assertTrue(self.user.verify_password("very_odd_password"))

    def test_verify_password_failure(self):
        self.assertFalse(self.user.verify_password("wrong_password"))

    def test_attempt_to_read_password(self):
        self.assertRaises(AttributeError, lambda: self.user.password)

    def test_password_hashing(self):
        self.assertEqual(64, len(self.user.password_hash))
        self.assertNotEqual(self.user.password_hash,
                            "very_odd_password")


if __name__ == '__main__':
    unittest.main()
