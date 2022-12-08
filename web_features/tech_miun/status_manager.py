import csv
import os

ESTIMATOR_COLUMN = 1
ESTIMATOR_EMAIL_COLUMNS = 2
MALSHAB_NUMBER_COLUMN = 5

LOCAL_DIR = os.path.abspath(os.path.dirname(__file__))


class StatusManager:

    def __init__(self, filename):
        self.filename = filename

        self.estimator_email_to_malshab_nums = {}

        self.load_local_file()

    def load_local_file(self):
        # opens the results
        if not os.path.isfile(os.path.join(LOCAL_DIR, self.filename)):
            return

        with open(os.path.join(LOCAL_DIR, self.filename), 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            data = list(reader)

        self.estimator_email_to_malshab_nums = {}

        for row in data[1:]:

            malshab_num = row[MALSHAB_NUMBER_COLUMN]
            email = row[ESTIMATOR_EMAIL_COLUMNS]

            if malshab_num == '' or email == '':
                continue

            if email not in self.estimator_email_to_malshab_nums:
                self.estimator_email_to_malshab_nums[email] = []

            self.estimator_email_to_malshab_nums[email].append(int(malshab_num))

    def is_filled(self, estiamtor_email, malshab):
        return malshab.serial_number in self.estimator_email_to_malshab_nums.get(estiamtor_email, [])
