import os
from datetime import datetime
from shutil import copy2

from src.constants.constants import (
    DATETAKEN_TEMPLATE,
    IMG_EXTENSIONS,
    OTHER_ALLOWED_EXTENSIONS,
    VIDEO_EXTENSIONS,
)
from src.features.duplicates_remover.duplicates_remover import duplicates_remover
from src.features.exif_fixer.exif_fixer import exif_fixer
from src.utils.console import bcolors, printProgressBar


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
    return [(fp, fn) for fp, fn in filepaths if os.path.splitext(fn)[-1] in allowed_ext]


def main(
    input_path: str,
    output_path: str,
    recursive: bool,
    fix_datetaken: DATETAKEN_TEMPLATE,
    overwrite_datetaken: bool,
    hash_size: int,
    similarity: int,
):
    print()

    if not os.path.exists(input_path):
        raise FileNotFoundError("Path specified does not exist")

    if not os.path.isdir(input_path):
        raise TypeError("Path specified is not a directory")

    # Creating output directory if not exists
    path_full_destination = os.path.join(os.getcwd(), output_path)
    if not os.path.exists(path_full_destination):
        os.makedirs(path_full_destination)

    filepaths = get_filepaths(input_path, recursive)

    print(
        bcolors.BLUE
        + "\u2731"
        + bcolors.ENDC
        + f" {len(filepaths)} files scanned in the target directory"
    )

    filepaths = filter_filepaths(
        filepaths,
        allowed_ext=set(IMG_EXTENSIONS + VIDEO_EXTENSIONS + OTHER_ALLOWED_EXTENSIONS),
    )
    num_files = len(filepaths)

    if len(filepaths) == 0:
        print(
            bcolors.BLUE
            + "\u2731"
            + bcolors.ENDC
            + " No usefull files for the gallery has been found. Exiting..."
        )
        print()

    print(
        bcolors.BLUE
        + "\u2731"
        + bcolors.ENDC
        + f" {num_files} of that files has a valid extension ({100 * num_files / len(filepaths)}%), and will be copied to the output directory"
    )
    print()

    exif_fixer(input_path, output_path, filepaths, fix_datetaken, overwrite_datetaken)

    duplicates_remover(
        filter_filepaths(
            get_filepaths(output_path, recursive),
            allowed_ext=set(IMG_EXTENSIONS),
        ),
        hash_size,
        similarity,
    )
