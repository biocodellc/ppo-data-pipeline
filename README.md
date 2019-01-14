# ppo-data-pipeline

**NOTE:** in January of 2019, we refactored the ppo-data-pipeline codebase to store just the configuration files and test framework for processing plant phenologcial data (contained in this repo), and created the [ontology-data-pipeline](https://github.com/biocodellc/ontology-data-pipeline) repository to store all code and logic.  Users wishing to implement the ontology data pipeline for their own purposes should visit the [ontology-data-pipeline](https://github.com/biocodellc/ontology-data-pipeline) repository. 

To get started, first follow the installation instructions at [ontology-data-pipeline](https://github.com/biocodellc/ontology-data-pipeline). Once you have installed the ontology-data-pipeline, you should be able to fork this repository, which contains the configuration files to run the ontology data pipeline for plant phenological data, and run the tests to ensure that the environment is working properly:

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
