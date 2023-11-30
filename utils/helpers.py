import os
from os.path import join
from datetime import datetime


def convert_datetime(datetime_string):
    """
    Convert date-time string in the YYYY-MM-DD HH:MM:SS format
    into datetime object.
    datetime_strong example: 2023-06-25 06:56:34
    """
    return datetime.strptime(datetime_string, "%Y-%m-%d %H:%M:%S")


def convert_filter_to_str(filter_obj):
    """
    Convert filter object to a string.
    """
    return "".join(filter_obj)


def clean_telephone_num(telephone_num):
    """
    Remove special characters from a telephone number.
    """
    return filter(str.isdigit, telephone_num)


def normalize_telephone_num(telephone_num):
    cleaned_num = clean_telephone_num(telephone_num)
    return convert_filter_to_str(cleaned_num)[-9:]


def get_file_extension(path):
    _, file_extension = os.path.splitext(path)
    return file_extension


def list_files_for_import(path, file_extensions):
    """
    Find files with given extensions within directory.
    :param path: path relative to the working directory
    :param file_extensions: list of file extensions, e.g.: [".txt", ".png"]
    :return: list of relative paths (to the working directory) within
    subdirectory.
    """
    found_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if get_file_extension(file) in file_extensions:
                found_files.append(join(root, file))
    return found_files
