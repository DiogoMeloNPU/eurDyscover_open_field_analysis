# Dystonia Analysis

## Goal
This project has the goal of generalizing the notebooks to be able to automatically obtain single session analysis for all sessions of all mice and perform group level analysis as well.

## Structure

This project contains all the scripts I developed so far for organization and analysis of the data available from the Dystonia Project.
Here, you can find...

### 1. Dystonia Analysis virtual environment
- Corresponds to the 'venv_dystoniaAnalysis' folder. Necessary to deal with dependencies.

### 2. Jupyter Notebooks Folder
- Several preliminary analysis, including a script for analysis of a single session of the Dystonia Open Field recordings was developed and reproduced for 4 sessions (Wt/Bl; Wt/W09; DYTd1/Bl; DYTd1/W09) in 4 different Jupyter Notebooks.

### 3. Matlab files for generation of processed CNMFE dictionaries that can be opened in python
- This includes:
1. Batch_convertSources2D_simplerFiles.m (searches for all .mat files)
2. Sources2D_to_simple_mat.m (converts these files into a basic .mat file that can be opened in Python using scipy.io.loadmat.)
3. Sources2D.m (matlab class)

Source2D class doesn't exist in Python. So, to work with this information in Python it is necessary to create new files in which 'neuron', a Sources2D object, is unfolded into matrices that can be manipulated in Python, as lists or numpy arrays. This script performs the described task by searching for the original CNFME mat files in the folder 'Organized_data_JAS' (GoogleDrive) and generates the desired simpler/readable .mat file in the respective folder for easy access. Keep in mind that for this, you need to have the path of your function 'Sources2D_to_simple_mat.m', as well as 'Sources2D.m' in your MATLAB search path.

### 4. .py files for creating a dataframe with all path and replicating the current state of the analysis for all groups

There is a set of modules with the pattern "organizeDF" which have a similar structure. There is a different module for every file I want to create to help the analysis. Each file ultimately serves for creating a dataframe with some type of data, namely:
1. DLC coordinate predictions (organizeDF_DLCcoordiantes.py)
2. Acceleration data (organizeDF_acceleration.py)
3. C_raw (raw traces of temporal components) (organizeDF_C_raw.py)
4. Velocity magnitude of each body part (organizeDF_DLCvelocities.py)
5. ...more?

Maybe create a module that runs all the above mentioned modules and saves the dataframes as different csv files, saves them to the respective folder, and finally adds their file paths as new columns in the main file, dystoniaFilesDF.csv

Add indications for other possible users, namely the order in which the files should be run.

I want to improve this description, however I am now focused on creating a database with all the files for every mice, in order to replicate the analysis developed in **Single_session_analysis.ipynb**.

So far, the data used to develop the current pipeline corresponds to the following Google Drive Folders.

Describe all the types of raw available data


## Guidelines

To use this content you may start by cloning the repository to VS Code. Make sure you have git installed, as well as all the proper VS code extensions (Python, Jupyter Notebook, GitHub Pull Requests and Issues). As described, the project already has a virtual environment to deal with dependencies