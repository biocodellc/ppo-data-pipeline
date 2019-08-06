PROJECT=$1

if [[ -z $PROJECT]] 
   then
     echo "Usage: run.sh {PROJECT}"
     echo ""
     echo "This bash script runs the pipeline for any PROJECT."
     exit 0
fi


# check that we have the latest ...
docker pull jdeck88/ontology-data-pipeline

docker run -v "$(pwd)":/process -w=/app -i jdeck88/ontology-data-pipeline \
    python pipeline.py \
    -v --drop_invalid \
    --project_base /process/projects \
    --input_dir /process/data/$PROJECT/input/ \
    --project $PROJECT \
    /process/data/npn/output \
    https://raw.githubusercontent.com/PlantPhenoOntology/ppo/master/releases/2018-10-26/ppo.owl \
    /process/config \

