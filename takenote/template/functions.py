from pathlib import Path
from typing import Dict, Optional
from jinja2 import Template
from takenote.template.objects import DateTemplate


def filename_from_format(format: Dict[str, str], title: Optional[str]) -> str:
    """
    Generate filename string from defined format.

    Formatting objects
        date, title.

    Parameters
    ----------
    format:
        Jinja string representting format as described.
    title: Optional[str]
        Title string.

    Returns
    ----------
    str
        Processed template string.
    """

    tp = Template(format)
    return tp.render(date=DateTemplate(), title=title)


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
