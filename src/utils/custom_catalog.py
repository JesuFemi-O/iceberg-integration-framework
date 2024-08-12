from pyiceberg.catalog import Catalog
from pyiceberg.catalog.hive import HiveCatalog

def load_catalog(catalog_type: str, catalog_name: str, properties: dict) -> Catalog:
    """
    Custom function to load an Iceberg catalog.

    Parameters:
    - catalog_type: The type of catalog to load (only 'hive_catalog' is supported).
    - catalog_name: The name of the catalog.
    - properties: A dictionary of properties required to configure the catalog.

    Returns:
    - Catalog: An instance of the Iceberg Catalog.

    Raises:
    - NotImplementedError: If the catalog_type is not 'hive_catalog'.
    """
    if catalog_type == 'hive_catalog':
        return HiveCatalog(name=catalog_name, **properties)
    else:
        raise NotImplementedError(f"Catalog type '{catalog_type}' is not supported. Only 'hive_catalog' is implemented.")
