# import necessary packages
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# open the dystoniaFilesDF.csv that was created in DystoniaDataFrame.py
#dystoniaFilesDFpath = "G:\\.shortcut-targets-by-id\\1MH0egFqTqTToPE-wxCs7mDWL48lVKqDB\\EurDyscover\\Dystonia_Data\\dystoniaFilesDF.pkl"
#dystoniaFilesDF = pd.read_pickle(dystoniaFilesDFpath)
dystoniaFilesDFpath = r"H:\.shortcut-targets-by-id\1MH0egFqTqTToPE-wxCs7mDWL48lVKqDB\EurDyscover\Dystonia_Data\df_eurDyscover_open_field_analysis_files.xlsx"
dystoniaFilesDF = pd.read_excel(dystoniaFilesDFpath)

# define groups for analysis
surgeries = ['SNL', 'Sham']
genotypes = ['DYT1', 'WT']
sessions = ['BL1', 'W3', 'W9']

groups = np.array(np.meshgrid(surgeries, genotypes, sessions)).T.reshape(-1, 3)

# create a function to get the necessary files from each group
def getRatioHindPaws(group):
    respectiveFiles = dystoniaFilesDF['ratio_hindPaws.npy'].loc[(dystoniaFilesDF['Surgery'] == group[0]) & (dystoniaFilesDF['Genotype'] == group[1]) & (dystoniaFilesDF['Session'] == group[2])]
    respectiveFiles = [file for file in respectiveFiles if isinstance(file, str)]

    return respectiveFiles   

# create empty list to save the values for each session
allMiceResults = []

for group in groups:
    groupSpecs = '_'.join(group)
    groupFiles = getRatioHindPaws(group)
    miceIDs = [str(file.split('\\')[-2].split('_')[0]) for file in groupFiles]
    groupValues = np.array([np.load(file) for file in groupFiles])
    group_n = groupValues.shape[0]
    for mice in range(group_n):
        arr1 = np.array([str(miceIDs[mice]), str(groupSpecs)])
        arr2 = np.array(groupValues[mice])
        mean_arr2 = np.mean(arr2)
        #miceValues = np.concatenate((arr1, arr2))
        miceValues = np.append(arr1, mean_arr2); print(miceValues)
        allMiceResults.append(miceValues)

# convert dictionary to dataframe
df_results_per_mice = pd.DataFrame(allMiceResults)

# change column names
df_results_per_mice.columns = ['miceID', 'groupSpecs', 'ratioDistances_digitalTip_heel_hindPaws']

# display the results
print(df_results_per_mice)

# create a path to save the dataframe containing results for all sessions
filePathResultsPerMice = "H:\\.shortcut-targets-by-id\\1MH0egFqTqTToPE-wxCs7mDWL48lVKqDB\\EurDyscover\\Dystonia_Data\\perSessionAnalysis_meanRatioHindPaws.csv"
df_results_per_mice.to_csv(filePathResultsPerMice, index = False)