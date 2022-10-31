#In this file I will be using multiindexing to structure a pandas dataframe with all the files 
#available for the Dystonia Project

#COLUMNS
#D1/D2
#Sham/Lesioned
#WT/DYT
#BL1/BL2/W01/W03/W06/W09
#mice1/mice2/mice3/...

#ROWS
#neuron.mat
#simpler_neuron.mat (simpler mat file that can be oppened in python)
#AccelData.csv
#DLC_coordinate_predictions.csv
#FrameDiff_Centroid.csv
#VideoProcessed.avi

import pandas as pd

neurons = ['D1', 'D2']
surgery = ['Sham', 'Lesioned']
genotype = ['WT', 'DYT']
session = ['BL1', 'BL2', 'W01', 'W03', 'W06', 'W09']

cols = pd.MultiIndex.from_product([neurons, surgery, genotype, session])

files_available = ['Simpler_neuron.mat', 'AccelData.csv', 'DLC_coordinate_prediction',
    'FrameDiff.csv', 'VideoProcessed.avi']

dystoniaFilesDF = pd.DataFrame(columns = cols, 
                                index = files_available)

dystoniaFilesDF.index.names = ['file type']
print(dystoniaFilesDF)

#save the dataframe as csv/excel file
filepath = "E:\\.shortcut-targets-by-id\\1MH0egFqTqTToPE-wxCs7mDWL48lVKqDB\\EurDyscover\\Organized_data_JAS\\dystoniaFilesDF.csv"
#dystoniaFilesDF.to_csv(filepath)