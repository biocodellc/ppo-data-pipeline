PROJECT=$1

if [[ -z $PROJECT ]]
   then
     echo "Usage: run.sh {PROJECT}"
     echo ""
     echo "This bash script runs the pipeline for any INPUT_DATAFILE and places output in the specified OUTPUT_DIRECTORY."
     exit 0
fi

# check that we have the latest ...
docker pull jdeck88/ontology-data-pipeline

docker run -v "$(pwd)":/process -w=/app -i jdeck88/ontology-data-pipeline \
    python pipeline.py \
    -v --drop_invalid \
    /process/data/$PROJECT/processed/data.csv \
    /process/data/$PROJECT/processed \
    https://raw.githubusercontent.com/PlantPhenoOntology/ppo/master/releases/2019-01-16/ppo.owl \
    /process/config \

