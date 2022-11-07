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

#create a function that calculates the vector magnitude (total body acceleration from the x, y and z components)
def calculate_totalBodyAcceleration(createAccelDataDF(path_acceldata)):
    '''
    This function calculates the vector magnitude or total body acceleration using the AccelData dataframe.
    It also produces a dataframe containing only the accelerometer information (total body acceleration and timestamps)
    ''' 
    # create a dataframe with the accel data exclusively (command=3 and register address = 34)
    df_acceldata_accel = df_acceldata.loc[df_acceldata['Command']
                                      == 3].loc[df_acceldata['RegisterAddress'] == 34]


    # based on the matlab code Marcelo sent me
    fs = 200  # sampling frequency
    f_cut = 1/(fs/2)

    filter_order = 5
    b, a = signal.butter(filter_order, f_cut, 'high')
    w, h = signal.freqs(b, a)

    #DataElement0 corresponds to Accel_x
    x = df_acceldata_accel['DataElement0']
    y = df_acceldata_accel['Accel_y']
    z = df_acceldata_accel['Accel_z']

    medfilt_order = 7
    x = signal.medfilt(x, medfilt_order)
    y = signal.medfilt(y, medfilt_order)
    z = signal.medfilt(z, medfilt_order)

    x_BA = signal.filtfilt(b, a, x)
    y_BA = signal.filtfilt(b, a, y)
    z_BA = signal.filtfilt(b, a, z)

    array_sum_x = np.sum(x)
    array_has_nan_x = np.isnan(array_sum_x)

    array_sum_y = np.sum(y)
    array_has_nan_y = np.isnan(array_sum_y)

    array_sum_z = np.sum(z)
    array_has_nan_z = np.isnan(array_sum_z)

    print('Are there any null/none values in the x, y, or z acceldata?: {}'.format(
        array_has_nan_x+array_has_nan_y+array_has_nan_z))
    if array_has_nan_x+array_has_nan_y+array_has_nan_z == False:
        print('No null values were found in the accelerometer data.')

    x_GA = x - x_BA
    y_GA = y - y_BA
    z_GA = z - z_BA

    # metric: high-pass filter followed by the euclidian norm
    # the original signal consisted in the three components of ...
    # body+gravitational acceleration. After applying a filter, I computed the
    # total body acceleration, from which movement initiations will be detected
    # euclidian norm/vector magnitude
    total_bodyaccel = np.sqrt(x_BA**2+y_BA**2+z_BA**2)

    df_acceldata_accel['Total_accel'] = total_bodyaccel
    df_acceldata_accel = df_acceldata_accel[['Command', 'RegisterAddress', 'Timestamp',
                                            'DataElement0', 'Accel_y', 'Accel_z',
                                            'Gyr_x', 'Gyr_y', 'Gyr_z',
                                            'Magn_x', 'Magn_y', 'Magn_z',
                                            'Counter',
                                            'Total_accel']]


    df_acceldata_accel.reset_index(inplace=True, drop=True)
    df_acceldata_accel