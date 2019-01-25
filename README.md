# ppo-data-pipeline

**NOTE:** in January of 2019, we refactored the ppo-data-pipeline codebase to store just the configuration files and test framework for processing plant phenologcial data (contained in this repo), and created the [ontology-data-pipeline](https://github.com/biocodellc/ontology-data-pipeline) repository to store all code and logic.  Users wishing to implement the ontology data pipeline for their own purposes should visit the [ontology-data-pipeline](https://github.com/biocodellc/ontology-data-pipeline) repository. 

To get started, choose one of two paths, outlined below and follw the instructions.  

# Docker Method
[Install docker](https://docs.docker.com/install/) and then clone this repository.  Once that is done, you can enter the following:
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

If all of the tests pass, update incoming data files in ```data/{project-name}/input/``` and  run the data processor for each project.  A ```run_docker.sh``` script is provided to run each project:

```
./run_docker.sh npn
```

# Non-docker Method
First follow the installation instructions at [ontology-data-pipeline](https://github.com/biocodellc/ontology-data-pipeline). Once you have installed the ontology-data-pipeline, you should be able to fork this repository, which contains the configuration files to run the ontology data pipeline for plant phenological data, and run the tests to ensure that the environment is working properly:

```pytest``` 

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

Some information about the ppo-data-pipeline is mentioned in:

[Brian J. Stucky, Rob Guralnick, John Deck, Ellen G. Denny, Kjell Bolmgren, and Ramona Walls. *The Plant Phenology Ontology: A New Informatics Resource for Large-Scale Integration of Plant Phenology Data*, Front Plant Sci. 2018; 9: 517, doi: 10.3389/fpls.2018.00517](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5938398/)
