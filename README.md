# ppo-data-pipeline

This repository stores configuration information for running the [ontology-data-pipeline](https://github.com/biocodellc/ontology-data-pipeline) for Plant Phenology Data and alignment with the [Plant Phenology Ontology](https://github.com/PlantPhenoOntology/ppo).  To get started, choose either the "Docker Method" or "Non-Docker Method" below: 

# Installation/Setup
[Install docker](https://docs.docker.com/install/) and then clone this repository.  Please refer to the Docker documentation itself if you have troubles getting your docker instance to run.  Once docker is running, you can enter the following:
```
pytest
```

The above runs tests for at least one of the projects and will confirm if things are working

```

You can find the docker image at [Docker Hub](https://cloud.docker.com/u/jdeck88/repository/docker/jdeck88/ontology-data-pipeline)

If all of the tests pass, you can started processing each project

```
# process NPN data
cd projects/npn
# fetch NPN data and store in data/npn/input/
python data_fetcher.py
# pre-process NPN data, specifying the chunk-size to use in pre-processor (suggest 50,000)
# stores output data/npn/output/data.csv
python data_preprocessor.py 50000
# run the pipeline
cd ../..
./run.sh data/npn/output/data.csv data/npn/output

# process PEP725 data
./run.sh pep725 
# process neon data
./run.sh neon
# process herbarium data
./run.sh herbarium
```

# Updating data
Some of the projects contain scripts which help you fetch data from source API's.  You will need to run these scripts using python:

```
# updating neon
cd projects/neon
python data_fetcher.py  ../../data/neon/input

# updating npn
cd projects/npn
python data_fetcher.py  ../../data/npn/input
```

Some information about the ppo-data-pipeline is mentioned in:

[Brian J. Stucky, Rob Guralnick, John Deck, Ellen G. Denny, Kjell Bolmgren, and Ramona Walls. *The Plant Phenology Ontology: A New Informatics Resource for Large-Scale Integration of Plant Phenology Data*, Front Plant Sci. 2018; 9: 517, doi: 10.3389/fpls.2018.00517](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5938398/)
