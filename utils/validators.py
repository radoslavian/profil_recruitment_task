import re

from utils.exceptions import InvalidEmailError

email_regex = (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.'
               r'(?=.*?[A-Z|a-z])[A-Z|a-z|0-9]{2,4}\b')


def validate_email(email_address):
    if re.fullmatch(email_regex, email_address):
        return True
    raise InvalidEmailError
