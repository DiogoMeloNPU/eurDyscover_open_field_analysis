# Dystonia Analysis

Justify here what is being done
...trying to generalize the script **Single_session_analysis.ipynb** (organize it in a modular structure instead of a Jyputer Notebook, in order to replicate the analysis for all mice).

This project contains all the scripts I developed so far for organization and analysis of the data available from the Dystonia Project.

It includes:

## 1. Dystonia Analysis Environment
- Necessary to deal with dependencies.

## 2. Jupyter Notebooks Folder
- Several preliminary analysis.

## 3. Matlab files for generation of processed CNMFE dictionaries that can be opened in python
- This include x, y, and z, which are necessary for generating the matlab files that can be opened in python

## 4. .py files for creating a dataframe with all path and replicating the current state of the analysis for all groups

There is a set of modules with the pattern "organizeDF" which have a similar structure. There is a different module for every file I want to create to help the analysis. Each file ultimately serves for creating a dataframe with some type of data, namely:
1. DLC coordinate predictions (organizeDF_DLCcoordiantes.py)
2. Acceleration data (organizeDF_acceleration.py)
3. C_raw (raw traces of temporal components) (organizeDF_C_raw.py)
4. Velocity magnitude of each body part (organizeDF_DLCvelocities.py)
5. ...more?

Maybe create a module that runs all the above mentioned modules and saves the dataframes as different csv files, saves them to the respective folder, and finally adds their file paths as new columns in the main file, dystoniaFilesDF.csv

Add indications for other possible users, namely the order in which the files should be run.

I want to improve this description, however I am now focused on creating a database with all the files for every mice, in order to replicate the analysis developed in **Single_session_analysis.ipynb**.