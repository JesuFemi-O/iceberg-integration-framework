import pyarrow.csv as csv
import pyarrow as pa
import pyarrow.json as pajson
from extraction.extractors.base_extractor import BaseExtractor
import json

class CSVExtractor(BaseExtractor):
    def extract(self) -> pa.Table:
        """
        Extract data from a CSV file and return as a PyArrow Table.
        """
        return csv.read_csv(self.file_path)
    
class JSONLExtractor(BaseExtractor):
    def extract(self) -> pa.Table:
        """
        Extract data from a JSONL file and return as a PyArrow Table.
        """
        return pajson.read_json(self.file_path, parse_options=pajson.ParseOptions(newlines_in_values=True))