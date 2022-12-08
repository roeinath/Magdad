from bot_framework.Feature.FeatureSettings import FeatureSettings, FeatureType


def get_settings():
    return FeatureSettings(display_name=r'רפואה', _type=FeatureType.FEATURE_CATEGORY)
