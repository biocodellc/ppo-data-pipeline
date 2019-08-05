PROJECT=$1
if [ -z $PROJECT ]
   then
     echo "Usage: sample_data.sh {project}"
     echo "Current projects are neon, pep725, npn, herbarium."
     echo "This script runs the pipeline for minimal examples of each of the projects."
     echo "...NOT a substitute for real tests"
     exit 0
fi

# check that we have latest docker image
docker pull jdeck88/ontology-data-pipeline

# run the pipeline using docker
docker run -v "$(pwd)":/process -w=/app -ti jdeck88/ontology-data-pipeline \
    python pipeline.py \
    -v --drop_invalid \
    --project $PROJECT \
    --project_base /process/projects \
    --input_dir /process/sample_data/$PROJECT/input/ \
    /process/sample_data/$PROJECT/output \
    https://raw.githubusercontent.com/PlantPhenoOntology/ppo/master/releases/2018-10-26/ppo.owl \
    /process/config \

