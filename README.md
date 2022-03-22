
Collection Service
====================

The collection service aims to collect Data IDentifiers of different sources and to provide collections of data identifiers for data-driven web  applications and services in the research context. The data identifiers can be categorized by type, schema, and owner, as depicted by the [architecture](https://drive.google.com/file/d/1vhseWbXVzK9OCsqd00fmZaQ2CEmMfCbi/view?usp=sharing).

# Intended use case

The collection service is intended to serve as a connection between two services, starting with the [GFBio Search](https://www.gfbio.org/search) and [GFBio Visualize](https://www.gfbio.org/visualize), where data identifiers are stored by the search user to later visualization at the second web-service. A service of collection of data identifiers that can be easilyextended to other data-driven web applications.

# Intended users and scope

The intended users are data scientists and graduate students within the community of biodiversity and environmental research. The GFBio DaSS Team develops the collection service within the scope of the National Research Data Infrastructure (NFDI) - [NFDI4Biodiversity](https://www.nfdi4biodiversity.org).
 
# Current development status

The collection service is a web application at initial development stage
and starts with a minimal set of features:

## functional features:
- deploy at the [development server](https://collections.rdc.gfbio.dev)
- stores JSON files that contain collections of data identifiers
- do not require administrator approval for posting or retrieval
- allow authorized users to edit collections and list all users and all API operations
- use [JSON Web Token](https://jwt.io/) for authentication
- identify each the collection by the owner's username
- validate the payload as JSON file
- currently, the JSON payload must contain the *_id* and *hits* attributes of [pansimple](http://ws.pangaea.de/es/portals/pansimple/_search?pretty)  

## non-functional features:
- uses [Django Web](https://github.com/django/django) and [REST](https://github.com/encode/django-rest-framework/tree/master) frameworks.
- uses docker-compose to run multiple background applications:
  - traefik with LetsEncrypt for website certification,
  - redis and celery for handling asynchronous tasks,
  - PostgreSQL (v.13.5) database for storing user and data identifiers.
- uses CI/CD for automatic merge and test pipelines
- include unit tests for CRUD operations
- build API documentation using Swagger UI
- uses bootstrap front-end framework
## Deployment 

Be sure you have following software installed and running:
* [python 3.8+](https://www.python.org/downloads/)
* docker and [docker compose](https://docs.docker.com/compose/install/)

Deployment using docker provides easier isolation and transferability.
After installing the requirements, clone this source, then build and run the stack with docker-compose:
                            
```
git clone git@gitlab.gwdg.de:gfbio/collections.gfbio.org.git
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
curl --header "Content-Type: application/json" --request POST --data 
'{"hits": {"hits": [{"_id": "1234567", "_source": {"data": [3, 2, 1]}}]}}' 
https://collections.rdc.gfbio.dev/collection/collections/
````

- Use the _Swagger_ [API documentation](https://collections.rdc.gfbio.dev/api)

## Access via token

Get the token of an existing user with:

````
curl  \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"username": "gfbio", "password": "biodiversity"}' \
  https://collections.rdc.gfbio.dev/api/token/ | grep -oP "\"access\":(.*?)\}"
````
Then use the token to access the list of users:

````
curl \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQwNzc5ODM5LCJpYXQiOjE2NDA3Nzk1MzksImp0aSI6IjE0ODkzNzFiN2JjODQzZjg5ZTQ2YjU1YTQyZjk1NTJkIiwidXNlcl9pZCI6Mn0.lTabwrxPvTXvqDkvkI-psM1FsMfPS3jaVWNEk1dppx0" \
  https://collections.rdc.gfbio.dev/collection/api/users/
````

## Contribute

Create a [new issue](https://gitlab.gwdg.de/gfbio_collections/-/issues/new?issue%5Bassignee_id%5D=&issue%5Bmilestone_id%5D=)

