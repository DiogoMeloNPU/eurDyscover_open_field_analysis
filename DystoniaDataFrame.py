#please note that this code is not resusable for other excel files, this works without alterations specifically for 
# 'Mice list_Dystonia_WORKING_230922.xlsx' (14-10-2022)
from os import walk
import pandas as pd
import numpy as np
import os

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
dystoniaMiceInfoDF = dystoniaMiceInfoDF.rename_axis('Index', axis = 'columns') #remove the '1' that was 'labeling' the df indices

#dystoniaFilesDF contains detailed information on all mice used
#it is necessary to create a new df in which each row of dystoniaMiceIndoDF is replicated as much times as the number of sessions
session = ['BL1', 'BL2', 'W1', 'W3', 'W6', 'W9']
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

#add a new column containing the session time info (BL1, W09,...)
sessionInfo = np.array(session*dystoniaMiceInfoDF.shape[0]) #create the values for the new column
dystoniaFilesDF['Session'] = sessionInfo

#separate the 'Gene' column info in two columns: 'Genotype' - DYT1 or WT; 'CRE' - D1 or D2
gene = np.array(dystoniaFilesDF['Gene'])
gene = [session.replace(' ', '') for session in gene]
genotype = [session.split('/')[0] for session in gene]
cre = [session.split('/')[1][:-3] for session in gene]
dystoniaFilesDF['Genotype'] = genotype
dystoniaFilesDF['CRE'] = cre
dystoniaFilesDF.drop(columns = ['Gene'], inplace=True)

#temporarily add a new column to dystoniaFilesDF containing only the ID number
NumberID = np.array(dystoniaFilesDF['ID'])
NumberID = [str(numberID)[-5:]
            for numberID in NumberID]  # check for the '-0122' mice
dystoniaFilesDF['NumberID'] = NumberID

#Now, the structure is ready to be filled with the paths of every available file
#starting with the DLC coordinates, which are stored in a separate Google Drive Folder named 'DLC_data_movie_processed'...
parentFolderDLC = "E:\\.shortcut-targets-by-id\\1MH0egFqTqTToPE-wxCs7mDWL48lVKqDB\\EurDyscover\\Organized_data_JAS\\DLC_data_movie_processed"

#filterDystoniaFilesDF = dystoniaFilesDF[(currentSession[0] in dystoniaFilesDF['ID']) & (dystoniaFilesDF['Session'] == currentSession[1])]
for path, subdirs, files in os.walk(parentFolderDLC):
    for name in files:
        if name.endswith('.csv'):
            # list containing the session (0), the mice id (1) and the path for the DLC coordinates .csv file (2)
            currentSession = [str(path).split('\\')[-2], str(path).split('\\')[-1][1:], os.path.join(path, name)]
            #if, in a specific row, there is a match for 'NumberID' (currentSession[0]) and 'Session' (currentSession[1]), 
            #then the path of the DLC file (currentSession[2]) should be added in that row in the cell from column 'DLC_coordinate_predictions.csv'
            match = dystoniaFilesDF.loc[(dystoniaFilesDF['Session'] == currentSession[0]) & (
                dystoniaFilesDF['NumberID'] == currentSession[1])]
            if len(match) == 1:
                dystoniaFilesDF['DLC_coordinate_prediction.csv'][match.index[0]] = currentSession[2]
                print('The following file path was added to the "DLC_coordinate_predictions" column: {}\n'.format(currentSession[2]))

#show df
print(dystoniaFilesDF)

#all the other files are organized in the same session folder...
#use the name of lower level subfolders to search for specific files using a file pattern

#use the following path to produce a file list
parentFolderOtherFiles_D1 = "E:\\.shortcut-targets-by-id\\1MH0egFqTqTToPE-wxCs7mDWL48lVKqDB\\EurDyscover\\Organized_data_JAS\\D1"
parentFolderOtherFiles_D2 = "E:\\.shortcut-targets-by-id\\1MH0egFqTqTToPE-wxCs7mDWL48lVKqDB\\EurDyscover\\Organized_data_JAS\\D2"
parentFoldersOtherFiles = np.array([parentFolderOtherFiles_D1, parentFolderOtherFiles_D2])

