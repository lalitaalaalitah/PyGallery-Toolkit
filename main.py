import argparse

from src.constants.datetaken_templates import FIX_DATETIME_MODE
from src.entry_point import main

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Restore discarded Exif date information in WhatsApp media based on the filename. For videos, only the created and modified dates are set",
        add_help=True,
        exit_on_error=True,
    )

    parser.add_argument("--input_path", type=str, help="Path to the images to proccess")
    parser.add_argument(
        "--output_path",
        type=str,
        help="Path to save the proccessed images. If it is the same as the input_path the images will be overwritten in that same directory",
    )

    parser.add_argument(
        "--recursive",
        action=argparse.BooleanOptionalAction,
        required=False,
        help="Recursively process media (look for media in all the subfolders of the input_path) or not.\nDefaults to True (--recursive)",
    )
    parser.set_defaults(recursive=True)

    parser.add_argument(
        "--fix_datetaken_mode",
        choices=list(map(lambda x: x.value, FIX_DATETIME_MODE._member_map_.values())),
        required=False,
        default=FIX_DATETIME_MODE.NO_OVERWRITE.value,
        help="File metadata update/correction mode",
    )

    parser.add_argument(
        "--hash_size",
        type=int,
        required=False,
        default=64,
        help="Hash size. Used for identification of similar images. With larger values the search will be more exhaustive but slower. Giving a value of 0 skips the search for duplicates/similar altogether. Defaults to 64",
    )

    parser.add_argument(
        "--similarity",
        type=int,
        required=False,
        default=99,
        help="Similarity of the images to be deleted by the user (always after being asked during the process). It is a number from 0 to 100, with 100 being the number to pass when we want only completely identical images to appear. This parameter does not affect the speed of the process, as does --hash_size. Defaults to 99",
    )

    parser.add_argument(
        "--folder_structure",
        type=str,
        required=False,
        default="year>month",
        help="Folder tree in which your files will be organized based on their metadata. By default it is 'year>month', that is, first folders will be created with the years of the files, and within these, folders with the months. Within each month the corresponding files will be located. You can find more information about how to customize your organization in the github repo",
    )

    args = parser.parse_args()

    main(
        args.input_path,
        args.output_path,
        args.recursive,
        args.fix_datetaken_mode,
        args.hash_size,
        args.similarity,
        args.folder_structure,
    )
