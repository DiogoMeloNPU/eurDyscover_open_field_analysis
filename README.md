# eurDyscover Open Field Analysis

In development...

## Goal
This project has the goal of generalising python notebooks containing preliminary analysis of open field data from experiments related to the EurDyscover project developed @ Alves da Silva lab, Champalimaud Foundation. My aim is to automate single subject and group analysis reports for the experiments performed so far.
## Structure
This project contains all the scripts I've developed so far for organisation and analysis of the data available.

Following is a description of the project structure and data used:

### 1. venv_dystoniaAnalysis (ignore for know)
- Virtual environment. Necessary to deal with dependencies.
- You will need to change **pyvenv.cfg** file according to the path of your python executable.

### 2. data_analysis

### 3. data_structuring

### 4. preprocess_cnmfe_mat2py
1. **Batch_convertSources2D_simplerFiles.m** (searches for all neuron.mat files and calls **Sources2D_to_simple_mat.m**)
2. **Sources2D_to_simple_mat.m** (converts these files into a basic .mat file that can be opened in Python using scipy.io.loadmat.)
3. **Sources2D.m** (matlab class)

- Source2D class doesn't exist in Python. So, to work with this information in Python it is necessary to create new files in which 'neuron', a Sources2D object, is unfolded into matrices that can be manipulated in Python, as lists or numpy arrays. This script performs the described task by searching for the original CNFME mat files in the folder 'Organized_data_JAS' (Google Drive) and generates the desired simpler/readable .mat file in the respective folder for easy access. Keep in mind that for this, you need to have the path of your function 'Sources2D_to_simple_mat.m', as well as 'Sources2D.m' in your MATLAB search path.

### 5. Jupyter notebooks
- Several preliminary analysis, including a script for single session analysis was developed and reproduced for 4 example sessions (Wt/Bl; Wt/W09; DYTd1/Bl; DYTd1/W09) in 4 different Jupyter Notebooks. These files are being used to generalize the analysis for all subjects.
- **Single_session_analysis.ipynb** (main script)

### 4. Python files

- Let's start with **DystoniaDataFrame.py**. This file is necessary to generate a pickle/csv file containing all the informationon the available files for all sessions. Generally, if a specific file for one session of one mice exists, the Google Drive file path will be in the respective folder. If the file does not exist, or is stored elsewhere there will be an empty cell. Some other notations are being used, namely -1 whose meaning is explained in the respective module in which such files are being generated. 

- "Organize" modules. There is a set of modules (python files) with the pattern "organizeDF" which have a similar structure. There is a different module for every file I want to create to help the analysis. Each file ultimately serves for creating a simpler data structure with some type of data, namely:
1. **organizeDF_DLCcoordiantes.py** (restructures the files containing the coordinate predictions generated by the custom DeepLabCut project, saves the simpler structure as pickle and updates dystoniaFilesDF.py)
2. **organizeDF_acceleration.py** (computes the total body acceleration, builds a dataframe containing the acceleration and respective timestamps, exports this structure as a pickle file which is stored in the same directory as the **AccelData.csv** and creates a new column in dystoniaFilesDF.pkl file with the paths of the new files)
3. **organizeNPY_C_raw.py** (obtains the C raw data from the simpler .mat files and generates .npy files containing both the raw traces, as well as the timestamps. After generating the files, a new column is created in dystoniaFilesDF.pkl containing the respective file paths) 
4. **organizeDF_C_raw.py** (organizes the C raw data and respective timestamps in a separate structure, saves the files. In development...)
5. **organizeDF_DLCvelocities.py** (computes the velocity magnitude of each body part )
6. **organizeDF_FrameDiff** (simplifies the FrameDiff files, stores the main info as .pkl and updates the dystoniaFilesDF.pkl file)

- **organize_AccelDataTimestamps.py** is different from the other "Organize" modules. It is necessary to open the **AccelData.csv** file for each session and separate the timestamps from the different hardware, namely Inscopix, Camera and Accelerometer. It also gets the information on the first and last TTL sent in each session (between the first and last Inscopix TTL, which is the period considered to be the session).
 
- "Check" modules:
1. **check_inscopix_timestamps.py** (this script plots the timestamps from the accelerometer, to check for missing frames)
2. **check_TotalBodyAccel_distributions.py** (in development)
3. **checkMissingFrames_MetaData.py** (so far, this module can open imaging meta data files and extract the lost frames; in development)

- "Find" modules. Two scripts were developed to check for videos that were either not analyzed or not filtered using DeepLabCut (https://deeplabcut.github.io/DeepLabCut/docs/standardDeepLabCut_UserGuide.html) recommended filters. For each case, a .npy file is generated containing a numpy array of the video paths that were not filtered and not analyzed:
1. **FindVideosNotAnalyzed.py** (generates missingDLCanalysis.npy)
2. **FindVideosNotFiltered.py** (generates missingFiltering.npy)

## Data 

- So far, the data used to develop the current pipeline corresponds to the Google Drive Folder 'Organized_data_JAS'. 

- Raw data files include...
1. **VideoRaw.avi/.mp4**
    - This videos were processed to correct distortion, generating VideoProcessed.avi/.mp4 files
2. **neuron.m** files (CNMFE)
    - Contains the calcium traces
3. **AccelData.xml**
    - Contains the timestamps of the inscopix, accelerometer and camera, as well as the acceleration and gyroscope data (x,y and z)

## DLC project

Several body parts were tracked using DeepLabCut, namely nose, left hind paw, right hind paw, left front paw, right front paw, tail base and tail tip.
The project itself can be shared in Google Drive to generate new files from processed videos.

Trainning specifications can be found in the Benchling log book shared with Filipa.

## Guidelines

To use this content you may start by cloning the repository to VS Code. Make sure you have git installed, as well as all the proper VS code extensions (Python, Jupyter Notebook, GitHub Pull Requests and Issues). As described, the project already has a virtual environment to deal with dependencies. Inside **venv_dystoniaAnalysis** there is a **pyvenv.cfg** file, that needs to be adapted according to your python executable location. For this implementation the user is advised to download the same python version 3.11.1 and store it locally, in a separate folder from the project.

In order to achieve a final version of this project it is necessary to first organize all the files in a similar structure to what is implemented, as well as generate all DLC predictions. This implies that **DystoniaDataFrame.py** will have to be adapted (keeping the rational) to get access to a new, to be created folder, containing all the files from each session.

In development...

## Missing Implementation

- If you are following **Single_session_analysis.ipynb**, after having all the necessary files generated, organised and properly corrected for missing frames, the next steps in the implementation should be:
1. Detecting movement initiations from acceleration and DLC velocity files. A separate module could be made for generating kernel density estimation in the log scale for each file, as well as performing gaussian fittings.
2. A separate module could be created to do the psth plots aligned to all a specific event of interest.
3. Separate module for the classification of neurons as negatively, positively and non modulated by initiation of movement (should be abstract to the event)
4. Probability density function is not very informative as it is. It should include initiations detected using the accelerometer for every event
5. Alignment of different types of data (considering the different acquisition rates and the timestamps)
6. Separate module to build the complete figure with the DLC analysis
7. There shoudl be something facilitating local use of the database, for example providing the path until the folder in which the project is locally ans use it to perform searches in the dataframe
In development...

