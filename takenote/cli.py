from pathlib import Path
from typing import Any, Dict
import click
from takenote.config import config_file
from takenote.note import append_to_note, create_note

CONFIG_FILE_NAME = "tn-config.toml"
GLOBAL_CONFIG_FILE = Path(f"~/.config/{CONFIG_FILE_NAME}").expanduser()


def new_note(settings: Dict[str, Any], note: str, title: str = None) -> None:
    """New note function."""
    output_dir = Path(settings["save_path_notes"])
    filepath = create_note(output_dir, note, title=title)
    click.secho(f"Note saved successfully!\n{filepath}", fg="green")


def append_note(settings: Dict[str, Any], key: str, note: str) -> None:
    """Append to note."""
    filepath = Path(settings["append_notes"][key])
    click.secho(f"Appending to note!\n{filepath}", fg="green")
    append_to_note(filepath, "\n" + note)


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
@click.option("--generate-config", is_flag=True, default=False, help="Use to generate a local config file.")
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
    try:
        # Generate settings, check for local
        local_config = Path().cwd() / CONFIG_FILE_NAME

        if local_config.exists():
            config_path = local_config
        else:
            config_path = GLOBAL_CONFIG_FILE
            click.echo("Using global settings")

        settings = config_file(config_path, generate_config)
        if generate_config:
            return 0

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
