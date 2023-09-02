import os
from datetime import datetime
from shutil import SameFileError, copy2

import piexif

from src.constants.new_filenames_utils import (
    MONTH_NAMES,
    UNKOWN_LITERAL,
    VALID_NAME_KEYS,
)
from src.utils.rich_console import console, progress_bar


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

    except Exception:
        return min(
            datetime.fromtimestamp(os.path.getctime(filepath)),
            datetime.fromtimestamp(os.path.getmtime(filepath)),
        )


def get_folder_path(folder_structure: list[str], filedate: datetime):
    if len(folder_structure) > 3:
        raise RecursionError("The max depth for the folder structure is 3")

    to_return: list[str] = []

    for key in folder_structure:
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
    _folder_structure: list[str], output_path: str, filename: str, filedate: datetime
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
    filepaths: list[tuple[str, str]], output_path: str, folder_structure: list[str]
):
    with progress_bar() as p:
        for path, filename in p.track(
            filepaths, description="Organizing your library:"
        ):
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
