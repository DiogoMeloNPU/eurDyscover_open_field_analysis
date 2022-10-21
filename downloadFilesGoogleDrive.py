import os 
import io
from Google import Create_Service
from googleapiclient.http import MediaIoBaseDownload

CLIENT_SECRET_FILE = 'client_secrets.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ["https://www.googleapis.com/auth/drive"]

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

file_ids = ['1e0ypPZzEpgx76cvy8Mb5LBtlEr8qPp0Q']
file_names = [
    'VideoRaw2021-04-28T13_45_56DLC_resnet50_Dystonia_TestApr21shuffle1_500000.csv']

for file_id, file_name in zip(file_ids, file_names):
    request = service.files().get_media(fileId=file_id)

    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fd=fh, request=request)

    done = False

    while not done:
        status, done = downloader.next_chunk()
        print('Download progress {}'.format(status.progress() * 100))

fh.seek(0)

with open(os.path.join("C:\\Users\\user\\Desktop\\Test_Undistorted", file_name), 'wb') as f:
    f.write(fh.read())
    f.close()