from bot_framework.Feature.FeatureSettings import FeatureSettings, FeatureType


def get_settings():
    return FeatureSettings(display_name="דוקים", _type=FeatureType.REGULAR_FEATURE, db_name="forms_db")
