בדף הזה נבין איך פועל אחד מהפיצ'רים הבסיסיים שיש לבוט שלנו להציע - ARP.
אם אתם עומדים לכתוב את הפיצ'ר הראשון ועדיין לא לגמרי סגורים איך זה קורה, הדף הזה הוא 
כנראה בשבילכם.

# הקוד

הקוד כולו - כולל imports ותיעוד - מונה כמה עשרות שורות. בסוף יש לנו פחות מ-20 שורות בעלות משמעות.

### המבנה

כל פיצ'ר ממומש בתור class שיורש מהמחלקה BotFeature. יש כמה מתודות שהפיצ'ר יירש מהמחלקה הזו ושהוא חייב להביא להן מימוש משלו. אף פעם לא תצטרכו לקרוא לפונקציות האלו בעצמכם (אבל כמובן שתוכלו אם תרצו) - חלקים אחרים בבוט כן יקראו להן. ככה זה נראה ב-ARP:
(כדי לצמצם במקום לא מופיעים כאן כל ה-imports, התיעוד והמימוש של main)

```python
from BotAPI.Feature.bot_feature import BotFeature
...

class ARP(BotFeature):

    def __init__(self, ui: UI):
        super().__init__(ui)
    
    def get_command(self) -> str:
        return "arp"

    def get_summarize_views(self, session: Session) -> [View]:
        return []

    def is_authorized(self, user: User) -> bool:
        return "מתלם" in user.role

    def main(self, session: Session) -> None:
        ...
```

<div dir="rtl" align="right">

נעבור על כל מה שאנחנו רואים כאן:

* `class ARP(BotFeature)` זו פשוט ההכרזה על המחלקה, ועל כך שהיא יורשת מ-`BotFeature`. אותה השורה תופיע בקוד שלכם, חוץ משם הפיצ'ר ARP. 

* הבנאי `__init__` כאן לא מוסיף כלום לבנאי של `BotFeature`. אתם אף פעם לא תצטרכו לקרוא לבנאי הזה בעצמכם! הבוט יוצר בעצמו אובייקט של הפיצ'ר שלכם כשהוא מתחיל לרוץ.

* הפונקציה `get_command` פשוט מחזירה את השם של הפיצ'ר.

* המתודה `get_summarize_views` מחזירה את מה שתרצו להציג למשתמש כשהפיצ'ר מסיים לרוץ. ספציפית כאן אנחנו לא מחזירים כלום, אבל איך אפשר לעשות את זה בכל זאת?
    - המתודה מקבלת אובייקט `session` כארגומנט (נזכיר שאתם לא צריכים לקרוא למתודה ולא צריכים ליצור את האובייקט, חלקים אחרים בבוט יקראו לה ויעבירו לה את הארגומנט הזה). האובייקט מכיל מידע שיכול להיות שימושי למימוש שלכם, כמו פרטים על המשתמש שאיתו הבוט מדבר - ניתן למצוא תיעוד שלו [כאן](Using the main DB/).
    - המתודה מחזירה מערך של אובייקטי `View`. ניתן לקרוא עליהם [כאן](Using Telegram UI#אובייקטי View).

* הפונקציה `is_authorized` מקבלת משתמש (אובייקט `User`) וצריכה להחזיר האם יש לו הרשאה להשתמש בפיצ'ר.

* הפונקציה `main` היא הפונקצייה שנקראת כאשר משתמש מתחיל את הפיצ'ר. כאן הלוגיקה של הפיצ'ר שלכם מתחילה.

</div>

### הלוגיקה

זה בעצם המח של הפיצ'ר. מומלץ לקרוא את התיעוד של ה-[UI](Using Telegram UI) לפני שניגשים לקוד הזה.

```python
    def main(self, session: Session) -> None:
        self.ui.create_text_view(session, "את מי לחפש?").draw()
        self.ui.get_text(session, self.got_name_from_user)

    def got_name_from_user(self, session: Session, name: str) -> None:
        users = User.objects

        data = {}
        for user in users:
            data[user.name] = user

        def try_again(s: Session) -> None:
            self.ui.clear(s)
            self.main(s)

        self.ui.create_closest_name_view(session, data, name, 5, lambda s, u: self.button_pressed(s, u), try_again).draw()

    def button_pressed(self, session: Session, user: User) -> None:
        self.ui.clear(session)
        self.ui.summarize_and_close(session, [self.ui.create_contact_view(session, user.name, user.phone_number, user.email)])
```

<div dir="rtl" align="right">

מה אנחנו רואים כאן?

* המתודה `main`, שנקראת ברגע שמשתמש מתחיל את הפיצ'ר, בסך הכל מבקשת מהמשתמש הודעת קלט. ברגע שהמשתמש ישלח הודעה בחזרה, התוכן שלה יועבר (כ-`str` למתודה `got_name_from_user`).

* המתודה `got_name_from_user` **להשלים**

* המתודה `button_pressed` מוחקת את כל ההודעות שהפיצ'ר שלח עד כה, ולאחר מכן מסיימת את הריצה של הפיצ'ר ושולחת הודעת סיכום באמצעות `ui.summarize_and_close` (מומלץ להסתכל בתיעוד שלה). הודעת הסיכום היא הודעה אחת מסוג `ContactView`.

</div>