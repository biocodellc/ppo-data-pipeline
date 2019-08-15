# Project Processing

Contains a directory for each project incoming data source
Contains code for pre-processing data.  Incoming Data should be:
  * 2d structure (flat file)
  * Define trait mappings to ontologies, as, e.g. {ripe fruit presence}
  * map all columns defined in config/mapping.csv

The {ROOT} in the context of projects/{PROJECT}
{ROOT} should be defined as "../../"

All incoming data referenced by projects is stored with the following structure:
{ROOT}/data/{PROJECT}/input

All outgoing data referenced by projects is stored with the following structure:
{ROOT}/data/{PROJECT}/output/data.csv
