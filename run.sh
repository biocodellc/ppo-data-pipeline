PROJECT=$1 
if [[ -z $PROJECT ]] 
   then
     echo "Usage: non_docker_run.sh {PROJECT}"
     echo ""
     echo "This bash script runs the pipeline for any INPUT_DATAFILE and places output in the specified OUTPUT_DIRECTORY."
     exit 0
fi

echo "processing incoming data file data/$PROJECT/processed/data.csv" 

    python ../ontology-data-pipeline/pipeline.py \
    -v --drop_invalid \
    --num_processes 1 \
    data/$PROJECT/processed/data.csv \
    data/$PROJECT/processed \
    file:/Users/jdeck/IdeaProjects/ppo-data-pipeline/config/ppo.owl \
    config \
