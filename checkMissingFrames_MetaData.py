#This module opens metadata files containing information on missing frames and 
#...retrives the respective missing frames for correction of C_raw data

# xml - Extensible Markup Language -> tree of elements

#Two libraries for processing xml files
# xml.sax -> Simple API for XML (you can read pieces only and not the full file, in case of lack of resources, not enough RAM, for example)
# xml.dom -> Document Object Model

import os
from os import walk
import numpy as np
import xml.etree.ElementTree as ET

#parent file path
file_path = "E:\\.shortcut-targets-by-id\\1MH0egFqTqTToPE-wxCs7mDWL48lVKqDB\\EurDyscover\\Imaging"

test_xml_file = "E:\\.shortcut-targets-by-id\\1MH0egFqTqTToPE-wxCs7mDWL48lVKqDB\\EurDyscover\\Imaging\\A2A G1\\W03\\43509_RF_W3\\recording_20210819_125428.xml"

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

    #inform the user about the file that is being processed, and show the array of dropped frames
    print('Searching for dropped frames  in: {}\nResult: {}'.format(path_xml, np.array(droppedFrames)))

    return droppedFrames
     

for file_path, subdirs, files in os.walk(file_path):
    for name in files:
        print(os.path.join(file_path, name))

        #save the np.array in the respective path as .npy

        #save the path in the respective dataframe cell

#create a new column in the dystoniaFilesDF with the array of missing frames
