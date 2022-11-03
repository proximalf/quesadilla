from pathlib import Path
import click
from takenote.config import create_config_file, settings
from takenote.note import create_note


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
def cli(note: str, title: str) -> None:
    """
    The note has to be wrapped in quotes for single line.

    Example
    ----------
    tn -t "Title" -- "Note"
    tn "Note"

    """
    click.secho("Take note!", fg="green")
    try:
        # Generate settings
        create_config_file()
        output_dir = Path(settings["save_path_notes"])

        if note is None:
            note = click.edit()

        if note is not None:
            create_note(output_dir, note)
            click.secho("Note saved successfully!", fg="green")
        else:
            click.echo("No note saved!")

    except Exception as e:
        click.secho(f"Error occured:\n{e}", fg="red")
