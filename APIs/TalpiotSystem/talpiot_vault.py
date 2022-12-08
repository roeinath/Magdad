from __future__ import annotations

from threading import Thread
from typing import Dict, Any

from mongoengine import connect, DEFAULT_CONNECTION_NAME as MONGOENGINE_DEFAULT_CONNECTION_NAME
from mongoengine.context_managers import switch_db

from APIs.TalpiotSystem import TalpiotSettings, TBLogger


class Vault:
    __instance = None

    def __init__(self):
        if Vault.__instance is not None:
            raise Exception("This class is a singleton!")

        self._active_db_connections: Dict[str, Any] = dict()

        #  Get username&password from db
        self.settings = TalpiotSettings.get().database_settings
        self.database_creds = TalpiotSettings.get().database_creds
        self._synced_collections = None

        Vault.__instance = self

    @staticmethod
    def get_vault() -> Vault:
        if Vault.__instance is None:
            Vault()
        return Vault.__instance

    def connect_all_dbs(self):
        self.connect_to_db()
        self.connect_to_db(self.settings.authentication_table)
        self.connect_to_db(self.settings.current_database_name)
        self.connect_to_db("talpiot_dev")

    def connect_to_db(self, alias=MONGOENGINE_DEFAULT_CONNECTION_NAME):
        """
        Connects to a DB with the given alias. The alias of every db
        equals to the db name, except for the talpibot_main db that
        it's alias is "default"
        :param alias: The name of the DB or "default" for talpibot_main
        :return:
        """

        #  Check if this connection is not already open
        if alias in self._active_db_connections:
            return

        #  Get real db name
        db_name = alias
        if alias == MONGOENGINE_DEFAULT_CONNECTION_NAME:
            db_name = self.settings.current_database_name

        #  Connect to the DB
        TBLogger.info("Connecting to db `%s` [%s]..." % (alias, db_name))

        self._active_db_connections[alias] = connect(
            db=db_name,
            username=self.database_creds.username,
            password=self.database_creds.password,
            authentication_source=self.settings.authentication_table,
            host=self.settings.server_url,
            port=self.settings.server_port,
            ssl=self.settings.use_ssl,
            ssl_ca_certs=self.settings.ssl_server_certificate,
            alias=alias
        )

    def objects_from_main_db(self, document_class, filters={}):
        with switch_db(document_class, self.settings.authentication_table) as document:
            return document.objects(**filters)

    def get_database(self, db_name=None):
        if db_name is None:
            db_name = self.settings.authentication_table
        self.connect_to_db(db_name)
        return self._active_db_connections[db_name].get_database(db_name)

    def list_collection_names(self, db_name=None):
        database = self.get_database(db_name)
        if database is not None:
            return database.list_collection_names()

    def sync_db_to_main(self, collection_names, db_name=None, wait_until_finished=False):
        if db_name is None:
            db_name = self.settings.current_database_name
        if db_name == self.settings.authentication_table:
            return

        db = self.get_database(db_name)
        main_db = self.get_database(self.settings.authentication_table)

        threads = []
        self._synced_collections = {}

        for collection_name in collection_names:
            t = Thread(target=self._sync_a_collection, args=(main_db, db, collection_name,))
            threads.append(t)
            t.start()

        if wait_until_finished:
            self._log_when_sync_finished(threads)
            return self._synced_collections

        TBLogger.info(f"Syncing database `%s`" % db_name)
        Thread(target=self._log_when_sync_finished, args=(threads,)).start()  # Notify on thread finish

    def _sync_a_collection(self, from_db, to_db, collection_name):
        to_db_found_ids = [document['_id'] for document in to_db[collection_name].find()]
        new_documents_in_from_db = list(from_db[collection_name].find({'_id': {'$nin': to_db_found_ids}}))

        if len(new_documents_in_from_db) > 0:
            response = to_db[collection_name].insert_many(new_documents_in_from_db)
            self._synced_collections[collection_name] = len(response.inserted_ids)

    def _log_when_sync_finished(self, threads):
        for t in threads:
            t.join()

        TBLogger.info(f"Done syncing database with %s updated collections"
                      % sum(value > 0 for name, value in self._synced_collections.items()))
