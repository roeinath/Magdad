import time
from typing import List, Optional, Dict

from DateTime import DateTime
from mongoengine import Document, StringField, ListField, ReferenceField, \
    DateTimeField

from APIs.TalpiotAPIs.Forms.form_field import FormField
from APIs.TalpiotAPIs.Forms.questions.question import Question
from APIs.TalpiotAPIs.User.user import User


class NewForm(Document):
    meta = {'collection': 'forms'}

    form_identifier = StringField(db_field='identifier', required=True, unique=True)
    name = StringField(required=True)
    fields: List[FormField] = ListField(ReferenceField(FormField), required=False)
    # Some metadata
    creator: User = ReferenceField(User, required=False)
    creation_date: DateTime = DateTimeField()
    last_edited: DateTime = DateTimeField()

    def get_field_by_identifier(self, field_identifier) -> Optional[FormField]:
        for field in self.fields:
            if field.get_identifier() == field_identifier:
                return field

        return None

    def __getitem__(self, item):
        return self.get_field_by_identifier(item)

    def submit(self, answers: Dict[str, any], creator: User = None, creation_date: DateTime = None):
        from APIs.TalpiotAPIs.Forms.form_submission import FormSubmission

        submission = FormSubmission()
        submission.submitted_by = creator
        submission.submission_date = creation_date
        submission.form = self
        submission.last_edited = None

        for ques, val in answers.items():
            question = self[ques]
            if question is not None and isinstance(question, Question):
                answer = question.new_answer()
                answer.set_value(val)
                answer.question = question
                answer.save()

                submission.answers.append(answer)
            else:
                # Unknown field is in the answers ot the field is not an answer
                pass

        submission.save()



    def get_submissions(self, group_by: str = None, sort_groups=False, sort_by: str = None, filters=None) -> List[Dict]:
        """
        Returns a set of all the submissions for this form. Submissions may be grouped by a certain answer's value
        and/or sorted by an answer's value.
        :param sort_groups: Whether to sort the groups by the key or not
        :param group_by: An identifier of a question, to group the submissions by
        the answer for it. by default groups by submission date.
        :param sort_by: An identifier of a question, to sort the submissions by the answer for it (
        a list will be returned). by default sorts by submission date.
        If the submissions has been grouped, the items of each group will be sorted by the ket
        :param filters: A dictionary of filters, a filter refers to the identifier of the
        question, and it's value will filter the submissions :return:
        """
        if filters is None:
            filters = {}

        from APIs.TalpiotAPIs import FormSubmission
        # Get the submissions for this form
        before_time = time.time()
        submissions = FormSubmission.objects(form=self)

        # Create a list of the submissions
        submissions_list = [submission.to_dict()
                            for submission in submissions
                            ]

        return submissions_list
