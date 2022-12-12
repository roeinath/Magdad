from mongoengine import IntField

from APIs.TalpiotAPIs.Forms.answers.answer import Answer


class IntegerAnswer(Answer):
    value: int = IntField()

    def set_value(self, value: int):
        self.value = value

    def get_value(self) -> int:
        return self.value
