from __future__ import annotations
from typing import Optional
import traceback
import os
from bot_framework.Feature.FeatureSettings import FeatureType
from bot_framework.Feature.FeatureSettings import FeatureSettings
from bot_framework.Feature.feature_loader import FeatureLoader
from bot_framework.ui.ui import UI
from bot_features.SystemFeatures.HierarchicalMenu.Code.helper import get_abs_dirs_in_dir
from APIs.TalpiotSystem import Vault, TBLogger


class MenuNode:
    """
    Represents a node in the menu (A feature that is in the menu)
    """

    def __init__(self, dir_path: str, parent: Optional[MenuNode], ui: UI):
        """
        Creates a new MenuNode.
        :param dir_path: The directory path the node exists in
        :param parent: The parent MenuNode (Where to go back?)
        :param ui: The UI to use (What UI to give the features?)
        """

        self.parent: MenuNode = parent
        self.is_valid = True
        feature_settings: FeatureSettings = MenuNode.get_settings(dir_path)

        if feature_settings is None:
            self.is_valid = False
            TBLogger.error(f'No feature settings in: {dir_path}')
            return

        self.display_name = feature_settings.display_name
        self.show_in_menu = feature_settings.show_in_menu
        self.emoji = feature_settings.emoji

        if self.parent is not None and self.emoji == FeatureSettings.DEFAULT_EMOJI and not self.parent.emoji == FeatureSettings.DEFAULT_EMOJI:
            self.emoji = self.parent.emoji

        if not self.show_in_menu:
            self.is_valid = False
            return

        self.payload = self.load_payload(feature_settings, dir_path, ui)
        if self.payload is None:
            self.is_valid = False
            return
        self.type = feature_settings.type

    def load_payload(self, feature_settings: FeatureSettings, dir_path: str, ui: UI):
        """
        Returns the payload - the thing that is going to happen once this
        menu_node is being clicked.
        :param feature_settings: The feature settings we are in
        :param dir_path: The directory path we are in
        :param ui: The UI
        :return: Payload
        """

        #  Connect the feature specific database name
        if feature_settings.db_name is not None:
            Vault.get_vault().connect_to_db()

        #  If it is a regular feature, load it
        if feature_settings.type == FeatureType.REGULAR_FEATURE:
            try:
                classes_dict = FeatureLoader.get_classes_in_directory(dir_path, "AutoLoadedFeatures")
                _class = next(iter(classes_dict.values()))
                try:
                    return _class(ui)
                except:
                    TBLogger.error(f'Cannot load class {_class}. Got exception.')
                    TBLogger.error(f'Traceback: {traceback.print_exc()}')
                    return None
            except:
                TBLogger.error(f"error loading feature {feature_settings.display_name}")
                TBLogger.error(f'Traceback: {traceback.print_exc()}')
                return None
        #  If it is a feature category, load it
        elif feature_settings.type == FeatureType.FEATURE_CATEGORY:
            payload = []
            for _path in get_abs_dirs_in_dir(dir_path):
                node = MenuNode(_path, self, ui)
                if node.is_valid and node.show_in_menu:
                    payload.append(node)

            return payload

    @staticmethod
    def get_settings(dir_path: str) -> FeatureSettings:
        """
        Returns the FeatureSettings of the given directory path.
        (Loads the settings that exist in the __init__.py in the dir_path)
        :param dir_path: The directory path to look in
        :return:
        """
        settings = None
        try:
            if os.path.isdir(dir_path):
                import importlib.util
                spec = importlib.util.spec_from_file_location(dir_path.split(os.sep)[-1], dir_path + "/__init__.py")
                foo = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(foo)
                settings: FeatureSettings = getattr(foo, "get_settings")()
        except:
            pass

        return settings
