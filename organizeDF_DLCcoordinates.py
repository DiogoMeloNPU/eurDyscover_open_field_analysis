#this module organizes every file containing the DLC predictions for easier manipulation of the data as a pandas dataframe
#it also stores each new file in the respective folder containing all other files (neuron.mat, simpler_neuron.mat, AccelData.csv,
# FrameDiff.csv, VideoProcessed.csv)
#finally it updates the dystoniaFilesDF.pkl with a new column with the paths for the files created here

from os import walk
import pandas as pd
import numpy as np
import os
#import the module necessary for obtaining the camera timestamps
from organize_AccelDataTimestamps import open_AccelData_asDF, get_camera_timestamps

def buildDLCpredictionsDF(path_predictions_DLC, path_acceldata):
    '''
    This function organizes the csv file contanining the DLC predictions for bodypart coordinates 
    (as well as label likelihood) into a more structured and easier to manipulate dataframe. Furthermore, 
    it adds a new column to the df with the camera timestamps.
    '''
    df_DLC = pd.read_csv(path_predictions_DLC)
    df_DLC = df_DLC.drop(columns='scorer')
    df_DLC.iloc[0] + ' ' + '(' + df_DLC.iloc[1] + ')'
    df_DLC.iloc[0] = df_DLC.iloc[0] + ' ' + '(' + df_DLC.iloc[1] + ')'
    df_DLC.drop(index=1)
    df_DLC.columns = df_DLC.iloc[0]
    df_DLC = df_DLC.drop(index=0)
    df_DLC = df_DLC.drop(index=1)
    df_DLC.reset_index(inplace = True, drop = True)
    df_DLC.rename_axis('Index', axis='columns', inplace=True)
    for column in df_DLC.columns:
        df_DLC[column] = pd.to_numeric(df_DLC[column])

    #save the timestamps, the first and last TTLs in separate variables
    timestamps, first_TTL, last_TTL = get_camera_timestamps(path_acceldata)

    #delete
    print("Length DLC predictions: {}\nLength timestamps: {}\nfirst_TTL: {}\nlast_TTL: {}\n".format(len(df_DLC), len(timestamps), first_TTL, last_TTL))

    #note that it is possible that the last timestamp does not have a correspondent frame
    #check the dimensions and eliminate the last TTL if necessary
    if len(df_DLC) == len(timestamps):
        #add the column with the camera timestamps
        df_DLC['Timestamp'] = timestamps
    elif len(df_DLC) == len(timestamps)-1:
        #remove the last element from the timestamps array
        df_DLC['Timestamp'] = timestamps[:-1]
    else:
        print("-"*15+"The selected timestamps don't match the DLC predictions"+"-"*15)

    return df_DLC #dataframe with the DLC predictions

#open the dystoniaFilesDF.csv that was created in DystoniaDataFrame.py
dystoniaFilesDFpath = "E:\\.shortcut-targets-by-id\\1MH0egFqTqTToPE-wxCs7mDWL48lVKqDB\\EurDyscover\\Organized_data_JAS\\dystoniaFilesDF.pkl"
dystoniaFilesDF = pd.read_pickle(dystoniaFilesDFpath)

#create an array to save the paths of the new OrganizedDLC files
OrganizedDLCpaths = []
#create a file pattern to name the new files
file_pattern = 'OrganizedDLC_'
#create a new file with an organized dataframe of DLC predictions for all prediction files
for row, (DLCpredictionFile, AccelDataFile) in enumerate(zip(dystoniaFilesDF['DLC_coordinate_prediction.csv'], dystoniaFilesDF['AccelData.csv'])):
    #if the two files are present...
    if isinstance(DLCpredictionFile, str) and isinstance(AccelDataFile, str):
        #print('\n\n----Organize the following file and display the new dataframe----: {}'.format(DLCpredictionFile))
        organized_DLC_predictionsDF = buildDLCpredictionsDF(DLCpredictionFile, AccelDataFile)
        print(organized_DLC_predictionsDF)
        print(DLCpredictionFile, AccelDataFile)
        print('\n'*5)
        #create the path of the new file
        #temp_path = dystoniaFilesDF['neuron.mat'].iloc[row].split('\\')[:-1]
        #file_type = 'pkl'
        #temp_path.append(file_pattern+DLCpredictionFile.split('\\')[-1][:-3]+file_type) 
        #same path as the other files, not the path of the original DLC file (which was in a separate folder)
        #path2save_organizedDLC_DF = '\\'.join(temp_path)
        #print('A new file was created in the following folder: {}'.format(path2save_organizedDLC_DF))
        #organized_DLC_predictionsDF.to_pickle(path2save_organizedDLC_DF)
        #OrganizedDLCpaths.append(path2save_organizedDLC_DF)
    else:
        OrganizedDLCpaths.append(np.nan)
        
#create a new column in dystoniaFileDF to save the path of the new file
#dystoniaFilesDF['OrganizedDLC_coordinate_predictions.pkl'] = OrganizedDLCpaths

#show the df
#print(dystoniaFilesDF)

#save the dataframe as a pickle file in google drive - this will overwrite the fist dystoniaFilesDF.csv
#path2saveDF = dystoniaFilesDFpath
#dystoniaFilesDF.to_pickle(path2saveDF)
#print('\n\nThe dystoniaFileDF.pkl file was updated.')