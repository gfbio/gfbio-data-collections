
Collection Service
====================

# NFDI collection service for Data Identificators

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
git clone https://gitlab.gwdg.de/gfbio/nfdi_collection.git
cd nfdi_collection
docker-compose -f local.yml build
docker-compose -f local.yml up
``` 


## Contribute

Create a [new issue](https://gitlab.gwdg.de/gfbio/nfdi_collection/-/issues/new?issue%5Bassignee_id%5D=&issue%5Bmilestone_id%5D=) 
