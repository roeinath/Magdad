import smtplib
from email.header import Header
from email.mime.text import MIMEText

from APIs.TalpiotSystem import TalpiotSettings


class MailClient:
    def __init__(self):
        self.server: smtplib.SMTP_SSL = None
        gmail_settings = TalpiotSettings.get().gmail_settings
        self.user = gmail_settings.username
        self.password = gmail_settings.password

    def connect(self):
        self.server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        self.server.ehlo()
        self.server.login(self.user, self.password)

    def close(self):
        self.server.close()

    def send_mail(self, to, subject, content, text_type="plain"):
        # message = 'Subject: {}\n\n{}'.format(subject, content)
        msg = MIMEText(content, text_type, _charset="UTF-8")
        msg['Subject'] = Header(subject, "utf-8")
        self.server.sendmail(self.user, to, msg.as_string())
