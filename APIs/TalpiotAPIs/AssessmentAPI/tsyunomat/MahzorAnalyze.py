import os
import glob
import pandas as pd
from pathlib import Path
from APIs.TalpiotAPIs.AssessmentAPI.tsyunomat.ExcelWriter import format_table_body_dict, format_table_header_dict

def analyze_mahzor(mahzor_directory):

    xlsx_file_name = os.path.join(mahzor_directory, f'Mahzor_summary.xlsx')
    writer = pd.ExcelWriter(xlsx_file_name, engine='xlsxwriter', options={'strings_to_numbers': True})
    
    #set default font to Gisha
    workbook = writer.book
    workbook.formats[0].set_font_name("Gisha")

    #get all student files in the directories
    student_files = glob.glob(os.path.join(mahzor_directory, "*.xlsx"))
    student_files = [x for x in student_files if 'Mahzor_summary.xlsx' not in x]
    
    student_names = [Path(f).stem for f in student_files]
    student_tables = [pd.read_excel(f, usecols=lambda x: 'Unnamed' not in x, sheet_name='Final Grades') for f in student_files]

    #add for each student table a column to all the courses with the name
    for name, table in zip(student_names, student_tables):
        table['שם התלמיד'] = name

    great_student_table = pd.concat(student_tables)

    #drop courses with a non-numeric grade
    great_student_table = great_student_table[pd.to_numeric(great_student_table["ציון סופי"], errors='coerce').notnull()]
    great_student_table["ציון סופי"] = pd.to_numeric(great_student_table["ציון סופי"])
    
    great_student_table.to_excel(writer, sheet_name='ריכוז תלמידים')

    #fit columns to width of dataframe (see documentation of get_col_widths)
    worksheet = writer.sheets['ריכוז תלמידים']
    for i, width in enumerate(get_col_widths(great_student_table)):
        worksheet.set_column(i, i, width)

    course_summary = great_student_table.groupby(['שם הקורס', 'שנה', 'מספר הקורס']).agg({'ציון סופי': ['size', 'mean', 'std', 'median']})
    course_summary['ממוצע כללי'] = great_student_table.groupby(['שם הקורס', 'שנה', 'מספר הקורס'])['ממוצע קורסי'].agg(pd.Series.mode)
    course_summary.columns = ['מספר חניכים', 'ציון ממוצע', 'סטיית תקן', 'ציון חציוני', 'ממוצע כללי']
    course_summary = course_summary.reset_index()
    course_summary = course_summary.sort_values('שנה', ascending=False)
    course_summary.to_excel(writer, sheet_name='ריכוז קורסים')

    #fit columns to width of dataframe (see documentation of get_col_widths)
    worksheet = writer.sheets['ריכוז קורסים']
    for i, width in enumerate(get_col_widths(course_summary)):
        worksheet.set_column(i, i, width)
    
    #find yearA by technoz 1
    technoz1_course = great_student_table[great_student_table['מספר הקורס']==83536]
    if len(technoz1_course) != 0:
        yearB = great_student_table[great_student_table['מספר הקורס']==83536].iloc[0].loc['שנה']
        yearA = yearB - 1
    else:
        yearA = 2021

    great_student_table['_grade_times_weight'] = great_student_table['ציון סופי']*great_student_table['נקודות זכות']
    g = great_student_table.groupby('שם התלמיד')
    students_means = pd.DataFrame()
    students_means['שם התלמיד'] = list(g.groups.keys())
    students_means = students_means.set_index('שם התלמיד')
    students_means['ממוצע'] = (g['_grade_times_weight'].sum() / g['נקודות זכות'].sum()).values
    
    #create average list for each year
    labels_year = ['ממוצע א', 'ממוצע ב', 'ממוצע ג']
    for i in range(3):
        g_year = great_student_table[great_student_table['שנה']==yearA+i].groupby('שם התלמיד')
        if len(g_year) != 0:
            s_year = (g_year['_grade_times_weight'].sum() / g_year['נקודות זכות'].sum()).rename(labels_year[i])
            students_means = students_means.merge(s_year, on='שם התלמיד', how='left')
    
    students_means.to_excel(writer, sheet_name='ממוצעי תלמידים')

    #fit columns to width of dataframe (see documentation of get_col_widths)
    worksheet = writer.sheets['ממוצעי תלמידים']
    for i, width in enumerate(get_col_widths(students_means)):
        worksheet.set_column(i, i, width)

    writer.save()

#get the width of all columns in a dataframe
def get_col_widths(dataframe):
    #taken from: https://stackoverflow.com/questions/29463274/simulate-autofit-column-in-xslxwriter

    # First we find the maximum length of the index column   
    idx_max = max([len(str(s)) for s in dataframe.index.values] + [len(str(dataframe.index.name))])
    # Then, we concatenate this to the max of the lengths of column name and its values for each column, left to right
    return [idx_max] + [max([len(str(s)) for s in dataframe[col].values] + [len(col)]) for col in dataframe.columns]
