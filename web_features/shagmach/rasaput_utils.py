from APIs.ExternalAPIs.Mail.system_mail_client import MailClient
from APIs.TalpiotAPIs import User
from APIs.TalpiotAPIs.Shagmach.computer_fix_request import ComputerFixRequest2
from web_framework.server_side.infastructure.actions import simple_send_message

emails_to_send_to = [
    "tamampum@gmail.com",
    "lior.simionovici.42@gmail.com"
]

KAMAT_MIHSHUV = "גיא דניאל הדס"


def type_request_as_message(req: ComputerFixRequest2):
    mail_content = "<h3>פרטי התקלה:</h3>"
    mail_content += "נפתחה על ידי: " + str(req.user.name) + "<br>"
    mail_content += "בתאריך: " + req.time.strftime("%d/%m/%Y") + "<br>"
    mail_content += f"בשעה: {req.time.hour}:{req.time.minute}<br>"
    mail_content += "סוג תקלה: " + str(req.fix_type) + "<br>"
    mail_content += "תיאור תקלה: " + str(req.description) + "<br>"
    mail_content += "סיריאלי מחשב: " + str(req.computer_serial) + "<br>"
    mail_content += "האם המחשב שמיש: " + str(req.is_computer_working) + "<br>"
    mail_content += "טלפון של פותח התקלה: " + str(req.user.phone_number) + "<br>"
    status = "" if len(req.statuses) == 0 else str(req.statuses[-1])
    mail_content += "סטטוס: " + status
    return mail_content


def format_message(message: str):
    message = message.replace("<h2>", '')
    strs = ['<h3>', '<br>', '</h3>', '</h2>']
    for s in strs:
        message = message.replace(s, '\n')
    return message


def send_request_in_email(req: ComputerFixRequest2):
    mail_content = "<h2>דווחה תקלת מחשוב חדשה!</h2>"
    mail_content += type_request_as_message(req)

    try:
        client = MailClient()
        client.connect()
        for mail in emails_to_send_to:
            client.send_mail(mail, "תקלת מחשוב חדשה (talpix)", mail_content, text_type="html")
        client.send_mail(req.user.email, "תקלת מחשוב חדשה (talpix)", mail_content, text_type="html")
        client.close()
    except Exception as e:
        simple_send_message(format_message(mail_content), [req.user, User.objects(name=KAMAT_MIHSHUV).first()])


def send_status_in_email(req: ComputerFixRequest2):
    mail_content = "<h2>עודכן סטטוס עבור תקלת המחשוב שלך:" + "<br>" + str(req.statuses[-1]) + "</h2>"
    mail_content += type_request_as_message(req)
    try:
        client = MailClient()
        client.connect()
        client.send_mail(req.user.email, "עודכן סטטוס תקלת המחשוב שלך (talpix)", mail_content, text_type="html")
        client.close()
    except Exception as e:
        simple_send_message(format_message(mail_content), [req.user, User.objects(name=KAMAT_MIHSHUV).first()])


def send_switch_message_in_email(req: ComputerFixRequest2):

    mail_content = "<h2>" + "תקלת המחשוב שלך "
    # Check only after switching the closed state! (in the function switch_computer_fix).
    if req.closed:
        msg = "נפתחה מחדש"
    else:
        msg = "נסגרה"
    mail_content += msg + ":</h2>"
    mail_content += type_request_as_message(req)
    try:
        client = MailClient()
        client.connect()
        client.send_mail(req.user.email, f"תקלת המחשוב שלך {msg} (talpix)", mail_content, text_type="html")
        client.close()
    except:
        simple_send_message(format_message(mail_content), [req.user, User.objects(name=KAMAT_MIHSHUV).first()])


def send_delete_msg_in_email(req: ComputerFixRequest2):
    mail_content = "<h2>תקלת המחשוב שלך נמחקה מהמאגר.</h2>"
    mail_content += "אין דרך לשחזר אותה אך ניתן לדווח על חדשה במידה והיא נמחקה בטעות."
    mail_content += type_request_as_message(req)
    try:
        client = MailClient()
        client.connect()
        client.send_mail("lior.simionovici.42@gmail.com", "תקלת המחשוב הבאה נמחקה (talpix)", mail_content,
                         text_type="html")
        client.send_mail(req.user.email, "תקלת המחשוב שלך נמחקה (talpix)", mail_content, text_type="html")
        client.close()
    except:
        simple_send_message(format_message(mail_content), [req.user, User.objects(name=KAMAT_MIHSHUV).first()])
