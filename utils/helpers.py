from datetime import datetime


def convert_datetime(datetime_string):
    """
    Convert date-time string in the YYYY-MM-DD HH:MM:SS format
    into datetime object.
    datetime_strong example: 2023-06-25 06:56:34
    """
    return datetime.strptime(datetime_string, "%Y-%m-%d %H:%M:%S")