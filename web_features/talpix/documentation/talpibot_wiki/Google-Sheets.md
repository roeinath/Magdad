# עבודה עם Google Sheets
ניתן לעבוד עם Google Sheets באמצעות ספריית `ExternalAPIs.GoogleSheets`.
## גישה לSpreadsheet
על מנת לעבוד עם sheet מסויים יש תחילה להשיג את ה-spreadsheet_id שלו. דרך נוחה היא דרך ה-URL של הקובץ:

`https://docs.google.com/spreadsheets/d/***spreadsheet_id***/edit#gid=0`



ניתן לבצע פעולות באמצעות הפונקציות של האובייקט המוחזר ע"י הקריאה `()GoogleSheets.get_instance`. כדי לקרוא לפונקציה זאת, צריך להשתמש ב`with` בצורה הבאה:


```python
with GoogleSheets.get_instance() as gs:
    ... usage of gs ...
```
## פרטי חוברת העבודה והגליון

ניתן לקבל את הפרטים של חוברת העבודה ושל הגליון (ה"כרטיסייה" בחוברת העבודה) באמצעות הפונקציות הבאות:


``` python
gc.get_spreadsheet_details(spreadsheet_id: str)
gc.get_sheet_details(spreadsheet_id: str, sheet_name: str)
```

* `spreadsheet_id` המזהה של חוברת העבודה, אותו משיגים דרך ה-URL

* `sheet_name` שם הגליון (מופיע בכרטיסייה למטה, כברירת מחדל יהיה `Sheet1` או `גליון1`)


## קריאה וכתיבה לטווח בגליון

``` python 
gc.get_range(spreadsheet_id: str, sheet_name: str, range_name: str, major_dimension: str = MAJOR_DIMENSION_ROWS)
gc.set_range(spreadsheet_id: str, sheet_name: str, range_name: str, values: [[str]], value_input_option=VALUE_INPUT_OPTION_USER_ENTERED)
```


* `spreadsheet_id` המזהה של חוברת העבודה, אותו משיגים מה-URL

* `sheet_name` שם הגליון (מופיע בכרטיסייה למטה, כברירת מחדל יהיה `Sheet1` או `גליון1`)

* `range_name` הטווח המבוקש. לסימון מלבן צריך להכניס את שמות הפינה השמאלית־עליונה והפינה הימנית־תחתונה מופרדות בנקודותיים (לדוגמה `A1:D17`). ניתן לסמן גם שורות שלמות או עמודות שלמות (לדוגמה `C:E` או `6:6`).

* `values` הערכים לעדכון בכתיבה

* `major_dimension`, `value_input_option` אפשרויות טכניות לצורת הקלט או הפלט. פירוט בתיעוד של Google.

## דוגמה לשימוש


דוגמה - העתקת טווח התאים `A1:B10` מהגליון `Sheet1` לגליון `Sheet2`:



``` python
from APIs.GoogleSheets import GoogleSheets

sheets = GoogleSheets.get_instance()

data = sheets.get_range(
    "1bO7ZXxMeoh4J4ocZxnyVawm9dH75qBsaCyVojon50Ik",
    "Sheet1",
    "A1:B10"
)

sheets.set_range(
    "1bO7ZXxMeoh4J4ocZxnyVawm9dH75qBsaCyVojon50Ik",
    "Sheet2",
    data,
    "A1:B10"
)
```