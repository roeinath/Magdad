import csv
import os.path
import random
import traceback
from dataclasses import dataclass

# constants for analyzing csv file
from web_features.tech_miun import constants

NOT_FILLED = 0
ESTIMATOR_COLUMNS = (2, 4, 6)
ESTIMATOR_EMAIL_COLUMNS = (3, 5, 7)
CLASS_NUMBER_COLUMN = 8
TEAM_COLUMN = 9
MALSHAB_COLUMNS = (10, 12, 14, 16)

LOCAL_DIR = os.path.abspath(os.path.dirname(__file__))


@dataclass
class Malshab:
    name: str
    serial_number: int
    class_number: str
    team: str


"""
This class is responsible for pulling the malshabs' partition from an outside source and keeping it
updated.
"""


class MalshabInfo:
    def __init__(self, filename):
        self.filename = filename

        self.estimator_email_to_malshabs = {}
        self.estiamtor_email_to_name = {}

        self.load_local_file()

    def load_local_file(self):
        # opens the master file
        if not os.path.isfile(os.path.join(LOCAL_DIR, self.filename)):
            return

        with open(os.path.join(LOCAL_DIR, self.filename), 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            data = list(reader)

        # a dict that maps estimators (represented by their email) to the list of malshabs they need to estimate
        self.estimator_email_to_malshabs = {}
        self.estiamtor_email_to_name = {}

        for row in data[1:]:
            # each line contains multiple malshabs, which are estimated by multiple estimators (in the same line)

            est_emails = [row[i] for i in ESTIMATOR_EMAIL_COLUMNS]
            class_number = row[CLASS_NUMBER_COLUMN]
            team = row[TEAM_COLUMN]

            estimators = []  # tuples of (name, email)
            for i in ESTIMATOR_COLUMNS:
                if i + 1 < len(row) and row[i] != '' and row[i + 1] != '':
                    estimators.append((row[i], row[i + 1]))

            malshabs = []
            for i in MALSHAB_COLUMNS:
                if i + 1 < len(row) and row[i] != '' and row[i + 1] != '':
                    malshabs.append(Malshab(row[i], int(row[i + 1]), class_number, team))

            for name, email in estimators:
                # add the estimator to the dictionary if they aren't in it
                if email not in self.estiamtor_email_to_name:
                    self.estiamtor_email_to_name[email] = name
                if email not in self.estimator_email_to_malshabs:
                    self.estimator_email_to_malshabs[email] = []

                # add the malshabs to the dictionary
                for malshab in malshabs:
                    self.estimator_email_to_malshabs[email].append(malshab)

    def get_malshabs_by_estimator_email(self, estimator_email):
        return self.estimator_email_to_malshabs.get(estimator_email, [])

    def get_malshabs_by_estimator(self, estimator_user):
        """
        :param estimator_user: a User object of the estimator
        :return: a list of Malshabs the estimator needs to estimate
        """
        return self.get_malshabs_by_estimator_email(estimator_user.email)

    def get_estimator_name_by_email(self, est_email):
        return self.estiamtor_email_to_name[est_email]

    def get_all_estimator(self):
        """
        :return: a list of all estimators
        """
        return list(self.estimator_email_to_malshabs.keys())

    def is_filled(self, estimator_email, malshab):
        return bool(random.choice([True, False]))
