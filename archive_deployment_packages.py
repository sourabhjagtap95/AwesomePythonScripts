from __future__ import print_function
import httplib2
import subprocess
import json
import os
import os.path
import sys

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient.http import MediaFileUpload

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def upload_file_to_drive(service, file_name, path_to_file):
    file_metadata = {
        'name': file_name,
        'parents': ['0B_qHZ9yaJLRnd1RSUTNZazdicGs']
    }
    media = MediaFileUpload(f'{path_to_file}\\{file_name}', resumable=True)
    request = service.files().create(body=file_metadata,
                                     media_body=media,
                                     fields='id')
    response = None

    while response is None:
        status, response = request.next_chunk()
        if status:
            sys.stdout.write(("Uploaded %d%%. \r" % int(status.progress() * 100)))
            sys.stdout.flush()


def mv(source, destination):
    return subprocess.run(['../.bin/mv', source, destination])

def zip(source, destination):
    return subprocess.run(['../.bin/7za', 'a', '-tzip', destination, source])

def get_json_config(json_file_path):
    with open(json_file_path) as json_file:
        return json.load(json_file)

def archive_dirs(files, source_path, destination_path, backup_dir):
    for file in files:
        source_dir = f'{source_path}\\{file}'
        destination_file = f'{destination_path}\\{file}.zip'

        if not os.path.isdir(source_dir): continue

        if os.path.isfile(destination_file):
            print(f'{destination_file} already exist')
            continue

        print(f'({i + 1}/{len(files)}) Archiving {file}...')
        zip(f'{source_dir}\\*', destination_file)
        print('Archive Complete!')

        mv(source_dir, backup_dir)

def upload_archives(files, source_path, service, backup_dir):
    for i, file in enumerate(files):
        source_file = f'{source_path}\\{file}'

        if not os.path.isfile(source_file): continue
        if not file.lower().endswith('.zip'): continue

        print(f'({i + 1}/{len(files)}) Uploading {file}...')
        upload_file_to_drive(service, file, source_path)
        print('Upload Complete!')

        mv(source_file, backup_dir)

def main():
    # Initialize and authorize Google Drive API
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    # Get local config
    local_config = get_json_config('config.json')

    deployment_package_dir = local_config['deployment_package_dir']
    archive_dir = local_config['archive_dir']
    deployment_package_backup_dir = local_config['deployment_package_backup_dir']
    archive_backup_dir = local_config['archive_backup_dir']

    if not deployment_package_dir and not archive_dir:
        print('Script is not configured properly.')
        return 1

    # Archive the directories in deployment package dir
    archive_dirs(os.listdir(deployment_package_dir),
                 deployment_package_dir, archive_dir,
                 deployment_package_backup_dir)

    # Upload to Google Drive
    upload_archives(os.listdir(archive_dir), archive_dir, service, archive_backup_dir)

if __name__ == '__main__':
    main()
