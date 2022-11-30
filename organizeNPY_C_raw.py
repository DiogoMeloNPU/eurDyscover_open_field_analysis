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

    print(C_raw)

    #save the timestamps in a variable
    timestamps = get_microscope_timestamps(path_acceldata)
    print(timestamps)

    #there are cases in which there is a problem with the timestamps (check 30/11/2022 notebook for a sketch with an example), in a way that the length of the timestamsp doesn't match the length of the C raw data
    #in those cases, assign -1 to the C_raw array
    if len(timestamps[::2]) == C_raw.shape[1]:
        #join the timestamps info in the last position of the array (keep in mind that you should only consider one in each two inscopix timestamps)
        C_raw = np.vstack((C_raw, timestamps[::2]))
    else:
        C_raw = -1

    print(C_raw)
    #print(C_raw.shape)

    return C_raw

#open the dystoniaFilesDF.csv that was created in DystoniaDataFrame.py
dystoniaFilesDFpath = "E:\\.shortcut-targets-by-id\\1MH0egFqTqTToPE-wxCs7mDWL48lVKqDB\\EurDyscover\\Organized_data_JAS\\dystoniaFilesDF.pkl"
dystoniaFilesDF = pd.read_pickle(dystoniaFilesDFpath)

#now, let's create the C_raw array containing the respective timestamps for each of the SimplerNeuron.mat files available and store them in Google Drive

#create an array to save the paths of the new C_rawTS.npy files
C_raw_paths = []
#create a file pattern to name the new files (C_rawTS, meaning both the C_raw data, as well as the timestamps are in the array)
file_pattern = 'C_rawTS_'
#define the file type
file_type = '.npy'

for row, simplerNeuron in enumerate(dystoniaFilesDF['Simpler_neuron.mat']):
    if isinstance(simplerNeuron, str):
        print('\n\n----Organize the following file and display the new C_raw array containing the timestamps----: {}'.format(simplerNeuron))
        C_rawNPY = buildCrawNPY(simplerNeuron, dystoniaFilesDF['AccelData.csv'][row])
        if not isinstance(C_rawNPY, int):
            #create the path of the new file
            temp_path = dystoniaFilesDF['neuron.mat'].iloc[row].split('\\')[:-1]
            temp_path.append(file_pattern+simplerNeuron.split('\\')[-1][:-4]+file_type)
            path2save_organized_C_rawNPY = '\\'.join(temp_path)
            print('A new file was created in the following folder: {}'.format(path2save_organized_C_rawNPY))
            np.save(path2save_organized_C_rawNPY, C_rawNPY)
            C_raw_paths.append(path2save_organized_C_rawNPY)
        else:
            C_raw_paths.append(-1)
    else:
        C_raw_paths.append(np.nan)

#create a new column in dystoniaFilesDF to save the path of the new file
dystoniaFilesDF['C_rawNPY'] = C_raw_paths

#show the df
print(dystoniaFilesDF)

#save the dataframe as pkl file in google drive -  this will overwrite (update) the first dystoniaFilesDF.csv
path2saveDF = dystoniaFilesDFpath
dystoniaFilesDF.to_pickle(path2saveDF)
print('\n\nThe dystoniaFileDF.pkl file was updated.')


'''#delete - test
simplerNeuronPath = "E:\\.shortcut-targets-by-id\\1MH0egFqTqTToPE-wxCs7mDWL48lVKqDB\\EurDyscover\\Organized_data_JAS\\D1\\Baseline 1\\42308_RF_B1\\simpler_26-Jul_17_58_11.mat"
acceldata_path = "E:\\.shortcut-targets-by-id\\1MH0egFqTqTToPE-wxCs7mDWL48lVKqDB\\EurDyscover\\Organized_data_JAS\\D1\\Baseline 1\\42308_RF_B1\\AccelData2021-04-28T13_45_51.6713216+01_00.csv"
df_C_raw, timestamps = buildCrawNPY(simplerNeuronPath, acceldata_path)

plt.subplot(1, 2, 1)
plt.plot(range(len(timestamps[0::2])), timestamps[0::2])
plt.subplot(1, 2, 2)
plt.plot(range(len(timestamps[2::2])), timestamps[2::2])
plt.show()
'''