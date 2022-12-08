import os


def get_abs_dirs_in_dir(dirpath) -> [str]:
    """
    Returns all directories in dirpath with absolute path.
    :param dirpath: The directory to search in
    :return: list of
    """
    dirs = []
    for dir in next(os.walk(dirpath))[1]:
        if dir.startswith("_") or dir.startswith("HierarchicalMenu") or dir.endswith("Ag"):
            continue
        dirs.append(os.path.abspath(os.path.join(dirpath, dir)))
    return dirs
