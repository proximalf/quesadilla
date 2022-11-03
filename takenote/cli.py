from pathlib import Path
from typing import Any, Dict
import click
from takenote.config import create_config_file, settings
from takenote.note import append_to_note, create_note


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
    help="Sets the filename of a note.",
)
@click.option(
    "-a",
    "--append",
    "append_key",
    type=str,
    default=None,
    help="Sets the filename of a note.",
)
def cli(
    note: str,
    title: str = None,
    append_key: str = None,
) -> None:
    """
    The note has to be wrapped in quotes for single line.

    Example
    ----------
    tn -t "Title" -- "Note"
    tn "Note"

    """
    click.secho("Take note!", fg="magenta")
    try:
        # Generate settings
        create_config_file()

        if note is None:
            note = click.edit()

        if note is None:
            click.echo("No note saved!")
        else:
            if append_key:
                append_note(settings, append_key, note)
            else:
                new_note(settings, note, title)

    except Exception as e:
        click.secho(f"Error occured:\n{e}", fg="red")
