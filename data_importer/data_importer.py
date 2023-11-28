class DataImporter:
    """
    Abstract class for data importers (JSON, CSV, XML).
    """
    def __init__(self, filename):
        self.filedata = None
        self.converted_data = None
        self.load_data(filename)

    def load_data(self, filename):
        with open(filename, "r") as file:
            self.filedata = file.read()

    def convert_data(self):
        """
        Convert loaded data into Python dict.
        """
        pass

    def get_data(self):
        if not self.converted_data:
            self.convert_data()
        return self.converted_data
