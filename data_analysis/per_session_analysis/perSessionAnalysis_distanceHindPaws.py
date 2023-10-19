# this file contains the necessary functions to compute a metric of paw opening
# ratio between the distance between the digital tips of the left and right hind paws and the...
# distance between the heels of the left and right hind paws 

# import necessary packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import dlc2kinematics # (https://github.com/AdaptiveMotorControlLab/DLC2Kinematics)

cutOffLikelihood = 0.99 # under which data points are not considered for analysis

cutOffStandingStill = 0.25 # cm/s

def computeStandingStillFrames(npy_speedPath):

    # load the npy file containing the speed of the tailbase during one specific session
    speedTailBase = np.load(npy_speedPath)

    # find speed datapoint with likelihood 0.99 or above
    compliantLikelihood = speedTailBase[1] >= cutOffLikelihood
    
    # create an npy array with the indexes of the frames in which the animal is standing still
    frames_StandingStill = np.where(speedTailBase[0][compliantLikelihood] < cutOffStandingStill)[0]

    return frames_StandingStill


def ratioDigitalTipsHeels(path_h5_DLC, npy_speedPath):

    # load the respective DLC coordinates
    df_coordinatesDLC, _, _ = dlc2kinematics.load_data(path_h5_DLC)

    # access only the frames that have a compliant likelihood and where the animal is considered to be standing still
    df_coordinatesDLC_standingStill = df_coordinatesDLC.iloc[computeStandingStillFrames(npy_speedPath)]
    
    # simplify the dataframe to include only x and y coordinates for left digitalTip hindpaw, right digitalTip hindpaw, left heel hindpaw, right heel hindpaw
    df_coordinatesDLC_standingStill_hindPaws = df_coordinatesDLC_standingStill.DLC_resnet50_Dystonia_TestApr21shuffle1_500000[['left_hindlimb_digitaltip', 'right_hindlimb_digitaltip', 'left_hindlimb_heel', 'right_hindlimb_heel']]

    # simplify the dataframe to include only the x and y subdivisions (exclude likelihood)
    df_coordinatesDLC_standingStill_hindPaws = df_coordinatesDLC_standingStill_hindPaws.loc[:, (slice(None), ['x', 'y'])]
    
    # compute euclidian distance between the digital tips of the hind paws
    df_coordinatesDLC_standingStill_hindPaws['dist_digitalTips'] = np.sqrt((df_coordinatesDLC_standingStill_hindPaws.loc[:, ('left_hindlimb_digitaltip', 'x')] - df_coordinatesDLC_standingStill_hindPaws.loc[:, ('right_hindlimb_digitaltip', 'x')])**2 + 
                                                                           (df_coordinatesDLC_standingStill_hindPaws.loc[:, ('left_hindlimb_digitaltip', 'y')] - df_coordinatesDLC_standingStill_hindPaws.loc[:, ('right_hindlimb_digitaltip', 'y')])**2)

    # compute euclidian distance between the heels of the hind paws
    df_coordinatesDLC_standingStill_hindPaws['dist_heels'] = np.sqrt((df_coordinatesDLC_standingStill_hindPaws.loc[:, ('left_hindlimb_heel', 'x')] - df_coordinatesDLC_standingStill_hindPaws.loc[:, ('right_hindlimb_heel', 'x')])**2 + 
                                                                           (df_coordinatesDLC_standingStill_hindPaws.loc[:, ('left_hindlimb_heel', 'y')] - df_coordinatesDLC_standingStill_hindPaws.loc[:, ('right_hindlimb_heel', 'y')])**2)

    # compute the ratio between the two former distances
    df_coordinatesDLC_standingStill_hindPaws['ratio_digitalTips_heels'] = df_coordinatesDLC_standingStill_hindPaws['dist_digitalTips'] / df_coordinatesDLC_standingStill_hindPaws['dist_heels']

    # convert the ratio metric to a numpy array to save in a separate file
    npy_ratio_distances = np.array(df_coordinatesDLC_standingStill_hindPaws.ratio_digitalTips_heels)

    # obtain the mean value for the whole session
    mean_ratio_digitalTips_heels = np.mean(npy_ratio_distances); print(mean_ratio_digitalTips_heels); print('\n')

    return npy_ratio_distances, mean_ratio_digitalTips_heels

#open the dystoniaFilesDF.csv that was created in DystoniaDataFrame.py
dystoniaFilesDFpath = "G:\\.shortcut-targets-by-id\\1MH0egFqTqTToPE-wxCs7mDWL48lVKqDB\\EurDyscover\\Dystonia_Data\\dystoniaFilesDF.pkl"
dystoniaFilesDF = pd.read_pickle(dystoniaFilesDFpath)

# compute locomotion percentage for all sessions

# create an array to save the paths of the npy containing the percentages
ratio_hindPaws_paths = []

# create a file pattern for the new files containing the percentages
file_pattern = 'ratio_hindPaws_'

# corrected subfolders for DLC.h5 files
corrected_DLC_path = "G:\\.shortcut-targets-by-id\\1MH0egFqTqTToPE-wxCs7mDWL48lVKqDB\\"

for row, (npy_speedDLC, DLC_h5_file) in enumerate(zip(dystoniaFilesDF['npy_speed_DLC.pkl'], dystoniaFilesDF['DLC_coordinate_prediction.h5'])):
    if isinstance(npy_speedDLC, str) and isinstance(DLC_h5_file, str):
        # correct path of DLC.h5 files
        DLC_h5_file = corrected_DLC_path + '\\'.join(DLC_h5_file.split('\\')[2:]); print(DLC_h5_file)
        # print(f'\n\n----Processing the following files----: {npy_speedDLC} and {DLC_h5_file}')
        npy_ratio_distances, mean_ratio_digitalTips_heels = ratioDigitalTipsHeels(DLC_h5_file, npy_speedDLC)
        print(npy_ratio_distances)
        # create the path of the new file
        beginningPath = 'G:\\.shortcut-targets-by-id\\1MH0egFqTqTToPE-wxCs7mDWL48lVKqDB\\'
        temp_path = beginningPath.split('\\') + dystoniaFilesDF['neuron.mat'].iloc[row].split('\\')[2:-1]
        file_type = 'npy'
        temp_path.append(file_pattern + npy_speedDLC.split('\\')[-1][:-3] + file_type)
        path2save_results = '\\'.join(temp_path)
        np.save(path2save_results, npy_ratio_distances)
        # print('A new file was created in the following folder: {}'.format(path2save_results))
        ratio_hindPaws_paths.append(path2save_results)
    else:
        ratio_hindPaws_paths.append(np.nan)

#create a new column in dystoniaFilesDF to save the path of the new line
dystoniaFilesDF['ratio_hindPaws.npy'] = ratio_hindPaws_paths

#show the df
print(dystoniaFilesDF)

#save the df as a pkl file in google drive - this will overwrite (update) dystoniaFilesDF.pkl
path2saveDF = dystoniaFilesDFpath
dystoniaFilesDF.to_pickle(path2saveDF)
print('\n\nThe dystoniaFilesDF.pkl file was updated.')