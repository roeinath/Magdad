# from pydrive.drive import GoogleDrive
# from pydrive.auth import GoogleAuth
import pandas as pd
# import gspread
import time
import json
import os
from itertools import zip_longest


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def save_data(filename, data):
    # Serialize data into file:
    json.dump(data, open(filename + ".json", 'w'))


def read_data(filename):
    # Read data from file:
    data = json.load(open(filename))
    return data

#
# def google_authentication():
#     gauth = GoogleAuth()
#
#     # Try to load saved client credentials
#     gauth.LoadCredentialsFile("mycreds.txt")
#     if gauth.credentials is None:
#         # Authenticate if they're not there
#         gauth.LocalWebserverAuth()
#     elif gauth.access_token_expired:
#         # Refresh them if expired
#         gauth.Refresh()
#     else:
#         # Initialize the saved creds
#         gauth.Authorize()
#     # Save the current credentials to a file
#     gauth.SaveCredentialsFile("mycreds.txt")
#
#     drive = GoogleDrive(gauth)
#
#     return drive
#
#
# def download_file(id):
#     drive = google_authentication()
#     file = drive.CreateFile({'id': id})
#     file.GetContentFile(file['title'])
#     return file['title']
