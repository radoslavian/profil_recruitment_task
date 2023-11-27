import unittest
from utils.email_validator import validate_email


class EmailValidatorTestCase(unittest.TestCase):
    """
    Email must contain only one "@" symbol.
    """
    def test_single_at(self):
        """
        Single '@' in an email address: should return True.
        """
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
