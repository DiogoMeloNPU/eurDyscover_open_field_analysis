#This module opens metadata files containing information on missing frames and 
#...retrives the respective missing frames for correction of C_raw data

#The approach will be analogous to other modules: I will search for the files and save
#the dropped frames as a .npy. Once this is done, I will save all the paths of the 
#.npy files in the dystoniaFilesDF. I will then be able to search for these files in 
#the 'organizeNPY_C_raw.py' module, which will have a corresponding C_raw file in the
#same dystoniaFilesDF row, and correct the C_raw .npy files for dropped frames

# xml - Extensible Markup Language -> tree of elements

#Two libraries for processing xml files
# xml.sax -> Simple API for XML (you can read pieces only and not the full file, in case of lack of resources, not enough RAM, for example)
# xml.dom -> Document Object Model

import pandas as pd
import os
from os import walk
import numpy as np
import xml.etree.ElementTree as ET

#open the dystoniaFilesDF.pkl that was created in DystoniaDataFrame.py
dystoniaFilesDFpath = "J:\\O meu disco\\EurDyscover\\Dystonia_Data\\dystoniaFilesDF.pkl"
dystoniaFilesDF = pd.read_pickle(dystoniaFilesDFpath)

def retrieveMissingFrames(path_xml):
    '''
    This function opens a .xml file and returns a nd.array corresponding to the missing frames.
    '''
    tree = ET.parse(path_xml)
    root = tree.getroot()

    #search for the text in the attribute with name 'dropped'
    droppedFrames = root.find(".//attr[@name='dropped']")

    #convert it to a numpy array
    droppedFrames = np.array(droppedFrames)

    return droppedFrames

# use the following path to produce a file list
parentFolderOtherFiles_D1 = "J:\\O meu disco\\EurDyscover\\Dystonia_Data\\D1"
parentFolderOtherFiles_D2 = "J:\\O meu disco\\EurDyscover\\Dystonia_Data\\D2"
parentFoldersOtherFiles = np.array([parentFolderOtherFiles_D1, parentFolderOtherFiles_D2])

# create an array to save the paths of the new droppedFrames.npy files
droppedFramesInscPaths = []
# create a file pattern to name the new files
file_pattern = 'droppedFramesInscopix_'
#create a new pkl file with a dataframe containing the frame diff values
for row, metaDataInscFile in enumerate(dystoniaFilesDF['MetadataInscopix.xml']):
    if isinstance(metaDataInscFile, str):
        print('\n\n----Extract and display the dropped frames for this inscopix file----: {}'.format(metaDataInscFile))
        droppedFrames_npy = retrieveMissingFrames(metaDataInscFile)
        print(droppedFrames_npy)
        #create the path of the new file
        temp_path = dystoniaFilesDF['MetadataInscopix.xml'].iloc[row].split('\\')[:-1]
        file_type = 'npy'
        temp_path.append(file_pattern+metaDataInscFile.split('\\')[-1][:-3]+file_type)
        path2save_droppedFrames_npy = '\\'.join(temp_path)
        print('A new file was created in the following folder: {}'.format(path2save_droppedFrames_npy))
        np.save(path2save_droppedFrames_npy, droppedFrames_npy)
        droppedFramesInscPaths.append(path2save_droppedFrames_npy)
    else:
        droppedFramesInscPaths.append(np.nan)

#create a new column in dystoniaFilesDF to save the path of the new line
dystoniaFilesDF['droppedFramesInscop.npy'] = droppedFramesInscPaths

#show the df
print(dystoniaFilesDF)

#save the df as a pkl file in google drive - this will overwrite (update) dystoniaFilesDF.pkl
path2saveDF = dystoniaFilesDFpath
dystoniaFilesDF.to_pickle(path2saveDF)
print('\n\nThe dystoniaFilesDF.pkl file was updated.')

#while dystoniaFilesDF is incomplete, just save it to the Desktop to check if is is being created correctly
DesktopPath = "C:\\Users\\Admin\\Desktop\\CheckDystoniaDF\\DystoniaDataBase.csv"
dystoniaFilesDF.to_csv(DesktopPath)