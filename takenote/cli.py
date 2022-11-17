from pathlib import Path
from typing import Any, Dict
import click

from takenote.__version__ import __version__
from takenote.config import config_file
from takenote.core import generate_template_folder, generate_config_file


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
        """Initialises with a set level 0."""
        self._level = 0

    def echo(self, msg, level: int = 3, **kwargs) -> None:
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
        level: int
            The level the message is printed as.
        kwargs: Dict[str, Any]
            Kwargs to pass to echo
        """
        if level <= self._level:
            click.secho(msg, **kwargs)  # type: ignore

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


output = Output()


def initialise_app_dir(
    directory: Path,
    config_file_name: str,
    config_template: Path,
    template_files_dir: Path,
    force_generate: bool = False,
) -> None:
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
    force_generate: bool
        Set to true to force generation of app dir.
    """
    directory.mkdir(exist_ok=True)
    config_path = directory / config_file_name
    templates_dir = directory / "templates"
    if not config_path.exists() or force_generate:
        # Write config
        generate_config_file(config_template, config_path, __version__)
    if not templates_dir.exists() or force_generate:
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
        output.echo(f"Using local settings: {local_config}", level=2)
        return config_file([global_config, local_config])
    else:
        return config_file([global_config])


def new_note(settings: Dict[str, Any], note: str, filename: str) -> None:
    """
    New note function. Overwrites any note.

    Parameters
    ----------
    settings: Dict[str, Any]
        Settings object.
    note: str
        Note string.
    filename: str
        Filename to save note under.

    Raises
    ----------
    FileExistsError
        File already exists.
    """
    # Expand user in case '~' is used.
    output_dir = Path(settings["SAVE_PATH_NOTES"]).expanduser()
    filepath = output_dir.absolute() / filename
    if filepath.exists():
        raise FileExistsError(f"File: {filepath}, already exists, and will be overwritten.")
    with filepath.open("w") as file:
        file.write(note)
    output.echo(f"Note saved successfully!\n{filepath}", level=1, fg="green")


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
        output.echo(f"Appending to note!\n{filepath}", level=2, fg="green")
        with filepath.open("a") as file:
            file.write(note)
    else:
        output.echo(f"File doesn't exist: {filepath}", level=0, fg="red")
