import sys
import traceback
from typing import Callable

from bot_framework.ui.ui import UI
import rstr
from bot_framework.session import Session
from APIs.ExternalAPIs.Mail.system_mail_client import MailClient
from APIs.TalpiotSystem import *

CODE_REGEX = r"^[a-zA-Z0-9]{8}$"
ERROR_OCCURRED_USER = "הפיצ'ר נתקל בשגיאה." + "\n" + "שם הפיצ'ר: %s" + "\n" + "מזהה שגיאה:" + " #%s"
ERROR_OCCURRED_ADMIN = "הפיצ'ר נתקל בשגיאה." + "\n" + "שם הפיצ'ר: %s" + "\n" + "מזהה שגיאה:" + " #%s" + "\n" + "השגיאה: ```%s```"
ERROR_OCCURED_ADMIN_HTML = """
<div dir="rtl">
הפיצ'ר נתקל בשגיאה.
<br>
שם הפיצ'ר: %s
<br>
מזהה שגיאה: %s
<br>
השגיאה:
<br>
</div>
<code>
%s
</code>
"""
ERROR_OCCURED_ADMIN_PLAIN_TEXT = """
======================================
הפיצ'ר נתקל בשגיאה.
שם הפיצ'ר: %s
מזהה שגיאה: %s
-------------------
השגיאה:
%s
======================================
"""

try:
    _mail_client = MailClient()
    _mail_client.connect()
except:
    print("Notice: The mail server connection could not be created.", file=sys.stderr)
    _mail_client = None


class ErrorReport:
    """
    Holds information about a Crash of the
    bot. Has option to format the report
    for the user, and for an admin.
    """

    def __init__(self, session: Session, crash_log: str):
        self.report_id: str = rstr.xeger(CODE_REGEX)
        self.session: Session = session
        self.crash_log: str = crash_log

    def get_user_readable_text(self) -> str:
        return ERROR_OCCURRED_USER % (self.session.feature_name, self.report_id)

    def get_admin_readable_text(self) -> str:
        return ERROR_OCCURRED_ADMIN % (self.session.feature_name, self.report_id, self.crash_log)

    def get_admin_html_text(self) -> str:
        return ERROR_OCCURED_ADMIN_HTML % (
            self.session.feature_name,
            self.report_id,
            self.crash_log.replace("\n", "<br>")
        )

    def get_admin_plaintext(self) -> str:
        return ERROR_OCCURED_ADMIN_PLAIN_TEXT % (
            self.session.feature_name,
            self.report_id,
            self.crash_log
        )


def send_report_main_mail(report: ErrorReport):
    return
    try:
        if _mail_client is None:
            print(report.get_admin_plaintext(), file=sys.stderr)
            return

        _mail_client.send_mail(
            "talpibotsystem@gmail.com",
            "EReport #%s - %s" % (report.report_id, report.session.user.name),
            report.get_admin_html_text(),
            text_type="html"
        )
    except:
        pass


def log_all_exceptions(function_to_call: Callable[[], None], session: Session, ui: UI):
    try:
        function_to_call()

    except:
        report = ErrorReport(session, traceback.format_exc())

        #  Send message according to the type of the user
        if session.user is not None and "admin" in session.user.role:
            ui.summarize_and_close(session, [ui.create_text_view(session, report.get_admin_readable_text())])
        else:
            ui.summarize_and_close(session, [ui.create_text_view(session, report.get_user_readable_text())])

        if TalpiotSettings.get().running_mode == TalpiotOperationMode.PRODUCTION:
            upload_report_to_git_issues(report)

        print(f'[-] Got Exception: {report.get_admin_plaintext()}')

    # #  Report the error to the Mail
    # send_report_main_mail(report)


def upload_report_to_git_issues(report):
    try:
        TalpiBotGit.get().create_new_issue(
            issue_object=TalpiBotGitIssue(
                title=f'EReport: {report.report_id}',
                description=report.get_admin_html_text(),
                labels=['ERROR REPORT', report.session.user.name],
                is_closed=True
            )
        )
    except:
        print(f'[-] Cannot upload report to git issues. Report is: {report.get_admin_plaintext()}')
