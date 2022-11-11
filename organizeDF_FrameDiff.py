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
    date = re.search(
        r' \d \d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])', df_frameDiff.iloc[index][0])
    df_frameDiff.at[index, 'Frame diff'] = date.group()[1]
    #drop unecessary column
    df_frameDiff = df_frameDiff.drop(0, axis=1)
    #convert to numeric values
    df_frameDiff['Frame diff'] = pd.to_numeric(df_frameDiff['Frame diff'])

    return df_frameDiff