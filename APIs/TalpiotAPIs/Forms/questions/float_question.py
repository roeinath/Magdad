from __future__ import annotations

from typing import Optional, List, Dict

from mongoengine import FloatField, DictField

from APIs.TalpiotAPIs.Forms.questions.question import Question
from APIs.TalpiotAPIs.Forms.answers.float_answer import FloatAnswer


class FloatQuestion(Question):
    _range_maximum: Optional[float] = FloatField()
    _range_minimum: Optional[float] = FloatField()
    _default_value: Optional[float] = FloatField()
    _possible_values: Optional[Dict[str, float]] = DictField(FloatField())

    def get_answer_type(self):
        return float

    def new_answer(self) -> FloatAnswer:
        return FloatAnswer()

    def get_default_value(self) -> float:
        return self._default_value

    def _set_options(self, values: List[float]):
        for value in values:
            self._possible_values[str(value)] = value

    def options(self) -> Optional[Dict[str, float]]:
        if self._possible_values:
            return self._possible_values
        return None
