כאן תמצאו את כל הפעולות הבסיסיות בתקשורת של הבוט בטלגרם.

<div dir="rtl" align="right">

[[_TOC_]]

</div>

## אובייקטי View

שליחת הודעה דרך הבוט תתבצע תמיד בשני שלבים. הראשון הוא יצירת אובייקט מסוג View. זהו אובייקט המייצג משהו שמוצג למשתמש. השלב השני הוא שליחת הview למשתמש.

יצירת View נעשית על ידי פעולות יעודיות שקיימות באובייקט self.ui.

לאחר שיצרתם View, שליחה שלו מתבצעת על ידי הפעולה draw.

ניתן לראות דוגמה לכך ב"שליחת הודעת טקסט".

## שליחת הודעות טקסט

יצירת View נעשית על ידי פעולות יעודיות שקיימות באובייקט self.ui. למשל, יצירת הודעת טקסט תתבצע על ידי השורה הבאה:


```python
msg = self.ui.create_text_view(session, text)
```

| פרמטר | הסבר |
| ------ | ------ |
| session | אובייקט session הרגיל, הוא תמיד מועבר לכם כפרמטר. |
| text | הטקסט שישלח בהודעה. | 

לאחר שיצרתם View, שליחה שלו מתבצעת על ידי הפעולה draw:

```python
msg.draw()
```

ניתן לכתוב את שתי הפעולות הללו בשורה אחת. למשל, אם היינו רוצים לשלוח את ההודעה "שלום" למשתמש, היינו כותבים:

```python
self.ui.create_text_view(session, "שלום").draw()
```

## שליחת קבוצת כפתורים

קבוצת כפתורים היא תצוגה של הודעה ומתחתיה כפתורים. יש לכם שליטה על מה יקרה כאשר כל כפתור נלחץ.

יצירת view של קבוצת כפתורים (או כפתור) ואז הציור שלה תתבצע באופן הבא:

```python 
msg = self.ui.create_button_group_view(session, text, buttons)
msg.draw()
```

| פרמטר | הסבר |
| ------ | ------ |
| session | אובייקט session הרגיל, הוא תמיד מועבר לכם כפרמטר. |
| text | הטקסט של ההודעה שהכפתורים ישלחו עליה. | 
| buttons | מערך של אובייקטים שנוצרו על ידי self.ui.create_button_view. | 

יצירת כפתורים למערך buttons מתבצעת על ידי הפעולה self.ui.create_button_view:

```python
self.ui.create_button_view(title, func_to_call)
```

| פרמטר | הסבר |
| ------ | ------ |
| func_to_call | הפונקציה שתיקרא כאשר המשתמש ילחץ על הכפתור. היא פונקציה עם פרמטר יחיד session שתיקרא כאשר משתמש ילחץ על הכפתור. היא יכולה להיות lambda. |
| title | הטקסט שיוצג על גבי הכפתור |

למשל, הקוד הבא לקוח מתוך הקוד של פיצ'ר עדכוני קורונה. הוא שולח קבוצת כפתורים ששואלת האם המשתמש רוצה לקבל מידע על כל המדינות או על מדינה ספציפית. 

```python
buttons = []
buttons.append(self.ui.create_button_view("מידע על כל המדינות יחדיו:", self.print_all_country_data))
buttons.append(self.ui.create_button_view("בחר מדינה ספציפית", self.get_specific_country_name))

self.ui.create_button_group_view(session, "מה ברצונך לראות?", buttons).draw()
```
מה אם אנחנו רוצים להעביר עוד מידע בלחיצת כפתור, למשל שם המדינה שנלחצה? במקרה כזה יש להשתמש בlambda. מחביאים את המידע הנוסף שרוצים להעביר לפונקציה בתוך lambda שמקבלת רק session כמו שצריך.
למשל, אם היינו רוצים שget_specific_country_name יקבל גם את המדינה שעליה רוצים לקבל מידע, היינו משתמשים בlambda באופן הבא:

```python
buttons = []
buttons.append(self.ui.create_button_view("מידע על גרמניה", lambda s: self.get_specific_country_name(s, "germany")))
buttons.append(self.ui.create_button_view("מידע על ישראל", lambda s: self.get_specific_country_name(s, "israel")))

self.ui.create_button_group_view(session, "מה ברצונך לראות?", buttons).draw()
```

שימו לב שבמקרה זה הlambda היא עדיין פונקציה שמקבלת רק session, אבל היא קוראת לפונקציה שמקבלת עוד פרמטרים.

חשוב לציין! היצירה ושליחה של כפתור לא עוצרים את הרצת הפיצ'ר שלכם. למשל הקוד הבא לא יעבוד:

