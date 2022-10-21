import os
import io
import pandas as pd
import numpy as np
from Google import Create_Service
from googleapiclient.http import MediaIoBaseDownload

def init_drive_service():
    CLIENT_SECRET_FILE = 'client_secrets.json'
    API_NAME = 'drive'
    API_VERSION = 'v3'
    SCOPES = ["https://www.googleapis.com/auth/drive"]
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    return service

service = init_drive_service()

folder_id = '1pOjD3Hd7m8u5eK7CxZvDwBVWvXCaMjLu'
query = f"parents = '{folder_id}'"
response = service.files().list(q=query).execute()

files = response.get('files')
nextPageToken = response.get('nextPagetoken')

while nextPageToken:
    response = service.files().list(q=query, pageToken=nextPageToken).execute()
    files.extend(response.get('files'))
    nextPageToken = response.get('nextPageToken')

df_Organized_data_JAS = pd.DataFrame(files)

# get the IDs of the folders
D2_folderID = df_Organized_data_JAS['id'].loc[df_Organized_data_JAS['name'] == 'D2']
D1_folderID = df_Organized_data_JAS['id'].loc[df_Organized_data_JAS['name'] == 'D1']
# save the two IDs in an array
DopamineRepector_FolderIds = [str(np.array(D2_folderID)[0]), str(np.array(D1_folderID)[0])]

# create a folder on the desktop to upload the CNMF-E files organized in the google drive
parent_dir = "C:\\Users\\user\\Desktop\\"
main_folder = 'Organized CNMF-E files'
parent_dir = os.path.join(parent_dir, main_folder)
os.mkdir(parent_dir)

# create a folder for each dopamine recepetor (D2, D1)
for i, dopReceptor_FolderId in enumerate(DopamineRepector_FolderIds):
    # create subfolder inside the main folder
    directory = str(np.array(df_Organized_data_JAS['name'].loc[df_Organized_data_JAS['id']
                                                               == DopamineRepector_FolderIds[i]])[0])
    path = os.path.join(parent_dir, directory)
    os.mkdir(path)
    print("Directory '% s' created" % directory)
    
    # create a folder for each time point (BL, W09, ...)
    # start by building a dataframe containing the information on the drive's folder content
    query = f"parents = '{dopReceptor_FolderId}'"
    response = service.files().list(q=query).execute()

    files = response.get('files')
    nextPageToken = response.get('nextPagetoken')

    while nextPageToken:
        response = service.files().list(q=query, pageToken=nextPageToken).execute()
        files.extend(response.get('files'))
        nextPageToken = response.get('nextPageToken')

    df_subfolder = pd.DataFrame(files)
    
    # for every folder (BL, W01, W03, ...) create a new subfolder
    # get the ID of the timepoints (save them in an array)
    TimePoints_FolderIds = np.array(df_subfolder['id'].loc[df_subfolder['mimeType'] == 'application/vnd.google-apps.folder'])
    for i, TimePoint_FolderID in enumerate(TimePoints_FolderIds):
        directory = str(np.array(df_subfoder['name'].loc[df_subfolder['id'] == df_subfolder_FolderIds[i]])[0])
        timePoint_Path = os.path.join(path, directory)
        os.mkdir(path)
        print("Directory '% s' created" % directory)
        # for each mice, create a folder and download the .mat file from the google drive