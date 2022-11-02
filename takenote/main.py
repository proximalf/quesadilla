from pathlib import Path
import click
from config import create_config_file, settings
from lib import zettelkasten


@click.command()
@click.argument("note", nargs=1, type=str)
@click.option("-t", "--title", "title", type=str)
def cli(note: str, title: str) -> None:
    """
    The note has to be wrapped in quotes for single line.

    Example
    ----------
    tn -t "Title" -- "Note"
    tn "Note"

    """
    # Generate settings
    create_config_file()

    print("Take note!")

    output_dir = Path(settings["save_path_notes"])

    if title is not None:
        file_path = output_dir / title
    else:
        # Can't save a file without a title/filepath.
        zettel = zettelkasten()
        print(f"no title provided, saved under {zettel} instead")
        file_path = output_dir / zettel

    with open(file_path, "w") as file:
        file.write(note)

    print("Note saved successfully!")


if __name__ == "__main__":
    cli()
