#this module returns the paths of the videos that were not analyzed by the DLC networks
#these correspond to those whose path is present in the videoPathsAndFPS.npy file, but whose DLC coordinate predictions csv file was not produced
#the need for this arose due to the fact that the DLC analyzes was stopped due to errors (not identified yet) which led to it not running completely

import numpy as np
import pandas as pd
import os

#open the dystoniaFilesDF.csv that was created in DystoniaDataFrame.py
dystoniaFilesDFpath = "J:\\O meu disco\\EurDyscover\\Dystonia_Data\\dystoniaFilesDF.pkl"
dystoniaFilesDF = pd.read_pickle(dystoniaFilesDFpath)

#create a variable to save the paths of the videos that were not analyzed
missingDLCanalysis = []
#iterate through the file to search for the rows in which there is not a path for a DLC file and then use that row index 
#...to find the name of the video that was not analyzed to give as input to the DLC network and produce the missing files
for i, path in enumerate(dystoniaFilesDF['DLC_coordinate_prediction.csv']):
    #if the DLC predictions file exists...
    if isinstance(path, str):
        continue
    #if the file doesn't exist, check if the video path is in the data frame, and if so, save the video path
    elif isinstance(dystoniaFilesDF['VideoProcessed.avi'][i], str):
        missingDLCanalysis.append(dystoniaFilesDF['VideoProcessed.avi'][i])
        
#keep in mind that for some lines there is no video and in those cases you should not save any info 

#print the number of videos that were not analyzed
if len(missingDLCanalysis) == 0:
    print('All videos were analyzed!\n')
elif len(missingDLCanalysis) == 1:
    print('Only one video missing the DLC analysis.\n')
else:
    print('!!A total of {} videos were not analyzed!!\n'.format(
        len(missingDLCanalysis)))

#print the array
print(missingDLCanalysis)

#convert to np.array and save the variable as a .npy
missingDLCanalysis = np.array(missingDLCanalysis)
save_here = "J:\\O meu disco\\EurDyscover\\Dystonia_Data\\missingDLCanalysis.npy"
np.save(save_here, missingDLCanalysis, allow_pickle=True)