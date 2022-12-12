#This module opens metadata files containing information on missing frames and 
#...retrives the respective missing frames for correction of C_raw data

import os
from os import walk
from xml.dom import minidom

#parent file path
file_path = "E:\\.shortcut-targets-by-id\\1MH0egFqTqTToPE-wxCs7mDWL48lVKqDB\\EurDyscover\\Imaging"

def retrieveMissingFrames(path_xml):
    '''
    This function opens a .xml file and returns an array corresponding to the missing frames.
    '''
    #parse the xml file by name
    file = minidrom.parse(path_xml)
    
    #
    
    return missingFrames
     

for file_path, subdirs, files in os.walk(file_path):
    for name in files:
        print(os.path.join(file_path, name))

        #save the np.array in the respective path as .npy

        #save the path in the respective dataframe cell

#create a new column in the dystoniaFilesDF with the array of missing frames
