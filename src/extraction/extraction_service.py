from extraction.extractors.file_extractor_factory import FileExtractorFactory
import pyarrow as pa

class ExtractionService:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def extract_data(self) -> pa.Table:
        """
        Extract data from the file using the appropriate extractor.
        """
        extractor = FileExtractorFactory.get_extractor(self.file_path)
        return extractor.extract()
