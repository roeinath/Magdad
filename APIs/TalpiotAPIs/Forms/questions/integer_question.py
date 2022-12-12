from __future__ import annotations

from typing import Optional, List, Dict

from django.forms import IntegerField
from mongoengine import DictField

from APIs.TalpiotAPIs.Forms.answers.integer_answer import IntegerAnswer
from APIs.TalpiotAPIs.Forms.questions.question import Question



class IntegerQuestion(Question):
    _range_maximum: Optional[int] = IntegerField()
    _range_minimum: Optional[int] = IntegerField()
    _default_value: Optional[int] = IntegerField()
    _possible_values: Optional[Dict[str, int]] = DictField(IntegerField())

    def new_answer(self) -> IntegerAnswer:
        return IntegerAnswer()

    def get_answer_type(self):
        return float

    def get_default_value(self) -> int:
        return self._default_value

    def _set_options(self, values: List[int]):
        for value in values:
            self._possible_values[str(value)] = value

    def options(self) -> Optional[Dict[str, int]]:
        if self._possible_values:
            return self._possible_values
        return None
