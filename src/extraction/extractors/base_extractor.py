import pyarrow as pa

class BaseExtractor:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def extract(self) -> pa.Table:
        """
        Extract data from the file and return as a PyArrow Table.
        Must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses should implement this method")
