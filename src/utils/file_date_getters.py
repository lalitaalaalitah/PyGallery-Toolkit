import os
from datetime import datetime
from typing import Any, Literal

from exiftool import ExifToolHelper

from src.constants.datetaken_templates import (
    FILENAME_DATE_MAX,
    FILENAME_DATE_MIN,
    FILENAMES,
)


def get_datetime_from_filename(filename: str):
    """Get the datetime of the file based on its name.

    Solution for managing the suffix thanks to: https://stackoverflow.com/questions/5045210/how-to-remove-unconverted-data-from-a-python-datetime-object
    """

    end_date: datetime | None = None

    for date_format in FILENAMES:
        try:
            end_date = datetime.strptime(filename, date_format)
            break
        except ValueError as v:
            ulr = len(v.args[0].partition("unconverted data remains: ")[2])
            if ulr:
                try:
                    end_date = datetime.strptime(filename[:-ulr], date_format)
                    break
                except:
                    continue
            else:
                continue

    if end_date is not None and (
        end_date.year < FILENAME_DATE_MIN or end_date.year > FILENAME_DATE_MAX
    ):
        return None

    return end_date


def get_date_from_os(filepath: str):
    return min(
        datetime.fromtimestamp(os.path.getctime(filepath)),
        datetime.fromtimestamp(os.path.getmtime(filepath)),
    )


def get_date_from_exif(filepath: str, et: ExifToolHelper):
    """Get the datetime of the file based on its metadata."""

    metadata: dict[str, Any] = et.get_metadata(filepath)[0]

    # print(json.dumps(str(metadata)))

    keys = [
        "EXIF:DateTimeOriginal",
        "XMP:DateTimeOriginal",
        "QuickTime:CreateDate",
        "EXIF:CreateDate",
        "EXIF:ModifyDate",
    ]

    for key in keys:
        if metadata.get(key):
            return datetime.strptime(
                str(metadata.get(key)),
                "%Y:%m:%d %H:%M:%S",
            )


def get_filedate(
    way: Literal["filename"] | Literal["filedate"] | Literal["fileexif"],
    filename: str,
    filepath: str,
    et: ExifToolHelper,
):
    if way == "filename":
        return get_datetime_from_filename(filename)

    elif way == "filedate":
        return get_date_from_os(filepath)

    else:
        return get_date_from_exif(filepath, et)


def get_datefile_to_organize(filepath: str, et: ExifToolHelper):
    """Get the datetime of the file based on its metadata. If we can not found the date in file metadata, the file OS date will be used"""

    try:
        to_return = get_date_from_exif(filepath, et)

    except:
        return get_date_from_os(filepath)

    if not to_return:
        to_return = get_date_from_os(filepath)

    return to_return
