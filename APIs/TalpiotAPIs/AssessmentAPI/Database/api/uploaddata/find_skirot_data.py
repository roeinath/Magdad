"""
Code for saving grades from Year 1 end of semester Skirot to one formatted Excel file
"""
from APIs.TalpiotAPIs.AssessmentAPI.Database.api.docx_for_docm import Document
from cryptography.fernet import Fernet
import os
from APIs.TalpiotAPIs.AssessmentAPI.Database.platform import Platform
from APIs.TalpiotAPIs.AssessmentAPI.Database.api.uploaddata import skirot_presubmit



# TODO: This code only works with some changes to the docx_new module source code, which allow working with .docm files.
# For more information, check:
# https://github.com/python-openxml/python-docx/pull/716/commits/c09da22afaebaed2f0a3139de6ba46c8824f179e


# files_to_skip- files which are located in the same dir
files_to_skip = ["upload_skira.py", "Skirot.xlsx", "db_upload.py", "presubmit.py", "ExcelParser.py"]

# Key for the symmetric encryption
__fernet_key = b'FVOwF-23paS9PIFBdmjCrYjhiQ6hyQEOfAcb832gS-0='


def encrypt(val: float) -> str:
    """
    A function for encrypting the grades
    :param val: the grade to be encrypted
    :return: the grade, encrypted using the fernet module
    """
    val = str(val).encode()
    return Fernet(__fernet_key).encrypt(val).decode()


def convert_to_csv(input_file_path, talpion_name):
    """
    The main function, which finds the grades in a directory of Skirot, and saves them in .xlsx file
    :param input_file_path:
    :return: Tuple(data to save in sheet, sheet name)
    """
    c = None
    error = False

    document = Document(input_file_path)

    p = document.tables

    text = []

    # Finding the grades' table in the Skira
    for table in p:
        if skirot_presubmit.FLAG in table.rows[0].cells[0].text:
            c = p.index(table)
            break

    if c:
        # Parsing the grades from the grades' table
        axis = [p[c].rows[1].cells[i].text for i in range(1, len(p[c].rows[0].cells))]
        cat = [p[c].rows[2].cells[i].text for i in range(1, len(p[c].rows[0].cells))]
        grade_types = [f"{cat[i]} ({axis[i]})" for i in range(len(axis))]
        text = []

        platforms = []
        rows = p[c].rows[3:]

        for i, row in enumerate(rows):
            # Getting the actual grades, parsing and encrypting them
            row_text = {}
            full_plat = [s.strip() for s in p[c].rows[i+3].cells[0].text.split("-")]
            if len(full_plat) == 1 and len([s.strip() for s in p[c].rows[i+3].cells[0].text.split("–")]) > 1:
                full_plat = [s.strip() for s in p[c].rows[i+3].cells[0].text.split("–")]
            if len(full_plat) > 2:
                return None, None, None, f" אחת הפלטפורמות לא בפורמט המתאים {'-'.join(full_plat)}"
            while len(full_plat) < 2:
                full_plat += [full_plat[0]]

            full_plat = full_plat[::-1]
            if not full_plat[1] in Platform.types:
                return None, None, None, f" אחת הפלטפורמות לא מתאימה לקטגוריות המוגדרות {'-'.join(full_plat)}"
            platforms.append(full_plat)
            for cell in range(len(row.cells[1:])+1):
                cell_text = row.cells[cell].text
                cell_text = cell_text.replace(",", "").replace("\n", "\t")
                if cell_text == '':
                    cell_text = 0

                try:
                    cell_text = float(cell_text)

                except ValueError:
                    # Error in the grades format,  even mafkatzim make mistakes sometimes
                    pass

                row_text[grade_types[cell-1]] = cell_text

            text.append(row_text)

        return text, platforms, talpion_name, error

    else:
        # No grades table was found. Probably an error in the Skira format
        error = f"לא נמצאו ציונים בסקירה של ({talpion_name})"
        return None, None, None, error


def find(filename, username):
    """
    The main function, which carries the whole operation, while using the helper methods above
    """

    if filename not in files_to_skip:
        text, platforms, name, error = convert_to_csv(os.path.abspath(filename), username)
        if text and name and platforms:
            return name, text, platforms, error
    return None, None, None, error
    # TODO change this


# Ido Ivri, MemGimel
