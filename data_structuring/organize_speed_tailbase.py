#Import pickle and pandas
import pickle
import pandas as pd
import numpy as np

#Import the library DLC2Kinematics (https://github.com/AdaptiveMotorControlLab/DLC2Kinematics)
import dlc2kinematics

#open the dystoniaFilesDF.csv that was created in DystoniaDataFrame.py
#dystoniaFilesDFpath = r"H:\.shortcut-targets-by-id\1MH0egFqTqTToPE-wxCs7mDWL48lVKqDB\EurDyscover\Dystonia_Data\dystoniaFilesDF_old.pkl"
#dystoniaFilesDF = pd.read_pickle(dystoniaFilesDFpath)
dystoniaFilesDFpath = r"H:\.shortcut-targets-by-id\1MH0egFqTqTToPE-wxCs7mDWL48lVKqDB\EurDyscover\Dystonia_Data\df_eurDyscover_open_field_analysis_files.xlsx"
dystoniaFilesDF = pd.read_excel(dystoniaFilesDFpath)

# create an array to save the paths of the new DLC speed files (tailbase)
speedDLCpaths = []

#create a file pattern to name the new files (containing tailbase speed)
file_pattern = 'npy_speedDLC_'
file_type = 'pkl'

for row, h5_DLC in enumerate(dystoniaFilesDF['DLC_coordinate_prediction.h5']):
    if isinstance(h5_DLC, str):
        beginningPath = 'H:\\.shortcut-targets-by-id\\1MH0egFqTqTToPE-wxCs7mDWL48lVKqDB'
        print(f'\n\n----Organize the following file and display the new dataframe----: {h5_DLC}')
        df, bodyparts, scorer = dlc2kinematics.load_data(h5_DLC)
        df_speed = dlc2kinematics.compute_speed(df,bodyparts=['tailbase'], filter_window=5, order=1)
        # create the path of the new file 
        temp_path = beginningPath.split('\\') + dystoniaFilesDF['neuron.mat'].iloc[row].split('\\')[3:-1]; print(temp_path)
        file_type = '.npy'
        temp_path.append(file_pattern + h5_DLC.split('\\')[-1][:-3] + file_type)
        path2save_speedDLC = '\\'.join(temp_path)
        print('A new file was created in the following folder: {}'.format(path2save_speedDLC))
        numpy_speed = df_speed.DLC_resnet50_Dystonia_TestApr21shuffle1_500000.tailbase.to_numpy()
        numpy_speed = np.transpose(numpy_speed)
        print(numpy_speed)
        np.save(path2save_speedDLC, numpy_speed)
        speedDLCpaths.append(path2save_speedDLC)
    else:
        speedDLCpaths.append(np.nan)    

# create a new column in dystoniaFilesDF to save the path of the new line
dystoniaFilesDF['npy_speed_DLC.npy'] = speedDLCpaths

# show the df
print(dystoniaFilesDF)


#save the df as a pkl file in google drive - this will overwrite (update) dystoniaFilesDF.pkl
path2saveDF = dystoniaFilesDFpath
dystoniaFilesDF.to_excel(path2saveDF)
print('\n\nThe dystoniaFilesDF.pkl file was updated.')

'''
#while dystoniaFilesDF is incomplete, just save it to the Desktop to check if is is being created correctly
DesktopPath = "C:\\Users\\diogo\\OneDrive\\Ambiente de Trabalho\\DystoniaDataBase.csv"
dystoniaFilesDF.to_csv(DesktopPath)
'''
