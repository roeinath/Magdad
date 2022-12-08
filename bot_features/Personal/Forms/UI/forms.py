from APIs.TalpiotAPIs.static_fields import get_mahzor_number_list
from bot_framework import *
from APIs.ExternalAPIs import *
from APIs.TalpiotAPIs import *

import datetime

from bot_features.Personal.Forms.DBModels.form import Form

from bot_framework.Feature.bot_feature import BotFeature
from bot_framework.View.view import View
from bot_framework.session import Session
from bot_framework.ui.ui import UI


class FormHandler(BotFeature):

    # init the class and call to super init - The same for every feature
    def __init__(self, ui: UI):
        super().__init__(ui)

    # Main Menu for the feature
    # Splits into 3 different menus -
    # 1) show forms to fill
    # 2) upload new form
    # 3) edit my forms
    def main(self, session: Session):
        buttons = [
            self.ui.create_button_view(
                "📝 צפייה בטפסים למילוי",
                lambda s: (
                    self.ui.clear(s),
                    self.display_form_list(s)
                )
            ),
            self.ui.create_button_view(
                "📝 העלאת טופס חדש",
                lambda s: (
                    self.ui.clear(s),
                    self.verify_upload_new_form(s)
                )
            ),
            self.ui.create_button_view(
                "📝 עריכת טפסים שהעליתי",
                lambda s: (
                    self.ui.clear(s),
                    self.edit_my_forms(s)
                )
            ),
            self.ui.create_button_view(
                "🔙",
                lambda s: (
                    self.ui.summarize_and_close(s, [
                        self.end_message(s)
                    ])
                )
            )
        ]
        self.ui.create_button_group_view(
            session,
            "ברוכים הבאים למנהל הטפסים שלכם! מה תרצו לעשות?",
            buttons
        ).draw()

    # Default end message for exting up, return text ui
    def end_message(self, session):
        return self.ui.create_text_view(
            session,
            "📢📢📢"
            + "\n\n"
            + "תודה שהשתמשתם במנהל הטפסים!"
            + "\n\n"
            + u"\u200F"
            + "📢📢📢"
        )

    # ---------------------------------------
    # Main callback list for 3) edit my forms
    # ---------------------------------------

    # Displays list of all editable forms
    def edit_my_forms(self, session):
        forms = [
            form for form in Form.objects()
            if form.creator == session.user
        ]
        forms.sort(key=lambda x: x.time)
        forms = forms[::-1]

        if len(forms):
            buttons = [
                          self.ui.create_button_view(
                              "%s: %s" % (form.name, form.time.strftime("%d/%m")),
                              lambda s, form=form: (
                                  self.ui.clear(s),
                                  self.ui.clear(s),
                                  self.edit_single_form(s, form)
                              )
                          )
                          for form in forms
                      ] + [
                          self.ui.create_button_view(
                              "🔙",
                              lambda s: (
                                  self.ui.clear(s),
                                  self.main(s)
                              )
                          )
                      ]

            self.ui.create_button_group_view(
                session,
                "רשימת הטפסים שהעלית לאחרונה:",
                buttons
            ).draw()
        else:
            # finish_msg = self.ui.create_text_view(session, "לא העליתם טפסים עדיין :)")
            # self.ui.summarize_and_close(session, [finish_msg, self.end_message(session)])
            buttons = [
                self.ui.create_button_view(
                    "🔙",
                    lambda s: (
                        self.ui.clear(s),
                        self.main(s)
                    )
                )
            ]
            self.ui.create_button_group_view(
                session,
                "לא העליתם טפסים עדיין :)",
                buttons
            ).draw()

    # Displays list of editable actions on form (delete, see filled)
    def edit_single_form(self, session, form_data):
        summary_text = "❓ סטטוס הטופס:" + "\n\n" + "\n".join([
            "שם הטופס: %s" % form_data["name"],
            "קישור: %s" % form_data["link"],
            "דדליין: %s" % form_data["time"],
            "כמה לא ענו: %s" % len(form_data["not_filled"]),
            "\n"
        ])
        buttons = [
            self.ui.create_button_view(
                "😈 הצגת רשימת מי לא ענה",
                lambda s: (
                    self.ui.clear(s),
                    self.display_unfilled_list(s, form_data)
                )
            ),
            self.ui.create_button_view(
                "⚠️ מחיקת טופס זה",
                lambda s: (self.ui.clear(s), self.verify_delete_form(s, form_data))
            ),
            self.ui.create_button_view(
                "📝️ שינוי דדליין",
                lambda s: (self.ui.clear(s), self.change_deadline(s, form_data))
            ),
            self.ui.create_button_view(
                "📝️ שינוי לינק",
                lambda s: (self.ui.clear(s), self.change_link(s, form_data))
            ),
            self.ui.create_button_view(
                "🔙",
                lambda s: (
                    self.ui.clear(s),
                    self.edit_my_forms(s)
                )
            ),
        ]
        self.ui.create_button_group_view(
            session,
            summary_text,
            buttons
        ).draw()

    # verify delete form
    def verify_delete_form(self, session, form_data):
        buttons = [
                      self.ui.create_button_view(
                          "לא",
                          lambda s: (
                              self.ui.clear(s),
                              self.edit_single_form(s, form_data)
                          )
                      )
                  ] + [
                      self.ui.create_button_view(
                          "כן",
                          lambda s: (
                              self.ui.clear(s),
                              self.delete_form(s, form_data)
                          )
                      )
                  ]

        self.ui.create_button_group_view(
            session,
            "האם למחוק את הטופס?",
            buttons
        ).draw()

    # Delete form action
    def delete_form(self, session, form_data):
        # try:
        #     with GoogleCalendar.get_instance() as gc:
        #         cal_obj = CalendarEvent(
        #             title=(
        #                     "מילוי טופס: " + form_data["name"]
        #             ),
        #             start_time=form_data["time"],
        #             end_time=form_data["time"],
        #             location=(
        #                     "נוצר על ידי פיצ'ר הטפסים של Talpibot"
        #                     + "  -  "
        #                     + form_data["link"]
        #             ),
        #             attendees=form_data["not_filled"],
        #             calendar_event_id=form_data["calendar"],
        #         )
        #         gc.delete_event(
        #             calendar_id="cd0pps0gvfslqistr86hno3cmo@group.calendar.google.com",
        #             event=cal_obj,
        #             send_updates=SEND_UPDATES_NONE
        #         )
        # except:
        #     pass

        form_data.delete()
        self.ui.clear(session)
        self.edit_my_forms(session)

    # change link
    def change_link(self, session, form_data):
        self.ui.clear(session)
        self.ui.create_text_view(session, "תכתוב כאן קישור מעודכן לforms").draw()
        self.ui.get_text(session, lambda s, t: self.finish_change_link(s, t, form_data))

    # update link
    def finish_change_link(self, session, link, form_data):
        form_data["link"] = link
        form_data.save()
        # buttons = [self.ui.create_button_view(
        #     "🔙",
        #     lambda s: (
        #         self.ui.clear(s),
        #         self.edit_single_form(s, form_data)
        #     )
        # )]
        # self.ui.create_button_group_view(
        #     session,
        #     "הלינק עודכן!",
        #     buttons
        # ).draw()
        # render summary
        summary_text = "הלינק עודכן!\n"
        summary_text += "❓ סטטוס הטופס:" + "\n\n" + "\n".join([
            "שם הטופס: %s" % form_data["name"],
            "קישור: %s" % form_data["link"],
            "דדליין: %s" % form_data["time"],
            "כמה לא ענו: %s" % len(form_data["not_filled"]),
            "\n"
        ])
        summary_msg = self.ui.create_text_view(session, summary_text).draw()
        self.ui.summarize_and_close(session, [summary_msg, self.end_message(session)])

    # change the deadline of the form
    def change_deadline(self, session, form_data):
        form_new_data = {}
        self.ui.create_text_view(session, "בחר תאריך הגשה חדש").draw()
        self.ui.create_date_choose_view(
            session,
            lambda s, t, d: self.change_form_date(s, t, d, form_new_data, form_data)
        ).draw()

    # Save form date + prompt for form time
    def change_form_date(self, _, session, form_date, form_new_data, form_data):
        form_new_data["date"] = form_date

        self.ui.clear(session)
        self.ui.create_text_view(session, "נפץ! ומה שעת ההגשה החדשה?").draw()
        self.ui.create_time_choose_view(
            session,
            lambda s, t, d: self.finish_change_deadline(s, t, d, form_new_data, form_data)
        ).draw()

    # Save form time + finish process
    def finish_change_deadline(self, _, session, form_time, form_new_data, form_data):
        form_new_data["time"] = form_time
        deadline = datetime.datetime(
            form_new_data["date"].year, form_new_data["date"].month, form_new_data["date"].day,
            form_new_data["time"].hour, form_new_data["time"].minute
        )
        form_data["time"] = deadline
        form_data.save()
        # buttons = [self.ui.create_button_view(
        #     "🔙",
        #     lambda s: (
        #         self.ui.clear(s),
        #         self.edit_single_form(s, form_data)
        #     )
        # )]
        # self.ui.create_button_group_view(
        #     session,
        #     "התאריך עודכן!",
        #     buttons
        # ).draw()
        summary_text = "הדדליין עודכן!\n"
        summary_text += "❓ סטטוס הטופס:" + "\n\n" + "\n".join([
            "שם הטופס: %s" % form_data["name"],
            "קישור: %s" % form_data["link"],
            "דדליין: %s" % form_data["time"],
            "כמה לא ענו: %s" % len(form_data["not_filled"]),
            "\n"
        ])
        summary_msg = self.ui.create_text_view(session, summary_text).draw()
        self.ui.summarize_and_close(session, [summary_msg, self.end_message(session)])

    # Show people who havent filled the form yet from the database action
    def display_unfilled_list(self, session, form_data):
        text = "😈 האנשים הבאים לא סימנו שהם מילאו את הטופס:\n\n"
        text += ", ".join([u.name for u in form_data["not_filled"]])

        if len(form_data["not_filled"]) == 0:
            text += "כולם מילאו את הטופס! פינוקים! מוזמן למחוק את הטופס עכשיו"

        buttons = [
            self.ui.create_button_view(
                "🔙",
                lambda s: (
                    self.ui.clear(s),
                    self.edit_single_form(s, form_data)
                )
            ),
        ]
        self.ui.create_button_group_view(
            session,
            text,
            buttons
        ).draw()

    # ---------------------------------------
    # Main callback list for 1) display my forms
    # ---------------------------------------

    # Main display list
    def display_form_list(self, session):
        # filter relevant forms
        # forms = [
        #     form for form in Form.objects()
        #     if (
        #             session.user in form.not_filled
        #     )
        # ]
        forms = list(Form.objects(not_filled=session.user))

        forms.sort(key=lambda x: x.time)
        forms = forms[::-1]

        if len(forms):
            buttons = [
                          self.ui.create_button_view(
                              "%s: %s" % (form.name, form.time.strftime("%d/%m")),
                              lambda s, form=form: (
                                  self.ui.clear(s),
                                  self.display_single_form(s, form)
                              )
                          )
                          for form in forms
                      ] + [
                          self.ui.create_button_view(
                              "🔙",
                              lambda s: (
                                  self.ui.clear(s),
                                  self.main(s)
                              )
                          )
                      ]

            self.ui.create_button_group_view(
                session,
                "📝 רשימת הטפסים שטרם מילאת:",
                buttons
            ).draw()
        else:
            # finish_msg = self.ui.create_text_view(session, "מילאתם את כל הטפסים שלכם - כל הכבוד!").draw()
            # self.ui.summarize_and_close(session, [finish_msg, self.end_message(session)])
            buttons = [
                self.ui.create_button_view(
                    "🔙",
                    lambda s: (
                        self.ui.clear(s),
                        self.main(s)
                    )
                )
            ]
            self.ui.create_button_group_view(
                session,
                "📝 מילאתם את כל הטפסים שלכם! כל הכבוד!",
                buttons
            ).draw()

    # Display user a single form and opt to fill in
    def display_single_form(self, session, form_data):
        summary_text = "❓ פרטי הטופס:" + "\n\n" + "\n".join([
            "שם הטופס: %s" % form_data["name"],
            "קישור: %s" % form_data["link"],
            "דדליין: %s" % form_data["time"],
            "\n\n"
        ])
        buttons = [
            self.ui.create_button_view(
                "✅ מילאתי את הטופס!",
                lambda s: (
                    self.ui.clear(s),
                    self.verify_answer_new_form(s, form_data)
                )
            ),
            self.ui.create_button_view(
                "🔙",
                lambda s: (
                    self.ui.clear(s),
                    self.display_form_list(s)
                )
            ),
        ]

        self.ui.create_button_group_view(
            session,
            summary_text,
            buttons
        ).draw()

    def verify_answer_new_form(self, session, form_data):
        buttons = [
                      self.ui.create_button_view(
                          "אופס, חזור אחורה",
                          lambda s: (
                              self.ui.clear(s),
                              self.display_single_form(s, form_data)
                          )
                      )
                  ] + [
                      self.ui.create_button_view(
                          "בטח שמילאתי!",
                          lambda s: (
                              self.ui.clear(s),
                              self.filled_in_form(s, form_data)
                          )
                      )
                  ]

        self.ui.create_button_group_view(
            session,
            "האם באמת מילאת את הטופס או שנלחץ בטעות?",
            buttons
        ).draw()

    # Fill in form action button
    def filled_in_form(self, session, form_data):
        print(session.user)
        print("\n\n\n\n\n\n")

        # form_data["not_filled"].remove(session.user),
        # form_data.save()

        Form.objects(id=form_data.id).update_one(pull__not_filled=session.user)

        # update google calendar event
        # with GoogleCalendar.get_instance() as gc:
        #     cal_obj = CalendarEvent(
        #         title=(
        #                 "מילוי טופס: " + form_data["name"]
        #         ),
        #         start_time=form_data["time"],
        #         end_time=form_data["time"],
        #         location=(
        #                 "נוצר על ידי פיצ'ר הטפסים של תלפיבוט"
        #                 + " - "
        #                 + form_data["link"]
        #         ),
        #         attendees=form_data["not_filled"],
        #         calendar_event_id=form_data["calendar"]
        #     )
        #     gc.update_event(
        #         calendar_id="cd0pps0gvfslqistr86hno3cmo@group.calendar.google.com",
        #         event=cal_obj,
        #         send_updates=SEND_UPDATES_NONE
        #     )

        self.ui.clear(session),
        self.display_form_list(session)

    # ---------------------------------------
    # Main callback list for 2) upload new forms
    # ---------------------------------------

    # verify that the user really wants to upload new form
    def verify_upload_new_form(self, session):
        buttons = [
                      self.ui.create_button_view(
                          "לא",
                          lambda s: (
                              self.ui.clear(s),
                              self.main(s)
                          )
                      )
                  ] + [
                      self.ui.create_button_view(
                          "כן",
                          lambda s: (
                              self.ui.clear(s),
                              self.upload_new_form(s)
                          )
                      )
                  ]

        self.ui.create_button_group_view(
            session,
            "האם אתה בטוח שאתה רוצה להעלות טופס?!",
            buttons
        ).draw()

    # Upload new form + prompt for form name
    def upload_new_form(self, session):
        form_data = {}
        self.ui.create_text_view(session, "העלאת טופס חדש! מה שם הטופס?").draw()
        self.ui.get_text(session, lambda s, t: self.get_form_name(s, t, form_data))

    # Save form name + prompt for form link
    def get_form_name(self, session, form_name, form_data):
        form_data["name"] = form_name

        self.ui.create_text_view(session, "אדיר! תזרוק כאן קישור לforms").draw()
        self.ui.get_text(session, lambda s, t: self.get_form_link(s, t, form_data))

    # Save form link + prompt for form date
    def get_form_link(self, session, form_link, form_data):
        form_data["link"] = form_link

        self.ui.create_text_view(session, "אש! בחר תאריך הגשה").draw()
        self.ui.create_date_choose_view(
            session,
            lambda s, t, d: self.get_form_date(s, t, d, form_data)
        ).draw()

    # Save form date + prompt for form time
    def get_form_date(self, _, session, form_date, form_data):
        form_data["date"] = form_date

        self.ui.create_text_view(session, "נפץ! ומה שעת ההגשה?").draw()
        self.ui.create_time_choose_view(
            session,
            lambda s, t, d: self.get_form_time(s, t, d, form_data)
        ).draw()

    # Save form time + prompt for form group
    def get_form_time(self, _, session, form_time, form_data):
        form_data["time"] = form_time

        # possible groups
        buttons = [
            self.ui.create_button_view(
                group.name + " - משתתפים: " + str(len(group.participants)),
                lambda s, group=group: self.finish_new_form(s, group, form_data)
            )
            for group in get_user_groups(session.user)
        ]
        self.ui.create_button_group_view(
            session,
            "כמעט בסוף! למי מיועד הטופס?",
            buttons
        ).draw()

    # Save form group + save all in DB + save to calendar + summarize to user
    def finish_new_form(self, session, group, form_data):
        form_data["group"] = group

        # upload
        deadline = datetime.datetime(
            form_data["date"].year, form_data["date"].month, form_data["date"].day,
            form_data["time"].hour, form_data["time"].minute
        )
        form_data["time"] = deadline

        calendar_fields = {
            "title": "מילוי טופס: " + form_data["name"],
            "start_time": deadline,
            "end_time": deadline,
            "location": "נוצר על ידי פיצ'ר הטפסים של Talpibot",
            "attendees": form_data["group"].participants,
            "calendar_event_id": 1
        }

        # upload to google calendar
        # with GoogleCalendar.get_instance() as gc:
        #     cal_obj = CalendarEvent(
        #         title=(
        #                 "מילוי טופס: " + form_data["name"]
        #         ),
        #         start_time=calendar_fields["start_time"],
        #         end_time=calendar_fields["end_time"],
        #         location=(
        #                 "נוצר על ידי פיצ'ר הטפסים של תלפיבוט"
        #                 + " - "
        #                 + form_data["link"]
        #         ),
        #         attendees=calendar_fields["attendees"]
        #     )
        #     cal_obj = gc.insert_event(
        #         calendar_id="cd0pps0gvfslqistr86hno3cmo@group.calendar.google.com",
        #         event=cal_obj,
        #         send_updates=SEND_UPDATES_NONE
        #     )
        #     calendar_fields["calendar_event_id"] = cal_obj.calendar_event_id

        # save to db
        new_form = Form(
            name=form_data["name"],
            link=form_data["link"],
            time=deadline,
            group=form_data["group"].name,
            creator=session.user,
            not_filled=calendar_fields["attendees"],
        )
        new_form.save()

        # remind users
        for user_obj in new_form["not_filled"]:
            if user_obj != session.user:
                self.notify_user(self.ui.create_session("remind_form", user_obj), new_form)

        # render summary
        summary_text = "❓ סיכום טופס:" + "\n\n" + "\n".join([
            "שם הטופס: %s" % form_data["name"],
            "מיועדים: %s" % form_data["group"].name,
            "תאריך דדליין: %s" % form_data["date"],
            "שעת דדליין: %s" % form_data["time"].strftime("%H:%M"),
        ])
        summary = self.ui.create_text_view(session, summary_text)
        finish_msg = self.ui.create_text_view(session, "תודה שהעלתם טופס!")
        self.ui.summarize_and_close(session, [summary, finish_msg, self.end_message(session)])

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

    # Notify user when new form is sent to him
    def notify_user(self, session, form_data):
        text = "שים לב! יש לך טופס נוסף למלא:"
        summary_text = text + "\n\n" + "❓ פרטי הטופס:" + "\n\n" + "\n".join([
            "שם הטופס: %s" % form_data["name"],
            "קישור: %s" % form_data["link"],
            "דדליין: %s" % form_data["time"],
            "\n\n"
        ])

        buttons = [
            self.ui.create_button_view(
                "✅ מילאתי את הטופס!",
                lambda s: (self.ui.clear(s), self.verify_answer_new_form(s, form_data))
            ),
            self.ui.create_button_view(
                "🔙",
                lambda s: (
                    self.ui.clear(s),
                    self.main(s)
                )
            )
        ]

        self.ui.create_button_group_view(
            session,
            summary_text,
            buttons
        ).draw()

    # Remind user about a form he has
    def remind_user(self, session):
        """Remind user about a form he has"""

        text = "עדיין לא מילאת את הטפסים הבאים - בטיפול?"
        self.ui.create_text_view(
            session, text
        ).draw()
        self.display_form_list(session)

    def remind_check(self):
        users = User.objects(mahzor__in=get_mahzor_number_list())
        users_not_filled = {}
        for form_data in Form.objects:
            # maybe need to make more efficient
            if form_data["time"] is None:
                continue
            if (datetime.datetime.now() - form_data["time"]).days > 7:
                continue
            for user in form_data["not_filled"]:
                users_not_filled[user] = 1
        for user_obj in users_not_filled.keys():
            # if user_obj not in users:
            #     continue
            self.remind_user(self.ui.create_session("remind_form", user_obj))

    # schedule job fot matlam
    def get_scheduled_jobs(self) -> [ScheduledJob]:
        """
        Get jobs (scheduled functions) that need to be called at specific times.
        :return: List of Jobs that will be created and called.
        """

        jobs = []
        jobs.append(ScheduledJob(
            self.remind_check,
            [], day="*", hour="22", minute="00"
        ))
        return jobs
