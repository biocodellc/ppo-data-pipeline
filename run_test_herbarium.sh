#!/bin/sh
python ./process.py test_herbarium test_data/data/test_herbarium/output --input_dir test_data/data/test_herbarium/input --config_dir test_data/config --ontology https://raw.githubusercontent.com/PlantPhenoOntology/ppo/master/releases/2017-10-20/ppo.owl --base_dir test_data/projects/test_herbarium --project_base test_data.projects.test_herbarium --verbose
