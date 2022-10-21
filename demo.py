from googleapiclient.http import MediaFileUpload
from Google import Create_Service

CLIENT_SECRET_FILE = 'client_secrets.json' #'client_secret_GoogleCloudDemo.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ["https://www.googleapis.com/auth/drive"]

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
# print(dir(service))
# from this line up, this code creates a google drive API service instance

# code to create folders in Google Drive
'''national_parks = ['Yellowstone', 'Rocky Mountains', 'Yosemite']

for national_park in national_parks:
    file_metadata = {
        'name': national_park,
        'mimeType': 'application/vnd.google-apps.folder',
        # 'parents': []
    }
    service.files().create(body=file_metadata).execute()'''

folder_id = '1zIj3QHj7qyEcfqEAX5BH38hksrlA3m_k'

file_paths = ["C:\\Users\\user\\Desktop\\VideoRaw2021-04-28T13_45_56DLC_resnet50_Dystonia_TestApr21shuffle1_500000.csv"]
mime_types = ['text/csv']

for file_path, mime_type in zip(file_paths, mime_types):
    file_metadata = {
        'name': file_path.split('\\')[-1], 
        'parents': [folder_id]
    }
    
    media = MediaFileUpload(file_path, mimetype = mime_type)
    
    service.files().create(
        body = file_metadata, 
        media_body = media, 
        fields = 'id'
    ).execute()