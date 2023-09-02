import os
from shutil import copy2

from src.constants.allowed_extensions import (
    IMG_EXTENSIONS,
    OTHER_ALLOWED_EXTENSIONS,
    VIDEO_EXTENSIONS,
)
from src.constants.user_settings import USER_SETTINGS
from src.features.duplicates_remover.duplicates_remover import duplicates_remover
from src.features.exif_fixer.exif_fixer import datetime_fixer
from src.features.file_organizer.file_organizer import file_organizer
from src.utils import rich_console
from src.utils.rich_console import console, print_error, print_separator, progress_bar


def get_filepaths(path: str, recursive: bool):
    all_filepaths: list[tuple[str, str]] = []

    if not recursive:
        abspath = os.path.abspath(path)
        all_filepaths += [
            (abspath, f)
            for f in os.listdir(abspath)
            if os.path.isfile(os.path.join(abspath, f))
        ]

    else:
        for dirpath, dirnames, filenames in os.walk(path):
            abspath = os.path.abspath(dirpath)
            all_filepaths += [(abspath, f) for f in filenames]

    return all_filepaths


def filter_filepaths(filepaths: list[tuple[str, str]], allowed_ext: set[str]):
    return [
        (fp, fn)
        for fp, fn in filepaths
        if os.path.splitext(fn)[-1].lower() in allowed_ext
    ]


def main(
    input_path: str,
    output_path: str,
    force_datetime_fix: bool,
    hash_size: int,
    similarity: int,
    folder_structure: list[str],
):
    if not os.path.exists(input_path):
        print_error(
            title="The input path specified does not exist.",
            descr=f"Modify your config file or create a folder called {input_path} in this directory and add some photos to start.",
        )

    if not os.path.isdir(input_path):
        print_error(
            title="The input path specified is not a directory",
            descr=f"Modify your config file or create a folder called {input_path} in this directory and add some photos to start.",
        )

    print()

    # Creating output directory if not exists
    path_full_destination = os.path.join(os.getcwd(), output_path)
    if not os.path.exists(path_full_destination):
        os.makedirs(path_full_destination)
        rich_console.console.print(
            "[blue bold][INFO]:[/blue bold] Output directory not found. A new one has been created"
        )

    # Wheter the search is recursive in the input folder
    recursive: bool = USER_SETTINGS.get("recursive")  # type: ignore

    filepaths_to_copy = get_filepaths(input_path, recursive)

    console.print(
        f"[blue bold][INFO]:[/blue bold] {len(filepaths_to_copy)} files scanned in the target directory"
    )

    if not USER_SETTINGS.get("include_all_files"):
        filepaths_to_copy = filter_filepaths(
            filepaths_to_copy,
            allowed_ext=set(
                IMG_EXTENSIONS + VIDEO_EXTENSIONS + OTHER_ALLOWED_EXTENSIONS
                if OTHER_ALLOWED_EXTENSIONS is not None
                else []
            ),
        )

    if len(filepaths_to_copy) == 0:
        console.print(
            "[blue bold][INFO]:[/blue bold] No usefull files for your new organized gallery has been found. Exiting..."
        )
        print()
        quit()

    if not USER_SETTINGS.get("include_all_files"):
        console.print(
            f"[blue bold][INFO]:[/blue bold] {len(filepaths_to_copy)} of that files ({round(100 * len(filepaths_to_copy) / len(get_filepaths(input_path, recursive)),2)}%) have an allowed format, and will be copied to the output directory",
        )
    else:
        console.print(
            f"[blue bold][INFO]:[/blue bold] All the files will be copied to the output directory since the [i]include_all_files[/i] option is true",
        )

    print()

    with progress_bar() as p:
        for path, filename in p.track(
            filepaths_to_copy, description=f"Copying files to [i]./{output_path}[/i]:"
        ):
            new_filepath = ""

            if input_path != output_path:
                copy2(os.path.join(path, filename), output_path + "/" + filename)

                new_filepath = os.path.join(output_path, filename)

            if new_filepath == "":
                new_filepath = os.path.join(path, filename)

            if not os.path.exists(new_filepath):
                raise Exception("Error copying the file to the output directory")

    if USER_SETTINGS.get("datetime_fixer").get("enabled"):  # type: ignore
        print_separator("Datetime fixer")
        datetime_fixer(filepaths_to_copy, force_datetime_fix)

    if USER_SETTINGS.get("file_organizer").get("enabled"):  # type: ignore
        print_separator("Organize files")
        file_organizer(get_filepaths(output_path, True), output_path, folder_structure)

    if USER_SETTINGS.get("duplicates_search").get("enabled"):  # type: ignore
        print_separator("Duplicates search")
        duplicates_remover(
            filter_filepaths(
                get_filepaths(output_path, True),
                allowed_ext=set(IMG_EXTENSIONS),
            ),
            hash_size,
            similarity,
        )

    print()
    console.print("[green bold]\u2714 All done! Your gallery is ready!")
