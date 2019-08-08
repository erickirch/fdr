# --- Standard Library Imports ------------------------------------------------
import time
import tkinter as tk
from pathlib import Path
from tkinter import filedialog

# --- Third Party Imports -----------------------------------------------------
import click

# --- Intra-Package Imports ---------------------------------------------------
from rtm.main import exceptions as exc
from rtm.main.exceptions import RTMValidatorError
from rtm.main.rtm_worksheet import RTMWorksheet


def validate(path_option='default'):

    click.clear()
    click.echo(
        "\nWelcome to the DePuy Synthes Requirements Trace Matrix (RTM) Validator."
        "\nPlease select an RTM excel file you wish to test_validate."
    )

    time.sleep(1)
    try:
        path = get_rtm_path(path_option)
        worksheet = RTMWorksheet(path)
        worksheet.validate()
    except RTMValidatorError as e:
        click.echo(e)

    click.echo(
        "\nThank you for using the RTM Validator."
        "\nIf you have questions or suggestions, please contact a Roebling team member."
    )


def get_rtm_path(path_option='default') -> Path:
    if path_option == 'default':
        path = get_new_path_from_dialog()
        required_extensions = '.xlsx .xls'.split()
        if str(path) == '.':
            raise exc.RTMValidatorFileError("\nError: You didn't select a file")
        if path.suffix not in required_extensions:
            raise exc.RTMValidatorFileError(
                f"\nError: You didn't select a file with "
                f"a proper extension: {required_extensions}"
            )
        click.echo(f"\nThe RTM you selected is {path}")
        return path
    elif isinstance(path_option, Path):
        return path_option


def get_new_path_from_dialog() -> Path:
    root = tk.Tk()
    root.withdraw()
    path = Path(filedialog.askopenfilename())
    return path


if __name__ == "__main__":
    validate()
