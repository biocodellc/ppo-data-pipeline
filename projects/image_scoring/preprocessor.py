# -*- coding: utf-8 -*-

"""proprocessor.AbstractPreProcessor implementation for preprocessing pep725 data"""

import re, uuid
import os
#import multiprocessing
import pandas as pd
import math
import sys
import numpy as np
from preprocessor import AbstractPreProcessor

PHENOPHASE_DESCRIPTIONS_FILE = os.path.join(os.path.dirname(__file__), 'phenophase_descriptions.csv')
FILE_PREFIX = "image_scoring_"
DATA_FILE = os.path.join(FILE_PREFIX+'_data.csv')

class PreProcessor(AbstractPreProcessor):

    def _process_data(self):
        self.descriptions = pd.read_csv(PHENOPHASE_DESCRIPTIONS_FILE, header=0, skipinitialspace=True, dtype='object')

        data = pd.read_csv(os.path.join(self.input_dir, "image_scoring.csv"), header=0, engine='python' )

        self._transform_data(data).to_csv(self.output_file, columns=self.headers, mode='a', header=False, index=False)

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
        data['source'] = 'IMAGE SCORING'

        rows_list = []
        count = 0
        for i, j in data.iterrows(): 
            count = count + 1
            dict1 = {}
            j['phenophase_name'] = j['flowers']
            j['record_id'] = count
            dict1.update(j)
            rows_list.append(dict1)

            count = count + 1
            dict2 = {}
            j['phenophase_name'] = j['open_flowers']
            j['record_id'] = count
            dict2.update(j)
            rows_list.append(dict2)
            
        # create a new data frame from the rows_list array
        newData = pd.DataFrame(rows_list) 
        newData= newData.drop("flowers", axis=1)
        newData= newData.drop("open_flowers", axis=1)

        # Set default lower and upper counts
        data = newData.apply(lambda row: self._set_defaults(row), axis=1)

        # As far as i know these are all unique individuals
        data['individualID'] = data.apply(lambda x: uuid.uuid4(), axis=1)

        return data

    def _set_defaults(self, row):
        try:
            if (row['whole_plant'] == "whole plant present"):
                row['lower_count_wholeplant'] = self.descriptions[self.descriptions['field'] == row['phenophase_name']]['lower'].values[0]
                row['upper_count_wholeplant'] = self.descriptions[self.descriptions['field'] == row['phenophase_name']]['upper'].values[0]
                row['lower_percent_wholeplant'] = np.nan
                row['upper_percent_wholeplant'] = np.nan 
            else:
                row['lower_count_partplant'] = self.descriptions[self.descriptions['field'] == row['phenophase_name']]['lower'].values[0]
                row['lower_count_wholeplant'] = self.descriptions[self.descriptions['field'] == row['phenophase_name']]['lower'].values[0]
                row['upper_count_partplant'] = self.descriptions[self.descriptions['field'] == row['phenophase_name']]['upper'].values[0]
                row['lower_percent_partplant'] = np.nan
                row['upper_percent_partplant'] = np.nan
        except IndexError:
            # thrown if missing phenophase_description in phenophase_descriptions.csv file
            pass

        return row
