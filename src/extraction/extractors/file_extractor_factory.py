from extraction.extractors.base_extractor import BaseExtractor
from extraction.extractors.flat_file_extractors import CSVExtractor, JSONLExtractor

class FileExtractorFactory:
    @staticmethod
    def get_extractor(file_path: str) -> BaseExtractor:
        """
        Return the appropriate extractor based on the file extension.
        """
        if file_path.endswith('.csv'):
            return CSVExtractor(file_path)
        elif file_path.endswith('.jsonl'):
            return JSONLExtractor(file_path)
        else:
            raise ValueError("Unsupported file format")
