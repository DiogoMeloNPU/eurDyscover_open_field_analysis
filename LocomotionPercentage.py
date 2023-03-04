# this file creates the necessary functions to compute the percentage of time during which locomotion occured

# import necessary packages
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

camera_aq_rate = 30 # Hz

sideOpenField = 40 # cm
px_sideOpenField = 617.655 # pixels
conversionFactor_cm = sideOpenField/px_sideOpenField

cutOffLikelihood = 0.99 # under which data points are not considered for analysis

cutOffLocomotion = 5 # cm/s
second_cutOffLocomotion = 10 # cm/s
third_cutOffLocomotion = 20 # cm/s

# convert speed from px/fr to cm/s
def convert2_cm_s(speedNPY, conversionFactor_cm):
    speedNPY_cm_fr = speedNPY * conversionFactor_cm
    speedNPY_cm_s = speedNPY_cm_fr * camera_aq_rate

    return speedNPY_cm_s

# the next function recieves a numpy array containing the tailbase speed for one session as well as likelihoods and returns the % of time in locomotion
def locomotionPercentages(npy_speedPath):

    # load the file
    speedTailBase = np.load(npy_speedPath)

    # find speed datapoint with likelihood 0.99 or above
    compliantLikelihood = speedTailBase[1] >= cutOffLikelihood

    # convert the speed to cm/s
    speed_tailbase_cms = convert2_cm_s(speedTailBase[0][compliantLikelihood], conversionFactor_cm)

    # compute the number of points in the speed time series that is above the cutOff for locomotion
    numDataPointsLocomotion = np.sum(speed_tailbase_cms >= cutOffLocomotion)

    # compute the percentage of the session that consists in locomotion
    percentageLocomotionInSession = np.round(numDataPointsLocomotion/len(speed_tailbase_cms), 3) 

    # compute the number of datapoints (frames) form the current session in which the speed of the tailbase is within the first and second cutOff
    numDataPointsLocomotion_st_nd_cutOff = len(np.where((speed_tailbase_cms >= cutOffLocomotion) & (speed_tailbase_cms < second_cutOffLocomotion))[0])

    # compute the number of datapoints (frames) form the current session in which the speed of the tailbase is within the second and third cutOff
    numDataPointsLocomotion_nd_rd_cutOff = len(np.where((speed_tailbase_cms >= second_cutOffLocomotion) & (speed_tailbase_cms < third_cutOffLocomotion))[0])

    # compute the number of datapoints (frames) form the current session in which the speed of the tailbase is above the third cutOff
    numDataPointsLocomotion_above_rd_cutOff = np.sum(speed_tailbase_cms >= third_cutOffLocomotion)

    # obtain the percentage of the three defined intervals within session (percentage relative to total time in locomotion)
    percentageLocomotionInSession_st_nd = np.round(numDataPointsLocomotion_st_nd_cutOff/numDataPointsLocomotion, 3)
    percentageLocomotionInSession_nd_rd = np.round(numDataPointsLocomotion_nd_rd_cutOff/numDataPointsLocomotion, 3)
    percentageLocomotionInSession_above_rd = np.round(numDataPointsLocomotion_above_rd_cutOff/numDataPointsLocomotion, 3)

    return percentageLocomotionInSession, percentageLocomotionInSession_st_nd, percentageLocomotionInSession_nd_rd, percentageLocomotionInSession_above_rd

#open the dystoniaFilesDF.csv that was created in DystoniaDataFrame.py
dystoniaFilesDFpath = "G:\\.shortcut-targets-by-id\\1MH0egFqTqTToPE-wxCs7mDWL48lVKqDB\\EurDyscover\\Dystonia_Data\\dystoniaFilesDF.pkl"
dystoniaFilesDF = pd.read_pickle(dystoniaFilesDFpath)

# compute locomotion percentage for all sessions

# create an array to save the paths of the npy containing the percentages
percentageLocomotionPaths = []

# create a file pattern for the new files containing the percentages
file_pattern = 'percentagesLocomotion_'

for row, npy_speedDLC in enumerate(dystoniaFilesDF['npy_speed_DLC.pkl']):
    if isinstance(npy_speedDLC, str):
        print(f'\n\n----Processing the following file----: {npy_speedDLC}')
        percent1, percent2, percent3, percent4 = locomotionPercentages(npy_speedDLC)
        percentagesLocomotion = np.array([percent1, percent2, percent3, percent4])
        print(percentagesLocomotion)
        #create the path of the new file
        beginningPath = 'G:\\.shortcut-targets-by-id\\1MH0egFqTqTToPE-wxCs7mDWL48lVKqDB\\'
        temp_path = beginningPath.split('\\') + dystoniaFilesDF['neuron.mat'].iloc[row].split('\\')[2:-1]
        file_type = 'npy'
        temp_path.append(file_pattern + npy_speedDLC.split('\\')[-1][:-3] + file_type)
        path2save_percentages = '\\'.join(temp_path)
        np.save(path2save_percentages, percentagesLocomotion)
        print('A new file was created in the following folder: {}'.format(path2save_percentages))
        percentageLocomotionPaths.append(path2save_percentages)
    else:
        percentageLocomotionPaths.append(np.nan)

#create a new column in dystoniaFilesDF to save the path of the new line
dystoniaFilesDF['percentageLocomotion.npy'] = percentageLocomotionPaths

#show the df
print(dystoniaFilesDF)

#save the df as a pkl file in google drive - this will overwrite (update) dystoniaFilesDF.pkl
path2saveDF = dystoniaFilesDFpath
dystoniaFilesDF.to_pickle(path2saveDF)
print('\n\nThe dystoniaFilesDF.pkl file was updated.')

#while dystoniaFilesDF is incomplete, just save it to the Desktop to check if is is being created correctly
DesktopPath = "C:\\Users\\diogo\\OneDrive\\Ambiente de Trabalho\\DystoniaDataBase.csv"
dystoniaFilesDF.to_csv(DesktopPath)