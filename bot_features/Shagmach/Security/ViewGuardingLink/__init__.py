from bot_framework.Feature.FeatureSettings import FeatureSettings, FeatureType


def get_settings():
    return FeatureSettings(display_name='הצגת שמירות', _type=FeatureType.REGULAR_FEATURE)
