#this module organizes the acceleration data present in AccelData.csv and computes total body acceleration
#it also stores each new file in the respective folder containing all other files (neuron.mat, simpler_neuron.mat, AccelData.csv,
# FrameDiff.csv, VideoProcessed.csv)
#finally is updates the dystoniaFilesDF.csv with a new column with the paths for the files created here

from os import walk
import pandas as pd
import numpy as np
import os
#import the module necessary for obtaining the acceleration timestamps
import organize_AccelDataTimestamps

#create a function that calculates the vector magnitude (total body acceleration from the x, y and z components)
def calculate_totalBodyAcceleration(path):
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

    return total_bodyaccel

def buildAccelDF(total_body_acceleration):
    df_acceleration = pd.DataFrame()
    df_acceleration['Total_accel'] = total_body_acceleration
    df_acceleration = df_acceleration[['Command', 'RegisterAddress', 'Timestamp',
                                            'DataElement0', 'Accel_y', 'Accel_z',
                                             'Gyr_x', 'Gyr_y', 'Gyr_z',
                                             'Magn_x', 'Magn_y', 'Magn_z',
                                             'Counter',
                                             'Total_accel']]

    df_acceldata_accel.reset_index(inplace=True, drop=True)
    
    #show the dataframe
    print(df_acceleration)

    return df_acceleration

#needs to import the timestamps from the organize_AccelDataTimestamps.py module
#get_accelerometer_timestamps(path) this must be inside one of the functions