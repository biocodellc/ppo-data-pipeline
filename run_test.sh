PROJECT=$1
if [ -z $PROJECT ]
   then
     echo "Usage: run_test.sh {project}"
     echo "Current projects are neon, pep725, npn, herbarium."
     echo "This bash script runs the pipeline for each of these projects using data in test_data directory" 
     exit 0
fi

python ../ontology-data-pipeline/process.py \
    -v --drop_invalid \
    $PROJECT \
    test_data/$PROJECT/input \
    test_data/$PROJECT/output \
    file:/Users/jdeck/IdeaProjects/ppo-data-pipeline/config/ppo-merged-reasoned.owl \
    config \
    projects \

