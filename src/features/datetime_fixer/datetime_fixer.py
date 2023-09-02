import os
from datetime import datetime

import filedate
import piexif
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


def datetime_fixer(
    filepaths: list[tuple[str, str]],
    force_fix: bool,
):
    console.print(
        f"[blue bold][INFO]:[/blue bold] Starting the datetime-fixer with the force mode {'enabled' if force_fix else 'disabled'}.\n"
    )

    files_modified = 0
    files_skipped = 0
    files_with_errors = 0

    with progress_bar() as p:
        for path, filename in p.track(filepaths, description="Fixing metadata:"):
            filepath = os.path.join(path, filename)

            file_datetime = get_datetime_from_filename(filename)

            if not file_datetime:
                files_skipped += 1
                print_log(
                    f"[orange1]\u2714[/orange1] File {filename} -> Skipped (date can not be found in its name)"
                )
                continue

            try:
                exif_dict = piexif.load(filepath)

                if (not force_fix) and exif_dict["Exif"].get(
                    piexif.ExifIFD.DateTimeOriginal
                ):
                    files_skipped += 1
                    print_log(
                        f"[orange1]\u2714[/orange1] File {filename} -> Skipped (datetaken already in exif)"
                    )
                    continue

                exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal] = get_exif_datestr(
                    file_datetime
                )

                exif_bytes = piexif.dump(exif_dict)
                piexif.insert(exif_bytes, filepath)

                if force_fix:
                    if not modify_filetime(file_datetime, filepath):
                        files_with_errors += 1
                        console.print(
                            f"[red][LOG]:[/red] [green]\u2716[/green] File {filename} -> Error: Modify date can not be setted"
                        )

                files_modified += 1
                print_log(f"[green]\u2714[/green] File {filename} -> Metadata updated")

            except piexif.InvalidImageDataError:
                if not force_fix:
                    files_skipped += 1
                    print_log(
                        f"[orange1]\u2714[/orange1] File {filename} -> Skipped (creation date already in file info)"
                    )
                else:
                    if modify_filetime(file_datetime, filepath):
                        print_log(
                            f"[green]\u2714[/green] File {filename} -> File creation date updated"
                        )
                        files_modified += 1
                    else:
                        files_with_errors += 1
                        console.print(
                            f"[red][LOG]:[/red] [green]\u2716[/green] File {filename} -> Error: Modify date can not be setted"
                        )
                continue
            except:
                if not force_fix:
                    files_skipped += 1
                else:
                    if modify_filetime(file_datetime, filepath):
                        files_modified += 1
                        print_log(
                            f"[green]\u2714[/green] File {filename} -> File creation date updated"
                        )
                    else:
                        files_with_errors += 1
                        console.print(
                            f"[red][LOG]:[/red] [green]\u2716[/green] File {filename} -> Error: Modify date can not be setted"
                        )
                continue

    console.print(
        "[green bold][OK]:[/green bold] All files have been successfully processed!\n"
    )

    table = Table(
        title="Results",
        show_header=False,
        show_lines=True,
        title_justify="left",
    )

    table.add_column(no_wrap=True)
    table.add_column(justify="right", style="bold")

    table.add_row(
        "[green]\u2714[/green] Files with new/updated metadata", f"{files_modified}"
    )
    table.add_row("[orange1]\u2714[/orange1] Files skipped", f"{files_skipped}")
    table.add_row("[red]\u2716[/red] Files with error", f"{files_with_errors}")

    console.print(table)
