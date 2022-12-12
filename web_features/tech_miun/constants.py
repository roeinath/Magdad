import os

LOCAL_DIR = os.path.abspath(os.path.dirname(__file__))
RESPONSES_DIR = os.path.join(LOCAL_DIR, 'responses_files')
MASTERS_DIR = os.path.join(LOCAL_DIR, 'master_files')

CREDS_FILENAME = 'internal-gsheets-creds.json'

SURVEY_NAME_DICT_KEY = "survey_name"
LINK_DICT_KEY = "link"
MASTER_FILE_DICT_KEY = "master_file"
RESULT_FILE_DICT_KEY = "result_file"
MASTER_URL_DICT_KEY = "master_url"
HEBREW_NAME_DICT_KEY = "hebrew_name"


SOLUTION_SURVEY = {
    SURVEY_NAME_DICT_KEY: "SOLUTIONS",
    LINK_DICT_KEY: "https://docs.google.com/forms/d/e/1FAIpQLSfjQ2PdB1p40E0LZHEQYhHTmXShQSki5g6hdQ-yuM2kKe9dZA/viewform?usp=pp_url&entry.751990674=<ESTIMATOR_NAME>&entry.691454428=<ESTIMATOR_MAIL>&entry.1523634118=<TEAM_NUMBER>&entry.206=<MALSHAB_NAME>&entry.1190630109=<MALSHAB_SERIAL_NUMBER>",
    MASTER_FILE_DICT_KEY: 'solution_master.csv',
    RESULT_FILE_DICT_KEY: 'Solution - Responses',
    MASTER_URL_DICT_KEY: r"https://docs.google.com/spreadsheets/d/1baCABSclpI7eiGVgAhqT_eyDr7fnAOFBjQFn0dgRwbc/edit",
    HEBREW_NAME_DICT_KEY: "סולושן"
                   }

CHAKAB_SURVEY = {
    SURVEY_NAME_DICT_KEY: "HACKAB",
    LINK_DICT_KEY: "https://docs.google.com/forms/d/e/1FAIpQLSeblAHPcLIV-89-J7df2zEnWGuDLX765mjFUKt_5GUnQ-V_GA/viewform?usp=pp_url&entry.751990674=<ESTIMATOR_NAME>&entry.983971753=<ESTIMATOR_MAIL>&entry.1523634118=<TEAM_NUMBER>&entry.206=<MALSHAB_NAME>&entry.1799172708=<MALSHAB_SERIAL_NUMBER>",
    MASTER_FILE_DICT_KEY: 'hackab_master.csv',
    RESULT_FILE_DICT_KEY: 'Hackab - Responses',
    MASTER_URL_DICT_KEY: r"https://docs.google.com/spreadsheets/d/1BmgiUSOjleRCqULxW77iSp-I0GZgKHfil6GG-GLPAyc/edit",
    HEBREW_NAME_DICT_KEY: 'חק"ב'
                 }

QA_SURVEY = {
    SURVEY_NAME_DICT_KEY: "QA",
    LINK_DICT_KEY: "https://docs.google.com/forms/d/e/1FAIpQLSckLEN9XOpcf8ynKZqESUVciDmUTe9RakkAo2WbxnQrMQxCtQ/viewform?usp=pp_url&entry.751990674=<ESTIMATOR_NAME>&entry.691454428=<ESTIMATOR_MAIL>&entry.1523634118=<TEAM_NUMBER>&entry.206=<MALSHAB_NAME>&entry.1190630109=<MALSHAB_SERIAL_NUMBER>",
    MASTER_FILE_DICT_KEY: 'QA_master.csv',
    RESULT_FILE_DICT_KEY: 'QA - Responses',
    MASTER_URL_DICT_KEY: r"https://docs.google.com/spreadsheets/d/1QYFtdjLh0dXvik1UmCvT-U_Xs_7K94lCGP4-VFdhsYw/edit",
    HEBREW_NAME_DICT_KEY: "QA"
}

