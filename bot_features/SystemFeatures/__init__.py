from bot_framework.Feature.FeatureSettings import FeatureSettings, FeatureType


def get_settings():
    return FeatureSettings(display_name="System Features", _type=FeatureType.FEATURE_CATEGORY, show_in_menu=False)
