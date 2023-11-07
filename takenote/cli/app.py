from pathlib import Path
from typing import Any, Dict, Optional
import click

from takenote.note.io import write_note

from ..note.note import Note
from ..note.template import filename_from_format


class App:
    """Main App class, initialises app using settings."""

    def __init__(self, settings: Dict[str, Any], debug: bool = False) -> None:
        """
        Parameters
        ----------
        settings: Dict[str, Any]
            Settings object.
        debug: bool = False
            Set debug mode on.
        """
        self.settings = settings
        self.note = Note()
        self.data = {}
        self.editor = True
        self.template_path = settings["DEFAULT_TEMPLATE"]
        self.level = settings["VERBOSITY_LEVEL"]
        self._filename = ""
        self.debug = debug if debug else settings["DEBUG"]

    def echo(self, string: str, level: int = 0, **kwargs) -> None:
        """
        Print output to terminal using clicks.secho function.
        Lowest level is most urgent messages.

        Parameters
        ----------
        string: str
            Message to print.
        level: int
            Set the level of the message to be printed, default is 0.
        **kwargs
            Arguments passed to secho function.
        """
        if level <= self.level or self._debug:
            click.secho(string, **kwargs)

    def open_editor(self, force_open: bool = False, text: str = "") -> None:
        """Open Editor"""
        # Skip editor
        if not self.editor and not force_open:
            return

        self.note.content = click.edit(text=text, editor=self.settings["EDITOR"], extension=self.settings["EXTENSION"])

    @property
    def filename(self) -> str:
        """Return formated filename as a str."""
        return self._filename

    @filename.setter
    def filename(self, title: Optional[str] = None) -> None:
        """Set filename."""
        filename_format = "short" if title is None else "long"
        self._filename = filename_from_format(self.settings["FORMAT"]["filename"][filename_format], title)
        self.note.title = title

    def set_template(self, template_key: str) -> None:
        """Set the template by referencing key to relavent template path as defined in the config file"""
        template_dir = self.settings["APP_DIR"] / self.settings["TEMPLATES_DIR"]
        relative_path = self.settings["TEMPLATES"].get(template_key)
        if relative_path is None:
            raise FileNotFoundError(f"Template {template_key} doesn't exist, please chck {template_dir}")
        self.template_path = template_dir / relative_path

    def write_to_file(self) -> None:
        """Write note to file."""
        save_dir = Path(self.settings["SAVE_PATH_NOTES"]).expanduser()
        path = save_dir / f"{self.filename}.{self.settings['FILE_TYPE']}"
        self.echo(f"Writing note to: {path}", level=1, fg="green")
        write_note(path, self.note, self.template_path, self.data)

    def print_template_keys(self) -> None:
        """Print template keys, as KEY:FILENAME."""
        self.echo("Printing template keys (KEY : FILENAME):")
        if not isinstance(self.settings["TEMPLATES"], dict):
            self.echo("No Templates found...", fg="red")
        for key, value in self.settings["TEMPLATES"].items():
            self.echo(f"\t- {key} : {value}", fg="yellow")
