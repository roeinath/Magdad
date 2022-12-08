# רציונל
לכל פיצ׳ר הולכים להיות כנראה טוקנים ושאר מידע רגיש שרלוונטי רק אליו. לדוגמה לכל אחד מכם יש טוקן לבוט האישי שלו. כדי לאפשר גישה נוחה למידע הזה נשתמש במחלקה `Vault` בתיקייה `TalpiBotSystem`.

# מבנה
המחלקה תומכת בשני סוגים של credentials: 
1. טוקן
2. שם משתמש וסיסמה

המידע נשמר בקובץ credentials.yaml שבתיקייה הראשית שלכם. המידע שבו לא אמור לעלות בחזרה לגיט. אם בכל זאת יש בעיה, והגיט שלכם רוצה להעלות אותו לשרת, כתבו את הפקודה הבאה:
```bash
git update-index --assume-unchanged credentials.yaml
```

# שימוש
המחלקה היא `singleton`, ולכן אין צורך ליצור אובייקט שלה. כדי לגשת אליה נכתוב `Vault.get_vault()`.

דוגמאת קוד:
```python
from TalpiBotSytem import Vault, UserPassCredentials

# Get the bot token
bot_token = Vault.get_vault().get_bot_token()

# Get custom token
custom_token = Vault.get_vault().get_token("TOKEN_KEY")

# Get user/pass credentials
# creds is of type UserPassCredentials
creds: UserPassCredentials = Vault.get_vault().get_user_pass('DB_READ_ONLY_ACCESS') 

# Or
username, password = Vault.get_vault().get_user_pass('DB_READ_ONLY_ACCESS') 
```

