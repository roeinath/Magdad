import os

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from web_features.tech_miun.constants import *

SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
          "https://www.googleapis.com/auth/drive.file",
          "https://www.googleapis.com/auth/drive"]

LOCAL_DIR = os.path.abspath(os.path.dirname(__file__))


class DriveConnection:

    def __init__(self):
        # File 'internal-gsheets-creds.json' doesn't exist in the repo.
        # It's a private saved on the azure machine separately
        # If you update locally make sure to update the docker-compose volumes as well.
        CREDS_PATH = os.path.join(LOCAL_DIR, CREDS_FILENAME)
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_PATH, SCOPES)
        self.client = gspread.authorize(self.creds)

        self.files_dict = dict()

    def update_sheet(self, filename):
        self.files_dict[filename] = self.client.open(os.path.splitext(filename)[0]).sheet1.get_all_values()

        print(f"Open file: {filename}")
        with open(os.path.join(LOCAL_DIR, filename), 'w', encoding='utf-8') as f:
            for line in self.files_dict[filename]:
                for item in line:
                    f.write(f"{item},")
                f.write('\n')
        print(f"Done writing file: {filename}")

    def __call__(self):
        print("DriveConnection: Updating files")
        self.update_sheet(SOLUTIONS)
        self.update_sheet(HACKAB)
        self.update_sheet(QA)
        self.update_sheet(SOLUTION_RESULTS)
        self.update_sheet(HACKAB_RESULTS)
        self.update_sheet(QA_RESULTS)
        print("DriveConnection: Done updating files")

    def get_sheet(self, filename):
        return self.files_dict.get(filename, None)
