import argparse
from ast import arg

from src.constants.constants import DATETAKEN_TEMPLATE
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
        "--fix_datetaken",
        choices=list(map(lambda x: x.value, DATETAKEN_TEMPLATE._member_map_.values())),
        required=False,
        help="If this parameter is specified, it will try to restore datetime data for the images by extracting them from the filename. This parameter accepts the 'whatsapp' option, which is useful if we only want to correct the dates of the files coming from this app, or the 'auto' option, which will try to correct any file whose date is in its file name.",
    )

    parser.add_argument(
        "--overwrite_datetaken",
        action=argparse.BooleanOptionalAction,
        help="Overwrite or not the EXIF capture date tag and the file creation datetime. Only applies if the fix-datetaken option has been specified. By default this option is disabled (--no-overwrite-datetaken), that is, the metadata will not be overwritten if it already exists",
    )
    parser.set_defaults(overwrite_datetaken=False)

    parser.add_argument(
        "--hash_size",
        type=int,
        required=False,
        default=64,
        help="Hash size. Used for identification of similar images. The larger the search will be more exhaustive but slower. Giving a value of 0 skips the search for duplicates/similar altogether. Defaults to 64",
    )

    parser.add_argument(
        "--similarity",
        type=int,
        required=False,
        default=99,
        help="Similarity of the images to be deleted by the user (always after being asked during the process). It is a number from 0 to 100, with 100 being the number to pass when we want only completely identical images to appear. This parameter does not affect the speed of the process, as does --hash_size. Defaults to 99",
    )

    args = parser.parse_args()

    main(
        args.input_path,
        args.output_path,
        args.recursive,
        args.fix_datetaken,
        args.overwrite_datetaken,
        args.hash_size,
        args.similarity
    )
