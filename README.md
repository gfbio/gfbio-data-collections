
Collection Service
====================

# Collection service for Data Identifiers

This project aims to collect Data IDs of different sources and provide the Data IDs for researcher applications and services.
The Data IDs can be categorized by type, schema, and owner, as depicted by the
[architecture](https://drive.google.com/file/d/1vhseWbXVzK9OCsqd00fmZaQ2CEmMfCbi/view?usp=sharing). 

Current implementation is a software stack based on Django web and REST frameworks.

## Requirements 

Be sure you have following software installed and running:
* [python 3.8+](https://www.python.org/downloads/)
* docker and [docker compose](https://docs.docker.com/compose/install/)

## Deployment

Deployment using docker provides easier isolation and transferability.
After installing the requirements, clone this source, then build and run the stack with docker-compose:
                            
```
git clone https://gitlab.gwdg.de/gfbio/gfbio_collectionss.git
cd collection.gfbio.org
docker-compose -f production.yml build
docker-compose -f production.yml up
``` 

## Usage

Test the service by sending a JSON payload to the database, as follows:

- Use curl:
````console
# GET collections
curl --header "Content-Type: application/json" --request GET https://c103-139.cloud.gwdg.de/api/collections/

# POST collection
curl --header "Content-Type: application/json" --request POST --data '{"collection_owner": "00N", "collection_payload": { "anykey": "anyvalue","anykey2": {"anyvalue": "orsubdict"}}}' https://c103-139.cloud.gwdg.de/api/collections/ 
````
- Use the 
[browsable API](https://c103-139.cloud.gwdg.de/api)

- Use the [API documentation](https://c103-139.cloud.gwdg.de/swagger)


## Contribute

Create a [new issue](https://gitlab.gwdg.de/gfbio/nfdi_collection/-/issues/new?issue%5Bassignee_id%5D=&issue%5Bmilestone_id%5D=)
