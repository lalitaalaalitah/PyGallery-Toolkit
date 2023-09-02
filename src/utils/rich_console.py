from rich.console import Console
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)

from src.constants.user_settings import USER_SETTINGS

console = Console(highlight=False)
__err_console = Console(stderr=True, log_time=False, log_path=False)


def progress_bar():
    return Progress(
        TextColumn("{task.description}"),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        BarColumn(
            style="white", complete_style="green bold", finished_style="green bold"
        ),
        MofNCompleteColumn(),
        TextColumn("•"),
        TimeElapsedColumn(),
        # TextColumn("•"),
        # TimeRemainingColumn(),
        TextColumn("\n"),
        console=console,
    )


def print_separator(title: str):
    print()
    console.rule(f"[bold dark_green on white]  {title}  ")
    print()


def print_warn(title: str):
    console.print(f"\n[orange1 bold][WARN]:[/orange1 bold][navajo_white1] {title}")


def print_log(title: str, start=""):
    if USER_SETTINGS.get("extended_logger") is True:
        console.print(f"{start}[light_steel_blue][LOG]:[/light_steel_blue] {title}")


def print_error(title: str, descr: str | None = None, finishExecution: bool = True):
    print()
    __err_console.log(f"[red bold][ERROR]: [/red bold][red]{title}")
    print()

    if descr is not None:
        __err_console.print(f"[#FFB5B5 italic]{descr}")

    if finishExecution:
        quit(1)
    else:
        print()
