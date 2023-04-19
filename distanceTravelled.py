# this file contains the necessary functions to compute the distance travelled by mice during a session
# ... using DLC data, and save this info in separate files

# import necessary packages
import numpy as np
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

def distanceTravelled(npy_speedPath):

    # load the file
    speedTailBase = np.load(npy_speedPath)

    # find speed datapoint with likelihood 0.99 or above
    compliantLikelihood = speedTailBase[1] >= cutOffLikelihood

    # convert the speed to cm/s
    speed_tailbase_cms = convert2_cm_s(speedTailBase[0][compliantLikelihood], conversionFactor_cm)

    # select datapoints (frames) in which tailbase speed time series is above the cutOff for locomotion
    speed_tailbase_Locomotion = speed_tailbase_cms[speed_tailbase_cms > cutOffLocomotion]

    # compute the number of points in the speed time series that is above the cutOff for locomotion
    numDataPointsLocomotion = np.sum(speed_tailbase_cms >= cutOffLocomotion)

    # compute the mean speed during locomotion
    meanSpeedLocomotion = np.mean(speed_tailbase_Locomotion)

    # time spend locomoting
    duration_s_Locomotion = numDataPointsLocomotion/(camera_aq_rate)

    # compute session duration
    session_duration_s = (speedTailBase.shape[1])/(camera_aq_rate)

    # compute the distance travelled in the current session
    distanceTravelledTailbase = meanSpeedLocomotion*duration_s_Locomotion

    # normalize the distance travelled to session duration (~20min baseline; ~10min other sessions)
    distanceTravelledTailbaseNormalized = distanceTravelledTailbase/session_duration_s

    return distanceTravelledTailbase, distanceTravelledTailbaseNormalized

#open the dystoniaFilesDF.csv that was created in DystoniaDataFrame.py
dystoniaFilesDFpath = "G:\\.shortcut-targets-by-id\\1MH0egFqTqTToPE-wxCs7mDWL48lVKqDB\\EurDyscover\\Dystonia_Data\\dystoniaFilesDF.pkl"
dystoniaFilesDF = pd.read_pickle(dystoniaFilesDFpath)

# compute distance travelled for all sessions

# create an array to save the paths of the .npy containing the distances travelled
distanceTravelledPaths = []

# create a file pattern for the new files containing the percentages
file_pattern = 'distanceTravelledTailbase_'

for row, npy_speedDLC in enumerate(dystoniaFilesDF['npy_speed_DLC.pkl']):
    if isinstance(npy_speedDLC, str):
        print(f'\n\n----Processing the following file----: {npy_speedDLC}')
        distTrav, distTravNorm = distanceTravelled(npy_speedDLC)
        distanceTravelledResults = np.array([distTrav, distTravNorm])
        print(distanceTravelledResults)
        # create the path of the new file
        beginningPath = 'G:\\.shortcut-targets-by-id\\1MH0egFqTqTToPE-wxCs7mDWL48lVKqDB\\'
        temp_path = beginningPath.split('\\') + dystoniaFilesDF['neuron.mat'].iloc[row].split('\\')[2:-1]
        file_type = 'npy'
        temp_path.append(file_pattern + npy_speedDLC.split('\\')[-1][:-3] + file_type)
        path2save_distances = '\\'.join(temp_path)
        np.save(path2save_distances, distanceTravelledResults)
        print('A new file was created in the following folder: {}'.format(path2save_distances))
        distanceTravelledPaths.append(path2save_distances)
    else:
        distanceTravelledPaths.append(np.nan)

#create a new column in dystoniaFilesDF to save the path of the new line
dystoniaFilesDF['distanceTravelled.npy'] = distanceTravelledPaths

#show the df
print(dystoniaFilesDF)

#save the df as a pkl file in google drive - this will overwrite (update) dystoniaFilesDF.pkl
path2saveDF = dystoniaFilesDFpath
dystoniaFilesDF.to_pickle(path2saveDF)
print('\n\nThe dystoniaFilesDF.pkl file was updated.')

#while dystoniaFilesDF is incomplete, just save it to the Desktop to check if is is being created correctly
#DesktopPath = "C:\\Users\\diogo\\OneDrive\\Ambiente de Trabalho\\DystoniaDataBase.csv"
#dystoniaFilesDF.to_csv(DesktopPath)