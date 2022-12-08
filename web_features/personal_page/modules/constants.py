from web_framework.server_side.infastructure.constants import *

mahzor_number_to_name = {44: "מחזור מד", 43: "מחזור מג", 42: "מחזור מב", 41: "מחזור מא"}
mahzor_name_to_number = {name: num for num, name in mahzor_number_to_name.items()}

mahzor_number_to_years = {43: [2022, 2023, 2024], 42: [2021, 2022, 2023], 41: [2020, 2021, 2022]}

mahzor_num_to_letters = {43: "מג", 42: "מב", 41: "מא"}
# This translates the above to {"מא":"41" ,"מב":"42" ,"מג":"43"} (example.. next year it would include 44)
mahzor_numstr_to_letters = {str(num): letters for num, letters in mahzor_num_to_letters.items()}

CURRENT_SAGAZ = 42  # int

GROUP_DATA_AUTHORIZED = ["יובל חבר", "יובל גת", "עומר ישראלי", "אלון קגן", "יותם אורן", "תומר סבן", "אייל מילר",
                         "שי גדות", "יובל יעקבי", "דן ישראל יפה", "עדי כהן", "ליאור סימיונוביץ", "אלכסיי שפובלוב",
                         "רן שיקלר", "אושר אלינגר",
                         "ענבר ארן"]  # patch for katzhams and katzhachs, need to add role for User TODO: change to a better solution

classes = {42: ["מחלקת פיץ", "מחלקת קויצקי", "מחלקת קרן"], 43: ["מחלקת גיא", "מחלקת רם", "מחלקת נימי"]}


def sem_index(year, semester, years_list):
    if year == years_list[0]:
        if semester == "A":
            return 0
        else:
            return 1
    if year == years_list[1]:
        if semester == "A":
            return 2
        else:
            return 3
    if year == years_list[2]:
        if semester == "A":
            return 4
        else:
            return 5


def normalize_grades_of_courses(grade):
    if grade >= 95:
        return 6
    if grade >= 92:
        return 5
    if grade >= 87:
        return 4
    if grade >= 83:
        return 3
    if grade >= 80:
        return 2
    if grade > 0:
        return 1
    return 0


def bg_color_of_courses(grade):
    return bg_color_dict[int(normalize_grades_of_courses(grade))]


def normalize_grades(grade, description, platform):
    if platform == STANDARD_DEVIATION:
        if grade <= -1.5:
            return 1
        if -0.7 <= grade < -1.5:
            return 2
        if 0 <= grade < -0.7:
            return 3
        if 0 < grade <= 0.7:
            return 4
        if 0.7 < grade <= 1.5:
            return 5
        else:
            return 6

    if 0 <= grade <= 6:
        if ARACHIM in description and platform != AVG and grade <= 3:
            return 2 * grade
        return grade
    # Grades of 0 -100
    if grade >= 95:
        return 6
    if grade >= 92:
        return 5
    if grade >= 87:
        return 4
    if grade >= 83:
        return 3
    if grade >= 80:
        return 2
    return 1


def platforms_dict_by_semester(platform_dict):
    """
    voodoo magic by Omer Israeli
    """
    platform_dict_by_sem = {}
    for platform, info in platform_dict.items():
        if (info["info"]["year"], info["info"]["semester"]) not in platform_dict_by_sem.keys():
            platform_dict_by_sem[(info["info"]["year"], info["info"]["semester"])] = {}
            platform_dict_by_sem[(info["info"]["year"], info["info"]["semester"])][COUNT] = {"grades": {
            }, "info": {"year": info["info"]["year"], "semester": info["info"]["semester"]}}

            # platform_dict_by_sem[(info["info"]["year"], info["info"]["semester"])][AVG] = {"grades": {
            # }, "info": {"year": info["info"]["year"], "semester": info["info"]["semester"]}}

        platform_dict_by_sem[(info["info"]["year"], info["info"]["semester"])][platform[0]] = info
        for i, (description, grade) in enumerate(info["grades"].items()):
            if description not in platform_dict_by_sem[(info["info"]["year"], info["info"]["semester"])][COUNT][
                "grades"].keys():
                # platform_dict_by_sem[(info["info"]["year"], info["info"]["semester"])][AVG]["grades"][description] = 0
                platform_dict_by_sem[(info["info"]["year"], info["info"]["semester"])][COUNT]["grades"][description] = 0
            # platform_dict_by_sem[(info["info"]["year"], info["info"]["semester"])][AVG]["grades"][description] += \
            #     normalize_grades(grade, description, "")
            if grade != 0:
                platform_dict_by_sem[(info["info"]["year"], info["info"]["semester"])][COUNT]["grades"][
                    description] += 1

    return platform_dict_by_sem


def bg_color_of_grade(grade, description, platform):
    return bg_color_dict[int(normalize_grades(grade, description, platform))]
