from abc import abstractmethod

from mongoengine import Document, ReferenceField
from APIs.TalpiotAPIs.Forms.questions.question import Question


class Answer(Document):
    meta = {'allow_inheritance': True, 'abstract': True}

    question: Question = ReferenceField(Question, required=True)

    @abstractmethod
    def set_value(self, value: any):
        pass

    @abstractmethod
    def get_value(self) -> any:
        pass

    def get_question_id(self) -> str:
        return self.question.field_identifier
