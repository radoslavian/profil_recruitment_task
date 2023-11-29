import unittest

from utils.security import generate_password_hash, check_password_hash


class PasswordHashingTestCase(unittest.TestCase):
    """
    Password has is generated using sha256.
    """
    password_hash = ("5e884898da28047151d0e56f8dc6292773603d"
                     "0d6aabbdd62a11ef721d1542d8")

    def test_generating_password_hash(self):
        output = generate_password_hash("password")
        self.assertEqual(self.password_hash, output)

    def test_checking_password_hash(self):
        result = check_password_hash(self.password_hash, "password")
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
