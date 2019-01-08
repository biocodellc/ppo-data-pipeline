# ppo-data-pipeline

This repository contains the configuration files and scripts to run the Plant Phenology Ontology data pipeline.  

To get started, follow the installation instructions at [ontology-data-pipeline](https://github.com/biocodellc/ontology-data-pipeline). Once you have installed the ontology-data-pipeline, you should be able to fork this repository and run the tests to ensure that the environment is working properly:

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



