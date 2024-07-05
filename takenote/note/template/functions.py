from datetime import datetime
from pathlib import Path
from typing import Dict, Optional
from jinja2 import Template
from ..note import Note

DEFAULT_TEMPLATE_STRING = """
---
{{ note.yaml }}
---
{% if note.title != "" or note.title is None %}
# {{ note.title }}
{% else %}

{% endif %}

{{ datetime.now().strftime("%A %d %B %Y %H:%M:%S") }}

{{ note.content }}
"""


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

    template = Template(format)
    try:
        return template.render(datetime=datetime, title=title)
    except TypeError:
        raise Exception(f"Error with template for file title: {title} format: {format}")


def fetch_template(template_path: Optional[Path]) -> Template:
    """
    Fetch template to process.

    Parameters
    ----------
    template_path: Optional[Path]
        Template file path, if left as None, will use default [DEFAULT_TEMPLATE_STRING].
    """
    return Template(template_path.read_text() if template_path is not None else DEFAULT_TEMPLATE_STRING)


def apply_template(template_path: Optional[Path], note: Note, addtional_data: Optional[Dict[str, str]]) -> str:
    """
    Generate title string from defined format.

    Formats covered:
        'long', 'short'.

    Formatting objects
        date, title, clipboard.

    Parameters
    ----------
    template_path: Optional[Path]
        Absolute path to template file, if left as None the default template is used.
    note: Note
        Note to save.
    addtional_data: Optional[Dict[str, str]]
        Any addtional data to be passed to a `data` object for acess in jinja templates.

    Returns
    ----------
    str
        Processed template string.
    """
    template = fetch_template(template_path)
    try:
        return template.render(note=note, datetime=datetime, **addtional_data)
    except TypeError:
        raise Exception(f"Error with template applying template, path: {template_path}")
