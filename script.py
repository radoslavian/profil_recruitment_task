import argparse
import os

from database.data_manager import DataManager
from modules.data_printer import *
from utils.exceptions import CredentialsError

DATABASE_PATH = os.path.join(
    os.path.dirname(__file__), "database", "users.db")
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def match_task(user_task, data_manager):
    match user_task:
        case "print-all-accounts":
            number_of_accounts = data_manager.accounts_total_number()
            print(number_of_accounts)
        case "print-oldest-account":
            oldest_account = data_manager.get_oldest_account()
            print_oldest_account(oldest_account)
        case "group-by-age":
            children_by_age = data_manager.group_children_by_age()
            print_children_by_age(children_by_age)
        case "print-children":
            users_children = data_manager.get_children()
            print_children(users_children)
        case "find-similar-children-by-age":
            similar_aged_children = data_manager \
                .users_w_similar_aged_children()
            print_users_children_same_age(similar_aged_children)
        case _:
            print("Unrecognized task.")


def main(args):
    task = args.task
    login = args.login or ""
    password = args.password or ""

    if (not login or not password) and not task == "create_database":
        print("Please provide full credentials.")
        exit(1)

    data_manager = DataManager(DATABASE_URL)

    if task == "create_database":
        print("Creating database...")
        data_manager.create_database(DATA_DIR)
        exit(0)

    try:
        data_manager.log_in(login, password)
        match_task(task, data_manager)
    except CredentialsError:
        print("Invalid Login")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    for argument in ["task", "--login", "--password"]:
        parser.add_argument(argument)

    script_args = parser.parse_args()
    main(script_args)
