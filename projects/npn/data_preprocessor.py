# -*- coding: utf-8 -*-

# Code to pre-process NPN data and reading for processing
import argparse
import os, csv, shutil
import sys
import multiprocessing 
import pandas as pd
sys.path.append('../')
import config

PROJECT = 'npn'
ROOT_PATH = os.path.join(os.path.dirname(__file__), '../../')
INPUT_DIR = os.path.join(ROOT_PATH,'data', PROJECT, 'input')
OUTPUT_DIR = os.path.join(ROOT_PATH, 'data', PROJECT, 'processed')
PHENO_FILE = os.path.join(os.path.dirname(__file__), 'phenophase_descriptions.csv')
PHENO_VALUE_FRAME = pd.read_csv(PHENO_FILE, header=0, skipinitialspace=True) if os.path.exists(PHENO_FILE) else None
DATASET_METADATA_FILE = os.path.join(os.path.dirname(__file__), 'ancillary_dataset_data.csv')
INPUT_FILE = os.path.join(INPUT_DIR, 'npn_observations_data.csv')
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'data.csv')
COLUMNS_MAP = {
        'observation_id': 'record_id',
        'species': 'specific_epithet',
        'Dataset_Name': 'sub_source'
        }
        #'defined_by': 'phenophase_name',

class PreProcessor():

    def __init__(self):
        self.descriptions = pd.read_csv(PHENO_FILE, header=0, skipinitialspace=True, dtype='object')

        self.dataset_metadata = pd.read_csv(DATASET_METADATA_FILE, header=0, skipinitialspace=True,
                usecols=['Dataset_ID', 'Dataset_Name'], dtype='object')

        self.num_processes = multiprocessing.cpu_count()
        # default chunk_size
        self.chunk_size = 50000
        self.headers = ''
    
    def main(self):
        parser = argparse.ArgumentParser(description='NPN Data Pre-Processor')
        parser.add_argument('chunk_size', help='the chunk size to use', type=int)

        args = parser.parse_args()
        self.chunk_size = args.chunk_size

        # trucnate OUTPUT_FILE file
        #with open(OUTPUT_FILE, 'r+') as f:
        #    f.truncate(0)
        self.run()

    def run(self):
        data = pd.read_csv(
                INPUT_FILE,
                header=0, 
                engine='python', 
                dtype='object', 
                chunksize = self.chunk_size)

		# clean
        self._clean()
        jobs = []
        count = 0
        for chunk in data:

            chunks = [chunk.loc[chunk.index[i:i + self.chunk_size]] for i in
                range(0, chunk.shape[0], self.chunk_size)]

            writeHeader = False
            if (count == 0):
                writeHeader = True

            p = multiprocessing.Process(target=self._transform_chunk, args=(chunks,writeHeader))
            jobs.append(p)
            p.start()

            # wait for first job to complete, so header can write
            if (count == 0):
                p.join()

            count = count + 1


        for p in jobs:
            p.join()

        
        #print ("finished, writing headers to top of file")
        #headerFrame = pd.DataFrame(self.headers)
        #headerFrame.to_csv(OUTPUT_FILE, index=False)

         
    def _transform_chunk(self, listchunk, writeHeader):
       chunk = listchunk[0]
       print("\tprocessing next {} records".format(len(chunk)))
       self._transform_data(chunk).to_csv(OUTPUT_FILE, columns=config._parse_headers(self), mode='a', header=writeHeader, index=False)

    def _transform_data(self, data):
        # Add an index name
        # data.index.name = 'record_id'

        # drop all records where the user is unsure of what was coded (this is phenophase_status = -1)
        data = data[data.phenophase_status != '-1']
        pd.options.mode.chained_assignment = None

        #data['phenophase_description'] = '{' + data.loc[:,'phenophase_description'] + '}'

        # Handle cases where we want to force a default intensity value.  These are annotated in the 
        # phenophase_descrptions file and indicated by force_default = true
        #self.descriptions['force_default_value'] = self.descriptions['force_default_value'].fillna(False)
        # Apply, row by row a filter that sets the intensity_value to -9999 when we want to force defaults
        #data = data.apply(lambda row: self._force_defaults(row), axis=1)


        # When intensity_value field is filled out, translate the definitions to actual counts using the intensity_values table
        #cols = ['value', 'lower_count_partplant', 'upper_count_partplant', 'lower_percent_partplant', 'upper_percent_partplant', 'lower_count_wholeplant', 'upper_count_wholeplant', 'lower_percent_wholeplant', 'upper_percent_wholeplant']
        #data = self._translate(os.path.join(os.path.dirname(__file__), 'intensity_values.csv'), cols, 'value', data, 'intensity_value')

       
        # when intensity_value field is not filled out (value of -9999) set upper/lower counts from descriptions table
        # Counts are set conditionally based on presence or absence of trait marked by phenophase_status
        # this part is SLOW...................
        #data = data.dropna(subset=['phenophase_status'])


        # set the source
        data['source'] = 'USA-NPN'
        data['basis_of_record'] = 'HumanObservation'
        data = data.merge(self.dataset_metadata, left_on='dataset_id', right_on='Dataset_ID', how='left')
        #data = data.merge(self.traits, left_on='phenophase_description', right_on='field', how='left')
        data = data.merge(PHENO_VALUE_FRAME, left_on='phenophase_description', right_on='field', how='left')
        data['phenophase_name'] = data.loc[:,'defined_by']
        data = data.apply(lambda row: self._set_defaults(row), axis=1)
        #data=data.rename(columns = {'phenophase_description':'phenophase_name'})
        del data['field']
        del data['defined_by']
        
        # drop rows where definition is not mapped
        data = data[data.Notes != 'Agreed to not map this definition']
        data = data[data.phenophase_name.notna()]
        # Normalize Date to just Year. we don't need to store actual date because we use only Year + DayOfYear
        data['year'] = pd.DatetimeIndex(data['observation_date']).year

        # Create ScientificName
        data['scientific_name'] = data['genus'] + ' ' + data['species']

        # drop duplicate ObservationIDs
        data.drop_duplicates('observation_id', inplace=True)
        # prepend ARK root to observation_id to form occurrenceID
        data['occurrenceID'] = 'http://n2t.net/ark:/21547/Amg2' + data['observation_id']

        # filling in remaining column names, even though there is no data
        data['individualID'] = ''

        data = data.rename(columns=COLUMNS_MAP)


        return data

    # Get true/false value for related force_default column in phenophase_descriptions and override the intensity_value
    # with -9999.  Force defaults overrides intensity_value descriptions with default values for phenophases where
    # user count data do not make sense for PPO purposes.
    #def _force_defaults(self, row):
    #    try:
    #        if self.descriptions[(self.descriptions['field'] == row['phenophase_description'])]['force_default_value'].values[0]:
    #            row['intensity_value'] = '-9999'
    #    except IndexError:
    #        # thrown if missing phenophase_description in phenophase_descriptions.csv file
    #        pass
