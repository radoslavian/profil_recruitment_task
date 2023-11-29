class DataImporter:
    """
    Abstract class for data importers (JSON, CSV, XML).
    """
    def __init__(self, filename):
        self.filedata = None
        self.converted_data = None
        self.is_loaded = False
        self.fail_reason = ""
        self.handle_errors_on_loading(filename)

    def handle_errors_on_loading(self, filename):
        """
        Handles possible errors while loading data.
        """
        try:
            self.load_data(filename)
        except FileNotFoundError as e:
            self.fail_reason = str(e)
        else:
            self.is_loaded = True

    def load_data(self, filename):
        with open(filename, "r") as file:
            self.import_from_file(file)

    def import_from_file(self, file):
        """
        Import data from file into Python dict.
        """
        pass

    def __iter__(self):
        self.current_iter_position = 0
        return self

    def __next__(self):
        try:
            user = self.converted_data[self.current_iter_position]
        except IndexError:
            raise StopIteration
        self.current_iter_position += 1
        return user
