PROJECT=npn

    python ../ontology-data-pipeline/pipeline.py \
    -v --drop_invalid \
    data/$PROJECT/processed/data.csv \
    data/$PROJECT/processed \
    file:/Users/jdeck/IdeaProjects/ppo-data-pipeline/config/ppo.owl \
    config \
