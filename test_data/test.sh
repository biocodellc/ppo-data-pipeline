python ../../ontology-data-pipeline/pipeline.py -v --drop_invalid --num_processes 1 data.csv output file:/Users/jdeck/IdeaProjects/ppo-data-pipeline/test_data/config/ppo.owl config 

# check that we have the latest ...
#docker pull jdeck88/ontology-data-pipeline
#
#docker run -v "$(pwd)":/process -w=/app -i jdeck88/ontology-data-pipeline \
#    python pipeline.py \
#    -v --drop_invalid \
#    /process/test_data/npn/output/data.csv \
#    /process/test_data/npn/output \
#    https://raw.githubusercontent.com/PlantPhenoOntology/ppo/master/releases/2018-10-26/ppo.owl \
#    /process/config \
