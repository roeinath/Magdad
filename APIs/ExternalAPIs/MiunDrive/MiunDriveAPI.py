from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from os import path
import os
import json
from datetime import datetime
import logging
from dateutil import parser
import pytz
from tzlocal import get_localzone
from pydrive.auth import GoogleAuth
import pandas as pd

former_cwd = os.getcwd()
os.chdir(os.path.join(path.abspath(__file__), '..'))

# Works in the scope of this working directory
gauth = GoogleAuth()
drive = GoogleDrive(gauth)

logger= logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('DriveAPI.log', 'a', 'utf-8')
handler.setFormatter(logging.Formatter('%(name)s %(message)s'))
logger.addHandler(handler)
# End

os.chdir(former_cwd)
is_in_drive_context = False

MIUN_FOLDER_NAME = 'Miun_Data'
MIUN_FOLDER_DRIVE_ID = '1b9SEF2q847oMZJlR-pe_ijsvuwrif751'
METADATA_FILE = 'Metadata'
CREDENTIALS_FILE = 'credentials.json'
metadata_dict = {}


MIMETYPES_DOWNLOADABLE = {
        # Drive Document files as Word
        'application/vnd.google-apps.document': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',

        # Drive Sheets files as MS Excel files.
        'application/vnd.google-apps.spreadsheet': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    }



class FileTree():
    def __init__(self, title, **dict_params):
      self.children = []
      self.title = title
      self.parent = None
      self.content = dict({'title':title},**dict_params)
        
    def add_child(self, child_tree):
      child_tree.parent = self
      self.children.append(child_tree)

    def get_all_children(self):
      return [child.title for child in self.children]

    def get_child(self, child_name):
      for child in self.children:
        if(child == child_name):
          return child
      raise ValueError(f'There is no child of {self.title} named {child_name}')  

    def get_parent(self):
        return self.parent

    def get_full_path(self):
        if self.parent:
            return self.parent.get_full_path() + '/' + self.title
        return ''
        
    def __eq__(self, title:str):
      return self.title == title

    def __getitem__(self, key):
        return self.content[key]

    def __repr__(self):
      return str(self.content)

def open_not_drive_file(file_name):
    return pd.read_excel(file_name)


def miun_drive_context(function):
    '''Decorator that makes function run with MiunDrive folder as its working directory'''

    def in_context_func(*args, **kwargs):
        global is_in_drive_context
        if(is_in_drive_context):
            ret_val = function(*args, **kwargs)
        else:
            former_cwd = os.getcwd()
            os.chdir(os.path.join(path.abspath(__file__), '..'))
            is_in_drive_context = True
            ret_val = function(*args, **kwargs)
            os.chdir(former_cwd)
            is_in_drive_context = False
        return ret_val

    return in_context_func

@miun_drive_context
def get_list_of_all_data_files():
    root_tree = FileTree('')
    try:
        recursive_list_all_files(MIUN_FOLDER_DRIVE_ID, root_tree)
    except Exception as e:
        logger.warning('Exception occurred during get_list_of_all_data_files():\n' + str(e))
        os.remove(CREDENTIALS_FILE)
        #recursive_list_all_files(MIUN_FOLDER_DRIVE_ID, root_tree)
    return root_tree

@miun_drive_context
def recursive_list_all_files(folder_id, folder_tree_obj):
    files_without_folders_list = drive.ListFile({"q": f'"{folder_id}" in parents and mimeType!="application/vnd.google-apps.folder" and trashed=false'}).GetList()
    for file in files_without_folders_list:
        last_update_date = file['modifiedDate'][:file['modifiedDate'].rfind('.')]
        file_tree_obj = FileTree(file['title'], type='file', id=file['id'],
                                 last_update_time=parser.parse(file['modifiedDate']),
                                 mimetype=file['mimeType'])
        folder_tree_obj.add_child(file_tree_obj)
        
    folders_list = drive.ListFile({"q": f'"{folder_id}" in parents and mimeType="application/vnd.google-apps.folder" and trashed=false'}).GetList()
    for file in folders_list:
        file_tree_obj = FileTree(file['title'], type='file', id=file['id'], last_update_time=file['modifiedDate'], mimetype=file['mimeType'])
        recursive_list_all_files(file['id'], file_tree_obj)
        folder_tree_obj.add_child(file_tree_obj)

@miun_drive_context
def create_path_to_file(file_tree_obj):
    file_path = file_tree_obj.get_full_path()
    curr_path = MIUN_FOLDER_NAME
    for folder in file_path.split('/'):
        if not path.exists(curr_path):
            os.mkdir(curr_path)
        curr_path += '/' + folder

@miun_drive_context
def redownload_file(file_tree_obj):
    file_path = MIUN_FOLDER_NAME + '/' + file_tree_obj.get_full_path()
    drive_file_obj = drive.CreateFile({'id': file_tree_obj['id']})
    
    if file_tree_obj['mimetype'] in MIMETYPES_DOWNLOADABLE:
        downloadable_mimetype = MIMETYPES_DOWNLOADABLE[file_tree_obj['mimetype']]
        drive_file_obj.GetContentFile(file_path, mimetype=downloadable_mimetype)
    else:
        drive_file_obj.GetContentFile(file_path)
        
    logger.info('Downloaded file successfully. Updating metadata...')
    metadata_dict[file_tree_obj.get_full_path()] = str(file_tree_obj['last_update_time'])
    with open(METADATA_FILE,'w+') as metadata_file:
        json.dump(metadata_dict, metadata_file)

@miun_drive_context
def is_file_updated(file_tree_obj):
    create_path_to_file(file_tree_obj)
    path_inside = file_tree_obj.get_full_path()
    file_path = MIUN_FOLDER_NAME + '/' + path_inside
    if not (path.exists(file_path) and path.exists(METADATA_FILE)):
        return False
    with open(METADATA_FILE, 'r') as metadata_file:
         metadata_dict = json.load(metadata_file)
         if(not path_inside in metadata_dict):
             return False
         metadata_last_update_time = parser.parse(metadata_dict[path_inside])
         #metadata_last_update_time = datetime.strptime(metadata_dict[path_inside], '%Y-%m-%d %H:%M:%S')
         return path_inside in metadata_dict and metadata_last_update_time >= file_tree_obj['last_update_time']

@miun_drive_context        
def update_file(file_tree_obj):
    if not is_file_updated(file_tree_obj):
        logger.info(f'{file_tree_obj["title"]} is not updated. Redownloading file...')
        redownload_file(file_tree_obj)
    else:
        logger.info(f'{file_tree_obj["title"]} is updated.')
       
def get_file_object(root: FileTree, path: str) -> FileTree:
    curr_obj = root
    while(path):
        i = path.find('/')
        if i == -1:
            child_name = path
            path = ''
        else:
            child_name = path[:i]
            path = path[i+1:]
        curr_obj = curr_obj.get_child(child_name)
    return curr_obj

@miun_drive_context 
def open_file(file: FileTree):
    print(MIUN_FOLDER_NAME + '/' + file.get_full_path())
    if('spreadsheet' in file['mimetype']):
        df = pd.read_excel(MIUN_FOLDER_NAME + '/' + file.get_full_path())
    elif('csv' in file['mimetype']):
        try:
            df = pd.read_csv(MIUN_FOLDER_NAME + '/' + file.get_full_path(), encoding='utf-16le')
        except Exception:
            df = pd.read_csv(MIUN_FOLDER_NAME + '/' + file.get_full_path(), encoding='utf-8')
    else:
        raise ValueError(f"File type is not supported: {file['mimetype']}")
    return df
    

        
        
