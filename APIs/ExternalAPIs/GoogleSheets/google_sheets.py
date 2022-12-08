from __future__ import annotations
import os
from APIs.ExternalAPIs.WorkerPool.pool import Pool
from APIs.ExternalAPIs.WorkerPool.pooled_worker import PooledWorker

#  If modifying this scopes, delete token.json
from APIs.TalpiotSystem import TalpiotSettings

SCOPES_SHEETS = ['https://www.googleapis.com/auth/spreadsheets.readonly']

VALUE_INPUT_OPTION_USER_ENTERED = "USER_ENTERED"
VALUE_INPUT_OPTION_RAW = "RAW"

MAJOR_DIMENSION_ROWS = "ROWS"
MAJOR_DIMENSION_COLUMNS = "COLUMNS"

MAX_WORKERS = 5


class GoogleSheets(PooledWorker):
    """
    A class that allows accessing GoogleSheets with
    the bot google account.
    """

    _pool = Pool(lambda: GoogleSheets(), MAX_WORKERS)

    @staticmethod
    def get_instance() -> GoogleSheets:
        return GoogleSheets._pool.get_free_worker()

    def __init__(self):
        super().__init__()
        self.creds_diary = None
        self.service = None

        self.connect_to_sheets()

    @staticmethod
    def A1_range(A1, B2):
        return A1 + ":" + B2

    @staticmethod
    def nums_to_A1_range(col1, row1, col2, row2):
        A1 = GoogleSheets.nums_to_A1(col1, row1)
        B2 = GoogleSheets.nums_to_A1(col2, row2)
        return GoogleSheets.A1_range(A1, B2)

    @staticmethod
    def nums_to_A1(col, row):
        string = ""
        n = col
        while n > 0:
            n, remainder = divmod(n - 1, 26)
            string = chr(65 + remainder) + string
        return string + str(row)

    def connect_to_sheets(self):
        token_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "token.pickle"
        )

        google_settings = TalpiotSettings.get().google_connection_settings
        self.service = google_settings.get_service('sheets', 'v4', SCOPES_SHEETS, token_path)

    def get_spreadsheet_details(self, spreadsheet_id: str):
        """
        Returns an result dictionary that has details about the specific
        spreadsheet.

        :param spreadsheet_id: The ID of the GoogleSheet document
        :return: dict
        """

        result = self.service.spreadsheets().get(
            spreadsheetId=spreadsheet_id
        ).execute()

        return result

    def get_sheet_details(self, spreadsheet_id: str, sheet_name: str):
        """
        Returns an result dictionary that has details about the specific
        spreadsheet.

        :param spreadsheet_id: The ID of the GoogleSheet document
        :param sheet_name: The sheet name to get details for
        :return: dict
        """

        result = self.get_spreadsheet_details(spreadsheet_id)

        #  Get list of sheets, if fails return None
        sheets = result.get("sheets", None)

        if sheets is None:
            return None

        #  Search for sheet with the same title
        for sheet in sheets:
            if sheet.get("properties", dict()).get("title") == sheet_name:
                return sheet

        return None

    def get_range_format(self, spreadsheet_id: str, sheet_name: str, ranges_name: str,
                         major_dimension: str = MAJOR_DIMENSION_ROWS) -> [[str]]:
        """
        Returns an array of rows, in the requested range, for the
        specific spreadSheetId, and inside looks only at the given
        sheet_name.

        :param spreadsheet_id: The ID of the GoogleSheet document
        :param sheet_name: Inside the document, what sheet to use.
        :param ranges_name: What ranges of cells to return. For example, ["A2:G8"]
        :param major_dimension: The major dimension to use in the return type.
        check google's sheets api reference for more explanation.
        :return: [[str]] Array of rows.
        """
        if type(ranges_name) != type([]):
            ranges_name = [ranges_name]
        sheet = self.service.spreadsheets()
        result = sheet.get(
            spreadsheetId=spreadsheet_id,
            ranges=[sheet_name + "!" + x for x in ranges_name],
            includeGridData=True
        ).execute()
        cells_groups = []
        for data_row in result.get("sheets", [{}])[0].get("data", [{}]):
            rows = [row.get("values", []) for row in data_row.get("rowData", [{}])]
            cells = []
            for row in rows:
                cells_row = []
                #print(row)
                for item in row:
                    bg = item.get("effectiveFormat", {}).get("backgroundColorStyle", {}).get("rgbColor", {})
                    cl = item.get("effectiveFormat", {}).get("textFormat", {}).get("foregroundColorStyle", {}).get(
                        "rgbColor", {})

                    cells_row.append({
                        "value": item.get("formattedValue", ""),
                        "formulaValue": item.get("userEnteredValue", {}).get("formulaValue", ""),
                        "backgroundColor": (bg.get("red", 0), bg.get("green", 0), bg.get("blue", 0)),
                        "foregroundColor": (cl.get("red", 0), cl.get("green", 0), cl.get("blue", 0)),
                        "bold": item.get("effectiveFormat", {}).get("textFormat", {}).get("bold", "false"),
                        "fontSize": item.get("effectiveFormat", {}).get("textFormat", {}).get("fontSize", 10),
                        "underline": item.get("effectiveFormat", {}).get("textFormat", {}).get("underline", "false"),
                        "hyperlink": item.get("hyperlink", "")
                    })
                cells.append(cells_row)
            cells_groups.append(cells)
        return cells_groups

    def get_range(self, spreadsheet_id: str, sheet_name: str, range_name: str, major_dimension: str = MAJOR_DIMENSION_ROWS) -> [[str]]:
        """
        Returns an array of rows, in the requested range, for the
        specific spreadSheetId, and inside looks only at the given
        sheet_name.

        :param spreadsheet_id: The ID of the GoogleSheet document
        :param sheet_name: Inside the document, what sheet to use.
        :param range_name: What range of cells to return. For example, "A2:G8"
        :param major_dimension: The major dimension to use in the return type.
        check google's sheets api reference for more explanation.
        :return: [[str]] Array of rows.
        """

        sheet = self.service.spreadsheets()
        result = sheet.values().get(
            spreadsheetId=spreadsheet_id,
            range=sheet_name + "!" + range_name,
            majorDimension=major_dimension
        ).execute()
        values = result.get('values', None)

        return values

    def set_range(self,
                  spreadsheet_id: str,
                  sheet_name: str,
                  range_name: str,
                  values: [[str]],
                  value_input_option=VALUE_INPUT_OPTION_USER_ENTERED):
        """
        Sets a range inside a GoogleSheet to a specific array.

        :param spreadsheet_id: The ID of the GoogleSheet document
        :param sheet_name: Inside the document, what sheet to use.
        :param range_name: What range of cells to return. For example, "A2:G8"
        :param values: [[str]] the values to update
        :param value_input_option: either RAW or USER_ENTERED, see google's
        documentation.
        :return: Number of updated cells.
        """

        body = {
            'values': values
        }

        result = self.service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=sheet_name + "!" + range_name,
            valueInputOption=value_input_option,
            body=body
        ).execute()

        return result.get('updatedCells')

    def get_free_sheet_row(self, spreadsheet_id, sheet_name, last_column_index):
        """
        :param spreadsheet_id: The ID of the GoogleSheet document
        :param sheet_name: Inside the document, what sheet to use
        :param last_column_index: the last column index to check if empty
        :return the first row in the google sheets file which is free. Free means that all the cells in the row until
        the last_column index are empty
        """
        row = 1
        while True:
            test_list = self.get_range(spreadsheet_id, sheet_name,
                                     "A" + str(row) + ":" + str(last_column_index) + str(row))
            if test_list is None:
                break
            row += 1
        return row

    def find_row_by_content_in_column(self, spreadsheet_id, sheet_name, column_index, content, last_column_index):
        """
        :param spreadsheet_id: The ID of the GoogleSheet document
        :param sheet_name: Inside the document, what sheet to use
        :param column_index: the index of the column to search in
        :param content: the content to search
        :param last_column_index: the last column in the table
        :return: the first row with the given content in the given column. None if there is an empty row before the
        content found.
        """
        row = 1
        while True:
            test_list = self.get_range(spreadsheet_id, sheet_name,
                                     "A" + str(row) + ":" + str(last_column_index) + str(row))
            if test_list is None:
                return None
            elif test_list[0][column_index] == content:
                return row
            row += 1

    def sort_sheet_by_column(self, spreadsheet_id, sheet_name, column_index, last_column):
        """
        :param spreadsheet_id: The ID of the GoogleSheet document
        :param sheet_name: Inside the document, what sheet to use
        :param column_index: the column to sort by
        :param last_column: the last column in the table
        sorts the table by the values in the given column.
        """
        max_row = self.get_free_sheet_row(spreadsheet_id, sheet_name, last_column)
        cell_range = self.get_range(spreadsheet_id, sheet_name,
                                  "A2:" + str(last_column) + str(max_row))
        cell_range.sort(key=lambda row: row[column_index])
        self.set_range(spreadsheet_id, sheet_name,
                     "A2:" + str(last_column) + str(max_row), cell_range)


if __name__ == "__main__":
    import os

    from APIs.TalpiotSystem.talpiot_settings import TalpiotGoogleConnectionSettingsServiceAccount
    TalpiotSettings()

    with GoogleSheets.get_instance() as gs:
        print(
            gs.get_range(spreadsheet_id="1mzap_6kwa8Ik5HpP7VViGL_a5jv2-xp0sIQmo4OECv8", sheet_name="Sheet1", range_name="A1:A3")
        )
