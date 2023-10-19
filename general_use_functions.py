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
def update_dystonia_database(dystoniaFilesDF, save_csv):

    # define a path for the updated file
    path2saveDF = "G:\.shortcut-targets-by-id\1MH0egFqTqTToPE-wxCs7mDWL48lVKqDB\EurDyscover\Dystonia_Data\\dystoniaFilesDF.pkl"
    # save the dataframe as pickle
    dystoniaFilesDF.to_pickle(path2saveDF)
    # inform the user that the file wa successfully updated
    print('\n\nThe dystoniaFilesDF.pkl file was updated.')

    # create a function to save the database in the desktop as csv for easier visualization
    save_csv = True
    if save_csv:
        path2saveDF_save_csv = "C:\\Users\\Administrador\\Desktop"
        path2saveDF_save_csv.to_csv

def allow_local_search(file_path_in_database):

    # obtain the fixed part of the file path (ex: 'EurDyscover\\Dystonia_Data\\...\\example_file.pkl') - should change the file that creates the dataframe to already save it like this

    # cut the variable part from the (this should be done in the ) 