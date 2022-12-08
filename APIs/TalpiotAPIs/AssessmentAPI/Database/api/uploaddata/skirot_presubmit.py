import tkinter as tk
from tkinter import filedialog
from APIs.TalpiotAPIs.AssessmentAPI.Database.api import docx_for_docm

FLAG = "כמותיים"
AXES = ["מנהיגות", "ערכים", "מקצועיות"]
CATEGORIES = {"מנהיגות": ["דמות", "תפקוד בחברה", "הובלה"], "מקצועיות": ["ניהול", "מדעי אקדמי", "מדעי יישומי", "בטחוני"], "ערכים": ["א", "ד", "ה", "י", "מ", "ש"]}
ALLCATS = ["דמות", "תפקוד בחברה", "הובלה", "מנהיגות", "ניהול", "מדעי אקדמי", "מדעי יישומי", "א", "ד", "ה", "י", "מ", "ש", "בטחוני"]


class SkiraPresubmitError(Exception):
    """
    This is a class representing an error while checking the file. The class implementation is actually redundant,
    but you can easily modify this part in order to work with python errors instead of the messages to the user
    """
    EXTENSION = "שגיאה! סוג הקובץ לא מתאים!"
    NOTABLES = "שגיאה! אין טבלאות ציונים בקובץ שהועלה!"
    YEARERROR = "שגיאה! השנה בקובץ לא שווה לשנה שנבחרה!"
    INTGRADE = "שגיאה! אחד הציונים בקובץ שהועלה הוא לא מספר!"
    EMPTYGRADE = "שגיאה! אחד הציונים בסקירה הוא ריק!"
    AXESERROR = "שגיאה! צירי ההכשרה המופיעים במסמך לא נכונים! "
    CATAXESFORMATION = "שגיאה! אחד הציונים לא נמצא תחת הציר המתאים!"
    UNKNOWNCAT = "שגיאה! סוג ציון לא קיים!"
    GRADEOUTOFRANGE = "שגיאה! ציון הוא מספר בין 1 ל-6!"
    ARACHIMOUTOFRANGE = "שגיאה! ציון בציר הערכי הוא מספר בין 1 ל-3!"

    def __init__(self, etype, *case):
        if case:
            super().__init__(f"{etype} [{case[0]}]")
        else:
            super().__init__(etype)


def floatable(i):
    try:
        float(i)
        return True
    except ValueError:
        return False


def check_axis(table):
    """
    A function for checking the axes of program's axes in the table.
    :param table: the data table to be checked
    :return: if there's an error- a message to the use. If everything is fine- None
    """
    axes = [table.rows[1].cells[i].text for i in range(1, len(table.rows[0].cells))]
    cats = [table.rows[2].cells[i].text for i in range(1, len(table.rows[0].cells))]

    for ax in axes:
        if ax not in AXES:
            return f"{SkiraPresubmitError.AXESERROR}  [{ax}]"

    for cat in cats:
        index = cats.index(cat)
        if cat not in ALLCATS:
            return f"{SkiraPresubmitError.UNKNOWNCAT}  [{cat}]"
        if cat not in CATEGORIES[axes[index]]:
            return f"{SkiraPresubmitError.CATAXESFORMATION}  [{cat}]"


def check_tables(table):
    """
    A function for checking the actual grades in the table
    :param table: the table to be checked
    :return: if there's an error- a message to the use. If everything is fine- None
    """
    rows = table.rows[3:]

    for row in rows:
        for i, cell in enumerate(row.cells[1:]):
            print("PLATFORM",row.cells[0].text, row.cells[0].text == "הערכה - סטיית תקן")
            if cell.text != '' and not floatable(cell.text):
                return f"{SkiraPresubmitError.INTGRADE}  [{cell.text}]"
            if (cell.text != '') and (not 1 <= float(cell.text) <= 6) and (row.cells[0].text != "הערכה - סטיית תקן"):
                return f"{SkiraPresubmitError.GRADEOUTOFRANGE}  [{cell.text}] hi"

            if table.rows[1].cells[i+1].text == "ערכים":
                #print(cell.text)
                if (cell.text != '') and (not 1 <= float(cell.text) <= 3) and (row.cells[0].text != "הערכה - סטיית "
                                                                                                    "תקן"):
                    return f"{SkiraPresubmitError.ARACHIMOUTOFRANGE}  [{cell.text}] hi2"

    return check_axis(table)


def basic_processing(name, year, sem, file):
    """
    A function for checking the basic parameters of the file, and finding the grades' tables.
    The excessive parameters are for implementing tests for the other parameters, such as comparing them to those
    found in the file
    :param name: cadet's name
    :param year: year of uploaded doc
    :param sem: sem of uploaded doc
    :param file: the actual file data
    :return: the final presubmit result
    """

    if not (file.endswith(".docx") or file.endswith(".docm")) and not file.endswith(".docm"):
        return SkiraPresubmitError.EXTENSION
    doc = docx_for_docm.Document(file)
    try:
        doc = docx_for_docm.Document(file)
    except:
        return SkiraPresubmitError.EXTENSION

    tabs = doc.tables
    our_tables = []
    for table in tabs:
        print(type(table.rows[0].cells[0].text), table.rows[0].cells[0].text)
        if FLAG in table.rows[0].cells[0].text:
            our_tables.append(table)

    if not our_tables:
        return SkiraPresubmitError.NOTABLES

    for tab in our_tables:
        rez = check_tables(tab)
        if rez:
            return rez


def get_file():
    """
    A function for tests on the presubmit code. It allows the debugger to choose a local file to run the presubmit on
    """
    root = tk.Tk()
    root.withdraw()
    file = filedialog.askopenfilename()
    name, year, sem, file = "עידו עברי", 2022, "A", file
    basic_processing(name, year, sem, file)


if __name__ == '__main__':
    get_file()
