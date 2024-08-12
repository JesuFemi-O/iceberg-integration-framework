from extraction.extraction_service import ExtractionService
from metadata.table_creation_service import TableCreationService
from utils.custom_catalog import load_catalog

def main():
    # Example usage
    extraction_service = ExtractionService("sample-data/sample.csv")
    table_creation_service = TableCreationService(
        catalog_name="my_catalog",
        catalog_loader=load_catalog
    )
    
    # Extract data
    arrow_table = extraction_service.extract_data()
    
    # Create or replace the table in the staging namespace
    table_creation_service.create_or_replace_table(
        namespace="my_namespace_staging",
        table_name="sample_table",
        arrow_table=arrow_table
    )

    # Create the table in the production namespace if it doesn't exist
    table_creation_service.create_or_replace_table(
        namespace="my_namespace",
        table_name="sample_table",
        arrow_table=arrow_table
    )

if __name__ == "__main__":
    main()