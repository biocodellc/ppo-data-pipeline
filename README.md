# ppo-data-pipeline

This repository contains configuration files and scripts to process plant phenological data using the [ontology-data-pipeline](https://github.com/biocodellc/ontology-data-pipeline).  Note that in January of 2019, we refactored the ppo-data-pipeline codebase to store just the configuration files and test framework to run plant phenological data through the ontology-data-pipeline application, which contains just the code logic to process this data.

To get started, first follow the installation instructions at [ontology-data-pipeline](https://github.com/biocodellc/ontology-data-pipeline). Once you have installed the ontology-data-pipeline, you should be able to fork this repository and run the tests to ensure that the environment is working properly:

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
