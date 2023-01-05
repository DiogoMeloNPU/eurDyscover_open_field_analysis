# Dystonia Analysis

In development...

## Goal
This project has the goal of generalizing the notebooks to be able to automatically obtain single subject analysis for all sessions of all mice, as well as perform group level analysis.

## Structure

This project contains all the scripts I developed so far for organization and analysis of the data available from the Dystonia Project.

Following is a description of the project structure and data used

### 1. Dystonia Analysis virtual environment
- Corresponds to the **venv_dystoniaAnalysis** folder. Necessary to deal with dependencies.
- You will need to change **pyvenv.cfg** file according to the path of your python executable.

### 2. Jupyter Notebooks Folder
- Several preliminary analysis, including a script for analysis of a single session of the Dystonia Open Field recordings was developed and reproduced for 4 sessions (Wt/Bl; Wt/W09; DYTd1/Bl; DYTd1/W09) in 4 different Jupyter Notebooks. These files are being used to generalize the analysis for all subjects.
- **Single_session_analysis.ipynb** (main script)

### 3. Matlab files for generation of processed CNMF-E dictionaries that can be opened using python
- This includes:
1. **Batch_convertSources2D_simplerFiles.m** (searches for all .mat files)
2. **Sources2D_to_simple_mat.m** (converts these files into a basic .mat file that can be opened in Python using scipy.io.loadmat.)
3. **Sources2D.m** (matlab class)

- Source2D class doesn't exist in Python. So, to work with this information in Python it is necessary to create new files in which 'neuron', a Sources2D object, is unfolded into matrices that can be manipulated in Python, as lists or numpy arrays. This script performs the described task by searching for the original CNFME mat files in the folder 'Organized_data_JAS' (Google Drive) and generates the desired simpler/readable .mat file in the respective folder for easy access. Keep in mind that for this, you need to have the path of your function 'Sources2D_to_simple_mat.m', as well as 'Sources2D.m' in your MATLAB search path.

### 4. Python files

- Let's start with **DystoniaDataFrame.py**. This file is necessary to generate a pickle/csv file containing all the informationon the available files for all sessions. Generally, if a specific file for one session of one mice exists, the Google Drive file path will be in the respective folder. If the file does not exist, or is stored elsewhere there will be an empty cell. Some other notations are being used, namely -1 whose meaning is explained in the respective module in which such files are being generated. 

- "Organize" modules. There is a set of modules (python files) with the pattern "organizeDF" which have a similar structure. There is a different module for every file I want to create to help the analysis. Each file ultimately serves for creating a simpler data structure with some type of data, namely:
1. DLC coordinate predictions **organizeDF_DLCcoordiantes.py**
2. Acceleration data **organizeDF_acceleration.py**
3. C_raw (raw traces of temporal components) **organizeDF_C_raw.py**
4. Velocity magnitude of each body part **organizeDF_DLCvelocities.py**

- "Check" modules:
1. **check_inscopix_timestamps.py** (this script plots the timestamps from the accelerometer, to check for missing frames)
2. **check_TotalBodyAccel_distributions.py** (in development)
3. **checkMissingFrames_MetaData.py** (so far, this module can open imaging meta data files and extract the lost frames; in development)

- "Find" modules. Two scripts were developed to check for videos that were either not analyzed or not filtered using DeepLabCut (https://deeplabcut.github.io/DeepLabCut/docs/standardDeepLabCut_UserGuide.html) recommended filters. For each case, a .npy file is generated containing a numpy array of the video paths that were not filtered and not analyzed:
1. **FindVideosNotAnalyzed.py** (generates missingDLCanalysis.npy)
2. **FindVideosNotFiltered.py** (generates missingFiltering.npy)

### 5. Data 

- So far, the data used to develop the current pipeline corresponds to the Google Drive Folder 'Organized_data_JAS'. 

- Raw data files include...
1. **VideoRaw.avi/.mp4**
    - This videos were processed to correct distortion, generating VideoProcessed.avi/.mp4 files
2. **neuron.m** files (CNMFE)
    - Contains the calcium traces
3. **AccelData.xml**
    - Contains the timestamps of the inscopix, accelerometer and camera, as well as the acceleration and gyroscope data (x,y and z)

### 6. DLC project

Several body parts were tracked using DeepLabCut, namely nose, left hind paw, right hind paw, left front paw, right front paw, tail base and tail tip.
The project itself can be shared in Google Drive to generate new files from processed videos.

Trainning specifications can be found in the Benchling log book shared with Filipa.

## Guidelines

To use this content you may start by cloning the repository to VS Code. Make sure you have git installed, as well as all the proper VS code extensions (Python, Jupyter Notebook, GitHub Pull Requests and Issues). As described, the project already has a virtual environment to deal with dependencies. Inside **venv_dystoniaAnalysis** there is a 