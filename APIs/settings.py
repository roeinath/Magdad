import json
import os
import shutil

import APIs.Database as dir_path

"""
setting.py - a settings file for the system. The TalpiBotSettings is a singleton class.

In order to get the settings in your code you can use TalpiBotSettings.get()

For example:
    return TalpiBotSetting.get().database_creds.username
        
DO NOT UPLOAD YOUR SETTINGS FILE TO GIT.
"""

CURR_DIR = os.path.abspath(os.path.dirname(__file__))
SETTINGS_JSON = os.path.join(CURR_DIR, "settings.json")
SECERTS_SETTINGS_JSON = os.path.join(CURR_DIR, "secret_settings.json")


def load_settings():
    from APIs.TalpiotSystem import TalpiotSettings, TalpiotDatabaseCredentials, TalpiotDatabaseSettings, \
        TalpiotGmailSettings

    if TalpiotSettings.is_loaded():
        return
    filename = SETTINGS_JSON
    if os.path.isfile(SECERTS_SETTINGS_JSON):
        print("+++++++++++++ USING SECRET JSON +++++++++++++++")
        filename = SECERTS_SETTINGS_JSON
    with open(filename) as f:
        settings_data = json.load(f)
    if 'CURRENT_DATABASE_NAME' in os.environ:  # set db to talpiot_dev_feature_name
        settings_data["CURRENT_DATABASE_NAME"] = os.environ['CURRENT_DATABASE_NAME']
    if 'BOT_TOKEN' in os.environ:  # set db to talpiot_dev_feature_name
        settings_data["BOT_TOKEN"] = os.environ['BOT_TOKEN']
    # INIT SETTINGS
    TalpiotSettings(
        database_creds=TalpiotDatabaseCredentials(
            settings_data["MONGO_USER"],
            settings_data["MONGO_PASSWORD"]
        ),
        database_settings=TalpiotDatabaseSettings(
            server_url=settings_data["MONGO_URL"],
            server_port=settings_data["MONGO_PORT"],
            use_ssl=True,
            ssl_server_certificate=os.path.join(os.path.dirname(dir_path.__file__), "server.crt"),
            authentication_table=settings_data["MAIN_DATABASE_NAME"],
            current_database_name=settings_data["CURRENT_DATABASE_NAME"]
        ),
        bot_token=settings_data["BOT_TOKEN"],
        gmail_settings=TalpiotGmailSettings(
            settings_data["GMAIL_USER"],
            settings_data["GMAIL_PASSWORD"]
        ),
        azure_blobs_connection_string=settings_data["AZURE_BLOBS_CONNECTION_STRING"]
    )


if __name__ == '__main__':
    shutil.copy(SETTINGS_JSON, SECERTS_SETTINGS_JSON)
    with open(SECERTS_SETTINGS_JSON, 'a') as f_:
        f_.write('\n// EDIT THIS FILE!\n// YOU MAY WANT TO CHANGE THE BOT TOKEN AND DELETE THESE LINES')
