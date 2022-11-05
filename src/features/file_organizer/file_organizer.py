import os
from datetime import datetime
from shutil import SameFileError, copy2

import piexif

from src.constants.new_filenames_utils import (
    MONTH_NAMES,
    UNKOWN_LITERAL,
    VALID_NAME_KEYS,
)
from src.utils.console import bcolors, printProgressBar


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


def get_datefile(filepath: str):
    try:
        exif_dict = piexif.load(filepath)

        if exif_dict["Exif"].get(piexif.ExifIFD.DateTimeOriginal):
            return datetime.strptime(
                exif_dict["Exif"].get(piexif.ExifIFD.DateTimeOriginal).decode("utf-8"),
                "%Y:%m:%d %H:%M:%S",
            )

        else:
            return min(
                datetime.fromtimestamp(os.path.getctime(filepath)),
                datetime.fromtimestamp(os.path.getmtime(filepath)),
            )

    except:
        return min(
            datetime.fromtimestamp(os.path.getctime(filepath)),
            datetime.fromtimestamp(os.path.getmtime(filepath)),
        )


def get_folder_path(folder_structure: str, filedate: datetime):
    keys = folder_structure.split(">")

    if len(keys) > 3:
        raise RecursionError("The max depth for the folder structure is 3")

    to_return: list[str] = []

    for key in keys:
        key = key.strip()
        if key not in VALID_NAME_KEYS._value2member_map_:
            raise NameError(
                "The folder structure param that you have passed is not valid. To check the valid keys please visit the file constants/new_filenames_utils.py"
            )

        if key == VALID_NAME_KEYS.MONTH.value:
            to_return.append(str(MONTH_NAMES[filedate.month - 1]))
        elif key == VALID_NAME_KEYS.YEAR.value:
            to_return.append(str(filedate.year))

    return to_return


def get_file_location(
    _folder_structure: str, output_path: str, filename: str, filedate: datetime
):
    path_destination: str = ""

    folder_structure = get_folder_path(_folder_structure, filedate)

    if len(folder_structure) == 1:
        path_destination = os.path.join(output_path, folder_structure[0])
    elif len(folder_structure) == 2:
        path_destination = os.path.join(
            output_path, folder_structure[0], folder_structure[1]
        )
    elif len(folder_structure) == 3:
        path_destination = os.path.join(
            output_path, folder_structure[0], folder_structure[1], folder_structure[2]
        )

    if path_destination == "":
        return UNKOWN_LITERAL

    if not os.path.exists(path_destination):
        os.makedirs(path_destination)

    return os.path.join(path_destination, filename)


def file_organizer(
    filepaths: list[tuple[str, str]], output_path: str, folder_structure: str
):
    print()
    print(
        bcolors.BLUE + "\u2731" + bcolors.ENDC + " Starting to organize your library!\n"
    )

    printProgressBar(
        0,
        len(filepaths),
        prefix="Organizing your library:",
        suffix="Complete",
        length=50,
    )

    for i, (path, filename) in enumerate(filepaths):
        printProgressBar(
            i + 1,
            len(filepaths),
            prefix="Organizing your library:",
            suffix="Complete",
            length=50,
        )

        filepath = os.path.join(path, filename)
        filedate = get_datefile(filepath)

        new_file_location = get_file_location(
            folder_structure, output_path, filename, filedate
        )

        if not new_file_location:
            continue

        try:
            copy2(
                filepath,
                new_file_location,
            )
        except SameFileError:
            continue

        if filepath != new_file_location:
            os.remove(filepath)

    folders_removed = remove_empty_folders(os.path.abspath(output_path))

    if len(folders_removed) > 0:
        print()
        print(
            bcolors.BLUE
            + "\u2731"
            + bcolors.ENDC
            + f" {len(folders_removed)} empty folders has been removed"
        )
