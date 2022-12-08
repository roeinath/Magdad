import os

from BotFramework import FeatureSettings, FeatureType

TALPI_BOT_PATH = os.path.abspath(__file__)

def get_settings():
    return FeatureSettings(display_name="חיפוש אנשים", _type=FeatureType.REGULAR_FEATURE)