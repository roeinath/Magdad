import importlib
import importlib.util
import inspect
from os import listdir, path, sep
from typing import Dict, Type
from bot_framework.Feature.bot_feature import BotFeature


class FeatureLoader:
    BASE_PACKAGE_NAME = "file_system_import"

    @staticmethod
    def get_classes_in_directory(dir_path: str, import_path: str) -> Dict[str, Type[BotFeature]]:
        """
        Returns all classes in the given directory,
        that are declared in a file in the given directory,
        and are subclasses of BotFeature. sets the package
        of the loaded classes to be:
        if the file loaded is at features/file_a.py has class FeatureA
        to the pacakge: file_system_import.features.file_a.FeatureA
        :param dir_path: The directory path to load from
        :param import_path:
        :return: Dictionary of
        """
        classes = dict()

        #  Loop all files in the given directory
        FeatureLoader._include_classes_from_directory(dir_path, "", import_path, classes)

        return classes

    @staticmethod
    def _include_classes_from_directory(dir_path: str,
                                        appending_dir_path: str,
                                        import_path: str,
                                        classes: Dict[str, Type[BotFeature]]) -> None:
        """
        (For internal use only).
        Includes all BotFeature classes from the given directory, recursively.
        """
        for x in listdir(dir_path):
            full_path = path.join(dir_path, x)

            if path.isdir(full_path):
                FeatureLoader._include_classes_from_directory(full_path, path.join(appending_dir_path, x), import_path, classes)

            if path.isfile(full_path):
                FeatureLoader._includes_classes_from_file(x, dir_path, appending_dir_path, import_path, classes)

    @staticmethod
    def _includes_classes_from_file(file_name: str,
                                    dir_path: str,
                                    appending_dir_path: str,
                                    import_path: str,
                                    classes: Dict[str, Type[BotFeature]]) -> None:
        """
        (for internal use only).
        Includes all relevent classes from the given file,
        dirpath, into the <classes> dictionary.
        :return:
        """
        #  For each file, calculate the full_path
        #  of the file, the file name and the extension.
        full_path = path.join(dir_path, file_name)
        file_wo_extension = ".".join(file_name.split(".")[:-1])
        file_extension = file_name.split(".")[-1]

        #  Only accept files that are regular files
        #  and their extension is "py" (python regular
        #  files).
        if file_extension != "py":
            return

        #  Find the wanted module_name for the new class.
        #  Will consist of BASE_PACKAGE_NAME, the file
        #  path and the file's name.
        module_name = '.'.join([
            FeatureLoader.BASE_PACKAGE_NAME,
            import_path.replace(sep, '.'),
            appending_dir_path.replace(sep, '.'),
            file_wo_extension
        ])

        #  Load all classes from the given file, into the module_name
        #  module.
        spec = importlib.util.spec_from_file_location(module_name, full_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        #  Loop on all classes that were given from the file.
        for name, obj in inspect.getmembers(module, inspect.isclass):
            #  Only access classes that their package
            #  starts with BASE_PACKAGE_NAME (So they are
            #  declared in the given file).
            if not obj.__module__.startswith(FeatureLoader.BASE_PACKAGE_NAME):
                continue

            #  Only access classes that are of type BotFeature.
            if not issubclass(obj, BotFeature):
                continue

            #  Add the class to their corresponding full package name
            #  in the result dictionary
            classes[obj.__module__ + "." + obj.__name__] = obj
