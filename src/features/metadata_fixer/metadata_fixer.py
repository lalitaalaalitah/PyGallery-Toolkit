import os
from datetime import datetime
from typing import Any, Literal

import exiftool
import filedate
from rich.table import Table

from src.constants.datetaken_templates import FILENAMES
from src.utils.rich_console import console, print_log, progress_bar


def get_datetime_from_filename(filename: str):
    """Get the datetime of the file based on its name.

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


FileStatus = Literal["updated"] | Literal["skipped"] | Literal["error"]


def get_filedate(
    way: Literal["filename"] | Literal["filedate"], filename: str, filepath: str
):
    if way == "filename":
        return get_datetime_from_filename(filename)

    elif way == "filedate":
        return datetime.fromtimestamp(
            os.path.getctime(filepath) or os.path.getmtime(filepath)
        )


def metadata_fixer(
    filepaths: list[tuple[str, str]],
    overwrite_datetime: bool,
    fill_missing_datetime_info_from: list[Literal["filename"] | Literal["filedate"]],
):
    console.print(
        f"[blue bold][INFO]:[/blue bold] Starting the datetime-fixer with the force mode {'enabled' if overwrite_datetime else 'disabled'}.\n"
    )

    results: list[FileStatus] = []

    with exiftool.ExifToolHelper() as et:
        with progress_bar() as p:
            for path, filename in p.track(filepaths, description="Fixing metadata:"):
                filepath = os.path.join(path, filename)

                file_status: FileStatus = "skipped"

                metadata: dict[str, Any] = et.get_metadata(filepath)[0]

                # ------------------------------------------------- #
                # ------------- DATETIME EXIF FIXER --------------- #
                # ------------------------------------------------- #

                """ We should edit the dates if the force mode is enabled or if no DateTimeOriginal tag is in the metadata"""
                shouldEditDates = (
                    overwrite_datetime
                    or sum(
                        1
                        for key in metadata.keys()
                        if len(key.split(":")) > 1
                        and key.split(":")[1] == "DateTimeOriginal"
                    )
                    == 0
                )

                if shouldEditDates:
                    file_datetime: datetime | None = None

                    for datimegetter in fill_missing_datetime_info_from:
                        # Get the filedate based on the user settings
                        if file_datetime is None:
                            file_datetime = get_filedate(
                                datimegetter, filename, filepath
                            )

                    if file_datetime:
                        try:
                            et.set_tags(
                                filepath,
                                {
                                    "DateTimeOriginal": get_exif_datestr(file_datetime),
                                    "CreateDate": get_exif_datestr(file_datetime),
                                },
                                params=["-overwrite_original"],
                            )

                            print_log(
                                f"[green]\u2714[/green] File {filename} -> DateTime metadata updated"
                            )

                            file_status = "updated"

                        except:
                            print_log(
                                f"[red]\u2716[/red] File {filename} -> Error while trying to update the datetime"
                            )

                            file_status = "error"

                            continue

                    else:
                        print_log(
                            f"[orange1]\u2714[/orange1] File {filename} -> Skipped (date can not be found)"
                        )

                else:
                    """print_log(
                        f"[orange1]\u2714[/orange1] File {filename} -> Skipped (dateTimeOriginal already in metadata)"
                    )"""

                # ------------------------------------------------- #
                # ---------------- GPS EXIF FIXER ----------------- #
                # ------------------------------------------------- #

                if (
                    metadata.get("Composite:GPSPosition") is not None
                    and sum(
                        1
                        for key in metadata.keys()
                        if len(key.split(":")) > 0 and key.split(":")[0] == "QuickTime"
                    )
                    > 0
                    and metadata.get("QuickTime:GPSCoordinates") is None
                ):
                    gps_position = str(metadata.get("Composite:GPSPosition")).split(" ")
                    new_latitude = round(float(gps_position[0]), 4)
                    new_longitude = round(float(gps_position[1]), 4)

                    # print(gps_position, new_latitude, new_longitude)

                    try:
                        et.set_tags(
                            filepath,
                            {
                                "QuickTime:GPSCoordinates": " ".join(
                                    [
                                        str(new_latitude),
                                        str(new_longitude),
                                    ]
                                ),
                            },
                            params=["-overwrite_original"],
                        )

                        print_log(
                            f"[green]\u2714[/green] File {filename} -> GPS metadata updated"
                        )

                        file_status = "updated"

                    except:
                        print_log(
                            f"[red]\u2716[/red] File {filename} -> Error while trying to update the GPS data"
                        )

                        file_status = "error"

                        continue

                results.append(file_status)

    console.print(
        "[green bold][OK]:[/green bold] All files have been successfully processed!\n"
    )

    # ---- PRINT THE RESULTS ---- #

    table = Table(
        title="Results",
        show_header=False,
        show_lines=True,
        title_justify="left",
    )

    table.add_column(no_wrap=True)
    table.add_column(justify="right", style="bold")

    table.add_row(
        "[green]\u2714[/green] Files with new/updated metadata",
        f"{results.count('updated')}",
    )
    table.add_row(
        "[orange1]\u2714[/orange1] Files skipped", f"{results.count('skipped')}"
    )
    table.add_row("[red]\u2716[/red] Files with error", f"{results.count('error')}")

    console.print(table)
