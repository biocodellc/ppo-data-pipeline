# ppo-data-pipeline

Process data for the [Global Plant Phenology Data Portal](https://plantphenology.org/).  This repository accumulates data from partners, processes it (in python) and then runs the [ontology-data-pipeline](https://github.com/biocodellc/ontology-data-pipeline) to process inferences and aggregate data. The pipeline calls the [Plant Phenology Ontology](https://github.com/PlantPhenoOntology/ppo) for term annotation.  

# Installation/Setup

# test pre-processing image_scoring project, using test sources
cd test_data
./test.sh

# Updating data
Some of the projects contain scripts which help you fetch data from source API's.  You will need to run these scripts using python:

```
# updating npn (NPN contains NEON data)
cd projects/npn
python data_fetcher.py  ../../data/npn/input
```

# Pre-processing data

Following is an example using NPN data:

```
# process NPN data
# This assumes that you have data processed and living in ../../data/npn/processed
cd projects/npn

# first make sure the 'processed' directory exists under /data/npn/.  If not, then create it:
mkdir ../../data/npn/processed

# pre-process NPN data, specifying the chunk-size to use in pre-processor 
# stores output data/npn/output/data.csv
python data_preprocessor.py 150000
cd ../..
./run.sh npn

# Loading Data
If you choose to load data into an elasticsearch instance, you can run the loader script
```
# if you are running on a desktop and want to load from a remote server, you will want to execute
# a command similar to this:
cd data
tar zcvf - data/npn/processed/output_reasoned_csv/* | ssh -l exouser 149.165.159.216 "cd /home/jdeck/data/ppo; tar xvzf -"

# ssh to remote server, checkout a copy of this code and run:
./loadit.sh
```

Some information about the ppo-data-pipeline is mentioned in:

[Brian J. Stucky, Rob Guralnick, John Deck, Ellen G. Denny, Kjell Bolmgren, and Ramona Walls. *The Plant Phenology Ontology: A New Informatics Resource for Large-Scale Integration of Plant Phenology Data*, Front Plant Sci. 2018; 9: 517, doi: 10.3389/fpls.2018.00517](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5938398/)
