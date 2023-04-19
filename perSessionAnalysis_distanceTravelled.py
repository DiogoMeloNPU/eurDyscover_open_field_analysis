# import necessary packages
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# open the dystoniaFilesDF.csv that was created in DystoniaDataFrame.py
dystoniaFilesDFpath = "G:\\.shortcut-targets-by-id\\1MH0egFqTqTToPE-wxCs7mDWL48lVKqDB\\EurDyscover\\Dystonia_Data\\dystoniaFilesDF.pkl"
dystoniaFilesDF = pd.read_pickle(dystoniaFilesDFpath)

# define groups for analysis
surgeries = ['SNL', 'Sham']
genotypes = ['DYT1', 'WT']
sessions = ['BL1', 'W3', 'W9']

groups = np.array(np.meshgrid(surgeries, genotypes, sessions)).T.reshape(-1, 3)

# create a function to get the necessary files from each group

# create empty list to save the values for each session
allMiceResults = []

for group in groups:
    groupSpecs = '_'.join(group)
    groupFiles = 