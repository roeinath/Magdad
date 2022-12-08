from ide_framework.ide_container_side import container_command_handler

from APIs.TalpiotSystem.talpiot_vault import Vault
from APIs.settings import load_settings
from APIs.TalpiotAPIs.Gitlab import update_file_tree

import traceback

try:
    load_settings()
    Vault.get_vault().connect_all_dbs()
    print("run ide")
    container = container_command_handler.ContainerCommandHandler()
    container.container_command_handler()
except Exception as e:
    print("There was an error with running the ide")
    print(traceback.format_exc())