#
#        return row

    def _clean(self):
        if os.path.exists(OUTPUT_DIR):
            shutil.rmtree(OUTPUT_DIR)
        os.makedirs(OUTPUT_DIR)
    # For any column with a -9999 in the intensity_value column, insert default values from the phenophase_descriptions sheet
    def _set_defaults(self, row):


        if int(row.phenophase_status) == 0:
            #print('phenophase_description ' + str(row.phenophase_description) + ' is mapped')
            row.phenophase_name = str(row.phenophase_name).replace('}',' absent}')
        else:
            #print('phenophase_description ' + str(row.phenophase_description) + ' is mapped')
            row.phenophase_name = str(row.phenophase_name).replace('}',' present}')

        return row

    #@staticmethod
    #def _translate(filename, cols, index_name, data_frame, lookup_column):
    #    """
    #     Function to read in a CSV file containing one or more values that we want
    #     to use to translate values  for.  using the dataframe's "lookup_column"
    #     as the key
    #    """
    #    # loop all columns
    #    for column in cols:
    #        # don't look at index column
    #        if column is not index_name:
    #            # read the incoming lookup filename into a dictionary using the
    #            # the appropriate columns to assign the dictionary key/value
    #            with open(filename) as f:
    #                this_dict = dict((rows[cols.index(index_name)], rows[cols.index(column)]) \
    #                        for rows in csv.reader(f))
    #                # assign the new column name values based on lookup column name
    #                data_frame[column] = data_frame[lookup_column].map(this_dict)
    #    return data_frame


if __name__ == '__main__':
    PreProcessor().main()
