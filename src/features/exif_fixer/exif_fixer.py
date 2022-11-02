import os
import re
from datetime import datetime
from shutil import copy2

import datefinder
import piexif
from src.constants.constants import DATETAKEN_TEMPLATE
from src.utils.console import bcolors, printProgressBar

img_filename_regex = re.compile(r"^IMG-\d{8}-WA\d{4}\.*\w*")
vid_filename_regex = re.compile(r"^VID-\d{8}-WA\d{4}\.*\w*")


def get_datetime(filename: str, mode: DATETAKEN_TEMPLATE):
    if mode == DATETAKEN_TEMPLATE.WHATSAPP.value:
        if (not bool(img_filename_regex.match(filename))) and (
            not bool(vid_filename_regex.match(filename))
        ):
            return None

        date_str = filename.split("-")[1]
        return datetime.strptime(date_str, "%Y%m%d")
    elif mode == DATETAKEN_TEMPLATE.AUTO.value:
        matches = list(datefinder.find_dates(filename))
        if len(matches) > 0 and isinstance(matches[0], datetime):
            return matches[0]


def get_exif_datestr(datetime: datetime):
    return datetime.strftime("%Y:%m:%d %H:%M:%S")


def modify_filetime(new_time: datetime, filepath: str):
    try:
        modTime = new_time.timestamp()
        os.utime(filepath, (modTime, modTime))
        return True
    except:
        return False


def exif_fixer(
    input_path: str,
    output_path: str,
    filepaths: list[tuple[str, str]],
    fix_datetaken: DATETAKEN_TEMPLATE,
    overwrite_datetaken: bool,
):
    num_files = len(filepaths)

    printProgressBar(
        0, num_files, prefix="Creating new files:", suffix="Complete", length=50
    )

    files_modified = 0
    files_skipped = 0
    files_with_errors = 0

    for i, (path, filename) in enumerate(filepaths):

        if input_path != output_path:
            copy2(input_path + "/" + filename, output_path + "/" + filename)

        filepath = os.path.join(output_path, filename)

        if not os.path.exists(input_path):
            raise Exception("Error copying the file to the output directory")

        printProgressBar(
            i + 1, num_files, prefix="Creating new files:", suffix="Complete", length=50
        )

        file_datetime = get_datetime(filename, fix_datetaken)

        if not file_datetime:
            files_skipped += 1
            continue

        try:
            exif_dict = piexif.load(filepath)

            if (
                exif_dict["Exif"].get(piexif.ExifIFD.DateTimeOriginal)
                and not overwrite_datetaken
            ):
                files_skipped += 1
                continue

            exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal] = get_exif_datestr(
                file_datetime
            )

            exif_bytes = piexif.dump(exif_dict)
            piexif.insert(exif_bytes, filepath)

            if overwrite_datetaken:
                if not modify_filetime(file_datetime, filepath):
                    files_with_errors += 1

            files_modified += 1

        except piexif.InvalidImageDataError:
            if not overwrite_datetaken:
                files_skipped += 1
            else:
                if modify_filetime(file_datetime, filepath):
                    files_modified += 1
                else:
                    files_with_errors += 1
            continue
        except:
            if not overwrite_datetaken:
                files_skipped += 1
            else:
                if modify_filetime(file_datetime, filepath):
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
