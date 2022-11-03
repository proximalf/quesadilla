from pathlib import Path
from typing import Optional
from takenote.lib import zettelkasten


def create_note(dirpath: Path, note: str, title: Optional[str] = None) -> None:
    """
    Create a note.

    Parameters
    ----------
    dirpath: Path
        Directory path to save file to.
    note: str
        Note string.
    title: Optional[str]
        Title of note, this is appended to filename

    Returns
    ----------
    filepath
        Filepath the note is saved to.
    """
    if title is not None:
        filepath = dirpath / title
    else:
        # Can't save a file without a title/filepath.
        zettel = zettelkasten()
        filepath = dirpath / zettel

    with filepath.open("w") as file:
        file.write(note)

    return filepath
