import os, csv, argparse
from zipfile import ZipFile
import logging
import multiprocessing
import pandas as pd
import numpy as np
import sys
sys.path.append('../')
import config

PROJECT = 'neon'
ROOT_PATH = os.path.join(os.path.dirname(__file__), '../../')
INPUT_DIR = os.path.join(ROOT_PATH,'data', PROJECT, 'input')
OUTPUT_DIR = os.path.join(ROOT_PATH, 'data', PROJECT, 'processed')
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'data.csv')

INTENSITY_FILE = os.path.join(os.path.dirname(__file__), 'intensity_values.csv')
INTENSITY_VALUE_FRAME = pd.read_csv(INTENSITY_FILE, skipinitialspace=True, header=0) if os.path.exists(
    INTENSITY_FILE) else None
INTENSITY = 0
PHENO_DESC = 1
PHENO_FILE = os.path.join(os.path.dirname(__file__), 'phenophase_descriptions.csv')
PHENO_VALUE_FRAME = pd.read_csv(PHENO_FILE, skipinitialspace=True, header=0) if os.path.exists(
    PHENO_FILE) else None
COLUMNS_MAP = {
    'uid': 'record_id',
    'dayOfYear': 'day_of_year',
    'scientificName': 'scientific_name',
    'phenophaseName': 'phenophase_name',
    'phenophaseStatus': 'phenophase_status',
    'phenophaseIntensity': 'phenophase_intensity',
    'decimalLatitude': 'latitude',
    'decimalLongitude': 'longitude'
}

class PreProcessor():
    def main(self):
        # loop all of the files in the NEON directory
        count = 0
        for f in walk_files(INPUT_DIR):
            self._process_zip(f, count)
            count = count + 1

    def _process_zip(self, file, count):
        statusintensity_file = None
        per_individual_file = None

        logging.debug("\tprocessing {}".format(file))
        with ZipFile(file) as zip_file:
            for filename in zip_file.namelist():

                if '.phe_statusintensity.' in filename:
                    if statusintensity_file:
                        logging.debug('multiple phe_statusintensity csv files found in zip_file {}'.format(zip_file.filename))
                        logging.debug('continuing...')
                        return
                    statusintensity_file = zip_file.open(filename)

                elif '.phe_perindividual.' in filename:
                    if per_individual_file:
                        logging.debug('multiple phe_perindividual csv files found in zip_file {}'.format(zip_file.filename))
                        logging.debug('continuing...')
                        return
                    per_individual_file = zip_file.open(filename)

        if not statusintensity_file or not per_individual_file:
            logging.debug('could not find needed files in zip_file {}'.format(zip_file.filename))
            logging.debug('continuing...')
            return

        individuals = pd.read_csv(per_individual_file, header=0, skipinitialspace=True,
                                  usecols=['decimalLatitude', 'decimalLongitude', 'namedLocation', 'individualID',
                                           'scientificName', 'date'],dtype='object')

        individuals = individuals.rename(index=str, columns={"date": "addDate"})
        # take the latest entry of an individualID as the source of truth
        individuals = individuals.sort_values('addDate', ascending=False).drop_duplicates('individualID')

        data = pd.read_csv(statusintensity_file, header=0, skipinitialspace=True,
                           usecols=['uid', 'date', 'dayOfYear', 'individualID', 'phenophaseName', 'phenophaseStatus',
                                    'phenophaseIntensity', 'namedLocation'], parse_dates=['date'], dtype={'phenophaseIntensity':str})

        data = data.merge(individuals, left_on=['individualID', 'namedLocation'],
                          right_on=['individualID', 'namedLocation'], how='left')

        if (count == 0):
            self._transform_data(data).to_csv(OUTPUT_FILE, mode='w', header=True, index=False)
        else:
            self._transform_data(data).to_csv(OUTPUT_FILE, mode='a', header=False, index=False)

        statusintensity_file.close()
        per_individual_file.close()

    @staticmethod
    def _transform_data(data):
        data['source'] = 'NEON'
        data['basis_of_record'] = 'HumanObservation'
        data['genus'] = data.apply(lambda row: row.scientificName.split()[0] if pd.notnull(row.scientificName) else "",
                                   axis=1)
        data['specific_epithet'] = data.apply(
            lambda row: row.scientificName.split()[1] if pd.notnull(row.scientificName) else "", axis=1)
        data['year'] = data.apply(lambda row: row['date'].year, axis=1)
        # original data had dayOfYear, but latest download doesn't. Try and fill from date
        data['dayOfYear'] = data.apply(
            lambda row: row['date'].timetuple().tm_yday if pd.isnull(row['dayOfYear']) and pd.notnull(row['date']) else
            row['dayOfYear'], axis=1)

        data['sub_source'] = ''

        # merge phenphase_description file eith data fram
        data = data.merge(PHENO_VALUE_FRAME, left_on='phenophaseName', right_on='field', how='left')
        data['phenophaseName'] = data.loc[:,'defined_by'] 

        # Populate dataframe with lower and upper count values based on intensity description
        df = data.merge(INTENSITY_VALUE_FRAME, left_on='phenophaseIntensity', right_on='value', how='left')

        # check that we have a 'value' value if we have a phenophaseIntensity value
        if not df.loc[df.phenophaseIntensity.notnull() & df.value.isnull()].empty:
            raise RuntimeError(
                'found row with a phenophaseIntensity, but is missing the appropriate counts. may need to '
                'regenerate the intensity_values.csv file. Run the Neon helpers.py script with the --intensity flag to '
                'append "values" that do not currently exist in the intensity_values.csv file. You will '
                'need to manually insert the correct counts in the intensity_values.csv file.')

        # if phenophaseStatus is 'yes' and no phenophaseIntensity, set lower_count = 1
        df.loc[df.phenophaseIntensity.isnull() & df.phenophaseStatus.str.match('yes', case=False), 'lower_count_partplant'] = 1
        df.loc[df.phenophaseIntensity.isnull() & df.phenophaseStatus.str.match('yes', case=False), 'lower_count_wholeplant'] = 1
        # if phenophaseStatus is 'yes' and no phenophaseIntensity, set lower_count = 1
        df.loc[df.phenophaseIntensity.isnull() & df.phenophaseStatus.str.match('no', case=False), 'upper_count_partplant'] = 0
        df.loc[df.phenophaseIntensity.isnull() & df.phenophaseStatus.str.match('no', case=False), 'upper_count_wholeplant'] = 0


        df = df.fillna('')  # replace all null values

        pd.options.mode.chained_assignment = None

        df = df.rename(columns=COLUMNS_MAP)

        #with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        #    print(df)
        return df


