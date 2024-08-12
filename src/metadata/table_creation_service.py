from pyarrow import Table as PyArrowTable
from pyiceberg.schema import Schema as IcebergSchema

class TableCreationService:
    def __init__(self, catalog_name: str, catalog_loader):
        self.catalog = catalog_loader(catalog_type="hive_catalog", catalog_name=catalog_name, properties={})
    
    def create_or_replace_table(self, namespace: str, table_name: str, arrow_table: PyArrowTable):
        full_table_name = f"{namespace}.{table_name}"

        if namespace.endswith("_staging"):
            self._create_or_replace_staging_table(full_table_name, arrow_table)
        else:
            self._create_production_table_if_not_exists(full_table_name, arrow_table)

    def _create_or_replace_staging_table(self, full_table_name: str, arrow_table: PyArrowTable):
        if self.catalog.table_exists(full_table_name):
            self.catalog.drop_table(full_table_name)
        self.catalog.create_table(full_table_name, schema=arrow_table.schema)

    def _create_production_table_if_not_exists(self, full_table_name: str, arrow_table: PyArrowTable):
        if not self.catalog.table_exists(full_table_name):
            self.catalog.create_table(full_table_name, schema=arrow_table.schema)
