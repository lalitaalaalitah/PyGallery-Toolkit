import os
from datetime import datetime
from shutil import copy2

import filedate
import piexif
from src.constants.datetaken_templates import FILENAMES, FIX_DATETIME_MODE
from src.utils.console import bcolors, printProgressBar


def get_datetime(filename: str):
    """Get the datetime of the file based on the name.

    Solution for managing the suffix thanks to: https://stackoverflow.com/questions/5045210/how-to-remove-unconverted-data-from-a-python-datetime-object
    """

    for date_format in FILENAMES:
        try:
            end_date = datetime.strptime(filename, date_format)
            return end_date
        except ValueError as v:
            ulr = len(v.args[0].partition("unconverted data remains: ")[2])
            if ulr:
                try:
                    end_date = datetime.strptime(filename[:-ulr], date_format)
                    return end_date
                except:
                    continue
            else:
                continue


def get_exif_datestr(datetime: datetime):
    return datetime.strftime("%Y:%m:%d %H:%M:%S")


def modify_filetime(new_time: datetime, filepath: str):
    try:
        date_str = new_time.strftime("%m/%d/%Y %H:%M:%S")
        filedate.File(filepath).set(
            created=date_str,
        )
        return True
    except:
        return False


def exif_fixer(
    input_path: str,
    output_path: str,
    filepaths: list[tuple[str, str]],
    fix_datetaken_mode: FIX_DATETIME_MODE,
):
    num_files = len(filepaths)

    printProgressBar(
        0, num_files, prefix="Creating new files:", suffix="Complete", length=50
    )

    files_modified = 0
    files_skipped = 0
    files_with_errors = 0

    for i, (path, filename) in enumerate(filepaths):

        new_filepath = ""

        if input_path != output_path:
            copy2(os.path.join(path, filename), output_path + "/" + filename)

            new_filepath = os.path.join(output_path, filename)

        if new_filepath == "":
            new_filepath = os.path.join(path, filename)

        if not os.path.exists(new_filepath):
            raise Exception("Error copying the file to the output directory")

        printProgressBar(
            i + 1, num_files, prefix="Creating new files:", suffix="Complete", length=50
        )

        if fix_datetaken_mode == FIX_DATETIME_MODE.NEVER.value:
            files_skipped += 1
            continue

        file_datetime = get_datetime(filename)

        if not file_datetime:
            files_skipped += 1
            continue

        try:
            exif_dict = piexif.load(new_filepath)

            if (
                exif_dict["Exif"].get(piexif.ExifIFD.DateTimeOriginal)
                and fix_datetaken_mode == FIX_DATETIME_MODE.NO_OVERWRITE.value
            ):
                files_skipped += 1
                continue

            exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal] = get_exif_datestr(
                file_datetime
            )

            exif_bytes = piexif.dump(exif_dict)
            piexif.insert(exif_bytes, new_filepath)

            if fix_datetaken_mode == FIX_DATETIME_MODE.OVERWRITE.value:
                if not modify_filetime(file_datetime, new_filepath):
                    files_with_errors += 1

            files_modified += 1

        except piexif.InvalidImageDataError:
            if fix_datetaken_mode == FIX_DATETIME_MODE.NO_OVERWRITE.value:
                files_skipped += 1
            else:
                if modify_filetime(file_datetime, new_filepath):
                    files_modified += 1
                else:
                    files_with_errors += 1
            continue
        except:
            if fix_datetaken_mode == FIX_DATETIME_MODE.NO_OVERWRITE.value:
                files_skipped += 1
            else:
                if modify_filetime(file_datetime, new_filepath):
                    files_modified += 1
                else:
                    files_with_errors += 1
            continue

    print()
    print(
        bcolors.BLUE
        + "\u2731"
        + bcolors.ENDC
        + " All files have been successfully processed!"
    )
    print()
    print("Results:")
    print(
        bcolors.GREEN
        + "\u2714"
        + bcolors.ENDC
        + f" {files_modified} file{'s' if files_modified != 1 else ''} have been copied with updated/fixed metadata"
    )
    print(
        bcolors.WARNING
        + "\u2714"
        + bcolors.ENDC
        + f" {files_skipped} file{'s' if files_skipped != 1 else ''} have been copied without changes in their metadata for not meeting the specified parameters"
    )
    print(
        bcolors.FAIL
        + "\u2714"
        + bcolors.ENDC
        + f" {files_with_errors} file{'s' if files_with_errors != 1 else ''} have been copied without changes in their metadata for some type of error"
    )

    print()
