# ppo-data-pipeline

This repository contains the configuration files and scripts to run the Plant Phenology Ontology data pipeline.  

To get started, follow the installation instructions at [ontology-data-pipeline](https://github.com/biocodellc/ontology-data-pipeline). Once everything is installed, you should be able to simply run ```pytest``` to see that everything is working.

Once you have verified with the tests that everything is working, you can first update incoming data files in data/{project-name}/input/ and then run the data processor for each project, like:

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



