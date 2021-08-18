# NFDI service for collection of Data IDs

This project aims to collect Data IDs of different sources and provide the Data IDs for researcher applications and services.
The Data IDs can be categorized by type, schema, and owner, as depicted by the
[diagram](https://drive.google.com/file/d/1vhseWbXVzK9OCsqd00fmZaQ2CEmMfCbi/view?usp=sharing) and
[outline](https://gitlab.gwdg.de/gfbio/collections.gfbio.org/-/issues/14/designs/IMG_20210708_141625_1.jpg).

Current implementation is a software stack based on Django web and REST frameworks.

## Requirements 

Be sure you have following software installed and running:
* [python 3.8+](https://www.python.org/downloads/)
* docker and [docker compose](https://docs.docker.com/compose/install/)

## Deployment

Deployment using docker provides easier isolation and transferability.
After installing the requirements, clone this source, then build and run the stack with docker-compose:
                            
```
git clone https://gitlab.gwdg.de/gfbio/gfbio_collections.git
cd collections.gfbio.org
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
curl --header "Content-Type: application/json" --request POST --data '{"collection_name": "sample test", "payload": { "anykey": "anyvalue","anykey2": {"anyvalue": "orsubdict"}}}' https://c103-139.cloud.gwdg.de/api/collections/ 
````
- Use the 
[browsable API](https://c103-139.cloud.gwdg.de/root)

- Use the [API documentation](https://c103-139.cloud.gwdg.de/api)


## Contribute

Create a [new issue](https://gitlab.gwdg.de/gfbio/gfbio_collections/-/issues/new?issue%5Bassignee_id%5D=&issue%5Bmilestone_id%5D=) 

 
