from pathlib import Path
from typing import Dict, Optional
from jinja2 import Template
from takenote.lib import DateTemplate

# Config template location.
DEFAULT_TEMPLATES_FOLDER = Path(__file__).parent / "resources/default-templates"


def title_from_format(format: Dict[str, str], title: Optional[str]):
    """
    Generate title string from defined format.

    Formats covered:
        'long', 'short'.

    Formatting objects
        date, title.

    Parameters
    ----------
    settings: Dict[str, str]
        Setting object
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


def generate_template_folder(dirpath: Path) -> None:
    """
    Generates template folder from example, and saves the templates
    under dirpath.

    Parameters
    ----------
    dirpath: Path
        Path to folder.
    """
    if not dirpath.exists():
        dirpath.mkdir(parents=True)

    for template_file in DEFAULT_TEMPLATES_FOLDER.glob("*"):
        with open(template_file, "r") as template:
            with open(dirpath / template_file.name, "w") as file:
                file.write(template.read())


def fetch_template(template_path: Path) -> str:
    """
    Fetch template to process.

    Parameters
    ----------
    template_path: Path
        Template file path.
    """
    with open(template_path, "r") as file:
        return Template(file.read())


def apply_template(template_path: Path, note: str, title: str):
    """
    Generate title string from defined format.

    Formats covered:
        'long', 'short'.

    Formatting objects
        date, title.

    Parameters
    ----------
    template_path: Path
        Path pointing to referencing template.
    note: str
        Note string.
    title: Optional[str]
        Title string.

    Returns
    ----------
    str
        Processed template string.
    """
    template = fetch_template(template_path)

    note = template.render(date=DateTemplate(), note=note, title=title)

    return note
