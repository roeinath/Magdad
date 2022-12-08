from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bot_framework.session import Session

class Button:
    """
    Button class that can be used by views that require it
    """

    def __init__(self, title: str = "", func_to_call=(lambda: print("func to call not given")), *args, **kwargs):
        self.title = title
        self.func_to_call = func_to_call
        self.args = args
        self.kwargs = kwargs

    def __eq__(self, other: Button):
        """Overrides the default implementation"""
        if isinstance(other, Button):
            return self.title == other.title and\
                   self.func_to_call == other.func_to_call and \
                   self.args == other.args and \
                   self.kwargs == other.kwargs

        return False

    def call_function(self, session: Session):
        self.func_to_call(session, *self.args, **self.kwargs)
