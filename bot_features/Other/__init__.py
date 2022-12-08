from bot_framework.Feature.FeatureSettings import FeatureSettings, FeatureType


def get_settings():
    return FeatureSettings(display_name=r'אחר', _type=FeatureType.FEATURE_CATEGORY)
