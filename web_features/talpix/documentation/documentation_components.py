import os

from web_framework.server_side.infastructure.components.all_components_import import *
from web_framework.server_side.infastructure.constants import *


class MainTitle(Label):
    def __init__(self, text):
        super().__init__(text=text, size=SIZE_EXTRA_LARGE, fg_color=COLOR_PRIMARY_DARK, bold=True)


class SubTitle(Label):
    def __init__(self, text):
        super().__init__(text=text, size=SIZE_EXTRA_LARGE, fg_color=COLOR_PRIMARY)


class TextBox(Label):
    def __init__(self, text):
        super().__init__(text=text, size=SIZE_MEDIUM)


class EvalCodeBlock(StackPanel):
    def __init__(self, text):
        sp = StackPanel([])
        for line in text.split('\n'):
            exec(line)
        super().__init__([
            CodeBlock(text),
            Label("זה נראה כך:", size=SIZE_MEDIUM, fg_color=COLOR_PRIMARY_DARK, bold=True),
            sp
        ])


CUR_DIR = os.path.dirname(os.path.realpath(__file__))


TAGS = {
    '&&&': MainTitle,
    '%%%': SubTitle,
    '$$$': CodeBlock,
    '$$$*': EvalCodeBlock,
    '^^^': HyperLink,
}


def get_page_by_file(file_path: str):
    sp = StackPanel([])

    with open(os.path.join(CUR_DIR, file_path), 'r', encoding='utf8') as f:
        lines = []
        current_tag = None
        for line in f.readlines():
            line = line.strip('\n')
            if line in TAGS:
                ComponentType = TAGS.get(current_tag, TextBox)  # set TextBox as default
                sp.add_component(ComponentType('\n'.join(lines)))
                lines.clear()
                current_tag = None if line == current_tag else line
            else:
                lines.append(line)
    return sp
