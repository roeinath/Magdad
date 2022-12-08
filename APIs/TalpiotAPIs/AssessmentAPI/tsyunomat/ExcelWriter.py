import os
import xlsxwriter
from copy import deepcopy

format_table_header_dict = {'font_name': 'Gisha',
                            'bold': True,
                            'border': False,
                            'text_wrap': False,
                            'reading_order': 2,
                            'align': 'center',
                            'valign': 'vcenter',
                            'fg_color': '#6495ED',
                            }

format_table_body_dict = {'font_name': 'Gisha',
                          'bold': False,
                          'border': False,
                          'text_wrap': True,
                          'reading_order': 2,
                          'align': 'center',
                          'valign': 'vcenter',
                          'fg_color': '#87CEEB',
                          'font_size': 8,
                          }

upper_alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
number_to_column_dict = {ord(c) - 64: c for c in upper_alphabet}
e = {26 + ord(c) - 64: 'A' + c for c in upper_alphabet}
f = {52 + ord(c) - 64: 'B' + c for c in upper_alphabet}
g = {78 + ord(c) - 64: 'C' + c for c in upper_alphabet}
number_to_column_dict.update(e)
number_to_column_dict.update(f)
number_to_column_dict.update(g)

class ExcelWriter:

    def __init__(self, team_directory_path, student_name):

        self.file_name = student_name + '.xlsx'
        self.rel_file_path = os.path.join(team_directory_path, self.file_name)

        self.workbook = xlsxwriter.Workbook(self.rel_file_path)

    def save(self, open_file=False):
        # save:
        self.workbook.close()

        if open_file:
            os.system('start ' + self.rel_file_path)

    def color_according_to_grade_moodle(self, worksheet, row, col, grade):

        format_grade_red = self.workbook.add_format({'bg_color': '#FF0000'})
        format_grade_orange = self.workbook.add_format({'bg_color': '#FFA500'})
        format_grade_yellow = self.workbook.add_format({'bg_color': '#FFFF00'})
        format_grade_light_green = self.workbook.add_format({'bg_color': '#92D050'})
        format_grade_green = self.workbook.add_format({'bg_color': '#00B050'})
        format_grade_gray = self.workbook.add_format({'bg_color': '#808080'})

        try:
            grade = int(grade)

        except:
            worksheet.write(row, col, '', format_grade_gray)
            return

        if grade in range(40):
            worksheet.write(row, col, '', format_grade_red)
        elif grade in range(40, 60):
            worksheet.write(row, col, '', format_grade_orange)
        elif grade in range(60, 80):
            worksheet.write(row, col, '', format_grade_yellow)
        elif grade in range(80, 90):
            worksheet.write(row, col, '', format_grade_light_green)
        elif grade in range(90, 200):
            worksheet.write(row, col, '', format_grade_green)
        else:
            worksheet.write(row, col, '', format_grade_gray)

    def color_according_to_grade_final(self, worksheet, row, col, grade):

        format_grade_dict = deepcopy(format_table_body_dict)
        format_grade_dict['fg_color'] = '#d10808'
        format_grade_strong_red1 = self.workbook.add_format(format_grade_dict)
        format_grade_dict['fg_color'] = '#FF0000'
        format_grade_red1 = self.workbook.add_format(format_grade_dict)
        format_grade_dict['fg_color'] = '#FFA500'
        format_grade_orange1 = self.workbook.add_format(format_grade_dict)
        format_grade_dict['fg_color'] = '#FFFF00'
        format_grade_yellow1 = self.workbook.add_format(format_grade_dict)
        format_grade_dict['fg_color'] = '#92D050'
        format_grade_light_green1 = self.workbook.add_format(format_grade_dict)
        format_grade_dict['fg_color'] = '#00B050'
        format_grade_green1 = self.workbook.add_format(format_grade_dict)
        format_grade_dict['fg_color'] = '#808080'
        format_grade_gray1 = self.workbook.add_format(format_grade_dict)

        if str.isnumeric(grade):
            grade = int(grade)
            if grade in range(80):
                worksheet.write_number(row, col, grade, format_grade_strong_red1)
            elif grade in range(80, 84):
                worksheet.write_number(row, col, grade, format_grade_red1)
            elif grade in range(84, 88):
                worksheet.write_number(row, col, grade, format_grade_orange1)
            elif grade in range(88, 93):
                worksheet.write_number(row, col, grade, format_grade_yellow1)
            elif grade in range(93, 96):
                worksheet.write_number(row, col, grade, format_grade_light_green1)
            elif grade in range(96, 200):
                worksheet.write_number(row, col, grade, format_grade_green1)
        else:
            worksheet.write(row, col, grade, format_grade_gray1)

    def write_final_grades(self, all_grades):

        workbook = self.workbook
        worksheet = self.workbook.add_worksheet('Final Grades')
        worksheet.right_to_left()

        format_table_header = workbook.add_format(format_table_header_dict)
        format_table_body = workbook.add_format(format_table_body_dict)

        # keep a list of max lengths for width autofit
        widths = [len('שם הקורס'), len('מספר הקורס'), len('פקולטה'), len('נקודות זכות'), len('שנה'), len('ציון סופי'), len('ציון מועד א'), len('ממוצע קורסי')]

        # write table categories:
        worksheet.write(0, 0, 'שם הקורס', format_table_header)
        worksheet.write(0, 1, 'מספר הקורס', format_table_header)
        worksheet.write(0, 2, 'פקולטה', format_table_header)
        worksheet.write(0, 3, 'נקודות זכות', format_table_header)
        worksheet.write(0, 4, 'שנה', format_table_header)
        worksheet.write(0, 5, 'ציון סופי', format_table_header)
        worksheet.write(0, 6, 'ציון מועד א', format_table_header)
        worksheet.write(0, 7, 'ממוצע קורסי', format_table_header)

        # fill table:
        for row, course in enumerate(all_grades):
            worksheet.write_string(row+1, 0, course['course name'], format_table_body)
            worksheet.write_number(row+1, 1, int(course['course number']), format_table_body)
            worksheet.write_string(row+1, 2, course['faculty'], format_table_body)
            worksheet.write_number(row+1, 3, int(float(course['naz'])), format_table_body)
            worksheet.write_number(row+1, 4, int(course['year']), format_table_body)
            self.color_according_to_grade_final(worksheet, row+1, 5, course['final grade'])
            if 'grade_א' in course:
                self.color_according_to_grade_final(worksheet, row+1, 6, course['grade_א'])
            else:
                self.color_according_to_grade_final(worksheet, row+1, 6, '')
            worksheet.write_string(row+1, 7, course['student mean'], format_table_body)

            widths[0] = max([widths[0], len(course['course name'])])
            widths[1] = max([widths[1], len(course['course number'])])
            widths[2] = max([widths[2], len(course['faculty'])])
            widths[3] = max([widths[3], len(course['naz'])])
            widths[4] = max([widths[4], len(course['year'])])
            widths[5] = max([widths[5], len(course['final grade'])])
            widths[6] = max([widths[6], len(course['final grade'])])
            widths[7] = max([widths[7], len(course['student mean'])])

        # simulate autofit:
        for i in range(7):
            worksheet.set_column(i, i, widths[i])

    def write_moodle_grades(self, all_grades):

        for year, yearly_courses in reversed(all_grades.items()):
            if len(yearly_courses) == 0: continue
            self.write_assignment_grades(year, yearly_courses)

        return

    def write_assignment_grades(self, year, courses_dict):

        workbook = self.workbook
        worksheet = self.workbook.add_worksheet(str(year))
        worksheet.right_to_left()

        format_table_header = workbook.add_format(format_table_header_dict)
        format_table_header_right = workbook.add_format(format_table_header_dict | {'align':'right'})
        format_table_body = workbook.add_format(format_table_body_dict)
        format_between_tables = workbook.add_format({'top': 2, 'bottom': 2})
        format_top_border = workbook.add_format({'top': 2})
        format_left_border = workbook.add_format({'left': 2})

        max_assignment_number = max([len(course['grades']) for course in courses_dict])

        for i, course in enumerate(courses_dict):

            # write first column:
            worksheet.write(5 * i, 0, course['course id'], format_table_header)
            worksheet.write(5 * i + 1, 0, 'שם המטלה', format_table_header)
            worksheet.write(5 * i + 2, 0, 'ציון', format_table_header)
            worksheet.write(5 * i + 3, 0, 'סטטוס', format_table_header)
            if i == len(courses_dict) - 1:
                worksheet.write_row(5 * i + 4, 0, [''] * (max_assignment_number + 1), cell_format=format_top_border)
            else:
                worksheet.write_row(5 * i + 4, 0, [''] * (max_assignment_number + 1), cell_format=format_between_tables)

            # write course names:
            place = 'B' + str(5*i+1) + ':' + number_to_column_dict[max_assignment_number+1] + str(5*i+1)
            worksheet.merge_range(place, course['course name'], format_table_header_right)

            # prepare table body:
            for j in range(1, max_assignment_number + 1):
                for k in range(2):
                    worksheet.write(5 * i + k + 1, j, '', format_table_body)
                self.color_according_to_grade_moodle(worksheet, 5 * i + 3, j, '')

            # write table body:
            assignment_names = sorted(course['grades'].keys(), key=lambda name: course['grades order'][name])
            # print(courses_names)
            for j, name in enumerate(assignment_names):
                grade = course['grades'][name]
                try:
                    grade = int(float(course['grades'][name]))
                except ValueError:
                    pass
                worksheet.write(5 * i + 1, j+1, name, format_table_body)
                worksheet.write(5 * i + 2, j+1, grade, format_table_body)
                self.color_according_to_grade_moodle(worksheet, 5 * i + 3, j+1, grade)

        # set borders:
        for i in range(len(courses_dict)):
            worksheet.write_column(5 * i, max_assignment_number+1, [''] * 4, format_left_border)

        # adjust width:
        worksheet.set_column(0, 0, len("שם המטלה") + 4)

    def write_grades(self, all_moodle_grades, all_final_grades):

        if all_moodle_grades:
            if len(all_moodle_grades) > 0:
                self.write_moodle_grades(all_moodle_grades)

        if all_final_grades:
            if len(all_final_grades) > 0:
                self.write_final_grades(all_final_grades)

        self.save(open_file=False)