import matplotlib.pyplot as plt
import numpy as np
from os.path import dirname, join as pjoin
import scipy.io as sio
import pandas as pd
#import the module necessary for obtaining the Inscopix timestamps
from data_structuring.organize_accel_data_timestamps import open_AccelData_asDF, get_microscope_timestamps

#open the dystoniaFilesDF.csv that was created in DystoniaDataFrame.py
dystoniaFilesDFpath = "G:\\.shortcut-targets-by-id\\1MH0egFqTqTToPE-wxCs7mDWL48lVKqDB\\EurDyscover\\Organized_data_JAS\\dystoniaFilesDF.pkl"
dystoniaFilesDF = pd.read_pickle(dystoniaFilesDFpath)

for row, AccelDataFile in enumerate(dystoniaFilesDF['AccelData.csv']):
    if not isinstance(AccelDataFile, float):
        print('\n\n----Check inscopix timestamps from this----: {}'.format(AccelDataFile))
        timestamps = get_microscope_timestamps('G' + AccelDataFile[1:])
        plt.plot(timestamps)
        plt.show()

#You will notice that in some cases, there are cases in which the difference between consecutive timestamps
#is multiple seconds right in the begginging. I think that if I remove the timestamps prior to this
#observation, I can match the timestamps to the C_raw values