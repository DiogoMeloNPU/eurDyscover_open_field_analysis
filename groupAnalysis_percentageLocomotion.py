
for group in groups: 
    respectiveFiles = dystoniaFilesDF['npy_speed_DLC.pkl'].loc[(dystoniaFilesDF['Surgery'] == group[0]) & (dystoniaFilesDF['Genotype'] == group[1]) & (dystoniaFilesDF['Session'] == group[2])]
    respectiveFiles = [file for file in respectiveFiles if isinstance(file, str)]
    print(respectiveFiles)'''