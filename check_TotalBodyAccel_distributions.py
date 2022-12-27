import matplotlib.pyplot as plt
import numpy as np
from os.path import dirname, join as pjoin
import scipy.io as sio
import pandas as pd
#import the module necessary for obtaining the Inscopix timestamps
from organize_AccelDataTimestamps import open_AccelData_asDF, get_microscope_timestamps

#open the dystoniaFilesDF.csv that was created in DystoniaDataFrame.py
dystoniaFilesDFpath = "E:\\.shortcut-targets-by-id\\1MH0egFqTqTToPE-wxCs7mDWL48lVKqDB\\EurDyscover\\Organized_data_JAS\\dystoniaFilesDF.pkl"
dystoniaFilesDF = pd.read_pickle(dystoniaFilesDFpath)

#creating initial data values
x=np.linspace(0, 50000)
y=np.linspace(0, 50000)

#to run GUI event loop
plt.ion()

# here we are creating sub plots
figure, ax = plt.subplots(figsize=(10, 8))
distr, = ax.plot(x, y)

# setting title
plt.title("Log scale distributions", fontsize=20)

# setting x-axis label and y-axis label
plt.xlabel("Data Point")
plt.ylabel("Timestamp (s)")

#print all the timestamps
for row, AccelDataFile in enumerate(dystoniaFilesDF['AccelData.csv']):
    if not isinstance(AccelDataFile, float):
        print('\n\n----Check inscopix timestamps from this file----: {}'.format(AccelDataFile))
        #creating new Y values
        timestamps = get_microscope_timestamps(AccelDataFile)
        #updating data values
        distr.set_ydata(timestamps)
        #plt.plot(timestamps)