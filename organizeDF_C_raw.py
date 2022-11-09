#this module creates a dataframe with the C_raw data

# Using matlab function Sources2D_to_simple_mat, I obtain the data.mat file
import numpy as np
from os.path import dirname, join as pjoin
import scipy.io as sio
import pandas as pd
#import the module necessary for obtaining the Inscopix timestamps
import organize_AccelDataTimestamps


'''# Convert A from sparse matrix to numpy array. Reshape A to be size [n_neurons, image_y_dim, image_x_dim]
A = neuron_mat_info['A'].toarray().reshape(
    [*np.flip(neuron_mat_info['image_size'][0]), -1]).transpose()
# Convert S from sparse matrix to numpy array.
S = neuron_mat_info['S'].toarray()
#save processed calcium traces in separate array
C = neuron_mat_info['C']
#save raw calcium traces in a separate array
C_raw = neuron_mat_info['C_raw']'''


simplerNeuronPath = "E:\\.shortcut-targets-by-id\\1MH0egFqTqTToPE-wxCs7mDWL48lVKqDB\\EurDyscover\\Organized_data_JAS\\D1\\Baseline 1\\42308_RF_B1\\simpler_26-Jul_17_58_11.mat"v

acceldata_path = ...
#add a new column containing the timestamps (import from organize_AccelDataTimestamps)
get_microscope_timestamps(acceldata_path)

#create a new column in dystoniaFilesDF to save the path of the new file

#show the dataframe

def buildCrawDF(path, C_raw):
    #this test varible contains the information of the data.mat file python dictionary
    neuron_mat_info = sio.loadmat(simplerNeuronPath)

    #save raw calcium traces in a separate array
    C_raw = neuron_mat_info['C_raw']


    #create the dataframes with the C_raw data, as well as the timestamps
    df_calcium = pd.DataFrame(C_raw)
    df_calcium = df_calcium.T  # transpose the calcium data

    #generate a label for each neuron of the dataframe (e.g.: neuron_1)
    neuron_labels = []
    for neuron in range(1, C_raw.shape[0]+1):
        neuron_label = 'neuron_'+str(neuron)
        neuron_labels.append(neuron_label)
    #change the labels on the dataframe
    df_calcium.columns = neuron_labels

    #show the dataframe
    print(df_calcium)

    return df_calcium

#save the dataframe as a csv in google drive - 