import os


def remove_empty_folders(path_abs: str):
    """
    Remove the empty folders and subfolders in the specific path, and returns a list with the deleted folders
    """

    walk = list(os.walk(path_abs))

    removed_directories: list[str] = []

    for path, _, _ in walk[::-1]:
        if len(os.listdir(path)) == 0:
            os.rmdir(path)
            removed_directories.append(path)

    return removed_directories
