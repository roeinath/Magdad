from bot_framework.Feature.FeatureSettings import FeatureSettings, FeatureType


def get_settings():
    return FeatureSettings(display_name="פיצ׳ר תפריט", _type=FeatureType.REGULAR_FEATURE, show_in_menu=False)
