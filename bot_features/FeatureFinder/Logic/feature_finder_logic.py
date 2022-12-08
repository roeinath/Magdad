from bot_framework.Feature import FeatureSettings
from bot_features.SystemFeatures.HierarchicalMenu.Code.hierarchical_menu import HierarchicalMenu
from bot_features.SystemFeatures.HierarchicalMenu.Code.menu_node import MenuNode


class FeatureFinderLogic:
    @staticmethod
    def get_all_features(root_node: MenuNode):
        features = []

        def get_all_features_recursive(node: MenuNode):
            if not node.show_in_menu or not node.is_valid:
                return

            if node.type == FeatureSettings.FeatureType.FEATURE_CATEGORY:
                for child_node in node.payload:
                    get_all_features_recursive(child_node)

            if node.type == FeatureSettings.FeatureType.REGULAR_FEATURE:
                features.append(node)

        get_all_features_recursive(root_node)
        return features