BEHAVIOR_DIAGNOSTICIAN_PLANNING_SURVEY = {
    SURVEY_NAME_DICT_KEY: "PLANNING",
    LINK_DICT_KEY: " https://docs.google.com/forms/d/e/1FAIpQLSel5h6BY_tQnQzn197eIORJLEksSJTYPZyDsMO-FghTy-LfeA/viewform?usp=pp_url&entry.751990674=<ESTIMATOR_NAME>&entry.691454428=<ESTIMATOR_MAIL>&entry.1523634118=<TEAM_NUMBER>&entry.206=<MALSHAB_NAME>&entry.1190630109=<MALSHAB_SERIAL_NUMBER>",
    MASTER_FILE_DICT_KEY: 'behaviour_planning_master.csv',
    RESULT_FILE_DICT_KEY: 'Behaviour Planning - Responses',
    MASTER_URL_DICT_KEY: "https://docs.google.com/spreadsheets/d/1c4TIW0ImU9IDKC0Ok7LjUJeRJNc2kRpAkHDJWEVNm3k/edit#gid=342675263",
    HEBREW_NAME_DICT_KEY: "מבחן תכנון"
             }

BEHAVIOR_DIAGNOSTICIAN_LAW_SURVEY = {
    SURVEY_NAME_DICT_KEY: "LAW",
    LINK_DICT_KEY: "https://docs.google.com/forms/d/e/1FAIpQLSdVfiFVR-pFHyk3DSintOM7vp1xYwLQ69N8LlX_euWOmg5hVg/viewform?usp=pp_url&entry.751990674=<ESTIMATOR_NAME>&entry.691454428=<ESTIMATOR_MAIL>&entry.1523634118=<TEAM_NUMBER>&entry.206=<MALSHAB_NAME>&entry.1190630109=<MALSHAB_SERIAL_NUMBER>",
    MASTER_FILE_DICT_KEY: 'behaviour_law_master.csv',
    RESULT_FILE_DICT_KEY: 'Behaviour Law - Responses',
    MASTER_URL_DICT_KEY: "https://docs.google.com/spreadsheets/d/1fJmL0uYL1q4GYGl4LJ5LuOK4ePbTMMgF0LM93NWocgo/edit#gid=342675263",
    HEBREW_NAME_DICT_KEY: "מבחן הצעת חוק"
             }

SAGAB_SURVEY = {
    SURVEY_NAME_DICT_KEY: "SAGAB",
    LINK_DICT_KEY: "https://docs.google.com/forms/d/e/1FAIpQLSd4-pUna1OVwvR_uCp0sMNS08H8_wbXRKMDYX1ENeBACsBuwQ/viewform?usp=pp_url&entry.751990674=<ESTIMATOR_NAME>&entry.691454428=<ESTIMATOR_MAIL>&entry.1523634118=<TEAM_NUMBER>&entry.206=<MALSHAB_NAME>&entry.1190630109=<MALSHAB_SERIAL_NUMBER>",
    MASTER_FILE_DICT_KEY: "sagab_master.csv",
    RESULT_FILE_DICT_KEY: "Sagab Planning - Responses",
    MASTER_URL_DICT_KEY:   "https://docs.google.com/spreadsheets/d/1tizwXe6L06wsntgMZA5wwX1UCvPwlFwkupvRnafoScs/edit",
    HEBREW_NAME_DICT_KEY: 'סג"ב'
             }

SURVEY_LIST_ESTIMATOR = [SOLUTION_SURVEY, CHAKAB_SURVEY]
SURVEY_LIST_SAGAB = [SAGAB_SURVEY]
SURVEY_LIST_BEHAVIOR_DIAGNOSTICIAN = [BEHAVIOR_DIAGNOSTICIAN_LAW_SURVEY, BEHAVIOR_DIAGNOSTICIAN_PLANNING_SURVEY]
SURVEY_LIST_ALL = SURVEY_LIST_ESTIMATOR + SURVEY_LIST_SAGAB + SURVEY_LIST_BEHAVIOR_DIAGNOSTICIAN + [QA_SURVEY]
