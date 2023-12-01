from database.database_creator import DatabaseCreator
from database.models import start_engine, drop_all, User, Child
from utils.helpers import list_files_for_import


class DataManager:
    def __init__(self, database_url="sqlite:///:memory:"):
        self.engine, self.session = start_engine(database_url)
        self.database_creator = DatabaseCreator(self.session)

    def drop_database(self):
        drop_all(self.engine)

    def create_database(self, toplevel_dir):
        file_extensions = [".xml", ".json", ".csv"]
        files_for_import = list_files_for_import(
            toplevel_dir, file_extensions)
        self.database_creator.feed_files(files_for_import)

    def accounts_total_number(self):
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
        return age_distribution

    @staticmethod
    def get_children(user):
        """
        Return information about the user's children.
        :param user: database.models.User instance
        :return: alphabetically sorted query object
        """
        return user.children.order_by(Child.name)

    def users_w_similar_aged_children(self, user):
        """
        Find users with children of the same age as at least one child
        ownd by the user.
        """
        user_children_ages = {child.age for child in user.children}
        all_children = self.session.query(Child)
        children_with_similar_ages = all_children.filter(
            Child.age.in_(user_children_ages)).filter(
            Child.parent_id != user.email)  # excluding user's children
        children_parents = {
            child.parent for child in children_with_similar_ages
        }

        return sorted(children_parents, key=lambda p: p.firstname)
