PROJECT=$1 
if [[ -z $PROJECT ]] 
   then
     echo "Usage: non_docker_run.sh {PROJECT}"
     echo ""
     echo "This bash script runs the pipeline for any INPUT_DATAFILE and places output in the specified OUTPUT_DIRECTORY."
     exit 0
fi

    python ../ontology-data-pipeline/pipeline.py \
    -v --drop_invalid \
    data/$PROJECT/processed/data.csv \
    data/$PROJECT/processed \
    file:/Users/jdeck/IdeaProjects/ppo-data-pipeline/config/ppo.owl \
    config \