def walk_files(input_dir):
    for root, dirs, files in os.walk(input_dir):

        for file in files:
            if file.endswith(".zip"):
                yield os.path.join(root, file)


def generate_phen_descriptions(input_dir):
    found_values = set()

    for file in walk_files(input_dir):
        csv_file = None

        with ZipFile(file) as zip_file:

            for filename in zip_file.namelist():
                if '.phe_statusintensity.' in filename:
                    if csv_file:
                        raise RuntimeError('multiple csv files found in zip_file {}'.format(zip_file.filename))
                    csv_file = zip_file.open(filename)

        if not csv_file:
            raise RuntimeError('didnt find csv file in zip_file {}'.format(zip_file.filename))

        data = pd.read_csv(csv_file, header=0, chunksize=1000000, skipinitialspace=True,
                           usecols=['phenophaseName'])

        for chunk in data:
            found_values.update(chunk.phenophaseName.unique().tolist())

    with open(os.path.join(os.path.dirname(__file__), 'phenophase_descriptions.csv'), 'w') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(['field', 'defined_by'])

        for value in found_values:
            writer.writerow([value, ''])


def generate_intensity_values(input_dir):
    if INTENSITY_VALUE_FRAME is None:
        intensity_frame = pd.DataFrame([], columns=['value', 'lower_count', 'upper_count', 'lower_percent',
                                                    'upper_percent'])
    else:
        intensity_frame = INTENSITY_VALUE_FRAME

    found_values = set()

    for file in walk_files(input_dir):
        csv_file = None

        with ZipFile(file) as zip_file:

            for filename in zip_file.namelist():
                if '.phe_statusintensity.' in filename:
                    if csv_file:
                        raise RuntimeError('multiple csv files found in zip_file {}'.format(zip_file.filename))
                    csv_file = zip_file.open(filename)

        if not csv_file:
            raise RuntimeError('didnt file csv file in zip_file {}'.format(zip_file))

        data = pd.read_csv(csv_file, header=0, chunksize=1000000, skipinitialspace=True,
                           usecols=['phenophaseIntensity'])

        for chunk in data:
            found_values.update(chunk.phenophaseIntensity.unique().tolist())

    found_values.difference_update(intensity_frame.index.tolist())

    intensity_frame = intensity_frame.append(
        pd.DataFrame.from_items([('value', list(found_values))])
    )

    intensity_frame.drop_duplicates('value', inplace=True)
    intensity_frame.set_index('value', inplace=True)

    intensity_frame.to_csv(INTENSITY_FILE)

if __name__ == '__main__':
    PreProcessor().main()
