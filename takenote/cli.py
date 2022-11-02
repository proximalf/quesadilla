from pathlib import Path
import click
from takenote.config import create_config_file, settings
from takenote.lib import zettelkasten


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

        if title is not None:
            file_path = output_dir / title
        else:
            # Can't save a file without a title/filepath.
            zettel = zettelkasten()
            click.echo(f"no title provided, saved under {zettel} instead")
            file_path = output_dir / zettel

        if note is None:
            note = click.edit()

        with file_path.open("w") as file:
            file.write(note)

        click.secho("Note saved successfully!", fg="green")

    except Exception as e:
        click.secho(f"Error occured:\n{e}", fg="red")
