import os
from pathlib import Path
from typing import Any, Dict, Optional
import click
from takenote.config import config_file, generate_config_file
from takenote.note import append_to_note, create_note

CONFIG_FILE_NAME = "takenote-config.toml"
APP_DIR = ".tn"
GLOBAL_DIR = Path.home() / APP_DIR
GLOBAL_CONFIG = Path(os.environ.get("TN_ENV")) if "TN_ENV" in os.environ else GLOBAL_DIR / CONFIG_FILE_NAME


def initialise_app_dir(directory: Path) -> None:
    """
    Initialise the directory for app.

    Parameters
    ----------
    directory: Path
        Directory path of app.
    """
    directory.mkdir(exist_ok=True)
    config_path = directory / CONFIG_FILE_NAME
    if not config_path.exists():
        # Write config
        generate_config_file(config_path)


def fetch_settings(local_config: Path) -> Dict[str, Any]:
    """
    Fetches settings. local config is checked to exist, else uses global.

    Parameters
    ----------
    local_config: Path
        File path to local config file.

    Returns
    ----------
    Dict[str, Any]
        Settings dict, from Dynaconf
    """
    if local_config.exists():
        click.echo("Using local settings")
        return config_file([GLOBAL_CONFIG, local_config])
    else:
        click.echo("Using global settings")
        return config_file([GLOBAL_CONFIG])


def new_note(settings: Dict[str, Any], note: str, title: str = None) -> None:
    """
    New note function.

    Parameters
    ----------
    settings: Dict[str, Any]
        Settings object.
    note: str
        Note string.
    title: str
        title string.
    """
    # Expand user in case '~' is used.
    output_dir = Path(settings["save_path_notes"]).expanduser()
    filepath = create_note(output_dir.absolute(), note, title=title)
    click.secho(f"Note saved successfully!\n{filepath}", fg="green")


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
        click.secho(f"Appending to note!\n{filepath}", fg="green")
        append_to_note(filepath, "\n" + note)
    else:
        click.secho(f"File doesn't exist: {filepath}", fg="red")


@click.command()
@click.argument("note", nargs=1, type=str, required=False)
@click.option(
    "-t",
    "--title",
    "title",
    type=str,
    default=None,
    help="Sets the filename of a note.",
)
@click.option(
    "-a",
    "--append",
    "append_key",
    type=str,
    default=None,
    help=f"Use a key as defined by APPEND_NOTES in the {CONFIG_FILE_NAME} file.",
)
@click.option(
    "-gc",
    "--generate-config",
    "generate_config",
    is_flag=True,
    default=False,
    help=f"Use to generate a local config file, path is {CONFIG_FILE_NAME}",
)
@click.option(
    "-p",
    "--path",
    "custom_path",
    default=None,
    help="A specifed path to save a note to, takes precedence over defined settings.",
)
def cli(
    note: str,
    title: str = None,
    append_key: str = None,
    generate_config: bool = False,
    custom_path: Optional[Path] = None,
) -> None:
    """
    Take note CLI program, for those that prefer using the terminal.
    The note has to be wrapped in quotes for single line.

    \b
    Example
    ----------
    tn -gc # Generate config in local directory
    tn "Note"
    tn -t "Title" -- "Note String"
    tn -t "Title" # Opens your favourite editor and saves note on close
    tn -a KEY -- "Note String"
    """
    click.secho("Take note!", fg="magenta")

    # Check for local config
    local = Path.cwd() / APP_DIR
    app_dir = local if not local.exists() and generate_config else GLOBAL_DIR
    initialise_app_dir(app_dir)

    if generate_config:
        return 0  # Don't continue after generating config

    settings = fetch_settings(local / CONFIG_FILE_NAME)
    if custom_path is not None:
        settings["save_path_notes"] = custom_path

    try:
        if note is None:
            note = click.edit()

        if note is None:
            click.echo("No note saved!")
            return 1
        else:
            if append_key:
                append_note(settings, append_key, note)
            else:
                new_note(settings, note, title)
            return 0
    except Exception as e:
        click.secho(f"Error occured:\n{e}", fg="red")


if __name__ == "__main__":
    cli()
