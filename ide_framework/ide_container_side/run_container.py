from bot_framework.main import main
from APIs.TalpiotSystem import talpiot_settings

import os


def run_git_command(git_cmd):
    os.system('eval "$(ssh-agent)" && ssh-add ../.ssh/id_rsa &&' + git_cmd)


def run_container(db_name: str, branch_name: str):
    os.chdir("ide_framework/feature_logs")
    os.system("> logs.txt")
    os.chdir("../../talpix")
    run_git_command("git fetch")
    run_git_command(f"git checkout {branch_name}")
    run_git_command("git pull")
    os.environ["CURRENT_DATABASE_NAME"] = db_name
    talpiot_settings.TalpiotSettings.get().database_settings.set_ide_db(db_name)
    main()

