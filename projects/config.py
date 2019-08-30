# Utilities for data pre-processing

import os
import csv
import pandas as pd
import sys

DATA_DIR_NAME = ''
try:
    if (sys.argv[1] == "test"):
        DATA_DIR_NAME = 'test_data'
except:
    DATA_DIR_NAME = 'data'

# read the mapping.csv file and convert to a list to use as column headers
# This replaces the need for a separate headers.csv file
def _parse_headers(self):
    file = os.path.join(os.path.join('..', 'config'), 'mapping.csv')
    if os.path.exists(file):
       with open(file) as f:
           reader = csv.reader(f, skipinitialspace=True)
           self.headers = next(reader)
       df = pd.read_csv(file)
       self.headers = df['column'].unique().tolist()
