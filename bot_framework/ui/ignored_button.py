from bot_framework.ui.button import Button


class IgnoredButton(Button):
    IGNORE_FUNC = None

    def __init__(self, title: str):
        super().__init__(title, IgnoredButton.IGNORE_FUNC)
