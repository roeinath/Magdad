import urllib.parse
from web_features.tech_miun.constants import *

PRE_FILlED = {
    "ESTIMATOR_NAME": "<ESTIMATOR_NAME>",
    "MALSHAB_NAME": "<MALSHAB_NAME>",
    "TEAM_NUMBER": "<TEAM_NUMBER>",
    "MALSHAB_SERIAL_NUMBER": "<MALSHAB_SERIAL_NUMBER>",
    "ESTIMATOR_MAIL": "<ESTIMATOR_MAIL>"
}


# TODO: add documentation to class and methods
class ReportSurvey:
    @staticmethod
    def pre_filled_survey(link, estimator, malshab):
        # TODO: change to constancts
        new_link = link.replace(PRE_FILlED["ESTIMATOR_NAME"], ReportSurvey.hebrew_to_url(estimator.name)) \
            .replace(PRE_FILlED["MALSHAB_NAME"], ReportSurvey.hebrew_to_url(malshab.name)) \
            .replace(PRE_FILlED["TEAM_NUMBER"], ReportSurvey.hebrew_to_url(malshab.team)) \
            .replace(PRE_FILlED["MALSHAB_SERIAL_NUMBER"], str(malshab.serial_number)) \
            .replace(PRE_FILlED["ESTIMATOR_MAIL"], str(estimator.email))

        return new_link

    @staticmethod
    def hebrew_to_url(hebrew):
        return urllib.parse.quote(hebrew)

    @staticmethod
    def generate_survey(survey, estimator, malshab):
        survey = {SURVEY_NAME_DICT_KEY: survey[SURVEY_NAME_DICT_KEY],
                  HEBREW_NAME_DICT_KEY: survey[HEBREW_NAME_DICT_KEY],
                  LINK_DICT_KEY: ReportSurvey.pre_filled_survey(survey[LINK_DICT_KEY], estimator, malshab), }
        return survey

    @staticmethod
    def get_surveys():
        return SURVEY_LIST_ALL


def format_link(link):
    FIELD_DIC = {
        "ESTIMATOR_NAME": "<ESTIMATOR_NAME>",
        "MALSHAB_NAME": "<MALSHAB_NAME>",
        "%D7%90": "<TEAM_NUMBER>",
        "MALSHAB_SERIAL_NUMBER": "<MALSHAB_SERIAL_NUMBER>",
        "ESTIMATOR_MAIL": "<ESTIMATOR_MAIL>"
    }
    for key in FIELD_DIC.keys():
        link = link.replace(key, FIELD_DIC[key])

    return link


def main():
    survey_link = [{SURVEY_NAME_DICT_KEY: SOLUTION_SURVEY[SURVEY_NAME_DICT_KEY],
                    LINK_DICT_KEY: "https://docs.google.com/forms/d/e/1FAIpQLSfjQ2PdB1p40E0LZHEQYhHTmXShQSki5g6hdQ-yuM2kKe9dZA/viewform?usp=pp_url&entry.751990674=ESTIMATOR_NAME&entry.691454428=ESTIMATOR_MAIL&entry.1523634118=%D7%90&entry.206=MALSHAB_NAME&entry.1190630109=MALSHAB_SERIAL_NUMBER"
                    },
                   {SURVEY_NAME_DICT_KEY: CHAKAB_SURVEY[SURVEY_NAME_DICT_KEY],
                    LINK_DICT_KEY: "https://docs.google.com/forms/d/e/1FAIpQLSeblAHPcLIV-89-J7df2zEnWGuDLX765mjFUKt_5GUnQ-V_GA/viewform?usp=pp_url&entry.751990674=ESTIMATOR_NAME&entry.983971753=ESTIMATOR_MAIL&entry.1523634118=%D7%90&entry.206=MALSHAB_NAME&entry.1799172708=MALSHAB_SERIAL_NUMBER"
                    },
                   {SURVEY_NAME_DICT_KEY: QA_SURVEY[SURVEY_NAME_DICT_KEY],
                    LINK_DICT_KEY: "https://docs.google.com/forms/d/e/1FAIpQLSckLEN9XOpcf8ynKZqESUVciDmUTe9RakkAo2WbxnQrMQxCtQ/viewform?usp=pp_url&entry.751990674=ESTIMATOR_NAME&entry.691454428=ESTIMATOR_MAIL&entry.1523634118=%D7%90&entry.206=MALSHAB_NAME&entry.1190630109=MALSHAB_SERIAL_NUMBER"
                    },
                   {SURVEY_NAME_DICT_KEY: BEHAVIOR_DIAGNOSTICIAN_PLANNING_SURVEY[SURVEY_NAME_DICT_KEY],
                    LINK_DICT_KEY: "https://docs.google.com/forms/d/e/1FAIpQLSel5h6BY_tQnQzn197eIORJLEksSJTYPZyDsMO-FghTy-LfeA/viewform?usp=pp_url&entry.751990674=ESTIMATOR_NAME&entry.691454428=ESTIMATOR_MAIL&entry.1523634118=%D7%90&entry.206=MALSHAB_NAME&entry.1190630109=MALSHAB_SERIAL_NUMBER"
                    },
                   {SURVEY_NAME_DICT_KEY: BEHAVIOR_DIAGNOSTICIAN_LAW_SURVEY[SURVEY_NAME_DICT_KEY],
                    LINK_DICT_KEY: "https://docs.google.com/forms/d/e/1FAIpQLSdVfiFVR-pFHyk3DSintOM7vp1xYwLQ69N8LlX_euWOmg5hVg/viewform?usp=pp_url&entry.751990674=ESTIMATOR_NAME&entry.691454428=ESTIMATOR_MAIL&entry.1523634118=%D7%90&entry.206=MALSHAB_NAME&entry.1190630109=MALSHAB_SERIAL_NUMBER"
                    },
                   {SURVEY_NAME_DICT_KEY: SAGAB_SURVEY[SURVEY_NAME_DICT_KEY],
                    LINK_DICT_KEY: "https://docs.google.com/forms/d/e/1FAIpQLSd4-pUna1OVwvR_uCp0sMNS08H8_wbXRKMDYX1ENeBACsBuwQ/viewform?usp=pp_url&entry.751990674=ESTIMATOR_NAME&entry.691454428=ESTIMATOR_MAIL&entry.1523634118=%D7%90&entry.206=MALSHAB_NAME&entry.1190630109=MALSHAB_SERIAL_NUMBER"
                    }
                   ]
    for index, link in enumerate(survey_link):
        survey_link[index][LINK_DICT_KEY] = format_link(link[LINK_DICT_KEY])

    for link in survey_link:
        print("for ", link[SURVEY_NAME_DICT_KEY], " survey copy:\n", link[LINK_DICT_KEY])


if __name__ == "__main__":
    main()
