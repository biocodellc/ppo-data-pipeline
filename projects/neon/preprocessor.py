# -*- coding: utf-8 -*-

"""preprocessor.AbstractPreProcessor implementation for preprocessing neon data"""

import os, csv, argparse
from zipfile import ZipFile
import logging
import multiprocessing
import pandas as pd
import numpy as np

from preprocessor import AbstractPreProcessor


INTENSITY_FILE = os.path.join(os.path.dirname(__file__), 'intensity_values.csv')
INTENSITY_VALUE_FRAME = pd.read_csv(INTENSITY_FILE, skipinitialspace=True, header=0) if os.path.exists(
    INTENSITY_FILE) else None
INTENSITY = 0
PHENO_DESC = 1
COLUMNS_MAP = {
    'uid': 'record_id',
    'dayOfYear': 'day_of_year',
    'scientificName': 'scientific_name',
    'phenophaseName': 'phenophase_name',
    'decimalLatitude': 'latitude',
    'decimalLongitude': 'longitude'
}

class PreProcessor(AbstractPreProcessor):
    def _process_data(self):
        # loop all of the files in the NEON directory
        for f in walk_files(self.input_dir):
            self._process_zip(f)

    def _process_zip(self, file):
        statusintensity_file = None
        per_individual_file = None

        logging.debug("\tprocessing {}".format(file))
        with ZipFile(file) as zip_file:
            for filename in zip_file.namelist():

                if '.phe_statusintensity.' in filename:
                    if statusintensity_file:
                        raise RuntimeError(
                            'multiple phe_statusintensity csv files found in zip_file {}'.format(zip_file.filename))
                    statusintensity_file = zip_file.open(filename)

                elif '.phe_perindividual.' in filename:
                    if per_individual_file:
                        raise RuntimeError(
                            'multiple phe_perindividual csv files found in zip_file {}'.format(zip_file.filename))
                    per_individual_file = zip_file.open(filename)

        if not statusintensity_file or not per_individual_file:
            raise RuntimeError('could not find needed files in zip_file {}'.format(zip_file.filename))

        individuals = pd.read_csv(per_individual_file, header=0, skipinitialspace=True,
                                  usecols=['decimalLatitude', 'decimalLongitude', 'namedLocation', 'individualID',
                                           'scientificName', 'date'],dtype='object')

        individuals = individuals.rename(index=str, columns={"date": "addDate"})
        # take the latest entry of an individualID as the source of truth
        individuals = individuals.sort_values('addDate', ascending=False).drop_duplicates('individualID')

        data = pd.read_csv(statusintensity_file, header=0, skipinitialspace=True,
                           usecols=['uid', 'date', 'dayOfYear', 'individualID', 'phenophaseName', 'phenophaseStatus',
                                    'phenophaseIntensity', 'namedLocation'], parse_dates=['date'])

        data = data.merge(individuals, left_on=['individualID', 'namedLocation'],
                          right_on=['individualID', 'namedLocation'], how='left')

        self._transform_data(data).to_csv(self.output_file, columns=self.headers, mode='a', header=False, index=False)

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
        data['upper_percent_partplant'] = ''
        data['upper_percent_wholeplant'] = ''
        data['lower_percent_partplant'] = ''
        data['lower_percent_wholeplant'] = ''

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

        df = df.rename(columns=COLUMNS_MAP)

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
            raise RuntimeError('didnt file csv file in zip_file {}'.format(zip_file.filename))

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

