# -*- coding: utf-8 -*-

"""proprocessor.AbstractPreProcessor implementation for preprocessing npn data"""


import os, csv
import multiprocessing
import pandas as pd
from preprocessor import AbstractPreProcessor

PHENOPHASE_DESCRIPTIONS_FILE = os.path.join(os.path.dirname(__file__), 'phenophase_descriptions.csv')
DATASET_METADATA_FILE = os.path.join(os.path.dirname(__file__), 'ancillary_dataset_data.csv')
COLUMNS_MAP = {
    'observation_id': 'record_id',
    'species': 'specific_epithet',
    'phenophase_description': 'phenophase_name',
    'Source': 'sub_source'
}

class PreProcessor(AbstractPreProcessor):
    def _process_data(self):
        self.descriptions = pd.read_csv(PHENOPHASE_DESCRIPTIONS_FILE, header=0, skipinitialspace=True, dtype='object')

        self.dataset_metadata = pd.read_csv(DATASET_METADATA_FILE, header=0, skipinitialspace=True,
                                            usecols=['Dataset_ID', 'Source'], dtype='object')

        chunk_size = 100000

        data = pd.read_csv(
            os.path.join(self.input_dir, "npn_observations_data.csv"), 
            header=0, 
            engine='python', 
            dtype='object', 
            chunksize = chunk_size)

        for chunk in data:
            self._transform_data(chunk).to_csv(
                self.output_file, 
                columns=self.headers, 
                mode='a', 
                header=False, 
                index=False)

    def _transform_data(self, data):
        # Add an index name
        # data.index.name = 'record_id'

        # drop all records where the user is unsure of what was coded (this is phenophase_status = -1)
        data = data[data.phenophase_status != -1]

        # Handle cases where we want to force a default intensity value 
        # First, fill out the force_default_value column with False where there is no value
        self.descriptions['force_default_value'] = self.descriptions['force_default_value'].fillna(False)
        # Second, apply, row by row a filter that sets the intensity_value to -9999 when we want to force defaults
        data = data.apply(lambda row: self._force_defaults(row), axis=1)

        # map counts from intensity_value table to upper and lower count/percents
        cols = ['value', 'lower_count', 'upper_count', 'lower_percent', 'upper_percent']
        data = self._translate(os.path.join(os.path.dirname(__file__), 'intensity_values.csv'), cols, 'value', data,
                             'intensity_value')

        # when intensity_value != -9999 set upper/lower counts 
        data = data.apply(lambda row: self._set_defaults(row), axis=1)

        # set the source
        data['source'] = 'USA-NPN'
        data['basis_of_record'] = 'HumanObservation'
        data = data.merge(self.dataset_metadata, left_on='dataset_id', right_on='Dataset_ID', how='left')

        # Normalize Date to just Year. we don't need to store actual date because we use only Year + DayOfYear
        data['year'] = pd.DatetimeIndex(data['observation_date']).year

        # Create ScientificName
        data['scientific_name'] = data['genus'] + ' ' + data['species']

        # drop duplicate ObservationIDs
        data.drop_duplicates('observation_id', inplace=True)

        # filling in remaining column names, even though there is no data
        data['individualID'] = ''
        data['lower_count_wholeplant'] = ''
        data['upper_count_wholeplant'] = ''
        data['lower_count_partplant'] = ''
        data['upper_count_partplant'] = ''

        data = data.rename(columns=COLUMNS_MAP)

        return data

    # Get true/false value for related force_default column in phenophase_descriptions and override the intensity_value
    # with -9999.  Force defaults overrides intensity_value descriptions with default values for phenophases where
    # user count data do not make sense for PPO purposes.
    def _force_defaults(self, row):
        #print (self.descriptions['field']['defined_by']).values[0]
        try:
            if self.descriptions[(self.descriptions['field'] == row['phenophase_description'])]['force_default_value'].values[0]:
                row['intensity_value'] = '-9999'
        except IndexError:
            # thrown if missing phenophase_description in phenophase_descriptions.csv file
            pass

        return row

    # For any column with a -9999 in the intensity_value column, insert default values from the phenophase_descriptions sheet
    def _set_defaults(self, row):
        if row.intensity_value != '-9999':
            return row

        try:
            if row.phenophase_status == 0:
                row['lower_percent_partplant'] = self.descriptions[self.descriptions['field'] == row['phenophase_description']]['lower_percent_absent'].values[0]
                row['upper_percent_partplant'] = self.descriptions[self.descriptions['field'] == row['phenophase_description']]['upper_percent_absent'].values[0]
                row['lower_percent_wholeplant'] = self.descriptions[self.descriptions['field'] == row['phenophase_description']]['lower_percent_absent'].values[0]
                row['upper_percent_wholeplant'] = self.descriptions[self.descriptions['field'] == row['phenophase_description']]['upper_percent_absent'].values[0]
            else:
                row['lower_percent_partplant'] = self.descriptions[self.descriptions['field'] == row['phenophase_description']]['lower_percent_present'].values[0]
                row['upper_percent_partplant'] = self.descriptions[self.descriptions['field'] == row['phenophase_description']]['upper_percent_present'].values[0]
                row['lower_percent_wholeplant'] = self.descriptions[self.descriptions['field'] == row['phenophase_description']]['lower_percent_present'].values[0]
                row['upper_percent_wholeplant'] = self.descriptions[self.descriptions['field'] == row['phenophase_description']]['upper_percent_present'].values[0]
        except IndexError:
            # thrown if missing phenophase_description in phenophase_descriptions.csv file
            pass

        return row

    @staticmethod
    def _translate(filename, cols, index_name, data_frame, lookup_column):
        """
         Function to read in a CSV file containing one or more values that we want
         to use to translate values  for.  using the dataframe's "lookup_column"
         as the key
        """
        # loop all columns
        for column in cols:
            # don't look at index column
            if column is not index_name:
                # read the incoming lookup filename into a dictionary using the
                # the appropriate columns to assign the dictionary key/value
                with open(filename) as f:
                    this_dict = dict((rows[cols.index(index_name)], rows[cols.index(column)]) \
                                     for rows in csv.reader(f))
                    # assign the new column name values based on lookup column name
                    data_frame[column] = data_frame[lookup_column].map(this_dict)
        return data_frame
