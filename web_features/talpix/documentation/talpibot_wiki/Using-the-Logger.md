# למה להשתמש ב`Logger`?
רוצים להודיע שקרה משהו? משהו משתבש בפיצ'ר שלכם? שווה לציין זאת בלוג של הפרוייקט. ככה תוכלו לדעת בדיוק מה קורה ותוכלו להבין את מהלך העניינים אם פתאום קורים דברים מוזרים. 

בנוסף, ה`Logger` שלנו מציין עוד הרבה מידע מעבר ל`print` רגיל - השעה, הקוד שקרא לו, צבעים וכו'.

**חשוב - `Logger` הוא לא דרך ל`debugging`! תשתמשו ב`breakpoints` כמו בני אדם מתורבתים.**
# איך להשתמש
השימוש בלוגר הוא די פשוט, וממומש במחלקה בשם `TBLogger` אשר נמצאת ב`TalpiBotSystem`.

דוגמאות לשימוש:
```python
From TalpiBotSystem import TBLogger

TBLogger.info('blah blah')
TBLogger.error('blah blah')
TBLogger.success('blah blah')
TBLogger.warning('blah blah')
TBLogger.debug('blah blah')
TBLogger.failure('blah blah')

```
