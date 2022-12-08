import numpy
import csv

NAMES = "שם ושם משפחה"
TIME = 'Timestamp'
BLANK_A = "תשובה ריקה"
BLANK_Q = "שאלה ריקה"

def read_form(file_name):
    """
    :param file_name: location of a CSV file of a google forms
    :return: an array of all the data relevant to comparison with db data
             an if an error rises, returns a string explaning the error
    """
    with open(file_name, mode='r', encoding='UTF-8') as file:
        forms_data = [None]
        forms = csv.reader(file)
        forms = list(forms)
        forms = list(map(list, zip(*forms)))

        for col in forms:
            list_check = check_if_not_empty(col[1:])
            if list_check == False or col[0] == TIME:
                continue
            if col[0] == NAMES:
                forms_data[0] = col
            else:
                forms_data.append([x if x != '' else BLANK_Q for x in [col[0]]]+[x if x != '' else BLANK_A for x in col[1:]])

        if not forms_data[0]:
            return f'לא נמצא שאלה עם הכותרת \"{NAMES}\"'
        if len(forms_data) <= 1:
            return "לא נמצאו שאלות בסקר"
        return forms_data



def check_if_not_empty(list):
    list = [value for value in list if value != ""]
    if not list:
        return False
    return list

    # test:
if __name__ == "__main__":
    file_name = "C:\\Users\\t8880316\\Downloads\\RSVP.csv"
    forms = read_form(file_name)
    for i in forms:
        print(i)
