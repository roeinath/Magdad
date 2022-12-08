from bot_framework.Feature.FeatureSettings import FeatureSettings, FeatureType


def get_settings():
    return FeatureSettings(display_name="ספורט", _type=FeatureType.FEATURE_CATEGORY, emoji='⚽')
