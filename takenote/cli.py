import os
from pathlib import Path
from typing import Any, Dict, Optional
import click

from takenote.config import config_file, generate_config_file
from takenote.note import append_to_note, create_note
from takenote.templates import apply_template, generate_template_folder, title_from_format

CONFIG_FILE_NAME = "takenote-config.toml"
APP_DIR_NAME = ".tn"
GLOBAL_DIR = Path(os.environ.get("TN_ENV")) if "TN_ENV" in os.environ else Path.home() / APP_DIR_NAME
GLOBAL_CONFIG = GLOBAL_DIR / CONFIG_FILE_NAME


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
        self._level = 3

    def echo(self, msg, style: Optional[Dict[str, str]] = None, level=3):
        """
        Parameters
        ----------
        msg: str
            Message to pass to echo.
        style: Optional[Dict[str, str]]
            Dict object representing chosen style.
        """
        if level <= self._level:
            if style is not None:
                # Unpack style
                click.secho(msg, **style)
            else:
                click.echo(msg)

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, level):
        self._level = level
        self.echo(f"Verbosity level set: {level}", level=3)


output = Output()


def initialise_app_dir(directory: Path) -> None:
    """
    Initialise the directory for app.

    Parameters
    ----------
    directory: Path
        Directory path of app.
    """
    directory.mkdir(exist_ok=True)
    config_path = directory / CONFIG_FILE_NAME
    templates_dir = directory / "templates"
    if not config_path.exists():
        # Write config
        generate_config_file(config_path)
    if not templates_dir.exists():
        generate_template_folder(templates_dir)


def fetch_settings(local_config: Path) -> Dict[str, Any]:
    """
    Fetches settings. local config is checked to exist, else uses global.

    Parameters
    ----------
    local_config: Path
        File path to local config file.

    Returns
    ----------
    Dict[str, Any]
        Settings dict, from Dynaconf
    """
    if local_config.exists():
        output.echo("Using local settings", level=2)
        return config_file([GLOBAL_CONFIG, local_config])
    else:
        return config_file([GLOBAL_CONFIG])


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
        output.echo(f"File doesn't exist: {filepath}", {"fg": "green"}, level=0)


@click.command()
@click.argument("note", nargs=1, type=str, required=False)
@click.option(
    "-t",
    "--title",
    "title",
    type=str,
    default=None,
    help="Sets the filename of a note.",
)
@click.option(
    "-a",
    "--append",
    "append_key",
    type=str,
    default=None,
    help="Use a key as defined by APPEND_NOTES in the config file.",
)
@click.option(
    "-gc",
    "--generate-config",
    "generate_config",
    is_flag=True,
    default=False,
    help=f"Use to generate a local config file, name is {CONFIG_FILE_NAME}",
)
@click.option(
    "-p",
    "--path",
    "custom_path",
    default=None,
    help="A specifed path to save a note to, takes precedence over defined settings.",
)
@click.option(
    "-v", "--verbose", "verbose", count=True, help="Set the verbosity level. Default is 0 level. Can be set in config."
)
@click.option(
    "-at",
    "--template",
    "template",
    type=str,
    default=None,
    help="Provide a key to apply a corrasponding template to a note.",
)
def cli(
    note: str,
    title: Optional[str] = None,
    append_key: Optional[str] = None,
    generate_config: bool = False,
    custom_path: Optional[Path] = None,
    verbose: int = 0,
    template: Optional[str] = None,
) -> None:
    """
    Take note CLI program, for those that prefer using the terminal.
    The note has to be wrapped in quotes for single line.
    Config file name: takenote-config.toml

    \b
    Example
    ----------
    tn -gc # Generate config in local directory
    tn "Note"
    tn -t "Title" -- "Note String"
    tn -t "Title" # Opens your favourite editor and saves note on close
    tn -a KEY -- "Note String"
    """

    # Check for local config
    local = Path.cwd() / APP_DIR_NAME
    app_dir = local if not local.exists() and generate_config else GLOBAL_DIR
    initialise_app_dir(app_dir)

    if generate_config:
        return 0  # Don't continue after generating config

    settings = fetch_settings(local / CONFIG_FILE_NAME)

    output.level = verbose if verbose != 0 else settings["VERBOSITY_LEVEL"]
    output.echo("Take note!", {"fg": "magenta"}, level=0)

    if custom_path is not None:
        settings["SAVE_PATH_NOTES"] = custom_path
        output.echo(f"Saving to output: {custom_path}", level=3)

    title = title_from_format(settings["FORMAT"]["title"], title)

    if note is None:
        note = click.edit()

    if template is not None:
        template_dir = app_dir / settings["TEMPLATES_DIR"]
        template_path = template_dir / settings["TEMPLATES"][template]
        output.echo(f"Applying template: {template}", level=3)
        note = apply_template(template_path, note, title)

    try:
        if note is None:
            output.echo("No note saved!", {"fg": "red"}, level=0)
            return 1
        else:
            if append_key:
                append_note(settings, append_key, note)
            else:
                new_note(settings, note, title)

        output.echo("Success!", level=1)
        return 0
    except Exception as e:
        output.echo(f"Error occured:\n{e}", {"fg": "red"}, level=0)


if __name__ == "__main__":
    cli()
