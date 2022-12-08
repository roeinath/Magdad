from bot_framework.Feature.FeatureSettings import FeatureSettings, FeatureType


def get_settings():
    return FeatureSettings(display_name="מחזורי", _type=FeatureType.FEATURE_CATEGORY)
