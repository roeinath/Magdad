import pandas as pd
import io
import msoffcrypto


def reach_malshab_excel(path, id):
    """receives the path of the excel's location and the malshab's ID and returns the full path of the
    @:param path - the location of the floder in which the file is saved
            id - the id of the malshab"""
    return path + 'excel_' + id + '.xlsx'


def get_data_from_xl(path, id, password):
    """returns the data from the malshab's information excel
    @:param path - the location of the floder in which the file is saved
            id - the id of the malshab
            password - the password that is required to access the file"""
    # get the path of the file's location
    filename = reach_malshab_excel(path, id)
    # open the password protected excel file
    decrypted_workbook = io.BytesIO()
    with open(filename, 'rb') as file:
        office_file = msoffcrypto.OfficeFile(file)
        office_file.load_key(password=password)
        office_file.decrypt(decrypted_workbook)
    # read the excel file
    df = pd.read_excel(decrypted_workbook)
    columns_list = df.columns.values.tolist()
    xl_list = df.values.tolist()
    # create the list of the personal info
    personal_info = []
    for col in range(1, 15):
        if col == 14:
            # Saves True if the data is כן, and False if it is לא
            if xl_list[2][col] == "כן":
                personal_info.append(True)
            else:
                personal_info.append(False)
            continue
        personal_info.append(xl_list[2][col])
    # create a list that contains the information of all the Shlav_Grades
    data_parameters = []
    malshab_id = xl_list[2][5]
    # default date
    date = "28.12.2021"
    grade_giver = float('nan')

    for col in range(15, len(columns_list)):
        # the parameter's name
        test_name = xl_list[1][col]
        # do not save the parameter's if it is the name of the grade giver
        if not test_name.find('שם ה'):
            continue
        # change the shlav name only when there is a new header in the "שלב" row
        if columns_list[col].find('Unnamed:'):
            shlav = columns_list[col]
        # change the part name only when there is a new header in the "חלק" row
        if not isinstance(xl_list[0][col], float):
            part = xl_list[0][col]
        # numeric garde
        grade_numeric = xl_list[2][col]
        # verbal assessment
        grade_str = xl_list[3][col]
        # change the grade giver's name if necessary
        if not test_name.find('שם ה'):
            grade_giver = xl_list[3][col]
        data_parameters.append([test_name, malshab_id, shlav, part, grade_numeric, grade_str, grade_giver, date])
    return personal_info, data_parameters


#if __name__ == '__main__':
   # print(get_data_from_xl('', '123456799', 'rephreph123'))
