import unittest
from utils.validators import validate_email, validate_telephone_number
from utils.exceptions import InvalidEmailError, InvalidPhoneNumberError


class EmailValidatorAtCharacterTestCase(unittest.TestCase):
    """
    Email must contain only one "@" symbol.
    """

    def test_single_at(self):
        """
        Single '@' in a valid email address: should return True.
        """
        valid_email = "user@domain.com"
        result = validate_email(valid_email)
        self.assertTrue(result)

    def test_multiple_at(self):
        """
        Multiple '@' put in different places of an email address:
        should raise InvalidEmailError.
        """
        invalid_email = "user1@very@long@domain@name.com"
        self.assertRaises(InvalidEmailError,
                          lambda: validate_email(invalid_email))

    def test_multiple_at_next_to_each_other(self):
        """
        Multiple '@' put next to each other in an email address:
        should raise InvalidEmailError.
        """
        invalid_email = "user@@domain.com"
        self.assertRaises(InvalidEmailError,
                          lambda: validate_email(invalid_email))

    def test_no_at(self):
        """
        No '@' character in an email address:
        should raise InvalidEmailError.
        """
        invalid_email = "user_at_domain.com"
        self.assertRaises(InvalidEmailError,
                          lambda: validate_email(invalid_email))


class EmailValidatorUsernameTestCase(unittest.TestCase):
    """
    The part before "@" (email username) must be at least 1 character long.
    """

    def test_single_character(self):
        """
        Should success: single character for an email username.
        """
        email_address = "a@domain.com"
        result = validate_email(email_address)
        self.assertTrue(result)

    def test_multiple_characters(self):
        """
        Should success: multiple characters for an email username.
        """
        email_address = "username_1@domain.com"
        result = validate_email(email_address)
        self.assertTrue(result)

    def test_no_username(self):
        """
        Should fail: no username (empty part before "@" character).
        """
        email_address = "@domain.com"
        self.assertRaises(InvalidEmailError,
                          lambda: validate_email(email_address))


class EmailValidatorMiddleDomains(unittest.TestCase):
    def test_middle_domains(self):
        """
        Should fail: the part between "@" and "." must be at
        least 1 character long.
        """
        email_address = "user@.com"
        self.assertRaises(InvalidEmailError,
                          lambda: validate_email(email_address))


class EmailValidatorTopLevelDomain(unittest.TestCase):
    """
    The part after the last "." must be between 1 and 4 characters long,
    containing only letters and/or digits.
    """

    def test_top_level_domain_too_long(self):
        """
        The top-level domain name is longer than 4 characters.
        """
        email_address = "user@domain1.com.topleveldomainname"
        self.assertRaises(InvalidEmailError,
                          lambda: validate_email(email_address))

    def test_top_level_invalid_characters(self):
        """
        The top-level domain name contains illegal characters.
        """
        email_address = "user@domain1.domain2.$;a"
        self.assertRaises(InvalidEmailError,
                          lambda: validate_email(email_address))

    def test_numbers_only(self):
        """
        Should fail: the top-level domain will never consist of only numbers.
        """
        email_address = "user@domain1.123"
        self.assertRaises(InvalidEmailError,
                          lambda: validate_email(email_address))

    def test_no_top_level_domain(self):
        """
        Should fail: no top-level domain.
        """
        email_address = "user@domain1"
        self.assertRaises(InvalidEmailError,
                          lambda: validate_email(email_address))

    def test_valid_top_level_domain_multiple_domains(self):
        """
        Should success: valid top-level domain name with multiple domains.
        """
        email_address = "user@domain.org.pl"
        self.assertTrue(validate_email(email_address))


class ValidateTelephoneNumberTestCase(unittest.TestCase):
    def test_raising_error_on_invalid_phone(self):
        """
        Should raise InvalidPhoneNumberError when invalid phone number is
        passed.
        """
        invalid_phone_num = "939387393837494765454767"
        self.assertRaises(
            InvalidPhoneNumberError,
            lambda: validate_telephone_number(invalid_phone_num))

    def test_raising_error_on_no_phone_empty_str(self):
        """
        Should raise InvalidPhoneNumberError when empty string is passed
        as an argument.
        """
        self.assertRaises(
            InvalidPhoneNumberError,
            lambda: validate_telephone_number(""))

    def test_successful_validation(self):
        phone_num = "123456789"
        self.assertTrue(validate_telephone_number(phone_num))


if __name__ == '__main__':
    unittest.main()
