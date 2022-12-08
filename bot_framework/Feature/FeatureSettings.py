from enum import Enum


class FeatureType(Enum):
    REGULAR_FEATURE, FEATURE_CATEGORY = range(2)


class FeatureSettings:
    DEFAULT_EMOJI = '📀'

    def __init__(self, display_name: str, show_in_menu: bool = True,
                 _type: FeatureType = FeatureType.REGULAR_FEATURE, emoji: str = DEFAULT_EMOJI, db_name: str = None):
        self.display_name: str = display_name
        self.show_in_menu: bool = show_in_menu
        self.type: FeatureType = _type
        self.emoji: str = emoji
        self.db_name = db_name
