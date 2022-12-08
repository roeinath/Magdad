from mongoengine import *
from tqdm import tqdm

from APIs.TalpiotAPIs import User
from APIs.TalpiotAPIs.AssessmentAPI.Database.api.uploaddata.ExcelParser import ExcelParser
from APIs.init_APIs import main as connect_db

from APIs.TalpiotAPIs.AssessmentAPI.Database.api.querycalls.filter import Filter
from APIs.TalpiotAPIs.AssessmentAPI.Database.platform_grade import PlatformGrade


def _validate_skirot_url(url):
    for key in url.keys():
        if key not in ["A", "B", "C", "D", "E", "F"]:
            raise ValidationError("Invalid semester")


class Files(Document):
    user = ReferenceField('User', required=True)
    skirot_url = MapField(StringField(), default={}, validation=_validate_skirot_url)

    meta = {'collection': 'files'}

    def __str__(self):
        return f"user files: \"{self.user}\""


def insert_urls_from_xlsx_file(path):
    """
    insert all urls to DB
    :param path:
    :return:
    """
    my_excel_parser = ExcelParser(path)
    data = my_excel_parser.get_data_from_sheet(0)
    for row in tqdm(data):
        name = row["שם"]
        semester = row["סמסטר"]
        url = str(row["קישור"])
        users = User.objects.filter(name=name)
        if len(users) == 0:
            print(name)
            continue
        files = Files.objects.filter(user=users[0])
        if len(files) == 0:
            file = Files(user=users[0], skirot_url={semester: url})
            file.save()
        else:
            file = files[0]
            file.skirot_url[semester] = url
            file.save()


if __name__ == "__main__":
    connect_db()
    # insert_urls_from_xlsx_file(r"C:\Users\t9028387\Downloads\קישורים לפורטל.xlsx")
    # get user by name
    user = User.objects(name="יואב פלטו").first()
    file = Files.objects.filter(user=user)[0]
    file.skirot_url = {"D": "https://docs.google.com/document/d/19wGhMatSSD0g7PBFYrD-uRCPdYMvTSZ6wPCIRFNXXF0/edit"}
    file.save()
    #
    # a = Files(user=user, skirot_url={"A": "https://skirot.talpiot.ac.il/"})
    # a.save()
