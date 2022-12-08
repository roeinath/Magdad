from __future__ import annotations
import os
import uuid

from googleapiclient.http import MediaFileUpload
from APIs.ExternalAPIs import TalpiotSettings
from APIs.ExternalAPIs.GoogleDrive.file_to_upload import FileToUpload
from APIs.ExternalAPIs.WorkerPool.pool import Pool
from APIs.ExternalAPIs.WorkerPool.pooled_worker import PooledWorker

from pathlib import Path

#  If modifying this scopes, delete token.json
from APIs.TalpiotSystem import TalpiotDatabaseCredentials

SCOPES_DRIVE = ['https://www.googleapis.com/auth/drive']
MAX_WORKERS = 5


class GoogleDrive(PooledWorker):
    """
    A class that allows accessing GoogleDrive with
    the bot google account.
    """
    _pool = Pool(lambda: GoogleDrive(), MAX_WORKERS)

    @staticmethod
    def get_instance() -> GoogleDrive:
        return GoogleDrive._pool.get_free_worker()

    def __init__(self):
        super().__init__()
        self.creds_diary = None
        self.service = None

        self.connect_to_drive()

    def connect_to_drive(self):
        from APIs.TalpiotAPIs.static_fields import StaticFields

        token_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "token.pickle"
        )

        static_field = StaticFields.objects()[0]
        if static_field.google_drive_token is not None:
            with open(token_path, 'wb') as token_file:
                token_file.write(static_field.google_drive_token)

        google_settings = TalpiotSettings.get().google_connection_settings
        self.service = google_settings.get_service('drive', 'v3', SCOPES_DRIVE, token_file_path=token_path)

    def list_files(self, folder_id="", no_folders=True):
        q_list = []
        if folder_id != "" and folder_id is not None:
            q_list.append(f"'{folder_id}' in parents")
        if no_folders:
            q_list.append(f"mimeType != 'application/vnd.google-apps.folder'")

        q = " and ".join(q_list)
        result = self.service.files().list(q=q).execute()
        return result

    def list_files_by_name(self, file_name, folder_id=""):
        all_files = self.list_files(folder_id=folder_id).get('files', [])
        return list(filter(lambda file: file.get('name') == file_name, all_files))

    def create_folder(self, name, parent_ids=None):
        file_metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        if parent_ids is not None:
            file_metadata["parents"] = parent_ids
        result = self.service.files().create(body=file_metadata, fields='id').execute()
        return result

    def remove_file(self, file_id):
        result = self.service.files().delete(fileId=file_id).execute()
        return result

    def upload_file_from_object(self, file_to_upload: FileToUpload, folder_id: str = '', publish: bool = False):
        temp_folder_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'temp_files'
        )
        Path(temp_folder_path).mkdir(parents=True, exist_ok=True)

        temp_file_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'temp_files',
            str(uuid.uuid4()) + file_to_upload.name
        )

        with open(temp_file_path, 'wb+') as temp_file:
            temp_file.write(file_to_upload.get_content())

        result = self.upload_file_by_path(temp_file_path, file_to_upload.name, folder_id,
                                          file_to_upload.get_mimetype(), publish)
        os.remove(temp_file_path)
        return result.get('id')

    def upload_file_by_bytes(self, content_bytes: bytes, file_name: str, folder_id: str = '', file_type: str = '',
                            publish: bool = False):
        temp_file_path = str(uuid.uuid4())
        with open(temp_file_path, 'wb') as temp_file:
            temp_file.write(content_bytes)
        result = self.upload_file_by_path(temp_file_path, file_name, folder_id, file_type, publish)
        os.remove(temp_file_path)
        return result.get('id')

    def upload_file_by_path(self, file_path: str, file_name: str, folder_id: str = '', file_type: str = '',
                            publish: bool = False):
        """
        Returns an result dictionary that has details about the specific
        spreadsheet.

        :param publish: (optional) whether to set the file as public.
        :param file_type: (optional) the type of the file.
        :param folder_id: (optional) the id of the folder to upload to.
                          can be typed manually or found through "get_files".
        :param file_path: local path of file to upload
        :param file_name: name for the created file on the drive
        :return: str: the id of the created file in the drive
        """

        file_metadata = {'name': file_name}
        if folder_id != '':
            file_metadata['parents'] = [folder_id]
        if file_type != '':
            file_metadata['mimeType'] = file_type

        media = MediaFileUpload(file_path, resumable=True)
        file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        if publish:
            self.set_file_as_public(file_id=file.get('id'))
        return file

    def download_file_by_id(self, file_id='', file_type='pdf'):
        request = self.service.files().export_media(fileId=file_id, mimeType=f'application/{file_type}')
        return request.execute()

    def download_file_by_name(self, file_name='', file_type='pdf'):
        files = self.list_files_by_name(file_name)
        if files:
            file_id = files[0].get('id')
            return self.download_file_by_id(file_id, file_type)

    def move_drive_obj(self, obj_id, destination_folder):
        # Move the file to the new folder
        return self.service.files().update(
            fileId=obj_id,
            addParents=destination_folder,
            removeParents=self.get_parent_ids(obj_id),
            fields='id, parents'
        ).execute()

    def get_parent_ids(self, obj_id):
        file = self.service.files().get(fileId=obj_id, fields='parents').execute()
        return ",".join(file.get('parents'))

    def rename_file(self, file_id, new_title):
        """Rename a file.

        Args:
          service: Drive API service instance.
          file_id: ID of the file to rename.
          new_title: New title for the file.
        Returns:
          Updated file metadata if successful, None otherwise.
        """
        try:
            file_metadata = {'name': new_title}

            # Rename the file.
            updated_file = self.service.files().update(
                fileId=file_id,
                body=file_metadata,
                fields='name').execute()

            return updated_file
        except Exception as e:
            print('An error occurred: %s' % e)
            return None

    def set_file_as_public(self, file_id):
        try:
            file_metadata = {'role': 'reader', 'type': 'anyone'}
            updated_file = self.service.permissions().create(
                fileId=file_id,
                body=file_metadata,
            ).execute()

            return updated_file
        except Exception as e:
            print('An error occurred: %s' % e)
            return None

    def get_url_from_id(self, file_id):
        if type(file_id) is dict:
            file_id = file_id.get('id')
        return f"https://drive.google.com/file/d/{file_id}/view"

    def get_folder_url_from_id(self, file_id):
        if type(file_id) is dict:
            file_id = file_id.get('id')
        return f"https://drive.google.com/drive/u/3/folders/{file_id}"

    def get_thumbnail_from_id(self, file_id):
        if type(file_id) is dict:
            file_id = file_id.get('id')
        return f"https://lh3.googleusercontent.com/d/{file_id}"


if __name__ == "__main__":
    settings = TalpiotSettings(TalpiotDatabaseCredentials("username", "password"))
    google_drive = GoogleDrive.get_instance()

    # gd.upload_file_by_path('./file_downloaded.pdf', 'test_file2', folder_id='1fxjtahIxwAn2_yVOMtrSNByzs1SCBlMJ')
    # files = google_drive.list_files()['files']
    # for f in files:
    #     print(f)

    # string_bytes = google_drive.download_file_by_name(file_name='בדיקה.txt', file_type='txt')
    # with open('בדיקה.txt', 'wb') as f:
    #     f.write(string_bytes)
