import locale
import os

from bot_framework.settings import load_settings
from APIs.TalpiotSystem import Vault
from APIs.TalpiotAPIs.static_fields import get_db_collections


def fix_git():
    for line in open('GettingStarted/git_ignore.bat').readlines():
        os.system(line)


def run_setup():
    if "CURRENT_DATABASE_NAME" not in os.environ:
        load_settings()
    # fix_git()
    locale_setup()
    Vault.get_vault().connect_all_dbs()
    Vault.get_vault().sync_db_to_main(get_db_collections())


def locale_setup():
    try:
        locale.setlocale(locale.LC_ALL, "he_IL.utf8")
    except:
        locale.setlocale(locale.LC_ALL, "he_IL")
