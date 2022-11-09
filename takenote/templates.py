from pathlib import Path
from typing import Dict, Optional
from jinja2 import Template
from takenote.core import DateTemplate


def title_from_format(format: Dict[str, str], title: Optional[str]) -> str:
    """
    Generate title string from defined format.

    Formats covered:
        'long', 'short'.

    Formatting objects
        date, title.

    Parameters
    ----------
    format: Dict[str, str]
        Dict object representting formats as described.
    title: Optional[str]
        Title string.

    Returns
    ----------
    str
        Processed template string.
    """

    if title is None:
        tp = Template(format["short"])
        return tp.render(date=DateTemplate())
    else:
        tp = Template(format["long"])
        return tp.render(date=DateTemplate(), title=title)


def generate_template_folder(template_folder: Path, dirpath: Path) -> None:
    """
    Generates template folder from example, and saves the templates
    under dirpath.

    Parameters
    ----------
    template_folder: Path
        Template folder to generate new folder from
    dirpath: Path
        Path to folder to be templated.
    """
    if not dirpath.exists():
        dirpath.mkdir(parents=True)

    for template_file in template_folder.glob("*"):
        with open(template_file, "r") as template:
            with open(dirpath / template_file.name, "w") as file:
                file.write(template.read())


def fetch_template(template_path: Path) -> Template:
    """
    Fetch template to process.

    Parameters
    ----------
    template_path: Path
        Template file path.
    """
    with open(template_path, "r") as file:
        return Template(file.read())


def apply_template(template_path: Path, note: str, title: Optional[str], clipboard: Optional[str]):
    """
    Generate title string from defined format.

    Formats covered:
        'long', 'short'.

    Formatting objects
        date, title, clipboard.

    Parameters
    ----------
    template_path: Path
        Path pointing to referencing template.
    note: str
        Note string.
    title: Optional[str]
        Title string.
    clipboard: Optional[str]
        Clipboard string

    Returns
    ----------
    str
        Processed template string.
    """
    template = fetch_template(template_path)

    template_object = {
        "clipboard": clipboard if not None else "",
        "date": DateTemplate(),
        "note": note,
        "title": title if not None else "",
    }

    note = template.render(template_object)

    return note
