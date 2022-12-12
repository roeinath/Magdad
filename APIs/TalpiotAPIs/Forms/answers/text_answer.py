from mongoengine import StringField

from APIs.TalpiotAPIs.Forms.answers.answer import Answer


class TextAnswer(Answer):
    value: str = StringField()

    def set_value(self, value: str):
        self.value = value

    def get_value(self) -> str:
        return self.value
