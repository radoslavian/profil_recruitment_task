from database.database_creator import DatabaseCreator
from database.models import start_engine, drop_all, User
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
