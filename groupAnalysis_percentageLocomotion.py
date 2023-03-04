# import necessary packages
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

#open the dystoniaFilesDF.csv that was created in DystoniaDataFrame.py
dystoniaFilesDFpath = "G:\\.shortcut-targets-by-id\\1MH0egFqTqTToPE-wxCs7mDWL48lVKqDB\\EurDyscover\\Dystonia_Data\\dystoniaFilesDF.pkl"
dystoniaFilesDF = pd.read_pickle(dystoniaFilesDFpath)

# define groups for analysis
surgeries = ['SNL', 'Sham']
genotypes = ['DYT1', 'WT']
sessions = ['BL1', 'W3', 'W9']

groups = np.array(np.meshgrid(surgeries, genotypes, sessions)).T.reshape(-1, 3)

# create a function to get the necessary npy files from each group
def getPercentageLocomotion(group):
    respectiveFiles = dystoniaFilesDF['percentageLocomotion.npy'].loc[(dystoniaFilesDF['Surgery'] == group[0]) & (dystoniaFilesDF['Genotype'] == group[1]) & (dystoniaFilesDF['Session'] == group[2])]
    respectiveFiles = [file for file in respectiveFiles if isinstance(file, str)]

    return respectiveFiles    

# create a dictionary to save the results
dictResults = {}

for group in groups: 
    groupSpecs = '_'.join(group)
    groupFiles = getPercentageLocomotion(group)
    groupValues = np.array([np.load(file) for file in groupFiles])
    groupValues_mean = np.round(np.mean(groupValues, axis = 0), 3) 
    groupValues_std = np.round(np.std(groupValues, axis = 0), 3)
    mean_std = np.concatenate((groupValues_mean, groupValues_std))
    dictResults[groupSpecs] = mean_std

# display the results
df_results = pd.DataFrame(dictResults)

# change the row indexes
df_results.index = ['% Locomotion', '% 5-10 cm/s', '% 10-20 cm/s', '% +20 cm/s', 'std_1', 'std_2', 'std_3', 'std_4']

# transpose the dataframe
df_results = df_results.transpose()

print(df_results)

# create bar plot
# df_results.plot.line(y = '% Locomotion')
# display figure
#plt.show()

plt.bar(df_results.index, df_results['% Locomotion'], yerr = df_results['std_1'], capsize=10)
plt.show()