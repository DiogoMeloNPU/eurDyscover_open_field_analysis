import pandas as pd

dystoniaMiceInfoPath = "E:\\.shortcut-targets-by-id\\1MH0egFqTqTToPE-wxCs7mDWL48lVKqDB\\EurDyscover\\Mice list_Dystonia_WORKING_230922.xlsx"
dystoniaFilesDF = pd.read_excel(dystoniaMiceInfoPath)

#process the dataframe in order to have a single continouslist
dystoniaFilesDF = dystoniaFilesDF.drop(dystoniaFilesDF.columns[[0, 8, 9, 17]], axis=1)
dystoniaFilesDF = dystoniaFilesDF.drop(dystoniaFilesDF.index[[0,2]])
dystoniaFilesDF.reset_index(inplace=True)  # reset index
dystoniaFilesDF = dystoniaFilesDF.drop(dystoniaFilesDF.index[26:])

print(dystoniaFilesDF)
#use the following path to produce a file list
parentFolder = "E:\\.shortcut-targets-by-id\\1MH0egFqTqTToPE-wxCs7mDWL48lVKqDB\\EurDyscover\\Organized_data_JAS"

#use the lower level subfolder name to search for specific files using a file pattern