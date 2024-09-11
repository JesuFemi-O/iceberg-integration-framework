from extraction.extraction_service import ExtractionService


if __name__ == "__main__":
    # Using this script to quickly test completed integrations
    # Example usage for CSV
    file_path = "../sample-data/sample.csv"
    service = ExtractionService(file_path)
    table = service.extract_data()
    print(table)

    # Example usage for JSONL
    file_path = "../sample-data/sample.jsonl"
    service = ExtractionService(file_path)
    table = service.extract_data()
    print(table)
