from bot_framework.Feature.FeatureSettings import FeatureSettings, FeatureType


def get_settings():
    return FeatureSettings(display_name="פאנל מפתחים", _type=FeatureType.REGULAR_FEATURE)
