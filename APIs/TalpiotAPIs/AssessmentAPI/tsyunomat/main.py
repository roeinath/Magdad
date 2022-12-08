import argparse
from datetime import datetime
from pprint import pprint

from APIs.TalpiotAPIs.AssessmentAPI.tsyunomat.GetDataFromDB import *
from APIs.TalpiotAPIs.AssessmentAPI.tsyunomat.HujiGradePuller import HujiGradePuller
from APIs.init_APIs import main as connect_db


def run(login_file, pull_final_grades, assignments_years, visible=False, is_real_data=True, update=False,
        wanted_year=None):
    # pull and save in DB:
    gradePuller = HujiGradePuller(login_file, is_real_data=is_real_data, update=update, wanted_year=wanted_year)
    directory_name = gradePuller.pull_grades(
        pull_final_grades=True, assignments_years=assignments_years, log=True, visible=visible
    )
    return directory_name


def start(madar_password, update=False, is_real_data=True, wanted_year=None):
    parser = argparse.ArgumentParser(description='Grab grades of students from huji sites')
    parser.add_argument('--tests', action='store_true', help='copy tests grades from web')
    parser.add_argument('--moodle', nargs='*', default=None, const=None,
                        help='the years you wish to pull grades from moodle separated with commas. For the years [2019, 2020], input: --moodle 19 20"')

    input_data = parser.add_mutually_exclusive_group()
    # input_data.add_argument('--gspread_id', help='an id of google spreadsheet to get data from')

    args = parser.parse_args()

    if isinstance(args.moodle, str): args.moodle = [args.moodle]

    data_dict = get_users_info(madar_password)
    directory_name = run(data_dict, args.tests, args.moodle, visible=False, is_real_data=is_real_data,
                         update=update, wanted_year=wanted_year)

    return directory_name


if __name__ == "__main__":
    # connect to DB
    connect_db()
    start_time = datetime.now()
    directory_name = start('INSERT_CODE_HERE', update=True)
    print("\nFinished in: ", datetime.now() - start_time)
    pprint(directory_name)
