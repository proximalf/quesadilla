import os
from pathlib import Path
from typing import Any, Dict
import click
from takenote.config import config_file, generate_config_file
from takenote.note import append_to_note, create_note

CONFIG_FILE_NAME = "takenote-config.toml"
GLOBAL_DIR = Path.home() / ".tn"
GLOBAL_CONFIG = Path(os.environ.get("TN_ENV")) if "TN_ENV" in os.environ else GLOBAL_DIR / CONFIG_FILE_NAME


def new_note(settings: Dict[str, Any], note: str, title: str = None) -> None:
    """New note function."""
    # Expand user in case '~' is used.
    output_dir = Path(settings["save_path_notes"]).expanduser()
    filepath = create_note(output_dir.absolute(), note, title=title)
    click.secho(f"Note saved successfully!\n{filepath}", fg="green")


def append_note(settings: Dict[str, Any], key: str, note: str) -> None:
    """Append to note."""
    filepath = Path(settings["append_notes"][key])
    click.secho(f"Appending to note!\n{filepath}", fg="green")
    append_to_note(filepath, "\n" + note)


def initialise_app_dir(directory: Path) -> None:
    """
    Initialise the global directory for app.

    Parameters
    ----------
    directory: Path
        Directory path of app.
    """
    directory.mkdir(exist_ok=True)
    generate_config_file(directory / CONFIG_FILE_NAME)


def fetch_settings(generate_config: bool) -> Dict[str, Any]:
    """
    Fetches settings.

    Parameters
    ----------
    generate_config: bool
        Flag requires setting to generate config.

    Returns
    ----------
    Dict[str, Any]
        Settings dict, from Dynaconf
    """
    # Generate settings, check for local
    local_config = Path().cwd() / CONFIG_FILE_NAME

    if not local_config.exists() and generate_config:
        click.secho(f"Generated config file: {local_config}", fg="blue")
        generate_config_file(local_config)

    if local_config.exists():
        click.echo("Using local settings")
        return config_file([GLOBAL_CONFIG, local_config])
    else:
        click.echo("Using global settings")
        return config_file([GLOBAL_CONFIG])


@click.command()
@click.argument("note", nargs=1, type=str, required=False)
@click.option(
    "-t",
    "--title",
    "title",
    type=str,
    default=None,
    help="Sets the filename of a note. Saves as per definition in config file.",
)
@click.option(
    "-a",
    "--append",
    "append_key",
    type=str,
    default=None,
    help="Use a key as defined by APPEND_NOTES in the tn-config file.",
)
@click.option("-gc", "--generate-config", is_flag=True, default=False, help="Use to generate a local config file.")
def cli(note: str, title: str = None, append_key: str = None, generate_config: bool = False) -> None:
    """
    The note has to be wrapped in quotes for single line.

    \b
    Example
    ----------
    tn -t "Title" -- "Note"
    tn "Note"

    """
    click.secho("Take note!", fg="magenta")

    initialise_app_dir(GLOBAL_DIR)

    settings = fetch_settings(generate_config)
    if generate_config:
        return 0  # Don't continue after generating config

    try:
        if note is None:
            note = click.edit()

        if note is None:
            click.echo("No note saved!")
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
