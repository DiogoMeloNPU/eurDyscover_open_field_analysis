#this module returns the paths of the videos whose DLC predictions were not filtered

import pandas as pd
import numpy as np
import os

#open the dystoniaFilesDF.csv that was created in DystoniaDataFrame.py
dystoniaFilesDFpath = "J:\\O meu disco\\EurDyscover\\Dystonia_Data\\dystoniaFilesDF.pkl"
dystoniaFilesDF = pd.read_pickle(dystoniaFilesDFpath)

#create a variable to save the paths of the videos whose DLC predictions were not filtered
missingFiltering = []
#iterate through the file to search only the column in the 2D array corresponding to the video paths
for i, path in enumerate(dystoniaFilesDF['VideoProcessed.avi']):
    if isinstance(path, str):
        videoName = path.split('\\')[-1][:-4]
        filePatternDLC = 'DLC_resnet50_Dystonia_TestApr21shuffle1_500000_filtered.csv'
        name2search4 = videoName+filePatternDLC
        file2search4 = np.append(np.array(path.split('\\')[:-1]), name2search4)
        file2search4 = str('\\\\'.join(file2search4))
        #if the file doesn't exist print its name and append the video path
        if not os.path.exists(file2search4):
            print('This file does not exist: {}'.format(file2search4))
            missingFiltering.append(path)

#print the number of videos that were not analyzed
if len(missingFiltering) == 0:
    print('All predictions were filtered!')
elif len(missingFiltering) == 1:
    print('Only one DLC file missing filtering.')
else:
    print('!!A total of {} prediction files were not filtered!!'.format(
        len(missingFiltering)))

#print the array
print(missingFiltering)

#convert to np.array and save the variable as a .npy
missingFiltering = np.array(missingFiltering)
save_here = "J:\\O meu disco\\EurDyscover\\Dystonia_Data\\missingFiltering.npy"
np.save(save_here, missingFiltering, allow_pickle=True)
