from web_features.talpix.talpix_category import TalpiXCategory
from web_features.guardings.guarding_category import GuardingCategory
from web_features.talpiwiki.talpiwiki_category import TalpiWikiCategory
from web_features.shagmach.shagmach_category import ShagmachCategory
from web_features.TVs.TVs_category import TVsCategory
from web_features.groups.groups_category import GroupsCategory
from web_features.cleaning_duties.cleaning_category import CleaningCategory
from web_features.logistic_events.logistic_category import LogisticEventsCategory
from web_features.Elements.elements_category import ElementsCategory
from web_features.tech_miun.miun_category import MiunCategory

categories = [
    GuardingCategory(),
    CleaningCategory(),
    ElementsCategory(),
    TalpiWikiCategory(),
    GroupsCategory(),
    TVsCategory(),
    ShagmachCategory(),
    LogisticEventsCategory(),
    TalpiXCategory(),
    MiunCategory()
]
