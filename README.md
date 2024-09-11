# iceberg-integration-framework

Building a simple end-to-end ingestion framework. This work is inspired by my work on [hacking-apache-iceberg](https://github.com/JesuFemi-O/hacking-apache-iceberg). 

I have created this repo to help me not drift away from my goal of piecing together and easy to follow open-tutorial on getting started with apache iceberg. 

The decisions in the hacking-apache-iceberg repo will directly influnce this work since the framework will be powered by the stack from that repo.

# Levraging another tool

So after careful consideration of the architecture I highlighted in [v1](./src/src_v1/), it has become pretty clear that I may be largely reinventing the wheel on may grounds. Most of the Stuff I want to achieve with this framework is already done out of the box with an existing framework called [DLT](https://dlthub.com/).

1. The idea that I should have a uniform interface that can ingest data from any kind of source such that the logic of the source can be abstracted away as an implementation detail is already possible through DLT

2. DLT integerates with all the sources I have identified here (relational DB, API, File-like systems like GCS, S3, Local file system, etc)

3. DLT gracefullt handles schema evolution (through a process called normalization & schema contracts)

4. DLT comes with multiple write dispositions (replace, merge, append) whcih means it can handle incremental loads

5. DLT can handle backfills

6. DLT supports apache Iceberg tables via it's Athena and Dremio destinations

7. If you have a destination in mind not yet officially supported, DLT can be extended to build your own custom destination

8. Becasue DLT is pythonic and open source, it's a great choice for technical maintainers as they can extend it to build custom source and destinations. It's also great for non-technical folks because once a source or destination exists it's fairly easy to run dlt


## levraging DLT and Dremio

Although I started out this project with some rather novel ideas on what my framework should look like, I spent most of August learning about the DLT framework.

There were a lot of simillarities to how DLT handle data integration and the way I was thinking about it. The really cool thing with DLT which was a big win for me was that it handled schema normalization and evolution out of the box and it could also handle different types of write dispositions (full loads, incremental loads with different merge strategies) and it could also handle backfills. DLT also had data contracts built into them making it more attractive to me.

so rather than re-inventing the wheel, it made the most sense to invest time in figuring out how I could levrage dlt in my framework.

The idea here would be that dlt would be the singular interface to handle any kind of source data I had to deal with and will write to my iceberg table.

The challenge initially was finding a way to get dlt to write to iceberg but then it turns out it's actually capable of writing to iceberg via dremio.

Dremio is able to connecto to a nessie catalog and also a hive catalog/metastore.

DLT requires data from your source to be written to object storage and copied from object storage into your iceberg table.

Behind the scene dlt uses arrow flight to talk to dremio (This is just FYI for me as i'll be spending time learning about the apache arrow project after I am able to stand this framework up.)


### Framework Architecture

![Architecture](./docs/assets/v2-archi.png)

dlt makes it extremely easy to write custom sources so if we have any new source there can always to two options:

1. Implement a custom source in dlt
2. write to object storage and allow dlt handle the load from object storage to your iceberg tables.

DLT's approach to writing to iceberg tables follows a data staging pattern where data is written to an intermediate storgae location and copied from there into your iceberg table.

as at the time of this writing I also learnt that airbyte has an integration for iceberg making it attractive for me.

DLT's trick IMO with dremio is that dremio can read from many different sources including object storage and it's not hard for dremio to copy data from object storage in parquet format into iceberg.


### Building a custom Iceberg destination

So this piece isn't 100% figured out at this point but basically a generic custom destination that supports catalogs like REST, Hive Metadata catalog, nessie, etc. would be great.

I've been thinking about what the destination should look like and in theory I guess the idea would be to implement an interface that let's dlt:

1. Figiure out what catalog it needs to talk to
2. check that the metadata (data schema, table name, etc) it has about incoming data can somehow be verified against the catalog
3. create a table with required information if it doesn't exist
4. perform DML operations on an existing table based on the state data, write disposiiton, etc.

If I can implement a destination that can somehow enable dlt to perform all these operations I think I'd have created a truly generic iceberg destination. There's also the trouble of figuring out what mechnism to use to talk to iceberg and it's catalog because pyiceberg is currently limited in what it's capable of doing as I've highlighted in previous sections of this doc.


### Notes on Apache Arrow Flight

I think that learning about flight and how it works would be greatly beneficial in the long run since it's how dlt communicate with dremio, once I understand the protocol it might just be easier to build a destination that talks to a rest catalog. Still a wild idea but one worth chasing I guess.