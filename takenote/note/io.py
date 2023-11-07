from loguru import logger
import yaml
from pathlib import Path
from typing import Dict, Optional
from markdown_it import MarkdownIt
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.footnote import footnote_plugin
from jinja2.exceptions import UndefinedError

from .template import apply_template
from .note import Note


class TemplateError(Exception):
    """Jinja Template Error"""


def write_note(
    path: Path, note: Note, template_path: Optional[Path] = None, addtional_data: Optional[Dict[str, str]] = None
) -> None:
    """
    Write a note using the template provided, else uses default.

    Parameters
    ----------
    path: Path
        Path to save note under.
    note: Note
        Note to save.
    template_path: Optional[Path]
        Absolute path to template file, if left as None the default template is used.
    addtional_data: Optional[Dict[str, str]]
        Any addtional data to be passed to a `data` object for acess in jinja templates.
    """
    try:
        path.write_text(apply_template(template_path, note, addtional_data))
    except UndefinedError as e:
        errmsg = f"Please check template {template_path} for errors, refer to log for debug information."
        logger.error(errmsg)
        logger.exception(e)
        raise TemplateError(errmsg)


def read_markdown(path: Path, ignore_title: bool = False) -> Note:
    """
    Read markdown note, assuming my format, which uses yaml.
    """
    md = (
        MarkdownIt("commonmark", {"breaks": True, "html": False})
        .use(front_matter_plugin)
        .use(footnote_plugin)
        .enable("table")
    )

    front_matter = None
    title = None
    content = 0
    tokens = md.parse(path.read_text())
    for i, token in enumerate(tokens):
        if token.type == "front_matter":
            front_matter = token.content
            content = token.map[-1]
        if token.tag == "h1" and token.nesting == 1:
            h = tokens[i + 1].children[0]
            title = h.content if h.content != "" else None
            # Assumes content starts after the line h1 is on
            if not ignore_title:
                content = token.map[0]

    if front_matter is not None:
        front_matter = yaml.safe_load(front_matter)

    content = "".join(path.open().readlines()[content::])
    date = front_matter["creation_date"] if front_matter is not None else None

    return Note(
        front_matter=front_matter,
        title=title,
        content=content,
        date=date,
    )
