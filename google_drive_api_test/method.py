from io import open as ioOpen, BytesIO
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from auth import Auth
from apiclient.http import MediaFileUpload, MediaIoBaseDownload
from apiclient import errors


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']
CLIENT_SECRET_FILE = 'client_secret.json'
authInst = Auth(SCOPES, CLIENT_SECRET_FILE)
credentials = authInst.get_credentials()
drive_service = build('drive', 'v3', credentials=credentials)


def list_file(size):
    results = drive_service.files().list(
        pageSize=size, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print('{}: {}'.format(item['id'], item['name']))


def upload_file(file_name, file_path, mimetype):
    file_metadata = {'name': file_name}
    media = MediaFileUpload(file_path,
                            mimetype=mimetype)
    file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    print('File ID: {}'.format(file.get('id')))


def download_file(file_id, destination):
    request = drive_service.files().get_media(fileId=file_id)
    fh = BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print("Download {}.".format(int(status.progress() * 100)))
    with ioOpen(destination, 'wb') as f:
        fh.seek(0)
        f.write(fh.read())


def create_folder(name):
    file_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    file = drive_service.files().create(body=file_metadata,
                                        fields='id').execute()
    print('Folder ID: {}'.format(file.get('id')))


def search_file(size, operator):
    results = drive_service.files().list(
        pageSize=size, fields="nextPageToken, files(id, name)",
        q=operator).execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{} ({})'.format(item['name'], item['id']))


def delete_file(file_id):
  """Permanently delete a file, skipping the trash.
  Args:
    service: Drive API service instance.
    file_id: ID of the file to delete.
  """
  try:
    drive_service.files().delete(fileId=file_id).execute()
  except errors.HttpError as error:
    print('An error occurred: {}'.format(error))