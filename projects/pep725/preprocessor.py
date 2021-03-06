# -*- coding: utf-8 -*-


"""proprocessor.AbstractPreProcessor implementation for preprocessing pep725 data"""

import re, uuid

import os

import pandas as pd
from preprocessor import AbstractPreProcessor

PHENOPHASE_DESCRIPTIONS_FILE = os.path.join(os.path.dirname(__file__), 'phenophase_descriptions.csv')
FILE_PREFIX = "pep725_"
COLUMNS_MAP = {
    'species': 'scientific_name',
    'day': 'day_of_year',
    'lat': 'latitude',
    'lon': 'longitude',
    'description': 'phenophase_name'
}
FILES = {
    'data': FILE_PREFIX + 'data.csv',
    'genus': FILE_PREFIX + 'genus.csv',
    'species': FILE_PREFIX + 'species.csv',
    'stations': FILE_PREFIX + 'stations.csv',
    'phase': FILE_PREFIX + 'phase.csv',
}


class PreProcessor(AbstractPreProcessor):
    def _process_data(self):
        self.frames = {
            'genus': pd.read_csv(os.path.join(self.input_dir,FILES['genus']), sep=';', header=0, usecols=['genus_id', 'genus'],
                                 skipinitialspace=True,dtype='object'),
            'species': pd.read_csv(os.path.join(self.input_dir,FILES['species']), sep=';', header=0, skipinitialspace=True,
                                   usecols=['species_id', 'species'],dtype='object'),
            'stations': pd.read_csv(os.path.join(self.input_dir,FILES['stations']), sep=';', header=0, skipinitialspace=True,
                                    usecols=['s_id', 'lat', 'lon'],dtype='object'),  # , 'alt', 'name']),
            'phase': pd.read_csv(os.path.join(self.input_dir,FILES['phase']), sep=';', header=0,
                                 usecols=['phase_id', 'description'], skipinitialspace=True,dtype='object'),
            'phenophase_descriptions': pd.read_csv(PHENOPHASE_DESCRIPTIONS_FILE, header=0, skipinitialspace=True,dtype='object')
        }

        chunk_size = 100000

        data = pd.read_csv(os.path.join(self.input_dir,FILES['data']), sep=';', header=0,
                           usecols=['s_id', 'genus_id', 'species_id', 'phase_id', 'year', 'day'],
                           skipinitialspace=True,dtype='object', chunksize= chunk_size)

        for chunk in data:
            self._transform_data(chunk).to_csv(
                self.output_file, 
                columns=self.headers, 
                mode='a', 
                header=False, 
                index=False)


    def _transform_data(self, data):
        joined_data = data \
            .merge(self.frames['species'], left_on='species_id', right_on='species_id', how='left') \
            .merge(self.frames['genus'], left_on='genus_id', right_on='genus_id', how='left') \
            .merge(self.frames['stations'], left_on='s_id', right_on='s_id', how='left') \
            .merge(self.frames['phase'], left_on='phase_id', right_on='phase_id', how='left') \
            .merge(self.frames['phenophase_descriptions'], left_on='description', right_on='field', how='left')


        joined_data.fillna("", inplace=True)  # replace all null values

        joined_data = self._filter_data(joined_data)

        joined_data['record_id'] = joined_data.apply(lambda x: uuid.uuid4(), axis=1)
        joined_data['specific_epithet'] = joined_data.apply(
            lambda row: re.sub('^%s' % row['genus'], "", row['species']).strip(), axis=1)
        joined_data['source'] = 'PEP725'
        joined_data['basis_of_record'] = 'HumanObservation'

        joined_data['individualID'] = ''
        joined_data['sub_source'] = ''
        
        joined_data = joined_data.rename(columns=COLUMNS_MAP)

        return joined_data

    def _filter_data(self, data):
        # we want to drop all data with a description in phenohase_descriptions.csv which is missing a defined_by
        descriptions = self.frames['phenophase_descriptions']
        to_exclude = descriptions[descriptions['defined_by'].isnull()]['field']
        return data[~data['description'].isin(to_exclude)]
