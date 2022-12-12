from typing import List, Optional

from DateTime import DateTime
from mongoengine import Document, StringField, ListField, ReferenceField, \
    DateTimeField

from APIs.TalpiotAPIs import User, NewForm
from APIs.TalpiotAPIs.Forms.questions.float_question import FloatQuestion
from APIs.TalpiotAPIs.Forms.questions.integer_question import IntegerQuestion
from APIs.TalpiotAPIs.Forms.questions.text_question import TextQuestion


class TrackedMentalData(Document):
    meta = {'collection': 'mental-dashboard_tracked-data'}

    VALUE_IDENTIFIER = 'value'
    WEEK_IDENTIFIER = 'week'
    MACHZOR_IDENTIFIER = 'machzor'

    form = ReferenceField(NewForm, required=True)
    name = StringField(required=True)
    identifier = StringField(required=True)

    # Some metadata
    creator: User = ReferenceField(User, required=False)
    creation_date: DateTime = DateTimeField()
    last_edited: DateTime = DateTimeField()

    @staticmethod
    def create(id, name, created_by=None, creation_date=None, *args, **values):
        super().__init__(*args, **values)

        # Create question instances
        value_question = FloatQuestion()
        value_question.field_identifier = TrackedMentalData.VALUE_IDENTIFIER
        value_question.question = name
        value_question.required = True
        value_question.save()

        week_question = IntegerQuestion()
        week_question.field_identifier = TrackedMentalData.WEEK_IDENTIFIER
        week_question.question = name
        week_question.required = True
        week_question.save()

        machzor_question = TextQuestion()
        machzor_question.field_identifier = TrackedMentalData.MACHZOR_IDENTIFIER
        machzor_question.question = name
        machzor_question.required = True
        machzor_question.save()

        form = NewForm()
        form.form_identifier = id
        form.fields = [
            value_question,
            week_question,
            machzor_question
        ]
        form.creator = created_by
        form.creation_date = creation_date
        form.name = name
        form.save()

        tracked_data = TrackedMentalData()

        tracked_data.form = form
        tracked_data.name = name
        tracked_data.identifier = id

        tracked_data.creator = created_by
        tracked_data.creation_date = creation_date
