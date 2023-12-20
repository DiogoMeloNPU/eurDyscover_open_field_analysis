#this module organizes the acceleration data present in AccelData.csv and computes total body acceleration
#it also stores each new file in the respective folder containing all other files (neuron.mat, simpler_neuron.mat, AccelData.csv,
# FrameDiff.csv, VideoProcessed.csv)
#finally is updates the dystoniaFilesDF.csv with a new column with the paths for the files created here

import sys
sys.path.append("C:\\Users\\Administrador\\DystoniaAnalysis")

from os import walk
import pandas as pd
import numpy as np
from scipy import signal
#import the module necessary for obtaining the acceleration timestamps
from data_structuring.organize_accel_data_timestamps import open_AccelData_asDF, get_accelerometer_timestamps
# import module with functions to access database
import general_use_functions as guf

#create a function that calculates the vector magnitude (total body acceleration from the x, y and z components)
def calculate_totalBodyAcceleration(path):
    '''
    This function calculates the vector magnitude or total body acceleration using the AccelData dataframe.
    '''
    df_acceldata_accel = open_AccelData_asDF(path)
    # create a dataframe with the accel data exclusively (command=3 and register address = 34)
    df_acceldata_accel = df_acceldata_accel.loc[df_acceldata_accel['Command']
                                          == 3].loc[df_acceldata_accel['RegisterAddress'] == 34]

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

def buildAccelDF(acceldata_path):
    '''
    This function gets the values of the total body acceleration and respective timestamps 
    from other functions and organizes them in a dataframe.
    '''
    #create the dataframe
    df_acceleration = pd.DataFrame()

    #save the total body acceleration in a variable and create a column in the datraframe with those values
    total_body_acceleration = calculate_totalBodyAcceleration(acceldata_path)
    df_acceleration['Total_accel'] = total_body_acceleration
    
    #not sure if this is necessary - delete
    df_acceleration.reset_index(inplace=True, drop=True)  

    #save the timestamps, the first and last TTLs in separate variables
    timestamps, first_TTL, last_TTL = get_accelerometer_timestamps(acceldata_path)

    #add the timestamps as a new df column
    df_acceleration['Timestamp'] = timestamps

    return df_acceleration

# load dystonia database
dystoniaFilesDF = guf.load_dystonia_database()

#now it is necessary to create a dataframe for each of the acceleration files available and store them in Google Drive

#create an array to save the paths of the new TotalBAccel.pkl files
TotalBAccelpaths = []

#creat a file pattern to name the new files
file_pattern = 'TotalBAccel_'

#create a new pkl file with a dataframe containing the total body acceleration and respective timestamps
for row, AccelDataFile in enumerate(dystoniaFilesDF['AccelData.csv']):
    
    if not isinstance(AccelDataFile, float):
        
        # print 
        print('\n\n----Organize the following file and display the new dataframe----: {}'.format(AccelDataFile))
        
        # build proper path for the local use to access data
        guf.allow_local_search(AccelDataFile)

        # organize acceleration data with timestamps from one session 
        organized_AccelDF = buildAccelDF(AccelDataFile)
        
        # display the st
        print(organized_AccelDF)

        #create the path of the new file
        temp_path = dystoniaFilesDF['neuron.mat'].iloc[row].split('\\')[:-1]
        
        # define file extension
        file_type = "pkl"
        
        # 
        temp_path.append(file_pattern+AccelDataFile.split('\\')[-1][:-3]+file_type)
        path2save_organized_AccelDF = '\\'.join(temp_path)
        
        # inform the user that a new file was created
        print('A new file was created in the following folder: {}'.format(path2save_organized_AccelDF))
        
        # save the new structured file as pickle
        organized_AccelDF.to_pickle(path2save_organized_AccelDF)
        
        # save the path of the file that was created in the list of paths
        TotalBAccelpaths.append(path2save_organized_AccelDF)
    else:

        # if no file was created for a particular session, then leave the cell empty
        TotalBAccelpaths.append(np.nan)

#create a new column in dystoniaFilesDF to save the path of the new file
dystoniaFilesDF['TotalBodyAccel.pkl'] = TotalBAccelpaths

# call function to update dystonia database
guf.update_dystonia_database(dystoniaFilesDF, True)