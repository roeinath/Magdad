from bot_framework import *
from APIs.ExternalAPIs import *
from bot_framework.Activity.FormActivity.form_activity import FormActivity
from APIs.TalpiotAPIs import *
from APIs.Database import *
from bot_framework.Feature.bot_feature import BotFeature
from bot_framework.View.view import View
from bot_framework.session import Session
from bot_framework.ui.ui import UI, Button
from APIs.TalpiotAPIs.User.user import User
from bot_features.Shagmach.Order_Equipment.DBModels.DB_equipment import OrderEquipment
from bot_features.Shagmach.Order_Equipment.Logic.order_equipment_form import OrderEquipmentForm
from bot_features.Shagmach.Order_Equipment.Logic.logic import *
INITIAL_STATUS = "מחכה לאישור"
view_update = None


class Order_Equipment(BotFeature):
    # init the class and call to super init - The same for every feature
    def __init__(self, ui: UI):
        super().__init__(ui)

    def main(self, session: Session):
        """
        Called externally when the user starts the feature. The BotManager
        creates a dedicated Session for the user and the feature, and asks
        the feature using this function to send the initial Views to him.
        :param session: Session object
        :return: nothing
        """
        buttons = [
            self.ui.create_button_view("צירוף בקשת ציוד", self.insert_item),
            self.ui.create_button_view("רשימת קניות מחזורית", self.view_list),
            self.ui.create_button_view("פעולות רס\"פ", self.admin_actions),
            self.ui.create_button_view("🔙", lambda s: self.return_to_menu(session))]
        self.ui.create_button_group_view(session, "משיכת ציוד", buttons).draw()


    def insert_item(self, session: Session):
        self.ui.clear(session)
        fv = self.ui.create_form_view(session, OrderEquipmentForm(), "בחר פרטים להזמנה", self.order)
        fv.draw()


    def order(self, session: Session, form_activity: FormActivity, form: OrderEquipmentForm):
        form.validate()
        form_activity.remove()
        product = form.product.value
        quantity = form.quantity.value
        add_order(mahzor=session.user.mahzor, quantity=quantity, product=product, status=INITIAL_STATUS)


    def get_all_orders(self, session: Session):
        orders = get_orders(session.user.mahzor)
        if not orders:
            self.ui.create_text_view(session, "אין הזמנות לבינתיים").draw()
            return None
        return orders


    def view_list(self, session: Session):
        orders = self.get_all_orders(session)
        if orders:
            for order in orders:
                self.ui.create_text_view(session, order).draw()


    def admin_actions(self, session: Session):
        if "רספ" in session.user.role:
            orders = self.get_all_orders(session)
            if orders:
                buttons = []
                for i in range(len(orders)):
                    my_order = orders[i]
                    button = self.create_button(session, my_order, my_order)
                    buttons.append(button)
                if "admin_view" not in session.data:
                    session.data["admin_view"] = self.ui.create_button_group_view(session, "פעולות על כל ההזמנה:", buttons)
                    session.data["admin_view"].draw()
                else:
                    session.data["admin_view"].update("פעולות על כל ההזמנה:", buttons)
            else:
                self.ui.create_text_view(session, "אין הזמנות").draw()
        else:
            self.ui.create_text_view(session, "אינך בעל הרשאה להשתמש בחלק זה").draw()

    def create_button(self, session: Session, text, info):
        button = self.ui.create_button_view(text, lambda s: self.update_status(s, info))
        return button

    def update_status(self, session: Session, order):
        update_status(order, session.user.mahzor)
        self.admin_actions(session)

    def return_to_menu(self, session: Session):
        from bot_features.SystemFeatures.HierarchicalMenu.Code.hierarchical_menu import \
            HierarchicalMenu
        self.ui.clear(session)
        HierarchicalMenu.run_menu(self.ui, session.user)


    def get_summarize_views(self, session: Session) -> [View]:
        """
        Called externally when the BotManager wants to close this feature.
        This function returns an array of views that summarize the current
        status of the session. The array can be empty.
        :param session: Session object
        :return: Array of views summarizing the current feature Status.
        """
        pass

    def is_authorized(self, user: User) -> bool:
        """
        A function to test if a user is authorized to use this feature.
        :param user: the user to test
        :return: True if access should be allowed, false if should be restricted.
        """
        return "מתלם" in user.role

    def get_scheduled_jobs(self) -> [ScheduledJob]:
        jobs = []
        jobs.append(ScheduledJob(lambda: into_excel(), day_of_week=1, hour="9", minute="30"))
        return jobs
