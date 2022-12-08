from BotFramework import FeatureSettings, FeatureType


def get_settings():
    return FeatureSettings(display_name="INSERT NAME IN INIT FILE", _type=FeatureType.REGULAR_FEATURE)
