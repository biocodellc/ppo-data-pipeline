#INPUT_DATAFILE=$1
#OUTPUT_DIRECTORY=$2

#if [[ -z $INPUT_DATAFILE ]] || [[ -z $OUTPUT_DIRECTORY ]]
#   then
#     echo "Usage: run.sh {INPUT_DATAFILE} {OUTPUT_DIRECTORY}"
#     echo ""
#     echo "This bash script runs the pipeline for any INPUT_DATAFILE and places output in the specified OUTPUT_DIRECTORY."
#     exit 0
#fi

PROJECT=npn

# check that we have the latest ...
docker pull jdeck88/ontology-data-pipeline

docker run -t -v "$(pwd)":/process -w=/app -ti jdeck88/ontology-data-pipeline \
    python pipeline.py \
    -v --drop_invalid \
    --project_base /process/projects \
    --input_dir /process/data/$PROJECT/input/ \
    --project $PROJECT \
    /process/data/npn/output \
    https://raw.githubusercontent.com/PlantPhenoOntology/ppo/master/releases/2018-10-26/ppo.owl \
    /process/config \

#usage: pipeline.py [-h] [--project PROJECT] [--input_dir INPUT_DIR]
#                   [--project_base PROJECT_BASE] [--data_file DATA_FILE]
#                   [--preprocessor PREPROCESSOR] [--drop_invalid] [--log_file]
#                   [--reasoner_config REASONER_CONFIG] [-v] [-c CHUNK_SIZE]
#                   [--num_processes NUM_PROCESSES] [-s SPLIT_DATA_COLUMN]
#                   output_dir ontology config_dir
#pipeline.py: error: the following arguments are required: output_dir, ontology, config_dir

#docker run -t -v "$(pwd)":/process -w=/app -ti jdeck88/ontology-data-pipeline \
#    python pipeline.py \
#    -v --drop_invalid \
#    --data_file /process/$INPUT_DATAFILE \
#    /process/$OUTPUT_DIRECTORY \
#    https://raw.githubusercontent.com/PlantPhenoOntology/ppo/master/releases/2018-10-26/ppo.owl \
#    /process/config \