```python
buttons = []
buttons.append(self.ui.create_button_view("מידע על גרמניה", lambda s: self.print_all_country_data(s, "germany")))
buttons.append(self.ui.create_button_view("מידע על ישראל", lambda s: self.get_specific_country_name(s, "israel")))

self.ui.create_button_group_view(session, "מה ברצונך לראות?", buttons).draw()
self.ui.create_text_view(session, "לחצת על כפתור!").draw()
```
הודעת הטקטס "לחצת על כפתור" תישלח מיד לאחר שליחת הכפתורים, היא לא תחכה למשתמש שילחץ על כפתור! על מנת שמשהו יקרה רק לאחר לחיצה על כפתור, הקוד צריך להיות בפונקציה נפרדת בcallback של הכפתורים, כמו שהודגם קודם.
## שליחת תמונה

יצירת הודעת תמונה תתבצע על ידי השורה הבאה:

```python
msg = self.ui.create_image_view(session, title, img_src)
```

| פרמטר | הסבר |
| ------ | ------ |
| session | אובייקט session הרגיל, הוא תמיד מועבר לכם כפרמטר. |
| title | הטקסט שישלח מתחת לתמונה כתיאור | 
| img_src | המיקום של התמונה. הוא צריך להיות פשוט השם של התמונה כולל הסייומת. | 


```python

self.ui.create_image_view(session, "תפוח", "apple.png").draw()

```

## קבלת מידע על לחיצת כפתור

על מנת לעשות משהו כשלוחצים על כפתור, יש לממש את הפונקציה שהעברתם בfunc_to_call. למשל, בדוגמה מהפרק "שליחת קבוצת כפתורים":

```python
def main(self, session: Session):
    buttons = []
    buttons.append(self.ui.create_button_view("מידע על גרמניה", lambda s: self.get_specific_country_data(s, "germany")))
    buttons.append(self.ui.create_button_view("מידע על ישראל", lambda s: self.get_specific_country_data(s, "israel")))

    self.ui.create_button_group_view(session, "מה ברצונך לראות?", buttons).draw()

def get_specific_country_data(self, session: Session, country: str):
    data = self.data[country]
    self.ui.create_text_view(session, data).draw() 

```
שימו לב ששני הכפתורים קוראים לפונקציה get_specific_country_data, אבל עם פרמטר אחר, שמועבר על ידי הלמבדה. כשהמשתמש ילחץ על הכפתור שאומר "מידע על גרמניה" הפונקציה תיקרא עם הפרמטר גרמניה, וכנ"ל אם הוא לוחץ על ישראל.


## קבלת טקסט מהמשתמש

קבלת טקסט מהמשתמש מתבצעת על ידי הפעולה self.ui.get_text באופן הבא:

```python

self.ui.get_text(session, func_to_call)

```

| פרמטר | הסבר |
| ------ | ------ |
| session | אובייקט session הרגיל, הוא תמיד מועבר לכם כפרמטר. |
| func_to_call | פונקציה שתיקרא כאשר המשתמש יקליד משהו לבוט. הפונקציה צריכה לקבל session ועוד משתנה text שיכיל את הטקסט שהמשתמש כתב. | 

למשל, אם נרצה שכאשר המשתמש יכתוב משהו, והבוט יענה לו אותו דבר:

```python

self.ui.get_text(session, self.echo_text)

def echo_text(self, session, text):
    self.ui.create_text_view(session, text).draw()

```

הפונקציה func_to_call יכולה להיות lambda.


שימו לב! בדומה לשליחת כפתורים, הקוד שמופיע לאחר draw יתבצע מיד לאחר שהפקודה get_text נקראת, הרצת הקוד לא תיעצר עד קבלת טקטס, היא תמשיך עד הסוף. כדי שמשהו יקרה רק לאחר קבלת טקסט מהמשתמש, הוא חייב להיות בתוך הפונקציה שמועברת בfunc_to_call.
## קבלת תמונה מהמשתמש

קבלת תמונה מהמשתמש מתבצעת על ידי הפעולה self.ui.get_photo באופן הבא:
```python

self.ui.get_photo(session, func_to_call)

```

השימוש זהה לקבלת טקסט מהמשתמש (ראו פרק קודם), רק שהפעם במקום שהפונקציה func_to_call תקבל טקסט שהמשתמש הקליד, היא תקבל תמונה.

התמונה שמוחזרת היא אובייקט מסוג file שאי אפשר לעבוד איתו - צריך להוריד את התמונה עצמה. עושים את זה על ידי file.download. למשל, קטע הקוד הבא יקבל תמונה מהמשתמש וישמור אותו בתור image.png:

```python

def main(self, session: Session):
    self.ui.get_photo(session, self.get_photo)

def get_photo(self, session: Session, photo: telegram.File):
    photo_path = str("image.png")
    photo.download(custom_path=photo_path)

```
