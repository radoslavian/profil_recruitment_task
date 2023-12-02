#!/usr/bin/env python

import argparse
import os

from database.data_manager import DataManager
from modules.data_printer import *

DATABASE_PATH = os.path.join(
    os.path.dirname(__file__), "database", "users.db")
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

parser = argparse.ArgumentParser()
parser.add_argument("task")
args = parser.parse_args()
task = args.task

if __name__ == '__main__':
    data_manager = DataManager(DATABASE_URL)

    match task:
        case "create_database":
            data_manager.create_database(DATA_DIR)
        case "print-all-accounts":
            number_of_accounts = data_manager.accounts_total_number()
            print(number_of_accounts)
        case "print-oldest-account":
            oldest_account = data_manager.get_oldest_account()
            print_oldest_account(oldest_account)
        case "group-by-age":
            children_by_age = data_manager.group_children_by_age()
            print_children_by_age(children_by_age)
