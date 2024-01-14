#this module organizes the FrameDiff.csv files in dataframes containing a single column...
#with a number corresponding to the difference in number of frames from two consecutive frame
#Should this difference be more than one, than there are lost frames which should be corrected for
#using linear interpolation in the x, y DLC coordinate predictions
#New files containing this info will be saved as pkl and a new column will be added to the dystoniaFilesDF.csv file
#containing the respective paths in which those files will be stored

from os import walk
import pandas as pd
import numpy as np
import os
import re

#create a function that extracts only the frame diff value from the FrameDiff.csv
def buildFrameDiffDF(frameDiffPath):
    '''
    This function simplifies a FrameDiff.csv file to contain only the frame diff values.
    '''
    #open the file as a df
    df_frameDiff = pd.read_csv(frameDiffPath, header=None)

    #rename the frame diff column
    df_frameDiff.rename(columns={0: 'Frame diff'})

    #iterate through each df row to find the frame diff digit by recognizing a date pattern
    for index in range(len(df_frameDiff)):
        #create a value to account for the casses in which there may be 10 (2 digits) or more missing frames which is problematic for the pattern used to find the frame diff values
        num_digits = 1
        date = re.search(r' \d \d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])', df_frameDiff.iloc[index][0])
        if date == None:
            num_digits = 2
            date = re.search(
                r' \d\d \d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])', df_frameDiff.iloc[index][0])
        if date == None:
            num_digits = 3
            date = re.search(
                r' \d\d\d \d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])', df_frameDiff.iloc[index][0])
        if num_digits == 1:
            df_frameDiff.at[index, 'Frame diff'] = date.group()[1]
        elif num_digits == 2:
            df_frameDiff.at[index, 'Frame diff'] = date.group()[1:3]
    
    df_frameDiff = df_frameDiff.drop(0, axis=1)
    #convert to numeric values
    df_frameDiff['Frame diff'] = pd.to_numeric(df_frameDiff['Frame diff'])

    return df_frameDiff


#open the dystoniaFilesDF.pkl that was created in DystoniaDataFrame.py
#dystoniaFilesDFpath = "J:\\O meu disco\\EurDyscover\\Dystonia_Data\\dystoniaFilesDF.pkl"
#dystoniaFilesDF = pd.read_pickle(dystoniaFilesDFpath)
dystoniaFilesDFpath = r"H:\.shortcut-targets-by-id\1MH0egFqTqTToPE-wxCs7mDWL48lVKqDB\EurDyscover\Dystonia_Data\df_eurDyscover_open_field_analysis_files.xlsx"
dystoniaFilesDF = pd.read_excel(dystoniaFilesDFpath)

#now, let's create a dataframe for each of the FrameDiff files available and store them in Google Drive

#create an array to save the paths of the new FrameDiff.pkl files
FrameDiffpaths = []
#create a file pattern to name the new files (this files are already called *FrameDiff*)
file_pattern = 'Simple_'
#create a new pkl file with a dataframe containing the frame diff values
for row, FrameDiffFile in enumerate(dystoniaFilesDF['FrameDiff.csv']):
    if isinstance(FrameDiffFile, str):
        print('\n\n----Organize the following file and display the new dataframe----: {}'.format(FrameDiffFile))
        simple_FrameDiffDF = buildFrameDiffDF(FrameDiffFile)
        print(simple_FrameDiffDF)
        #create the path of the new file
        temp_path = dystoniaFilesDF['neuron.mat'].iloc[row].split('\\')[:-1]
        file_type = 'pkl'
        temp_path.append(file_pattern+FrameDiffFile.split('\\')[-1][:-3]+file_type)
        path2save_simple_FrameDiffDF = '\\'.join(temp_path)
        print('A new file was created in the following folder: {}'.format(path2save_simple_FrameDiffDF))
        simple_FrameDiffDF.to_pickle(path2save_simple_FrameDiffDF)
        FrameDiffpaths.append(path2save_simple_FrameDiffDF)
    else:
        FrameDiffpaths.append(np.nan)

#create a new column in dystoniaFilesDF to save the path of the new line
dystoniaFilesDF['Simple_FrameDiff.pkl'] = FrameDiffpaths

#show the df
print(dystoniaFilesDF)

#save the df as a pkl file in google drive - this will overwrite (update) dystoniaFilesDF.pkl
path2saveDF = dystoniaFilesDFpath
dystoniaFilesDF.to_excel(path2saveDF)
print('\n\nThe file database was updated.')

#while dystoniaFilesDF is incomplete, just save it to the Desktop to check if is is being created correctly
#DesktopPath = "C:\\Users\\Admin\\Desktop\\CheckDystoniaDF\\DystoniaDataBase.csv"
#dystoniaFilesDF.to_csv(DesktopPath)