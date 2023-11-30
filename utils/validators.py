import re

from utils.exceptions import InvalidEmailError, InvalidPhoneNumberError

email_regex = (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\."
               r"(?=.*?[A-Z|a-z])[A-Z|a-z|0-9]{2,4}\b")

telephone_num_regex = r"\b\d{9}\b"


def validate_email(email_address):
    if re.fullmatch(email_regex, email_address):
        return True
    raise InvalidEmailError


def validate_telephone_number(telephone_num):
    if re.fullmatch(telephone_num_regex, telephone_num):
        return True
    raise InvalidPhoneNumberError
