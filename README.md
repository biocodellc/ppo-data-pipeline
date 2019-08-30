# ppo-data-pipeline

This repository stores configuration information for running the [ontology-data-pipeline](https://github.com/biocodellc/ontology-data-pipeline) for Plant Phenology Data and alignment with the [Plant Phenology Ontology](https://github.com/PlantPhenoOntology/ppo).  To get started, choose either the "Docker Method" or "Non-Docker Method" below: 

# Installation/Setup
[Install docker](https://docs.docker.com/install/) and then clone this repository.  Please refer to the Docker documentation itself if you have troubles getting your docker instance to run.  Once docker is running, you can enter the following:
```
# test pre-processing image_scoring project, using test sources
python projects/image_scoring/data_preprocessor.py test

# run the pipeline, using docker, for the image_scoring project
./run_test_data.sh image_scoring
```

The above scripts illustrate what the processing pipeline looks like. Output should look like:
```
Using default tag: latest
latest: Pulling from jdeck88/ontology-data-pipeline
Digest: sha256:825e59245e652adf0acc8d895d2561ea0f396466be3d5c68aad1771bf7b2f0be
Status: Image is up to date for jdeck88/ontology-data-pipeline:latest
DEBUG:urllib3.connectionpool:Starting new HTTPS connection (1): raw.githubusercontent.com:443
DEBUG:urllib3.connectionpool:https://raw.githubusercontent.com:443 "GET /PlantPhenoOntology/ppo/master/releases/2018-10-26/ppo.owl HTTP/1.1" 200 88716
configuring...
DEBUG:root:	validating 10 records
DEBUG:root:	triplifying 10 records
DEBUG:root:	running reasoner on data_1.ttl
DEBUG:root:reasoning on file /process/test_data/image_scoring/processed/output_unreasoned/data_1.ttl
DEBUG:root:running reasoner with:
DEBUG:root:java -cp /app/process/../lib/ontopilot-2017-08-04.jar:/app/process/../lib/jaxb-api-2.2.3.jar Main -i /process/test_data/image_scoring/processed/output_unreasoned/data_1.ttl -o /process/test_data/image_scoring/processed/output_reasoned/data_1.ttl -c /process/config/reasoner.conf inference_pipeline
INFO:root:reasoned output at test_data/image_scoring/processed/output_reasoned/data_1.ttl
DEBUG:root:	running csv2reasoner on data_1.ttl
DEBUG:root:converting reasoned data to csv for file /process/test_data/image_scoring/processed/output_reasoned/data_1.ttl
DEBUG:root:running query_fetcher with:
DEBUG:root:java -jar /app/process/../lib/query_fetcher-0.0.1.jar -i /process/test_data/image_scoring/processed/output_reasoned/data_1.ttl -inputFormat TURTLE -o /process/test_data/image_scoring/processed/output_reasoned_csv -numThreads 1 -sparql /process/config/fetch_reasoned.sparql
INFO:root:b'    writing /process/test_data/image_scoring/processed/output_reasoned_csv/data_1.ttl.csv\n'
INFO:root:reasoned_csv output at test_data/image_scoring/processed/output_reasoned_csv/data_1.ttl.csv
```

End to end data driven testing is run from the root level directory in the repository using ```pytest```


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
