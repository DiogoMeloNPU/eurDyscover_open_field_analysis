#please note that this code is not resusable for other excel files, this works without alterations specifically for 
# 'Mice list_Dystonia_WORKING_230922.xlsx' (14-10-2022)
import pandas as pd

dystoniaMiceInfoPath = "E:\\.shortcut-targets-by-id\\1MH0egFqTqTToPE-wxCs7mDWL48lVKqDB\\EurDyscover\\Mice list_Dystonia_WORKING_230922.xlsx"
dystoniaFilesDF = pd.read_excel(dystoniaMiceInfoPath)
#process the dataframe in order to have a single continous list

#Eliminate empty rows and columns
dystoniaFilesDF = dystoniaFilesDF.drop(dystoniaFilesDF.columns[[0, 8, 9, 17]], axis=1)
dystoniaFilesDF = dystoniaFilesDF.drop(dystoniaFilesDF.index[[0, 2, 4]])
dystoniaFilesDF.reset_index(inplace=True)  # reset index
dystoniaFilesDF = dystoniaFilesDF.drop(dystoniaFilesDF.index[25:])
#split the dataframe in two (D1 and D2)
D1dystoniaFilesDF = dystoniaFilesDF.iloc[1:-1,1:-7] #this df contains detailed info for D1 CRE mice
D2dystoniaFilesDF = dystoniaFilesDF.iloc[2:, 8:] #this df contains detailed info for D2 CRE mice
#stack the two dataframes
D1dystoniaFilesDF.columns = D1dystoniaFilesDF.iloc[0]
D2dystoniaFilesDF.columns = D1dystoniaFilesDF.iloc[0]
dystoniaFilesDF = pd.concat([D1dystoniaFilesDF, D2dystoniaFilesDF], ignore_index=True)
dystoniaFilesDF = dystoniaFilesDF.iloc[1: , :] #drop the first row
dystoniaFilesDF.reset_index(inplace=True)  # reset index
#dystoniaFilesDF#eliminate first column (incorrect indices)
#add new empty columns on which the google drive paths for every file type will be added (neuron.mat, 
#                                                                                         simpler_neuron.mat (simpler mat file that can be oppened in python), 
#                                                                                         AccelData.csv, 
#                                                                                         DLC_coordinate_predictions.csv, 
#                                                                                         FrameDiff_Centroid.csv, 
#                                                                                         VideoProcessed.avi)

#show the df
print(dystoniaFilesDF)

#use the following path to produce a file list
parentFolder = "E:\\.shortcut-targets-by-id\\1MH0egFqTqTToPE-wxCs7mDWL48lVKqDB\\EurDyscover\\Organized_data_JAS"

#use the lower level subfolder name to search for specific files using a file pattern

#rearrange the dataframe for multiindexing access