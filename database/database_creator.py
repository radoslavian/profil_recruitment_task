import sys
from datetime import datetime

from sqlalchemy.exc import IntegrityError

from data_importer.csv_importer import CSVImporter
from data_importer.json_importer import JsonImporter
from data_importer.xml_importer import XMLImporter
from database.models import User, Child, Role
from utils.exceptions import InvalidInputError, RoleNotFoundError
from utils.helpers import normalize_telephone_num, get_file_extension
from utils.security import ADMIN_ROLE_NAME


class DatabaseCreator:
    def __init__(self, session):
        self.session = session
        self.insert_roles()

    def insert_roles(self):
        roles = {ADMIN_ROLE_NAME, "user"}
        default_role = "user"

        for r in roles:
            role = self.session.query(Role).filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
                role.default = (role.name == default_role)
            self.session.add(role)
        self.session.commit()

    @staticmethod
    def _add_children(children, parent):
        """
        Helper to 'add_user_with_children'. Changes must be committed
        outside this method.
        """
        for child in children:
            Child(
                name=child["name"],
                age=child["age"],
                parent=parent
            )

    def add_user_with_children(self, user):
        role = self.session.query(Role).filter_by(name=user["role"]).first()
        if role is None:
            raise RoleNotFoundError(f"Role {user['role']} was not found.")

        new_user = User(
            email=user["email"],
            firstname=user["firstname"],
            telephone_number=normalize_telephone_num(
                user["telephone_number"]),
            password=user["password"],
            role=role,
            created_at=datetime.fromisoformat(user["created_at"])
        )
        self._add_children(user["children"], parent=new_user)
        self.session.add(new_user)
        self.session.commit()

    def _swap_users_conditionally(self, user):
        """
        Add a user (or keep already existing) with a newer creation date
        to the database.
        """
        # this method is called if IntegrityError occurs,
        # which (in this scenario) is raised when unique constraint
        # fails -> so that we have to query using all fields
        # with unique constraint imposed on them:
        user_query = self.session.query(User)
        normalized_tel_num = normalize_telephone_num(user["telephone_number"])
        user_in_db = (
                user_query.filter_by(email=user["email"]).first()
                or
                user_query.filter_by(
                    telephone_number=normalized_tel_num).first()
        )

        if datetime.fromisoformat(user["created_at"]) > user_in_db.created_at:
            self.session.delete(user_in_db)
            self.session.commit()
            self.add_user_with_children(user)

    def feed_data(self, users):
        """
        Import data into a database.
        :param users: list of dictionaries with user-data (returned by
        data_importer)
        """
        for user in users:
            try:
                self.add_user_with_children(user)
            except IntegrityError:
                self.session.rollback()
                self._swap_users_conditionally(user)
            except InvalidInputError:
                print("Warning: rolling back on invalid input "
                      f"(email or phone number): user {user['firstname']}",
                      file=sys.stderr)
                self.session.rollback()

    @staticmethod
    def get_importer_for_file(filename):
        """
        :filename: filename together with path
        :return: data importer class for a given filetype
         (based on extension).
        """
        file_extension = get_file_extension(filename).lower()
        match file_extension:
            case ".csv":
                return CSVImporter
            case ".json":
                return JsonImporter
            case ".xml":
                return XMLImporter
            case _:
                raise ValueError(
                    "Unknown file type: "
                    "can only import data from csv, json or xml files.")

    def import_data_from_file(self, filename):
        Importer = self.get_importer_for_file(filename)
        importer = Importer(filename)
        if importer.is_loaded:
            self.feed_data(importer)
        else:
            print(f"Data import error:\n"
                  f"File: {filename}\n"
                  f"Reason message: {importer.fail_reason}",
                  file=sys.stderr)

    def feed_files(self, filenames):
        """
        :param filenames: list of data filenames with paths.
        """
        for file in filenames:
            self.import_data_from_file(file)
