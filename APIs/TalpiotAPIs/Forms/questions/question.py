from __future__ import annotations

from abc import abstractmethod
from typing import Dict

from mongoengine import StringField, BooleanField

from APIs.TalpiotAPIs.Forms.form_field import FormField


class Question(FormField):
    """
    This model represents a form field of a generic question.
    Like form field, it may not be used by itself but rather
    implemented to create specific question types.
    """
    meta = {'allow_inheritance': True}

    question: str = StringField(db_field='question', max_length=100, required=False)
    from_values: bool = BooleanField()
    required: bool = BooleanField(db_field='required', required=True)

    # TODO: add some metadata?

    def get_question(self) -> str:
        """
        Get the literal question
        :return: The question
        """
        return self.question

    def is_required(self) -> bool:
        """
        Returns whether this question is marked as required
        :return: True if this question is required
        """
        return self.required

    @abstractmethod
    def get_default_value(self):
        raise NotImplementedError(f'Method \'get_default_value()\' is not define for \'{self.__class__}\'')

    @abstractmethod
    def get_answer_type(self) -> type:
        raise NotImplementedError(f'Method \'get_answer_type()\' is not define for \'{self.__class__}\'')

    def set_options(self, values: Dict[any, any]):
        self.from_values = True
        self._set_options(values)

    @abstractmethod
    def _set_options(self, values: Dict[any, any]):
        pass

    def options(self) -> Dict[str, any]:
        """
        Returns the possible values for this question, None if it is an open question
        :return: possible values for this question, None if it is an open question
        """
        pass

    @abstractmethod
    def new_answer(self):
        pass
