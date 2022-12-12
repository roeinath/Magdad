from typing import List, Optional

from DateTime import DateTime
from mongoengine import Document, StringField, ListField, ReferenceField, \
    DateTimeField

from APIs.TalpiotAPIs import User
from APIs.TalpiotAPIs.Forms.answers.answer import Answer
from APIs.TalpiotAPIs.Forms.newform import NewForm
from APIs.TalpiotAPIs.Forms.form_field import FormField


class FormSubmission(Document):
    meta = {'collection': 'form_submissions'}

    form = ReferenceField(NewForm, db_field='form', required=True)
    answers: List[Answer] = ListField(ReferenceField(Answer), required=False)

    # Some metadata
    submitted_by: User = ReferenceField(User, required=False)
    submission_date: DateTime = DateTimeField()
    last_edited: DateTime = DateTimeField()

    def get_answer_by_question_id(self, field_identifier) -> Optional[FormField]:
        for answer in self.answers:
            if answer.question.get_identifier() == field_identifier:
                return answer

        return None

    def to_dict(self):
        return {
            'form': self.form,
            'submitted_by': self.submitted_by,
            'submission_date': self.submission_date,
            'last_edited': self.last_edited,
            'answers': {
                answer.get_question_id(): answer.get_value() for answer in self.answers
            }
        }