# this file contains the necessary functions to compute the distance travelled by mice during a session

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
    duration_s_Locomotion = numDataPointsLocomotion/camera_aq_rate

    # compute the distance travelled in the current session
    distanceTravelledTailbase = meanSpeedLocomotion*duration_s_Locomotion

    return distanceTravelledTailbase