אם אתם לא חלק מצוות התשתית של הבוט, **דף זה לא רלוונטי עבורכם**.

כאן אנחנו הולכים לתעד איך השרת שלנו בנוי. לקרוא דף זה חשוב במיוחד לפני מעבר לשרת אחר, לפני שמתקנים באג שקורה רק בשרת. 

## מה יש בשרת?

*  את מסד הנתונים: תוכנה בשם `mongodb`
*  את הבוט עצמו: סקריפט `python`.

כמה דברים שחשוב לדעת על אופן הפעולה של התוכנות האלו:

1. שני התוכנות מוגדרות כservices של systemd - בשם talpibot-bot ו- talpibot-mongodb. זה אומר שאפשר להפעיל\לכבות\לראות את הסטטוס באמצעות הפקודה הפשוטה: ```sudo systemctl start/stop/status talpibot-bot```.
2. שני התוכנות האלו רצות כל אחת ב`container` משלהן - שמאפשר להעבירן במהירות משרת אחד לשרת אחר, ותכונות נוספות. התוכנה שיכולה ליצור, להפעיל ולכבות את ה`container`ים נקראת `docker`. מוזמנים לקרוא עליה עוד [כאן](https://docs.docker.com/get-started/overview/). 

## מבנה התיקיות בשרת
```
TalpiBot\
|---Bot\
|   |---config\
|   |---install\
|   |---install.sh
|   |---docker-compose.yml     
|---MongoDB\
|   |---data\
|   |---install\
|   |---install.sh
|   |---docker-compose.yml
```

*  תיקיית הBot:
*  תיקיית הMongoDB: 





# הDB של TalpiBot - למחוק מכאן
 
הDB של TalpiBot הוא מסוג NoSql MongoDB. אם אתם לא יודעים מה זה אומר, זה לא כזה חשוב. מה שכדאי להבין זה ההיררכיה של הDB. אובייקטים בDB נקראים Documents, למשל לכל חניך בתלפיות יש Document עם שם, פלאפון, יום הולדת ופרטים נוספים. 

אובייקטים מאוחסנים בתוך אוספים (Collection). למשל, כל Document למשתמש נמצא בתוך האוסף "users_info".

אוספים מאוחסנים בתוך מסדי נתונים (Database). לכל פיצ'ר יש Database משלו, בנוסף לDatabase הראשי של Talpibot. לכם בתור כותבי פיצ'ר יש גישת קריאה לDatabase הראשי (main) וגישת קריאה וכתיבה לDatabase האישי של הפיצ'ר שלכם.



הגדרת שדה היא במבנה הבא:

```python

field_name: field_python_type = MongoFieldType()

```
| פרמטר | הסבר |
| ------ | ------ |
| field_name | the name of the field (i.e 'participents') |
| field_python_type| the type the field will have in python (i.e list of User objects) | 
| MongoFieldType | the type the field will have in the database (for a list of fields, [click here](http://docs.mongoengine.org/guide/defining-documents.html#fields)) | 



</div>