#this module organizes every file containing the DLC predictions for easier manipulation of the data as a pandas dataframe
#it also stores each new file in the respective folder containing all other files (neuron.mat, simpler_neuron.mat, AccelData.csv,
# FrameDiff.csv, VideoProcessed.csv)

from os import walk
import pandas as pd
import numpy as np
import os

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

#delete
for DLCpredictionFile in dystoniaFilesDF['DLC_coordinate_prediction.csv']:
    print(type(DLCpredictionFile))

#create a new file with an organized dataframe of DLC predictions for all prediction files
for DLCpredictionFile in dystoniaFilesDF['DLC_coordinate_prediction.csv']:
    if not isinstance(DLCpredictionFile, float):
        print('----Organize the following file and display the new dataframe----: {}\n'.format(DLCpredictionFile))
        #organized_DLC_predictionsDF = organizeDLCinfo(DLCpredictionFile)
        print(organized_DLC_predictionsDF)
        path2save_organizedDLC_DF = #same path as the other files, not the path of the original DLC file (which was in a separate folder)
        path2save_organizedDLC_DF.to_csv(path2save_organizedDLC_DF)
