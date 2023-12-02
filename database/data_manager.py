import re

from database.database_creator import DatabaseCreator
from database.models import start_engine, drop_all, User, Child
from utils.exceptions import AuthenticationError
from utils.helpers import list_files_for_import
from utils.validators import email_regex, telephone_num_regex


class DataManager:
    def __init__(self, database_url="sqlite:///:memory:"):
        self.engine, self.session = start_engine(database_url)
        self.database_creator = DatabaseCreator(self.session)
        self._authenticated_user = None

    def log_in(self, login, password):
        user = None
        user_query = self.session.query(User)

        if re.fullmatch(email_regex, login):
            user = user_query.filter_by(email=login).first()
        elif re.fullmatch(telephone_num_regex, login):
            user = user_query.filter_by(telephone_number=login).first()

        if user is not None and user.verify_password(password):
            self._authenticated_user = user
        else:
            raise AuthenticationError

    def drop_database(self):
        drop_all(self.engine)

    def create_database(self, toplevel_dir):
        file_extensions = [".xml", ".json", ".csv"]
        files_for_import = list_files_for_import(
            toplevel_dir, file_extensions)
        self.database_creator.feed_files(files_for_import)

    def accounts_total_number(self):
        """
        Print The Number of All Valid Accounts
        """
        return self.session.query(User).count()

    def get_oldest_account(self):
        """
        Information about account with the longest existence.
        :return: User object
        """
        return self.session.query(User).order_by(User.created_at).first()

    def group_children_by_age(self):
        children = self.session.query(Child)
        unique_ages = {
            child.age for child in children
        }
        age_distribution = [
            {
                "age": age,
                "count": children.filter_by(age=age).count()
            } for age in sorted(unique_ages)
        ]
        age_distribution.sort(key=lambda item: item["count"])

        return age_distribution

    def get_children(self):
        """
        Return information about the user's children.
        :return: alphabetically sorted query object
        """
        return self._authenticated_user.children.order_by(Child.name)

    def users_w_similar_aged_children(self):
        """
        Find users with children of the same age as at least one child
        ownd by the user.
        """
        user = self._authenticated_user
        user_children_ages = {child.age for child in user.children}
        all_children = self.session.query(Child)
        children_with_similar_ages = all_children.filter(
            Child.age.in_(user_children_ages)).filter(
            Child.parent_id != user.email)  # excluding user's children
        parents = {
            child.parent for child in children_with_similar_ages
        }
        parents_children = {
            parent: sorted(
                [child for child in parent.children
                 if child in children_with_similar_ages],
                key=lambda c: c.name)
            for parent in parents
        }

        return parents_children
