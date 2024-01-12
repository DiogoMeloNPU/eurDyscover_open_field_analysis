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

# create a function to get the necessary .npy files from each group
def getPercentageLocomotion(group):
    respectiveFiles = dystoniaFilesDF['percentageLocomotion.npy'].loc[(dystoniaFilesDF['Surgery'] == group[0]) & (dystoniaFilesDF['Genotype'] == group[1]) & (dystoniaFilesDF['Session'] == group[2])]
    respectiveFiles = [file for file in respectiveFiles if isinstance(file, str)]

    return respectiveFiles    

# create a dictionary to save the results (mean % and standard deviation)
dictResults = {}

# create empty list to save the values for each session
allMiceResults = []

for group in groups:
    groupSpecs = '_'.join(group)
    groupFiles = getPercentageLocomotion(group)
    miceIDs = [str(file.split('\\')[-2].split('_')[0]) for file in groupFiles]
    groupValues = np.array([np.load(file) for file in groupFiles])
    groupValues_mean = np.round(np.mean(groupValues, axis = 0), 3) 
    groupValues_std = np.round(np.std(groupValues, axis = 0), 3)
    mean_std = np.concatenate((groupValues_mean, groupValues_std))
    group_n = groupValues.shape[0]
    mean_std_n = np.append(mean_std, group_n)
    dictResults[groupSpecs] = mean_std_n
    for mice in range(group_n):
        arr1 = np.array([str(miceIDs[mice]), str(groupSpecs)])
        arr2 = np.array(groupValues[mice])
        miceValues = np.concatenate((arr1, arr2))
        allMiceResults.append(miceValues)

# convert dictionaries to dataframes
# df_results = pd.DataFrame(dictResults)
df_results_per_mice = pd.DataFrame(allMiceResults)

# change the row indexes
# df_results.index = ['% Locomotion', '% 5-10 cm/s', '% 10-20 cm/s', '% +20 cm/s', 'std_1', 'std_2', 'std_3', 'std_4', 'n']
df_results_per_mice.columns = ['miceID', 'groupSpecs', '% Locomotion', '% 5-10 cm/s', '% 10-20 cm/s', '% +20 cm/s']

# transpose the dataframe
# df_results = df_results.transpose()
# df_results_per_mice = df_results_per_mice.transpose()

# display the results
# print(df_results)
print(df_results_per_mice)

# create bar plot
# df_results.plot.line(y = '% Locomotion')
# display figure
#plt.show()

#plt.bar(df_results.index, df_results['% Locomotion'], yerr = df_results['std_1'], capsize=10)
#plt.show()

# create a path to save the dataframe containing results for all sessions
filePathResultsPerMice = "H:\\.shortcut-targets-by-id\\1MH0egFqTqTToPE-wxCs7mDWL48lVKqDB\\EurDyscover\\Dystonia_Data\\perSessionAnalysis_locomotionPercentages.csv"
df_results_per_mice.to_csv(filePathResultsPerMice, index = False)