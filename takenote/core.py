from pathlib import Path
from typing import Any, Dict

from takenote.cli import output


def new_note(settings: Dict[str, Any], note: str, filename: str) -> None:
    """
    New note function. Overwrites any note.

    Parameters
    ----------
    settings: Dict[str, Any]
        Settings object.
    note: str
        Note string.
    filename: str
        Filename to save note under.

    Raises
    ----------
    FileExistsError
        File already exists.
    """
    # Expand user in case '~' is used.
    output_dir = Path(settings["SAVE_PATH_NOTES"]).expanduser()
    filepath = output_dir.absolute() / filename
    if filepath.exists():
        raise FileExistsError(f"File: {filepath}, already exists, and will be overwritten.")
    with filepath.open("w") as file:
        file.write(note)
    output.echo(f"Note saved successfully!\n{filepath}", level=1, fg="green")


def append_note(settings: Dict[str, Any], key: str, note: str) -> None:
    """
    Append to note.

    Parameters
    ----------
    settings: Dict[str, Any]
        Settings object.
    key: str
        Key for path to use as defined in the settings object.
    note: str
        Note string.
    """
    # Get key from settings, expand user in case '~' is used
    filepath = Path(settings["append_notes"][key]).expanduser()
    if filepath.exists():
        output.echo(f"Appending to note!\n{filepath}", level=2, fg="green")
        with filepath.open("a") as file:
            file.write(note)
    else:
        output.echo(f"File doesn't exist: {filepath}", level=0, fg="red")
