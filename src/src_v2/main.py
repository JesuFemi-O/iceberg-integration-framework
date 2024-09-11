import dlt
import requests
from dlt.common.pipeline import LoadInfo

@dlt.resource(table_name="launches", parallelized=True)
def get_launches():
    # put your code here
    url = "https://api.spacexdata.com/v4/launches"
    response = requests.get(url)
    response.raise_for_status()

    yield response.json()


@dlt.resource(table_name="rockets", parallelized=True)
def get_rockets():
    # put your code here
    url = "https://api.spacexdata.com/v4/rockets"
    response = requests.get(url)
    response.raise_for_status()

    yield response.json()

@dlt.resource(table_name="crew", parallelized=True)
def get_crew():
    # put your code here
    url = "https://api.spacexdata.com/v4/crew"
    response = requests.get(url)
    response.raise_for_status()

    yield response.json()

@dlt.source()
def spacex_api_source():
    return [
        get_launches(),
        get_rockets(),
        get_crew()
    ]

pipeline = dlt.pipeline(
    pipeline_name='spacex_with_source',
    destination='dremio',
    dataset_name='spacex_data',
    progress='log'
)

load_info = pipeline.run(spacex_api_source())
print(load_info)