#please note that this code is not resusable for other excel files, this works without alterations specifically for 
# 'Mice list_Dystonia_WORKING_230922.xlsx' (14-10-2022)
import pandas as pd
import numpy as np

dystoniaMiceInfoPath = "E:\\.shortcut-targets-by-id\\1MH0egFqTqTToPE-wxCs7mDWL48lVKqDB\\EurDyscover\\Mice list_Dystonia_WORKING_230922.xlsx"
dystoniaMiceInfoDF = pd.read_excel(dystoniaMiceInfoPath)
#process the dataframe in order to have a single continous list

#Eliminate empty rows and columns
dystoniaMiceInfoDF = dystoniaMiceInfoDF.drop(dystoniaMiceInfoDF.columns[[0, 8, 9, 17]], axis=1)
dystoniaMiceInfoDF = dystoniaMiceInfoDF.drop(dystoniaMiceInfoDF.index[[0, 2, 4]])
dystoniaMiceInfoDF.reset_index(inplace=True)  # reset index
dystoniaMiceInfoDF = dystoniaMiceInfoDF.drop(dystoniaMiceInfoDF.index[25:])
#split the dataframe in two (D1 and D2)
D1dystoniaMiceInfoDF = dystoniaMiceInfoDF.iloc[1:-1,1:-7] #this df contains detailed info for D1 CRE mice
D2dystoniaMiceInfoDF = dystoniaMiceInfoDF.iloc[2:, 8:] #this df contains detailed info for D2 CRE mice
#stack the two dataframes
D1dystoniaMiceInfoDF.columns = D1dystoniaMiceInfoDF.iloc[0]
D2dystoniaMiceInfoDF.columns = D1dystoniaMiceInfoDF.iloc[0]
dystoniaMiceInfoDF = pd.concat([D1dystoniaMiceInfoDF, D2dystoniaMiceInfoDF], ignore_index=True)
dystoniaMiceInfoDF = dystoniaMiceInfoDF.iloc[1: , :] #drop the first row
dystoniaMiceInfoDF.reset_index(inplace=True)  # reset index
dystoniaMiceInfoDF = dystoniaMiceInfoDF.iloc[:, 1:] #eliminate first column (incorrect indices)
dystoniaMiceInfoDF = dystoniaMiceInfoDF.rename_axis('', axis = 'columns') #remove the '1' that was 'labeling' the df indices

#dystoniaFilesDF contains detailed information on all mice used
#it is necessary to create a new df in which each row of dystoniaMiceIndoDF is replicated as much times as the number of sessions
session = ['BL1', 'BL2', 'W01', 'W03', 'W06', 'W09']
dystoniaFilesDF = pd.DataFrame(np.repeat(dystoniaMiceInfoDF.values, len(session), axis=0))
dystoniaFilesDF.columns = dystoniaMiceInfoDF.columns

#add new empty columns on which the google drive paths for every file type will be added (neuron.mat, 
#                                                                                         simpler_neuron.mat (simpler mat file that can be oppened in python), 
#                                                                                         AccelData.csv, 
#                                                                                         DLC_coordinate_predictions.csv, 
#                                                                                         FrameDiff_Centroid.csv, 
#                                                                                         VideoProcessed.avi)
files_available = ['neuron.mat', 'Simpler_neuron.mat', 'AccelData.csv', 'DLC_coordinate_prediction.csv',
                   'FrameDiff.csv', 'VideoProcessed.avi']
for file_type in files_available:
    dystoniaFilesDF[file_type] = np.nan

#show dystoniaFilesDF dataframe
print(dystoniaFilesDF)
print(dystoniaFilesDF.columns)

#use the following path to produce a file list
parentFolder = "E:\\.shortcut-targets-by-id\\1MH0egFqTqTToPE-wxCs7mDWL48lVKqDB\\EurDyscover\\Organized_data_JAS"

#use the lower level subfolder name to search for specific files using a file pattern

#rearrange the dataframe for multiindexing access