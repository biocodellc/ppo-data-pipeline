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
    data/$PROJECT/input/ \
    data/$PROJECT/output/ \
    https://raw.githubusercontent.com/PlantPhenoOntology/ppo/master/releases/2018-10-26/ppo.owl \
    config/ \
    projects/ \
