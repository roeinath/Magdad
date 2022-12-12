from mongoengine import FloatField

from APIs.TalpiotAPIs.Forms.answers.answer import Answer


class FloatAnswer(Answer):
    value: float = FloatField()

    def set_value(self, value: float):
        self.value = value

    def get_value(self):
        return self.value
