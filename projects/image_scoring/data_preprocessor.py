# -*- coding: utf-8 -*-

# processing specific builds
import re, uuid
import os,csv
import pandas as pd
import math
import sys
import numpy as np

# Set the project name
PROJECT = 'image_scoring'

#### BEGIN section that should be common to all projects ####
# appending paths so can run either in current directory or from ppo-data-pipeline root
sys.path.append('../')
sys.path.append('./projects/')
import config 
from config import DATA_DIR_NAME
ROOT_PATH = os.path.join(os.path.dirname(__file__), '../../')
INPUT_DIR = os.path.join(ROOT_PATH,DATA_DIR_NAME, PROJECT, 'input')
OUTPUT_DIR = os.path.join(ROOT_PATH, DATA_DIR_NAME, PROJECT, 'processed')
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'data.csv')
#### END section that should be common to all projects ####

PHENOPHASE_DESCRIPTIONS_FILE = os.path.join(os.path.dirname(__file__), 'phenophase_descriptions.csv')

class PreProcessor():

    def main(self):
        print("starting....")
        self._process_data()

    def _process_data(self):
        self.descriptions = pd.read_csv(PHENOPHASE_DESCRIPTIONS_FILE, header=0, skipinitialspace=True, dtype='object')

        data = pd.read_csv(os.path.join(INPUT_DIR, "image_scoring.csv"), header=0, engine='python' )

        print ("cleaning out old file....")
        try:
            os.remove(OUTPUT_FILE)
        except: 
            print ("\tnothing to clean....")
        
        print ("transforming data and writing file....")
        self._transform_data(data).to_csv(OUTPUT_FILE, columns=config._parse_headers(self), mode='w', header=True, index=False)

    def _transform_data(self, data):

        data.fillna("", inplace=True)  # replace all null values

        # rename incoming columns
        data = data.rename(index=str,columns={
            "observationSource":"institution_code",
            "imageSource":"sub_source",
            "basisOfRecord":"basis_of_record",
            "species":"specific_epithet"})

        # Capitalize genus
        data['genus'] = data['genus'].str.capitalize()

        # Create ScientificName
        data['scientific_name'] = data['genus'] + ' ' + data['specific_epithet']

        # Specify source as Herbarium
        data['source'] = 'IMAGE_SCORING'


        #data = data.merge(self.dataset_metadata, left_on='dataset_id', right_on='Dataset_ID', how='left')
        #whole_plant_s,flowers_s,open_flowers_s,lower count part plant,upper count part plant,lower count whole plant,upper count whole plant,trait
        data = data.merge(self.descriptions, how='left', left_on=['whole_plant_s','flowers_s','open_flowers_s'], right_on=['whole_plant_s','flowers_s','open_flowers_s'])
        
        # As far as i know these are all unique individuals
        #data['individualID'] = data.apply(lambda x: uuid.uuid4(), axis=1)
        data['individualID'] = np.arange(len(data))
        # Assign UUID for each unique record
        #data['record_id'] = data.apply(lambda x: uuid.uuid4(), axis=1)
        data['record_id'] = np.arange(len(data))

        return data

if __name__ == '__main__':
    PreProcessor().main()

