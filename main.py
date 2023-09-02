import json
from pathlib import Path
from time import sleep

import jsonschema
from jsonschema import validate
from rich import box
from rich.panel import Panel

from src.constants import allowed_extensions
from src.constants.user_settings import USER_SETTINGS
from src.entry_point import main
from src.utils.rich_console import console, print_error, print_warn

if __name__ == "__main__":
    print()
    console.print(
        Panel.fit(
            "Created with ❤ by [link=https://github.com/enrique-lozano]Enrique Lozano[/] and maintened by the Open Source community.",
            box=box.ROUNDED,
            padding=(1, 2),
            title="[b blue]Thanks for trying out PyGallery!",
            border_style="bright_blue",
        ),
        justify="center",
    )

    sleep(1.5)

    console.print(
        "\n[blue bold][INFO]:[/blue bold] Starting the program... Get ready to organize your local gallery!!!"
    )

    sleep(0.5)

    try:
        validate(
            instance=USER_SETTINGS,
            schema=json.loads(Path("settings/settings_schema.json").read_text()),
        )
    except jsonschema.ValidationError:
        print_error(
            title="Error validating your config file.",
            descr="Please check that your config file is correct. Your config file (in [u]settings/user_settings.yaml[/u]) should match the schema defined in our [u]settings/settings_schema.json[/u]. To match the required schema, we recommend to use an IDE like VSCode to display the errors on the yaml file",
        )

    if (
        USER_SETTINGS.get("include_all_files") is True
        and allowed_extensions.OTHER_ALLOWED_EXTENSIONS is not None
    ):
        print_warn(
            "The [i]include_extra_formats[/i] option will have no effect since all the files will be parsed (the option [i]include_all_files[/i] is true). You can remove this option from your config file if you want."
        )

    console.print("\n[green bold][OK]:[/green bold] User config readed successfully.")

    main(
        input_path=USER_SETTINGS.get("input_path"),  # type: ignore
        output_path=USER_SETTINGS.get("output_path"),  # type: ignore
        force_datetime_fix=USER_SETTINGS.get("datetime_fixer").get("force"),  # type: ignore
        hash_size=USER_SETTINGS.get("duplicates_search").get("hash_size"),  # type: ignore
        similarity=USER_SETTINGS.get("duplicates_search").get("similarity"),  # type: ignore
        folder_structure=USER_SETTINGS.get("file_organizer").get("folder_structure"),  # type: ignore
    )
