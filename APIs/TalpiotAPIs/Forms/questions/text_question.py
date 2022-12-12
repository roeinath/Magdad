from __future__ import annotations

from typing import Optional, Dict

from mongoengine import StringField, DictField

from APIs.TalpiotAPIs.Forms.answers.text_answer import TextAnswer
from APIs.TalpiotAPIs.Forms.questions.question import Question


class TextQuestion(Question):
    _default_value: Optional[str] = StringField()
    _possible_values: Optional[Dict[str, str]] = DictField(StringField())

    def new_answer(self) -> TextAnswer:
        return TextAnswer()

    def get_answer_type(self):
        return str

    def get_default_value(self) -> str:
        return self._default_value

    def _set_options(self, values: Dict[str, str]):
        self._possible_values = values

    def options(self) -> Dict[str, str]:
        if self.from_values:
            return self._possible_values
        return None
