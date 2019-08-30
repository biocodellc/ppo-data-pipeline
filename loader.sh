PROJECT=$1
if [ -z $PROJECT ]
   then
     echo "Usage: loader.sh {project}"
     echo "Current projects are neon, pep725, npn, herbarium, image_scoring"
     exit 0
fi

# check that we have the latest ...
docker pull jdeck88/ontology-data-pipeline

docker run -t -v "$(pwd)":/process -w=/app -ti jdeck88/ontology-data-pipeline \
    python loader.py \
    --es_input_dir /process/data/$PROJECT/processed/output_reasoned_csv/ \
    --index $PROJECT \
    --drop-existing \
    --alias ppo \
    --host tarly.cyverse.org:80 \
    elasticsearch
