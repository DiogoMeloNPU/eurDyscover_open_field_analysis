#this module organizes the data from the accelerometer, as well as the timestamps
#of all the hardware that was used (microscope, camera, accel)

import math
import numpy as np
import pandas as pd
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
-A session is defined as the data from the first to the last inscopix! (everything from the first to the last 35, inclusively). This is the period during which the camera, the microscope and the accelerometer are simlutaneously recording. 
'''

def convert(val):
    try:
        return float(val)
    except:
        return val

def open_AccelData_asDF(path_acceldata):
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

def get_microscope_timestamps(path):
    '''
    This function obtains the timestamps of the microscope given the path of an AccelData.csv file. 
    '''
    timestamps_df = open_AccelData_asDF(path)
    microscope_timestamps = timestamps_df['Timestamp'].loc[timestamps_df['Command']==3].loc[timestamps_df['RegisterAddress']==35]
    microscope_timestamps = np.array(microscope_timestamps)

    return microscope_timestamps

def get_camera_timestamps(path):
    '''
    This function obtains the timestamps of the camera, as well as information regarding which TTLs belong to the session.
    For that, it recieves as input the path of an AccelData.csv file.

    To obtain the first and last camera timestamps of the session it is necessary to obtain the first and last...
    ...inscopix timestamps and perform an index search which camera_timestamps are in between these indices.
    '''
    timestamps_df = open_AccelData_asDF(path_acceldata)

    camera_timestamps = timestamps_df['Timestamp'].loc[timestamps_df['Command']==3].loc[timestamps_df['RegisterAddress']==37]
    camera_timestamps = pd.DataFrame(camera_timestamps)
    camera_timestamps['index'] = range(0, len(camera_timestamps))

    microscope_timestamps = timestamps_df['Timestamp'].loc[timestamps_df['Command']
                                                           == 3].loc[timestamps_df['RegisterAddress'] == 35]

    #indices of first and last inscopix TTL                                                       
    i_first_incopTTL = microscope_timestamps.index[0]
    i_last_inscopTTL = microscope_timestamps.index[-1]
    
    session_camera_timestamps = timestamps_df['Timestamp'][i_first_incopTTL:i_last_inscopTTL].loc[timestamps_df['Command']
                                                               == 3].loc[timestamps_df['RegisterAddress'] == 37]

    #indices of the first and last camera TTL
    i_first_camTTL = session_camera_timestamps.index[0]
    i_last_camTTL = session_camera_timestamps.index[-1]

    first_TTL = int(camera_timestamps.loc[i_first_camTTL]['index'])
    last_TTL = int(camera_timestamps.loc[i_last_camTTL]['index'])

    camera_timestamps = np.array(camera_timestamps['Timestamp'])

    return camera_timestamps, first_TTL, last_TTL


def get_accelerometer_timestamp(path):
    '''
    This function obtains the timestamps of the accelerometer, as well as information regarding which TTLs belong to the session.
    For that, it recieves as input the path of an AccelData.csv file.

    To obtain the first and last accelerometer timestamps of the session it is necessary to obtain the first and last...
    ...inscopix timestamps and perform an index search which accelerometer_timestamps are in between these indices.
    '''
    timestamps_df = open_AccelData_asDF(path_acceldata)

    accelerometer_timestamps = timestamps_df['Timestamp'].loc[timestamps_df['Command']
                                                       == 3].loc[timestamps_df['RegisterAddress'] == 34]
    accelerometer_timestamps = pd.DataFrame(accelerometer_timestamps)
    accelerometer_timestamps['index'] = range(0, len(accelerometer_timestamps))

    microscope_timestamps = timestamps_df['Timestamp'].loc[timestamps_df['Command']
                                                           == 3].loc[timestamps_df['RegisterAddress'] == 35]

    #indices of first and last inscopix TTL
    i_first_incopTTL = microscope_timestamps.index[0]
    i_last_inscopTTL = microscope_timestamps.index[-1]

    session_accelerometer_timestamps = timestamps_df['Timestamp'][i_first_incopTTL:i_last_inscopTTL].loc[timestamps_df['Command']
                                                                                                  == 3].loc[timestamps_df['RegisterAddress'] == 34]

    #indices of the first and last camera TTL
    i_first_camTTL = session_accelerometer_timestamps.index[0]
    i_last_camTTL = session_accelerometer_timestamps.index[-1]

    first_TTL = int(accelerometer_timestamps.loc[i_first_camTTL]['index'])
    last_TTL = int(accelerometer_timestamps.loc[i_last_camTTL]['index'])

    accelerometer_timestamps = np.array(accelerometer_timestamps['Timestamp'])

    return accelerometer_timestamps, first_TTL, last_TTL