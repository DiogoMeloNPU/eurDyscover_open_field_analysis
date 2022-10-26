from Google import Create_Service
import pandas as pd

CLIENT_SECRET_FILE = 'client_secrets.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ["https://www.googleapis.com/auth/drive"]

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

folder_id = '1pOjD3Hd7m8u5eK7CxZvDwBVWvXCaMjLu'
query = f"parents = '{folder_id}'"

response = service.files().list(q=query).execute()

files = response.get('files')
nextPageToken = response.get('nextPagetoken')

while nextPageToken:
    response = service.files().list(q=query, pageToken = nextPageToken).execute()
    files.extend(response.get('files'))
    nextPageToken = response.get('nextPageToken')

df = pd.DataFrame(files)
print(df)