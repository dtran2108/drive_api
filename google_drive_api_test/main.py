from __future__ import print_function
import httplib2
import pickle
import os.path, io
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import auth
from apiclient.http import MediaFileUpload, MediaIoBaseDownload

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Drive API Project'
authInst = auth.Auth(SCOPES, CLIENT_SECRET_FILE, APPLICATION_NAME)
credentials = authInst.get_credentials()
drive_service = build('drive', 'v3', credentials=credentials)


def list_files(size):
    results = drive_service.files().list(
        pageSize=size, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))


def upload_files(file_name, file_path, minetype):
    file_metadata = {'name': file_name}
    media = MediaFileUpload(file_path,
                            mimetype=minetype)
    file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    print('File ID: %s' % file.get('id'))


def download_file(file_id, destination):
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    with io.open(destination, 'wb') as f:
        fh.seek(0)
        f.write(fh.read())