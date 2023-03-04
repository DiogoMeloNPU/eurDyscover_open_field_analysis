# this file creates the necessary functions to compute the percentage of time during which locomotion occured

# import necessary packages
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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

#for row, npy_speed_tailbase in enumerate(dystoniaFilesDF['npy_speed_DLC.pkl']):

examplePath = "G:\\.shortcut-targets-by-id\\1MH0egFqTqTToPE-wxCs7mDWL48lVKqDB\\EurDyscover\\Dystonia_Data\\D2\\BL2\\45008_LB_BL2\\npy_speedDLC_45008_lb_bl2videoprocessed2021-10-04t10_39_03dlc_resnet50_dystonia_testapr21shuffle1_500000.npy"

speedTailBase = np.load(examplePath)

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



'''
# Initialize the figure
plt.figure()
plt.title('Speed tailbase')
plt.xlabel('time (fr)')
plt.ylabel('Speed (px/fr)');
#plt.plot(speedTailbase[0]) # speed tailbase
plt.plot(convert2_cm_s(speedTailBase[0][compliantLikelihood], conversionFactor_cm))
plt.axhline(y = 5, color = 'r', linestyle = '-')
#plt.plot(speedTailbase[1]) # likelihood
# Display plot
plt.show()
'''