from web_framework.server_side.infastructure.category import Category
from web_features.TVs import TVpage41, TVpage42, TVpage43, TVs_add_image, TVs_view_images
from web_features.TVs import permissions


class TVsCategory(Category):
    def __init__(self):
        super().__init__(pages={
            'TV41': TVpage41.TVpage41,
            'TV42': TVpage42.TVpage42,
            'TV43': TVpage43.TVpage43,
            'ADD_IMAGE': TVs_add_image.AddImage,
            'VIEW_IMAGES': TVs_view_images.ViewImages
        })

    def get_title(self) -> str:
        return "טלווזיות"

    def is_authorized(self, user):
        return permissions.is_user_tv_allowed(user)
