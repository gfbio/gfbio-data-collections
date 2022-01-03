
Collection Service
====================

# Current development status

The collection service:

- runs at the GWDG [server](https://c103-114.cloud.gwdg.de/api)
- does not require administrator approval for posting or signing up. 
- uses JWT for token authentication
- receives a POST request and validate a JSON file based on "_pysample.xml"
- runs a PostgreSQL (v.13.5) to respond with the entry ID at each POST request.
- includes unit test stage for user and collection models and serializers

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
git clone https://gitlab.gwdg.de/gfbio/gfbio_collections.git
cd gfbio_collections
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
[browsable API](https://c103-114.cloud.gwdg.de/api)

- Use the [API documentation](https://c103-114.cloud.gwdg.de/swagger)

## Access via token

Get the token of an existing user with:

````
curl  \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"username": "gfbio", "password": "biodiversity"}' \
  http://localhost:8000/api/token/ | grep -oP "\"access\":(.*?)\}"
````
Then use the token to access the list of users:

````
curl \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQwNzc5ODM5LCJpYXQiOjE2NDA3Nzk1MzksImp0aSI6IjE0ODkzNzFiN2JjODQzZjg5ZTQ2YjU1YTQyZjk1NTJkIiwidXNlcl9pZCI6Mn0.lTabwrxPvTXvqDkvkI-psM1FsMfPS3jaVWNEk1dppx0" \
  http://localhost:8000/api/users/
````

## Contribute

Create a [new issue](https://gitlab.gwdg.de/gfbio_collections/-/issues/new?issue%5Bassignee_id%5D=&issue%5Bmilestone_id%5D=)

