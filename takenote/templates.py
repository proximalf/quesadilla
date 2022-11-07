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


def fetch_template(settings: Dict[str, str], template_dir, key: str) -> str:

    path = template_dir / settings["TEMPLATES"][key]
    with open(path, "r") as file:
        return Template(file.read())


def apply_template(settings: Dict[str, str], template_dir, key: str, data: Dict[str, str]):

    template = fetch_template(settings, template_dir, key)

    note = template.render(data=data)

    return note
