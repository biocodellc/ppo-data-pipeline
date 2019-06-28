PROJECT=$1
if [ -z $PROJECT ]
   then
     echo "Usage: run_test_docker.sh {project}"
     echo "Current projects are neon, pep725, npn, herbarium."
     echo "This bash script runs the pipeline for each of these projects using data in test_data directory" 
     echo "NOTE that this does not actually run the TEST script itself, but is used to run through the pipeline"
     echo "on the test_data... useful for testing the tests"
     exit 0
fi

# check that we have latest docker image
docker pull jdeck88/ontology-data-pipeline

# run the pipeline using docker
docker run -v "$(pwd)":/process -w=/app -ti jdeck88/ontology-data-pipeline \
    python pipeline.py \
    -v --drop_invalid \
    $PROJECT \
    /process/test_data/$PROJECT/input \
    /process/test_data/$PROJECT/output \
    https://raw.githubusercontent.com/PlantPhenoOntology/ppo/master/releases/2018-10-26/ppo.owl \
    /process/config \
    /process/projects \