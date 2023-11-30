from sqlalchemy.exc import IntegrityError

from database.models import start_engine, drop_all, User, Child
from utils.exceptions import InvalidInputError
from utils.helpers import convert_datetime, normalize_telephone_num
from utils.security import generate_password_hash


class DatabaseManager:
    def __init__(self, engine_url="sqlite:///:memory:"):
        self.engine, self.session = start_engine(engine_url)

    def drop_all(self):
        drop_all(self.engine)

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
        new_user = User(
            email=user["email"],
            firstname=user["firstname"],
            telephone_number=normalize_telephone_num(
                user["telephone_number"]),
            password_hash=generate_password_hash(user["password"]),
            created_at=convert_datetime(user["created_at"])
        )
        self._add_children(user["children"], parent=new_user)
        self.session.add(new_user)
        self.session.commit()

    def _swap_users_conditionally(self, user):
        """
        Add a user (or keep already existing) with a newer creation date
        to the database.
        """
        user_in_db = self.session.get(User, user["email"])
        if convert_datetime(user["created_at"]) > user_in_db.created_at:
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
                self.session.rollback()
                continue

    def feed_files(self, filenames):
        """
        :param filenames: list of data filenames with paths.
        """
        pass