def build_proper_session_name(str_file_path):
    proper_session_name = (str(str_file_path).split('\\')[6])
    if proper_session_name == 'Baseline 1':
        proper_session_name = 'BL1'
    elif proper_session_name == 'Baseline 2':
        proper_session_name = 'BL2'
    return proper_session_name


for parent in parentFoldersOtherFiles:
    for path, subdirs, files in os.walk(parent):
        for name in files:
            #set the name to lower case characters
            name = name.lower()
            length_path = len(str(path).split('\\'))
            if length_path == 8: #meaning you are in a lowest level subfolder
                current_number_id = str(path).split('\\')[-1][:5]
                current_session = build_proper_session_name(path)
                current_file_path = os.path.join(path, name)
                currentFile = [current_number_id, current_session, current_file_path]
                #print(currentFile); print('\n')
                match = dystoniaFilesDF.loc[(dystoniaFilesDF['NumberID'] == currentFile[0]) & (dystoniaFilesDF['Session'] == currentFile[1])]
                if len(match) == 1:
                    #define if elif conditional statements to search for files of interest and assigned the respective path to the dataframe
                    #nested if else for neuron.mat and simpler_neuron.mat
                    if name.endswith('.mat'):
                        if 'simpler' in name: #simpler_neuron.mat
                            dystoniaFilesDF['Simpler_neuron.mat'][match.index[0]] = currentFile[2]
                            print('The following file path was added to the "simpler_neuron.mat" column: {}\n'.format(currentFile[2]))
                        else: #neuron.mat
                            dystoniaFilesDF['neuron.mat'][match.index[0]] = currentFile[2]
                            print('The following file path was added to the "neuron.mat" column: {}\n'.format(currentFile[2]))
                    # nested if else for AccelData.csv and FrameDiff.csv
                    elif name.endswith('.csv'):
                        if 'acceldata' in name and 'metadata' not in name: #acceldata.csv
                            dystoniaFilesDF['AccelData.csv'][match.index[0]] = currentFile[2]
                            print('The following file path was added to the "AccelData.csv" column: {}\n'.format(currentFile[2]))
                        elif 'framediff' in name: #frameDiff.csv
                            dystoniaFilesDF['FrameDiff.csv'][match.index[0]] = currentFile[2]
                            print('The following file path was added to the "FrameDiff.csv" column: {}\n'.format(currentFile[2]))
                        elif 'dlc_resnet50_dystonia_testapr21shuffle1_500000' in name:
                            dystoniaFilesDF['DLC_coordinate_prediction.csv'][match.index[0]] = currentFile[2]
                            print('The following file path was added to the "DLC_coordinate_prediction.csv" column: {}\n'.format(currentFile[2]))
                    elif name.endswith('.avi'): #videoProcessed.avi
                        if 'processed' in name:
                            dystoniaFilesDF['VideoProcessed.avi'][match.index[0]] = currentFile[2]
                            print('The following file path was added to the "VideoProcessed.avi" column: {}\n'.format(currentFile[2]))

#show the dataframe
print(dystoniaFilesDF)

#save the dataframe as a pickle file in google drive
path2saveDF = "E:\\.shortcut-targets-by-id\\1MH0egFqTqTToPE-wxCs7mDWL48lVKqDB\\EurDyscover\\Organized_data_JAS\\dystoniaFilesDF.pkl"
dystoniaFilesDF.to_pickle(path2saveDF)

#while dystoniaFilesDF is incomplete, just save it to the Desktop to check if is is being created correctly
DesktopPath = "C:\\Users\\user\\Desktop\\DystoniaDataBase.csv"
dystoniaFilesDF.to_csv(DesktopPath)

#form here on, this file should not be changed. If you want to improve this file, please perform those changes on a copy (this version is suposed to work only as a database for the file paths for easier and structured access to what is needed for a specific analysis,  which should be implemented in a separate .py module as well)