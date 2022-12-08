# עבודה על הDB הראשי 
דף זה יפרט לעומק כיצד ניתן לקבל מידע מה-DB הראשי של TalpiBot (בכוונה כתוב רק קריאה - אין לכם אפשרות לערוך את ה-DB הנ"ל, אלא לערוך רק את ה-DB האישי של הפיצ'ר שלכם).
 <div dir="rtl" align="right">

[[_TOC_]]

</div>
## באמצעות ה-API שלנו.
הספרייה של TalpiBot מכילה פונקציות לגישה לאובייקטים נפוצים בDB, בעיקר לעבודה עם משתמשים.

<h2 align="right">קבלת מידע - דוגמא</h2>
<div dir="rtl" align="right">
מילת מפתח בכל הקשור לעבודה עם ה-DB זה Constraint - אילוץ. אנחנו נבנה אילוצים ואז נקבל מערך של אובייקטי user שעליהם יש פירוט מפורט למטה.

לדוגמא, בשביל לקבל את כל ה-users שנמצאים במחזור מ' נכתוב את הקוד הבא (לא להיבהל יהיה הסבר מסובר ישר לאחר מכן)
</div>

`UserConstraint.get_users_with_constraint(MachzorConstraint(40))`

<div dir="rtl" align="right">

* `UserConstraint.get_users_with_constraint` מציין שאתה מעוניין לקבל רשימה של users לפי התנאים שמופיעים בתוך הסוגריים
<br>

* `MachzorConstraint(40)` מציין שאנחנו רוצים לעשות אילוץ על המחזור, והאילוץ הוא שהחניך יהיה במחזור 40 - כלומר מ'<br>
</div>

<h2 align="right">תנאים מורכבים</h2>
<div dir="rtl" align="right">
במידה ואתם רוצים לעשות תנאים מסובכים יותר, אלו הם האופציות שלהם (במידה וחסר לכם משהו, פנו למישהו מצוות הבוט וזה יתווסף):
</div>
<h3 align="right">וגם</h3>
<div dir="rtl" align="right">
בשביל לבצע חיתוך של כמה תנאים:
</div>

```python
const = AndUserConstraint([MachzorConstraint(40), RoleUserConstraint("חנתר")])
UserConstraint.get_users_with_constraint(const)
```

<div dir="rtl" align="right">
נציין שניתן לעשות את זה בשורה אחת
<br>

* `([])AndUserConstraint` מציין שאנחנו מעוניינים לבצע איחוד של תנאים, התנאים יוכנסו לתוך רשימה, לדוגמא במקרה הנ"ל אנחנו רוצים את כל החניכים במחזור מ' שגם חנתרים.
<br>

* `UserConstraint.get_users_with_constraint` מציין שאתה מעוניין לקבל רשימה של users לפי התנאים שמופיעים בתוך הסוגריים
</div>

<h3 align="right">או</h3>
<div dir="rtl" align="right">
בשביל לקבל את כל ה-users שמקיימים אחד מבין מספר תנאים:
</div>

```python
const = OrUserConstraint([MachzorConstraint(40), RoleUserConstraint("חנתר")])
UserConstraint.get_users_with_constraint(const)
```

<div dir="rtl" align="right">
נציין שניתן לעשות את זה בשורה אחת
<br>

* `([])OrUserConstraint` מציין שאנחנו מעוניינים לקבל משהו שמקיים את אחד תנאים, התנאים יוכנסו לתוך רשימה. בדוגמא הנ"ל נקבל את כל החניכים שבמחזור מ' ואת כל החנתרים (גם של מחזורים אחרים)
<br>

* `UserConstraint.get_users_with_constraint` מציין שאתה מעוניין לקבל רשימה של users לפי התנאים שמופיעים בתוך הסוגריים

</div>

<h3 align="right">שלילה</h3>
<div dir="rtl" align="right">
בשביל לקבל את כל ה-users שלא מקיימים את התנאים הנ"ל:
</div>

```python
const = NotUserConstraint(MachzorConstraint(40))
UserConstraint.get_users_with_constraint(const)
```

<div dir="rtl" align="right">
נציין שניתן לעשות את זה בשורה אחת
<br>

* `()NotUserConstraint`  מציין שאנחנו מעוניינים בכל מה שלא מקיים את התנאי (ניתן שהתנאי יהיה בתוך and או or. בדוגמא הנ"ל נקבל את כל החניכים שלא במחזור מ'.
<br>

* `UserConstraint.get_users_with_constraint`  מציין שאתה מעוניין לקבל רשימה של users לפי התנאים שמופיעים בתוך הסוגריים

</div>


<h2 align="right">אילוצים</h2>
<div dir="rtl" align="right">
האילוצים שכרגע קיימים הם (במידה ואתם צריכים אילוץ נוסף, פנו למישהו מצוות הבוט וזה יתווסף):
</div>
<h3 align="right">לפי מחזור</h3>

`MachzorConstraint(40)`

<h3 align="right">לפי תפקיד</h3>

`RoleUserConstraint("שגמח")`

<h3 align="right">לפי שם</h3>

`NameUserConstraint("חניך גנרי")`


<h2 align="right">האובייקט User</h2>
<div dir="rtl" align="right">

שאילתות מה-DB יחזירו רשימה של אובייקטי `User`. תוכלו לקבל מידע על המשתמש המתאים לאובייקט באופן הבא:

| שדה | טיפוס | תיאור |
| :------ | :------ | ------: |
| name | str | השם המלא, כולל שם אמצעי |
| mahzor | int | המחזור של המשתמש כמספר (מחזור כ"ה לדוגמה יופיע כ-25) |
| email | str | כתובת המייל |
| phone_number | str | מספר הטלפון |
| role | List[str] | רשימה של התפקידים של המשתמש - כל תפקיד מיוצג כמחרוזת |

לדוגמה, כדי לקבל את השם המלא של המשתמש `user`, שהוא אובייקט מטיפוס `User`, ניתן להשתמש בשורה הבאה:
</div>

``` python
name = user.name
```


# עבודה ישירות עם ה-DB - לא מומלץ.
אם אתם מעדיפים, אתם יכולים לעבוד ישירות עם ה-DB ללא שימוש ב-API המוצא לכם, הדרך לעשות את זה היא:

על מנת לקבל את אובייקט החיבור ל-DB, ניתן להשתמש בפקודה הבאה:


`volt.get_connection()`

<div dir="rtl" align="right">

הפונקציה תחזיר אובייקט מסוג MongoClient על ה-DB של TalpiBot. 

אפשר למצוא collection ב-DB על ידי חיפוש כמו במילון:

</div>

`users = volt.get_connection()['users_info']`

<div dir="rtl" align="right">

אפשר להוסיף לcollection דברים למשל על ידי insert_one:

</div>

`users.insert_one({name: 'Hanih Generi'})`

<div dir="rtl" align="right">

משתמש בשם "Hanih Generi" יתווסף ל-DB.

אפשר לחפש בcollection דברים למשל על ידי find_one:

</div>

`users.find_one({name: 'Hanih Generi'})`

<div dir="rtl" align="right">

יוחזר אובייקט של חניך ששמו Hanih Generi אם יש כזה.

ניתן למצוא פירוט מלא על כל הפעולות שpymongo תומך בהן [כאן](https://api.mongodb.com/python/current/index.html).

</div>