# Building an ETL Integration stack with DLT and Dremio

![Architecture](../../docs/assets/v2-archi.png)

This version of my project adopts dlthub for data ingestion and loading into my iceberg tables.

rather building a common interface for sources I'm leveraging as much as possible a single tool. which would handle extraction, normalization, schema evolution, and loading into my datalake.

## Setting up The stack

notes about how to connect minio and nessie to dremio.

## configuring DLT


1. add a secrets.toml file to the .dlt folder

```
[destination.filesystem]
bucket_url = "s3://landing" # replace with your bucket name,

[destination.filesystem.credentials]
aws_access_key_id = "minioadmin"
aws_secret_access_key = "minioadmin"
endpoint_url = "http://localhost:9000"

[destination.dremio]
staging_data_source = "source_landing_stage" 

[destination.dremio.credentials]
database = "nessie" # can change to anything you name your catalog integration in dremio
password = "<ENTER PASSWORD>"
username = "<ENTER USERNAME>"
host = "localhost"
port = 32010
```

notes about how to configure your secrets.toml file and install the requirements.txt