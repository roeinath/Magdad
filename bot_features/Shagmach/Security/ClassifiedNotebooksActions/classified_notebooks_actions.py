import random

from APIs.TalpiotAPIs import *
from APIs.TalpiotAPIs.ClassifiedNotbooks.classified_notebooks import ClassifiedNotebook
from bot_framework.Feature.bot_feature import BotFeature
from bot_framework.session import Session
from bot_framework.ui.ui import UI

INVALID_ACTION = "פעולה לא חוקית"
WRONG_PASSCODE = "טעות בסיסמה"
NOTEBOOK_DOES_NOT_EXIST = "מחברת לא קיימת במערכת"
NOTEBOOK_ALREADY_EXIST = "מחברת כבר קיימת במערכת"
NOTEBOOK_ALREADY_SIGNED = "מחברת כבר חתומה"
NOTEBOOK_ALREADY_RETURNED = "מחברת כבר הוחזרה"
SUCCESS_MESSAGE = " הושלמה בהצלחה!"


class ClassifiedNotebookAction(BotFeature):
    def __init__(self, ui: UI):
        super().__init__(ui)

    def main(self, session: Session):
        buttons = [
            self.ui.create_button_view("חתימה על מחברת ✍️", lambda s: self.double_check(s, self.pull_notebook)),
            self.ui.create_button_view("החזרת מחברת 🔏", lambda s: self.double_check(s, self.return_notebook)),
            self.ui.create_button_view("הוספת המחברת למערכת➕", lambda s: self.double_check(s, self.add_notebook)),
            self.ui.create_button_view("מחיקת המחברת מהמערכת ❌", lambda s: self.double_check(s, self.delete_notebook)),
            self.ui.create_button_view("🔙 יציאה", self.ui.clear),
        ]
        self.ui.create_button_group_view(session, "פעולות למחברות ב\"מ 📓", buttons).draw()

    def is_authorized(self, user: User) -> bool:
        return "מתלם" in user.role

    def double_check(self, session: Session, call_action: Callable):
        num = str(random.randint(100, 1000))
        self.ui.create_text_view(session, f"כדי לאשר את הפעולה יש לשלוח את המספר {num}").draw()
        self.ui.get_text(session, lambda s, guess: self.finish_action(s, message=call_action(session, num == guess)))

    def finish_action(self, session: Session, message: str):
        text = message if SUCCESS_MESSAGE in message else f"הפעולה נכשלה:\n{message}\nאנא נסו שנית!"
        self.ui.create_text_view(session, text).draw()
        self.main(session)

    @staticmethod
    def pull_notebook(session: Session, is_confirmed: bool) -> str:
        if not is_confirmed:
            return WRONG_PASSCODE
        notebook = ClassifiedNotebook.objects(user=session.user).first()
        if notebook is None:
            return NOTEBOOK_DOES_NOT_EXIST
        if not notebook.is_locked:
            return NOTEBOOK_ALREADY_SIGNED
        notebook.is_locked = False
        notebook.save()
        return "משיכה" + SUCCESS_MESSAGE

    @staticmethod
    def return_notebook(session: Session, is_confirmed: bool) -> str:
        if not is_confirmed:
            return WRONG_PASSCODE
        notebook = ClassifiedNotebook.objects(user=session.user).first()
        if notebook is None:
            return NOTEBOOK_DOES_NOT_EXIST
        if notebook.is_locked:
            return NOTEBOOK_ALREADY_RETURNED
        notebook.is_locked = True
        notebook.save()
        return "החזרה" + SUCCESS_MESSAGE

    @staticmethod
    def add_notebook(session: Session, is_confirmed: bool) -> str:
        if not is_confirmed:
            return WRONG_PASSCODE
        notebook = ClassifiedNotebook.objects(user=session.user).first()
        if notebook is not None:
            return NOTEBOOK_ALREADY_EXIST
        notebook = ClassifiedNotebook(user=session.user, is_locked=True)
        notebook.save()
        return "הוספה" + SUCCESS_MESSAGE

    @staticmethod
    def delete_notebook(session: Session, is_confirmed: bool) -> str:
        if not is_confirmed:
            return WRONG_PASSCODE
        notebook = ClassifiedNotebook.objects(user=session.user).first()
        if notebook is None:
            return NOTEBOOK_DOES_NOT_EXIST
        notebook.delete()
        return "מחיקה" + SUCCESS_MESSAGE
