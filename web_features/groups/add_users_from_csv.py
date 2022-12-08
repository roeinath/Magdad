import csv
import os

from APIs.ExternalAPIs import FileToUpload
from APIs.TalpiotAPIs import User

NAME_FIELD = '\ufeffName'
EMAIL_FIELD = 'E-mail 1 - Value'
PHONE_FIELD = 'Phone 1 - Value'
MACHZOR_NUMBER_LENGTH = 5


def add_users_from_csv(file_to_upload, participants: list = None, remove_numer = True):
    file_ = FileToUpload.load_from_json(file_to_upload)
    if not file_ or not file_.name.endswith('.csv'):
        return
    temp_file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'temp_files',
        file_.name
    )
    with open(temp_file_path, 'wb') as f:
        f.write(file_.get_content())

    with open(temp_file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if remove_numer:
                name = row[NAME_FIELD][:-MACHZOR_NUMBER_LENGTH]  # removes the " - 42" from "Name - 42"
            else:
                name = row[NAME_FIELD]
            email = row[EMAIL_FIELD]
            phone_number = row[PHONE_FIELD]
            gender = 'male'
            user = User(name=name, email=email, phone_number=phone_number, mahzor=-1, gender=gender).save()
            participants.append(user)

    os.remove(temp_file_path)


