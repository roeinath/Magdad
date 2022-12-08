import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
from APIs.ExternalAPIs.FilesAPIs.talpix_file import TalpiXFile
from APIs.TalpiotSystem.talpiot_settings import TalpiotSettings


def upload_file(file_path: str) -> TalpiXFile:
    blob_service_client: BlobServiceClient = BlobServiceClient.from_connection_string(TalpiotSettings.get().azure_blobs_connection_string)
    blob_client = blob_service_client.get_container_client('talpix-user-files')

    keepcharacters = ('_', '.')
    filename = "".join(c for c in os.path.split(file_path)[-1] if c.isalnum() or c in keepcharacters).rstrip()
    path_on_server = filename + str(uuid.uuid4())

    with open(file_path, "rb") as data:
        blob_client.upload_blob(path_on_server, data)
    
    res = TalpiXFile(filename=filename, path_on_server=path_on_server)
    res.save()
    return res


def download_file_as_stream(file: TalpiXFile):
    blob_service_client: BlobServiceClient = BlobServiceClient.from_connection_string(TalpiotSettings.get().azure_blobs_connection_string)
    blob_client = blob_service_client.get_blob_client('talpix-user-files', file.path_on_server)

    return blob_client.download_blob()


def download_file_as_bytes(file: TalpiXFile):
    return download_file_as_stream(file).readall()
