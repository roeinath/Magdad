from bot_framework.Feature.FeatureSettings import FeatureSettings, FeatureType


def get_settings():
    return FeatureSettings(display_name='מחברות ב"מ', _type=FeatureType.REGULAR_FEATURE, emoji='📓')
