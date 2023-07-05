# this module contains functions that are used in most of the file managment and data analysis modules

# import necessary packages
import pandas as pd
import numpy as np

# load dystonia database
def load_dystonia_database():
    
    # file path
    dystoniaFilesDFpath = "G:\\.shortcut-targets-by-id\\1MH0egFqTqTToPE-wxCs7mDWL48lVKqDB\\EurDyscover\\Dystonia_Data\\dystoniaFilesDF.pkl"
    # open pickle file as df
    dystoniaFilesDF = pd.read_pickle(dystoniaFilesDFpath)

    return dystoniaFilesDF

# save updated dystonia database
def update_dystonia_database(dystoniaFilesDF):

    # define a path for the updated file
    path2saveDF = "G:\.shortcut-targets-by-id\1MH0egFqTqTToPE-wxCs7mDWL48lVKqDB\EurDyscover\Dystonia_Data\\dystoniaFilesDF.pkl"
    # save the dataframe as pickle
    dystoniaFilesDF.to_pickle(path2saveDF)
    # inform the user that the file wa successfully updated
    print('\n\nThe dystoniaFilesDF.pkl file was updated.')

import sys
sys.path.append("C:\\Users\\Administrador\\DystoniaAnalysis")

