from bot_framework.Feature.FeatureSettings import FeatureSettings, FeatureType


def get_settings():
    return FeatureSettings(display_name="אחד מדלג", _type=FeatureType.REGULAR_FEATURE)
