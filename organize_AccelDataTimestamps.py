#this module organizes the data from the accelerometer, as well as the timestamps
#of all the hardware that was used (microscope, camera, accel)

import math
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import csv
import numpy

'''
AccelData.csv is the file that contains the timestamps of all the hardware used in a session.

USEFUL INFORMATION:
-'Command' of interest - 3
-'RegisterAddress':
    34 (accelerometer; sampling_rate=200 Hz);
    37 (camera; sampling_rate=30 Hz);
    35 (inscopix; sampling_rate=20 Hz).
-Only consider the data from the first to the last inscopix!
'''

path_acceldata = "E:\\.shortcut-targets-by-id\\1MH0egFqTqTToPE-wxCs7mDWL48lVKqDB\\EurDyscover\\Organized_data_JAS\\D1\\Baseline 1\\42308_RF_B1\\AccelData2021-04-28T13_45_51.6713216+01_00.csv"

def convert(val):
    try:
        return float(val)
    except:
        return val

def createAccelDataDF(path_acceldata):
    '''
    This function opens the AccelData.csv file as a dataframe.
    '''
    with open(path_acceldata, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        values = []
        max_cols = 0
        for index, row in enumerate(spamreader):
            if index == 0:
                continue
            row = list(map(convert, row))
            if len(row) > max_cols:
                max_cols = len(row)
            values.append(row)
        matrix = []
        for row in values:
            row = row + [None for x in range(max_cols-len(row))]
            matrix.append(row)
        matrix = numpy.array(matrix)
    matrix_columns = ['Command', 'RegisterAddress', 'Timestamp',
                    'DataElement0', 'Accel_y', 'Accel_z',
                    'Gyr_x', 'Gyr_y', 'Gyr_z',
                    'Magn_x', 'Magn_y', 'Magn_z',
                    'Counter',
                    'col_14', 'col_15', 'col_16', 'col_17', 'col_18', 'col_19', 'col_20', 'col_21', 'col_22', 'col_23', 'col_24', 'col_25', 'col_26', 'col_27', 'col_28']
    df_acceldata = pd.DataFrame(matrix, columns=matrix_columns)
    df_acceldata = df_acceldata.apply(pd.to_numeric)
    to_drop = ['col_14', 'col_15', 'col_16', 'col_17', 'col_18', 'col_19', 'col_20',
            'col_21', 'col_22', 'col_23', 'col_24', 'col_25', 'col_26', 'col_27', 'col_28']
    df_acceldata = df_acceldata.drop(columns=to_drop)
    # this dataframe contains all the timestamps (camera, inscopix and accelerometer), as well as the accel data itself
    return df_acceldata

#create arrays with the timestamps of the microscope, camera and accelerometer
#if the respective dataframes exist, update those files by adding to each one a new column with the timestamps