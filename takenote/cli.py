from pathlib import Path
from typing import Any, Dict, Optional
import click

from takenote.config import config_file, generate_config_file
from takenote.note import append_to_note, create_note
from takenote.templates import generate_template_folder


class Output:
    """
    Object for writing using click.echo(), set level for verbosity.

    Level
    ----------
    0 : Minimum level, Errors
    1 : Info
    2 : Some Debug
    3 : Extra Debug
    """

    def __init__(self) -> None:
        """Initialises with a set level of 3."""
        self._level = 3

    def echo(self, msg, style: Optional[Dict[str, str]] = None, level: int = 3) -> None:
        """
        Echos msg to output.

        Level
        ----------
        0 : Minimum level, Errors
        1 : Info
        2 : Some Debug
        3 : Extra Debug

        Parameters
        ----------
        msg: str
            Message to pass to echo.
        style: Optional[Dict[str, str]]
            Dict object representing chosen style.
        level: int
            The level the message is printed as.
        """
        if level <= self._level:
            if style is not None:
                # Unpack style
                click.secho(msg, **style)
            else:
                click.echo(msg)

    @property
    def level(self) -> int:
        """
        Return set level.

        Returns
        ----------
        int
            Level as int.
        """
        return self._level

    @level.setter
    def level(self, level: int) -> None:
        """
        Set level. Refer to class doc for more on level.

        Parameters
        ----------
        level: int
            int to set level as.
        """
        self._level = level
        self.echo(f"Verbosity level set: {level}", level=3)


output = Output()


def initialise_app_dir(directory: Path, config_file_name: str, config_template: Path, template_files_dir: Path) -> None:
    """
    Initialise the directory for app.

    Parameters
    ----------
    directory: Path
        Directory path of app.
    config_file_name: str
        Filename of config file
    config_template: Path
        Path to template config file.
    template_files_dir: Path
        Path to directory of template files.
    """
    directory.mkdir(exist_ok=True)
    config_path = directory / config_file_name
    templates_dir = directory / "templates"
    if not config_path.exists():
        # Write config
        generate_config_file(config_template, config_path)
    if not templates_dir.exists():
        generate_template_folder(template_files_dir, templates_dir)


def fetch_settings(global_config: Path, local_config: Path) -> Dict[str, Any]:
    """
    Fetches settings. local config is checked to exist, else uses global.

    Parameters
    ----------
    global_config: Path
        Global config file path, loaded before local.
    local_config: Path
        File path to local config file.

    Returns
    ----------
    Dict[str, Any]
        Settings dict, from Dynaconf
    """
    if local_config.exists():
        output.echo("Using local settings", level=2)
        return config_file([global_config, local_config])
    else:
        return config_file([global_config])


def new_note(settings: Dict[str, Any], note: str, title: str = None) -> None:
    """
    New note function.

    Parameters
    ----------
    settings: Dict[str, Any]
        Settings object.
    note: str
        Note string.
    title: str
        title string.
    """
    # Expand user in case '~' is used.
    output_dir = Path(settings["SAVE_PATH_NOTES"]).expanduser()
    filepath = create_note(output_dir.absolute(), note, title=title)
    output.echo(f"Note saved successfully!\n{filepath}", {"fg": "green"}, level=1)


def append_note(settings: Dict[str, Any], key: str, note: str) -> None:
    """
    Append to note.

    Parameters
    ----------
    settings: Dict[str, Any]
        Settings object.
    key: str
        Key for path to use as defined in the settings object.
    note: str
        Note string.
    """
    # Get key from settings, expand user in case '~' is used
    filepath = Path(settings["append_notes"][key]).expanduser()
    if filepath.exists():
        output.echo(f"Appending to note!\n{filepath}", {"fg": "green"}, level=2)
        append_to_note(filepath, "\n" + note)
    else:
        output.echo(f"File doesn't exist: {filepath}", {"fg": "red"}, level=0)
