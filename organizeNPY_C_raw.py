#this module creates a .npy array containing the C_raw data, as well as the Inscopix timestamps (which will always be the last row of the array)
#This file is then stored in the google drive subfolder corresponding to the session
#finally, it updates the dystoniaFilesDF.csv with a new column with the paths for the files created here

import matplotlib.pyplot as plt
import numpy as np
from os.path import dirname, join as pjoin
import scipy.io as sio
import pandas as pd
#import the module necessary for obtaining the Inscopix timestamps
from organize_AccelDataTimestamps import open_AccelData_asDF, get_microscope_timestamps

#create a function that builds the .npy given a 'Simpler_neuron.mat', as well as a 'AccelData.csv' file paths
def buildCrawNPY(path_SimplerNeuron, path_acceldata):
    '''
    This function creates a dataframe with the C_raw values of each neuron (single session).
    It also creates a column with the inscopix timestamps.            
    '''
    #this varible contains the information of the simpler_neuron.mat file python dictionary
    neuron_mat_info = sio.loadmat(path_SimplerNeuron)

    #save raw calcium signal in a separate array
    C_raw = neuron_mat_info['C_raw']

    #create a dataframe with the C_raw data
    df_C_raw = pd.DataFrame(C_raw)
    df_C_raw = df_C_raw.T  # transpose the calcium data

    #generate a label for each neuron of the dataframe (e.g.: neuron_1, neuron_2, ...)
    neuron_labels = []
    for neuron in range(1, C_raw.shape[0]+1):
        neuron_label = 'neuron_'+str(neuron)
        neuron_labels.append(neuron_label)
    #change the labels on the dataframe
    df_C_raw.columns = neuron_labels

    #save the timestamps in a variable
    timestamps = get_microscope_timestamps(path_acceldata)

    #delete - plot the timestamp diffs and check for missing data
    print(np.diff(timestamps[0:10:2]))
    print(timestamps)
    print(len(df_C_raw), len(timestamps[2:])/2, len(np.diff(timestamps[0::2])))

    #add a new column with the inscopix timestamps (keep in mind that you should only consider one in each two inscopix timestamps)
    df_C_raw['Timestamp'] = timestamps[::2]

    #delete
    print(df_C_raw)

    return df_C_raw

#SAVE NPY INSTEAD OF DATAFRAME

'''
plt.subplot(1,2,1)
plt.plot(range(len(timestamps[0::2])), timestamps[0::2])
plt.subplot(1,2,2)
plt.plot(range(len(timestamps[2::2])), timestamps[2::2])
plt.show()
'''

#delete - test
simplerNeuronPath = "E:\\.shortcut-targets-by-id\\1MH0egFqTqTToPE-wxCs7mDWL48lVKqDB\\EurDyscover\\Organized_data_JAS\\D1\\Baseline 1\\42308_RF_B1\\simpler_26-Jul_17_58_11.mat"
acceldata_path = "E:\\.shortcut-targets-by-id\\1MH0egFqTqTToPE-wxCs7mDWL48lVKqDB\\EurDyscover\\Organized_data_JAS\\D1\\Baseline 1\\42308_RF_B1\\AccelData2021-04-28T13_45_51.6713216+01_00.csv"
buildCrawNPY(simplerNeuronPath, acceldata_path)

#open the dystoniaFilesDF.csv that was created in DystoniaDataFrame.py
#dystoniaFilesDFpath = "E:\\.shortcut-targets-by-id\\1MH0egFqTqTToPE-wxCs7mDWL48lVKqDB\\EurDyscover\\Organized_data_JAS\\dystoniaFilesDF.pkl"
#dystoniaFilesDF = pd.read_pickle(dystoniaFilesDFpath)

#now, let's create a df for each of the SimplerNeuron.mat files available and store them in Google Drive

#create an array to save the paths of the new FrameDiff.pkl files
#C_raw_paths = []
#create a file pattern to name the new files
'''
#ADAPT THIS TO THE C_RAW DATA
#create a new pkl file with a dataframe containing the total body acceleration and respective timestamps
for row, AccelDataFile in enumerate(dystoniaFilesDF['AccelData.csv']):
    if not isinstance(AccelDataFile, float):
        print('\n\n----Organize the following file and display the new dataframe----: {}'.format(AccelDataFile))
        organized_AccelDF = buildAccelDF(AccelDataFile)
        print(organized_AccelDF)
        #create the path of the new file
        temp_path = dystoniaFilesDF['neuron.mat'].iloc[row].split('\\')[:-1]
        file_type = "pkl"
        temp_path.append(file_pattern+AccelDataFile.split('\\')[-1][:-3]+file_type)
        path2save_organized_AccelDF = '\\'.join(temp_path)
        print('A new file was created in the following folder: {}'.format(path2save_organized_AccelDF))
        organized_AccelDF.to_pickle(path2save_organized_AccelDF)
        TotalBAccelpaths.append(path2save_organized_AccelDF)
    else:
        TotalBAccelpaths.append(np.nan)

#create a new column in dystoniaFilesDF to save the path of the new file
dystoniaFilesDF['TotalBodyAccel.pkl'] = TotalBAccelpaths

#show the df
print(dystoniaFilesDF)

#save the dataframe as pkl file in google drive -  this will overwrite (update) the first dystoniaFilesDF.csv
path2saveDF = dystoniaFilesDFpath
dystoniaFilesDF.to_pickle(path2saveDF)
print('\n\nThe dystoniaFileDF.pkl file was updated.')
'''