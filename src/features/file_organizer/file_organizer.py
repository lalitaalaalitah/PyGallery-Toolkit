import json
import os
import re
import shutil
from datetime import datetime
from typing import Any

import exiftool
from exiftool import ExifToolHelper

from src.constants.user_settings import USER_SETTINGS
from src.utils.file_date_getters import get_date_from_exif, get_date_from_os
from src.utils.rich_console import progress_bar

python_date_directives = [
    "a",
    "A",
    "w",
    "d",
    "b",
    "B",
    "m",
    "y",
    "Y",
    "H",
    "I",
    "p",
    "M",
    "S",
    "f",
    "z",
    "Z",
    "j",
    "U",
    "W",
    "x",
    "x",
    "X",
]

python_date_directives = ["%" + i for i in python_date_directives]

custom_app_directives = ["software", "camera_maker", "camera_model"]
custom_app_directives = ["%" + i for i in custom_app_directives]


def get_datefile_to_organize(filepath: str, et: ExifToolHelper):
    try:
        to_return = get_date_from_exif(filepath, et)

    except:
        return get_date_from_os(filepath)

    if not to_return:
        to_return = get_date_from_os(filepath)

    return to_return


def get_metadata_str(metadata: dict[str, Any], keys: list[str]):
    for key in keys:
        if metadata.get(key):
            return str(metadata.get(key))

    return "Unknown"


def replace_attr_variables(part: str, filepath: str, et: ExifToolHelper):
    custom_attr = re.findall("(%[a-zA-Z_]+)", part)

    if set(custom_attr) <= set(python_date_directives):
        filedate = get_datefile_to_organize(filepath, et)
        part = datetime.strftime(filedate, part)

    else:
        for directive in custom_attr:
            if directive in python_date_directives:
                filedate = get_datefile_to_organize(filepath, et)

                part = part.replace(directive, datetime.strftime(filedate, directive))

            elif directive in custom_app_directives:
                metadata: dict[str, Any] = et.get_metadata(filepath)[0]

                if "software" in directive:
                    part = part.replace(
                        directive, get_metadata_str(metadata, ["EXIF:Software"])
                    )

                if "camera_maker" in directive:
                    part = part.replace(
                        directive,
                        get_metadata_str(metadata, ["EXIF:Make", "QuickTime:Make"]),
                    )

                if "camera_model" in directive:
                    part = part.replace(
                        directive,
                        get_metadata_str(metadata, ["EXIF:Model", "QuickTime:Model"]),
                    )

            else:
                raise Exception(f"Custom directive not accepted: {directive}")

    return part


def get_folder_path(folder_structure: list[str], filepath: str, et: ExifToolHelper):
    to_return: list[str] = []

    for part in folder_structure:
        to_return.append(replace_attr_variables(part, filepath, et))

    return to_return


def get_file_location(
    _folder_structure: list[str], output_path: str, filepath: str, et: ExifToolHelper
):
    path_destination: str = ""

    folder_structure = get_folder_path(_folder_structure, filepath, et)

    path_destination = os.path.join(*([output_path] + folder_structure))

    if path_destination == "":
        return "Unknown"

    if not os.path.exists(path_destination):
        os.makedirs(path_destination)

    return path_destination


def get_new_file_name(filepath: str, et: ExifToolHelper):
    template: str | None = USER_SETTINGS.get("file_organizer").get("file_name_template")  # type: ignore

    if template == "" or template is None:
        return os.path.basename(filepath)

    base, extension = os.path.splitext(filepath)

    return f"{replace_attr_variables(template, filepath, et)}{extension}"


def make_unique_filename(file_path):
    duplicate_nr = 0
    base, extension = os.path.splitext(file_path)

    while os.path.exists(file_path):
        duplicate_nr += 1
        file_path = f"{base} ({duplicate_nr}){extension}"

    return file_path


def file_organizer(
    filepaths: list[tuple[str, str]], output_path: str, folder_structure: list[str]
):
    with exiftool.ExifToolHelper() as et:
        with progress_bar() as p:
            for path, filename in p.track(
                filepaths, description="Organizing your library:"
            ):
                filepath = os.path.join(path, filename)

                new_file_location = os.path.join(
                    get_file_location(folder_structure, output_path, filepath, et),
                    get_new_file_name(filepath, et),
                )

                new_file_location = os.path.abspath(new_file_location)

                new_file_location = make_unique_filename(new_file_location)

                shutil.move(filepath, new_file_location)
