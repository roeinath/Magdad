RECOMMANDATIONS = ['מאד מומלץ', 'מומלץ', 'מומלץ בהסתייגות', 'לא מומלץ', "אין מידע"]
STATUSES = ['הוטמע', 'סיים פיתוח', 'סיים ייזום', 'לא סיים ייזום', "אין מידע"]

DEFAULT_DISPLAY_NAMES = {
    "name": "שם",
    "writer": "כותב/י העמוד",
    "rational": "רציונל",
    "children": "דפים תחתיו",
    "parents": "דפים מעליו",
    "delete": "מחק דף זה",
    "last_modified": "תאריך עדכון אחרון",
    "files": "קבצים נוספים",
    "taglist": "רשימת תגיות",
    "page_type": "סוג הדף",
    "audience": "קהל יעד",
    "overall_grade": "ציון כללי",
    "summary": "תקציר",
    "background": "רקע",
    "organizers": "מארגנים",
    "logic_line": "רעיון מסדר",
    "lecturer": "מרצה/ים",
    "calendar_data": "מידע מהקלנדר",
    "lecturer_color": "אפיון המרצה",
    "phone_num": "מס' טלפון",
    "email": "כתובת אימייל",
    "goals": "מטרות ויעדים",
    "lecturer_page": "דף מרצה (מרצה חיצוני, מרצה בוגר התוכנית, ...)",
    "event": "דף אירוע (שבת חזון, משולשת מפגע בודד, ...)",
    "default": "דף מידע כללי",
    "platform": 'דף פלטפורמה (פרויקטון, סמו"פ,...)',
    "topic": "דף ציר (ציר מנהיגות שנה ב', ציר ביטחון שנה א', ...)",
    "lecture": "דף הרצאה (שיחת בוגר, שעת מפקד/ת, ...)",
    "activity": "דף פעילות (פעילות צוות, פעילות פנימית, ...)",
    "year": "דף שער (דף שנה ב', דף מטה ...)",
    "project": 'דף פרויקט (מגד"ד, פרויקטון, ...)',
    "client_page": 'דף לקוח (רלב"ד, משטרה, ...)',
    "recommendation": 'המלצה כמותית ' + f"({', '.join(RECOMMANDATIONS)})",
    "status": 'סטטוס הפרויקט ' + f"({', '.join(STATUSES)})",
    "feedback": 'משוב מילולי',
    "price": "אופן התגמול",
    "budget_id": "מזהה תקציבי (במידה ויש)",
    "logistic_tags": "תגיות לוגיסטיות",
    "content_tags": "תגיות תוכן",
    "bakara_tags": "תגיות בקרה",
    "additional_info": "מידע נוסף",
    "past_lectures": "הרצאות עבר",
    "output_calendar": "ייצא קלנדר בלעדי (פיצ'ר בבנייה)",
    "responsibilities": "תחומי אחריות",
    "core_values": "ערכים מובילים",
    "technologichal": "טכנולוגיות הגוף",
    "good_projects": "טיב הפרויקטים (התכנסות, עניין ואתגר טכנולטוגי, ...)",
    "project_list": "רשימת פרויקטים",
    "contact_details": "פרטי התקשרות נוספים",
    "projectal_tags": "תגיות פרויקטאליות",
    "calendar_id": "מזהה קלנדר (Calendar ID)",
    "drive_dir_id": "מזהה תיקייה (Drive Folder Id)",
    "divider": "מחיצה",
    "client": "לקוח",
    "connection_with_client": "קשר עם הלקוח",
    "conclusions": "מסקנות מרכזיות",
    "search_bar": "חיפוש דפים",
    "control_bar": "ממשק ניהול"

}

PARAGRAPH_TEXTS = [
    "rational", "good_projects", "contact_details", "technologichal", "additional_info",
    "feedback", "lecturer_color", "logic_line", "summary", "background", "connection_with_client"
]

RECOMMENDATION_BG_MAP = {'מאד מומלץ': "#00B050",
                         "מומלץ": "#92D050",
                         "מומלץ בהסתייגות": "#FFFF00",
                         "לא מומלץ": "#FF0000",
                         "אין מידע": "#808080"
                         }

STATUSES_BG_MAP = {'הוטמע': "#00B050",
                   "סיים פיתוח": "#92D050",
                   "סיים ייזום": "#FFFF00",
                   "לא סיים ייזום": "#FF0000",
                   "אין מידע": "#808080"
                   }

PAGE_TYPE_BG_MAP = {
    "lecturer_page": "#524f50",
    "event": "#41557d",
    "default": "#6fadba",
    "platform": '#293954',
    "topic": "#491f0b",
    "lecture": "#581e13",
    "activity": "#7f4e62",
    "year": "#c24423",
    "project": '#d97f6d',
    "client_page": '#38a19c',
}

(
    ALL_ACCESS,
    SHANA_B_ACCESS,
    SAGAZ_ACCESS,
    SAGAB_ACCESS
) = range(4)

(
    ABOVE,
    BELOW,
    NO_BUTTON
) = range(3)




DEFAULT_SAVE_FOLDER_ID = "1VPj9NuOmqM4e68Wz_NpjXqir1aKzDKTn"
ROOT_PARENT_FOLDER_ID = "1UfPpf6li--ureIewyHqMSW38Tge5xmdb"

# This is done for safekeeping
# Had an incident in the past - drive folders are NEVER delted! only manually moved to this
# folder. Total deletion can only be done through drive
DELETED_FOLDERS_DUMP = "1fGJv8tBZUQ7sNHs8BoUY5rA-Q6f9_FYl"

ORGANIZING_INTERVAL = 30
