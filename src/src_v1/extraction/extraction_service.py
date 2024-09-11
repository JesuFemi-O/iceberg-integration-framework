from extraction.extractors.file_extractor_factory import FileExtractorFactory
from extraction.extractors.api_extractor import APIExtractor
import pyarrow as pa

class ExtractionService:
    def __init__(self, file_path: str = None, api_url: str = None, params: dict = None):
        self.file_path = file_path
        self.api_url = api_url
        self.params = params

    def extract_data(self) -> pa.Table:
        """
        Extract data from the specified source (either a file or API) and return as a PyArrow Table.
        """
        if self.file_path:
            extractor = FileExtractorFactory.get_extractor(self.file_path)
        elif self.api_url:
            extractor = APIExtractor(self.api_url, self.params)
        else:
            raise ValueError("Either file_path or api_url must be provided.")

        return extractor.extract()
