import dlt
import pyarrow as pa
import pandas as pd

def create_rest_api_source(api_url: str, params: dict = None):
    """
    Creates a dlt REST API source that fetches data from the specified API.

    Parameters:
    - api_url: The endpoint of the REST API.
    - params: Query parameters for the API.

    Returns:
    - A dlt source that can be iterated to yield data.
    """
    config = {
        "client": {
            "base_url": api_url,
            "headers": {"Authorization": "Bearer YOUR_TOKEN"},  # Example header
            "paginator": {
                "type": "json_link",
                "next_url_path": "pagination.next"
            }
        },
        "resource_defaults": {
            "primary_key": "id",
            "write_disposition": "merge",
            "endpoint": {
                "params": params
            }
        },
        "resources": [
            {
                "name": "data",
                "endpoint": {
                    "path": "data",
                    "params": {
                        "per_page": 100,
                        "sort": "updated"
                    }
                }
            }
        ]
    }

    return dlt.source(config)

class APIExtractor:
    def __init__(self, api_url: str, params: dict = None):
        self.api_url = api_url
        self.params = params

    def extract(self) -> pa.Table:
        """
        Extract data from a REST API using dlt and convert it to a PyArrow Table.
        """
        source = create_rest_api_source(self.api_url, self.params)
        pipeline = dlt.pipeline(pipeline_name="api_pipeline", destination="duckdb", dataset_name="api_data")

        # Run the pipeline and capture the output
        # So the good thing is dlt pipeline.run() is a wrapper around 3 operationns which you can run individually
        # pipeline.extract() -> fetch the data from the source and temporarily wirte to local files
        # pipeline.normalize() -> handles normalisations with local files and writes backt local files
        # pipeline.load() -> writes the data into a destination and probably cleans up temp local files
        # There just might be a chance to get dlt to extract the data, intercept the raw data and stop dlt here, 
        # but we need to understand at what point dlt updates state information
        pipeline.run(source)

        # Convert the yielded data to a Pandas DataFrame and then to a PyArrow Table
        data_frames = [pd.DataFrame(entry) for entry in source()]
        combined_df = pd.concat(data_frames, ignore_index=True)
        return pa.Table.from_pandas(combined_df)
