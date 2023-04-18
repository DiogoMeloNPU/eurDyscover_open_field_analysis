# this file creates the necessary functions to compute the distances between left and right hind paw digital tips and ...
# ... and left and right hind paw heels while mice are standing still

# import necessary packages


camera_aq_rate = 30 # Hz

sideOpenField = 40 # cm
px_sideOpenField = 617.655 # pixels
conversionFactor_cm = sideOpenField/px_sideOpenField

cutOffLikelihood = 0.99 # under which data points are not considered for analysis

cutOffStandingStill = 2 # cm/s

# save the frame indexes during which mice are standing still

# go to the respective frames in the DLC coodinate files

    # compute euclidian distance between digital tips of the left and right hind paws

    # compute euclidian distance between heels of the left and right hind paws