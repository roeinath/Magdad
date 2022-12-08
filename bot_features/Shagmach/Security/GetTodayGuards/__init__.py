from bot_framework.Feature.FeatureSettings import FeatureSettings, FeatureType


def get_settings():
    return FeatureSettings(display_name="שומרים יומיים", _type=FeatureType.REGULAR_FEATURE)
