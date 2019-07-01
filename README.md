# ppo-data-pipeline

This repository stores configuration information for running the [ontology-data-pipeline](https://github.com/biocodellc/ontology-data-pipeline) for Plant Phenology Data and alignment with the [Plant Phenology Ontology](https://github.com/PlantPhenoOntology/ppo).  To get started, choose either the "Docker Method" or "Non-Docker Method" below: 

# Docker Method
[Install docker](https://docs.docker.com/install/) and then clone this repository.  Please refer to the Docker documentation itself if you have troubles getting your docker instance to run.  Once docker is running, you can enter the following:
```
./run_test_docker.sh npn
```

The above runs a small test project through the pipeline... you should see output that looks like:

```
configuring...
DEBUG:urllib3.connectionpool:Starting new HTTPS connection (1): raw.githubusercontent.com:443
DEBUG:urllib3.connectionpool:https://raw.githubusercontent.com:443 "GET /PlantPhenoOntology/ppo/master/releases/2018-10-26/ppo.owl HTTP/1.1" 200 88716
DEBUG:root:	validating 1 records
DEBUG:root:	triplifying 1 records
DEBUG:root:	running reasoner on data_1.ttl
DEBUG:root:reasoning on file /process/test_data/npn/output/output_unreasoned/data_1.ttl
DEBUG:root:running reasonder with:
DEBUG:root:java -jar /app/process/../lib/ontopilot-2019-01-15.jar -i /process/test_data/npn/output/output_unreasoned/data_1.ttl -o /process/test_data/npn/output/output_reasoned/data_1.ttl -c /process/config/reasoner.conf inference_pipeline
INFO:root:reasoned output at test_data/npn/output/output_reasoned/data_1.ttl
DEBUG:root:	running csv2reasoner on data_1.ttl
DEBUG:root:converting reasoned data to csv for file /process/test_data/npn/output/output_reasoned/data_1.ttl
DEBUG:root:running query_fetcher with:
DEBUG:root:java -jar /app/process/../lib/query_fetcher-0.0.1.jar -i /process/test_data/npn/output/output_reasoned/data_1.ttl -inputFormat TURTLE -o /process/test_data/npn/output/output_reasoned_csv -numThreads 1 -sparql /process/config/fetch_reasoned.sparql
INFO:root:b'    writing /process/test_data/npn/output/output_reasoned_csv/data_1.ttl.csv\n'
INFO:root:reasoned_csv output at test_data/npn/output/output_reasoned_csv/data_1.ttl.csv
```

You can find the docker image at [Docker Hub](https://cloud.docker.com/u/jdeck88/repository/docker/jdeck88/ontology-data-pipeline)

If all of the tests pass, update incoming data files in ```data/{project-name}/input/``` and  run the data processor for each project.  A ```run.sh``` script is provided to run each project:

```
# process NPN data
./run.sh npn 
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
