from bot_framework.Feature.FeatureSettings import FeatureSettings, FeatureType
from bot_features.SystemFeatures.Start.Code.start import Start


def get_settings():
    return FeatureSettings(display_name="Start", _type=FeatureType.REGULAR_FEATURE, show_in_menu=False)
