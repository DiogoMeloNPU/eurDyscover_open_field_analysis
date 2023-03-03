# this file creates the necessary functions to compute the percentage of time during which locomotion occured

# import necessary packages
import numpy as np
import matplotlib.pyplot as plt

examplePath = "J:\\O meu disco\\EurDyscover\\Dystonia_Data\\D1\\W1\\42312_2F_W1\\npy_speedDLC_videoprocessed2021-04-29t16_15_55dlc_resnet50_dystonia_testapr21shuffle1_500000.npy" 

speedTailbase = np.load(examplePath)

# Initialize the figure
plt.figure()
plt.title('Speed tailbase')
plt.xlabel('time (fr)')
plt.ylabel('Speed (px/fr)');
plt.plot(speedTailbase[0])
plt.plot(speedTailbase[1])
# Display plot
plt.show()