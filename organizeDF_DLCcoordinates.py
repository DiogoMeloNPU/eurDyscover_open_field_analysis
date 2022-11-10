#this module organizes every file containing the DLC predictions for easier manipulation of the data as a pandas dataframe
#it also stores each new file in the respective folder containing all other files (neuron.mat, simpler_neuron.mat, AccelData.csv,
# FrameDiff.csv, VideoProcessed.csv)
#finally is updates the dystoniaFilesDF.csv with a new column with the paths for the files created here

from os import walk
import pandas as pd
import numpy as np
import os
#import the module necessary for obtaining the camera timestamps
import organize_AccelDataTimestamps

def organizeDLCinfo(path_predictions_DLC):
    '''
    This function organizes the csv file contanining the DLC predictions for bodypart coordinates 
    (as well as label likelihood) into a more structured and easier to manipulate dataframe.
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

    return df_DLC #dataframe with the DLC predictions

#open the dystoniaFilesDF.csv that was created in DystoniaDataFrame.py
dystoniaFilesDFpath = "E:\\.shortcut-targets-by-id\\1MH0egFqTqTToPE-wxCs7mDWL48lVKqDB\\EurDyscover\\Organized_data_JAS\\dystoniaFilesDF.csv"
dystoniaFilesDF = pd.read_csv(dystoniaFilesDFpath)

#create an array to save the paths of the new OrganizedDLC files
OrganizedDLCpaths = []
#create a file pattern to name the new files
file_pattern = 'OrganizedDLC_'
#create a new file with an organized dataframe of DLC predictions for all prediction files
for row, DLCpredictionFile in enumerate(dystoniaFilesDF['DLC_coordinate_prediction.csv']):
    if not isinstance(DLCpredictionFile, float):
        print('\n\n----Organize the following file and display the new dataframe----: {}'.format(DLCpredictionFile))
        organized_DLC_predictionsDF = organizeDLCinfo(DLCpredictionFile)
        print(organized_DLC_predictionsDF)
        #create the path of the new file
        temp_path = dystoniaFilesDF['neuron.mat'].iloc[row].split('\\')[:-1]
        temp_path.append(file_pattern+DLCpredictionFile.split('\\')[-1]) 
        #same path as the other files, not the path of the original DLC file (which was in a separate folder)
        path2save_organizedDLC_DF = '\\'.join(temp_path)
        print('A new file was created in the following folder: {}'.format(path2save_organizedDLC_DF))
        organized_DLC_predictionsDF.to_csv(path2save_organizedDLC_DF)
        OrganizedDLCpaths.append(path2save_organizedDLC_DF)
    else:
        OrganizedDLCpaths.append(np.nan)
        
#create a new column in dystoniaFileDF to save the path of the new file
dystoniaFilesDF['OrganizedDLC_coordinate_predictions.csv'] = OrganizedDLCpaths

#show the df
print(dystoniaFilesDF)

#I already had the filepath
#save the dataframe as a csv file in google drive - this will overwrite the fist dystoniaFilesDF.csv
path2saveDF = "E:\\.shortcut-targets-by-id\\1MH0egFqTqTToPE-wxCs7mDWL48lVKqDB\\EurDyscover\\Organized_data_JAS\\dystoniaFilesDF.csv"
dystoniaFilesDF.to_csv(path2saveDF)
print('\n\nThe dystoniaFileDF.csv file was updated.')