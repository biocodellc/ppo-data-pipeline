PROJECT=$1
if [ -z $PROJECT ]
   then
     echo "Usage: run.sh {project}"
     echo "Current projects are neon, pep725, npn, herbarium."
     echo "This bash script runs the pipeline for each of these projects" 
     exit 0
fi

python ../ontology-data-pipeline/process.py \
    -v --drop_invalid \
    $PROJECT \
    test_data/$PROJECT/input \
    data/$PROJECT/output \
    file:/Users/jdeck/IdeaProjects/ppo-data-pipeline/config/ppo-merged-reasoned.owl \
    config \
    projects \

#!/bin/sh
python ./process.py test_herbarium test_data/data/test_herbarium/output --input_dir test_data/data/test_herbarium/input --config_dir test_data/config --ontology https://raw.githubusercontent.com/PlantPhenoOntology/ppo/master/releases/2017-10-20/ppo.owl --base_dir test_data/projects/test_herbarium --project_base test_data.projects.test_herbarium --verbose
