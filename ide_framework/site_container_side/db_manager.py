from APIs.TalpiotSystem import TalpiotSettings
from APIs.TalpiotSystem.talpiot_vault import Vault


class DBManager:
    def __init__(self):
        self.vault = None # Vault.get_vault()
        self.settings = TalpiotSettings.get().database_settings

    def connect_to_db(self, db_name: str):
        self.vault.connect_to_db(db_name)

    def get_main_db(self):
        return self.vault.get_database()

    def sync_db_to_main(self, db_name: str) -> dict:
        db = self.vault.get_database(db_name)
        main_db = self.get_main_db()

        synced_collection = {}

        for collection_name in main_db.list_collection_names():
            collection_data = list(main_db[collection_name].find())
            try:
                response = db[collection_name].insert_many(collection_data)
                synced_collection[collection_name] = len(response.inserted_ids)
            except:
                synced_collection[collection_name] = 0
        return synced_collection

