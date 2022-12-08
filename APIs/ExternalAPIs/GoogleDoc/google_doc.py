from __future__ import annotations
from typing import Union
import os
import dateutil.parser
from datetime import datetime, date

from APIs.ExternalAPIs.GoogleCalendar.calendar_event import CalendarEvent
from APIs.ExternalAPIs.GoogleCalendar.calendar_helper import iso_date_format
from APIs.ExternalAPIs.WorkerPool.pool import Pool
from APIs.ExternalAPIs.WorkerPool.pooled_worker import PooledWorker

#  If modifying this scopes, delete token.json
from APIs.TalpiotSystem import TalpiotSettings

SCOPES_DOC = ['https://www.googleapis.com/auth/documents']

MAX_WORKERS = 5


class GoogleDoc(PooledWorker):
    """
    A class that allows accessing a Google Doc documents with
    the bot google account. It is important that talpibotsystem@gmail.com is shared and can edit your document.
    """

    _pool = Pool(lambda: GoogleDoc(), MAX_WORKERS)

    @staticmethod
    def get_instance() -> GoogleDoc:
        return GoogleDoc._pool.get_free_worker()

    def __init__(self):
        super().__init__()
        self.creds_diary = None
        self.service = None

        self.connect_to_doc()

    def connect_to_doc(self):
        token_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "token.pickle"
        )

        google_settings = TalpiotSettings.get().google_connection_settings
        self.service = google_settings.get_service('docs', 'v1', scopes=SCOPES_DOC, token_file_path=token_path)

    def insert_list_to_sheet(self, document_id, lines):
        """
        Inserts a bulleted list to Google Doc. Expects to get list of strings.
        Documentation for changing the format: https://developers.google.com/docs/api/how-tos/move-text
        """
        index = 1
        for line in lines:
            requests = [
                {
                    'insertText': {
                        'location': {
                            'index': index
                        },
                        'text': line + '\n',
                    }}, {
                    'createParagraphBullets': {
                        'range': {
                            'startIndex': index,
                            'endIndex': index + len(line)
                        },
                        'bulletPreset': 'BULLET_DISC_CIRCLE_SQUARE',
                    }
                }
            ]

            result = self.service.documents().batchUpdate(
                documentId=document_id, body={'requests': requests}).execute()
            index += len(line) + 1

if __name__ == "__main__":
    from datetime import timedelta

    TalpiotSettings()
    with GoogleDoc.get_instance() as gc:
        gc.connect_to_doc()
