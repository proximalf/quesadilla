from pathlib import Path
from typing import Any, Dict, Optional
import click
from loguru import logger
import pyperclip

from .functions import initialise_app_dir
from ..config import (
    fetch_settings,
    APP_DIR_NAME,
    CONFIG_FILE_NAME,
    GLOBAL_CONFIG,
    DEFAULT_TEMPLATES_FOLDER,
    CONFIG_TEMPLATE,
    GLOBAL_DIR,
)
from .app import App


def write_and_close(app: App) -> None:
    """Write note to file, method will raise exceptions these are handled below."""
    try:
        if app.note.content is None:
            app.echo("No note saved!", level=0, fg="red")
        else:
            app.write_to_file()
            app.echo("Success!", level=1)
    except FileExistsError as e:
        app.echo(f"File already exists: {e}", level=0, fg="red")
    except Exception as e:
        logger.exception(e)
        app.echo(f"Error occured:\n{e}", level=0, fg="red")


CONTEXT_SETTINGS: Dict[str, Any] = {"help_option_names": ["-h", "--help"]}


@click.group(invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@click.option("-t", "--title", "title", type=str, required=False, default=None, help="Title of note.")
@click.option(
    "-cb",
    "--clipboard",
    "clipboard_flag",
    type=bool,
    is_flag=True,
    default=False,
    help="Fetch contents from clipboard, must be a string.",
)
@click.option(
    "--debug",
    "debug",
    is_flag=True,
    type=bool,
    default=False,
    help="Flag to set debug mode on.",
)
@click.option(
    "-p",
    "--path",
    "custom_path",
    type=Path,
    default=None,
    help="A specifed path to save a note to, takes precedence over defined settings.",
)
@click.option(
    "-n",
    "--no-edit",
    "no_edit",
    is_flag=True,
    type=bool,
    default=False,
    help="Skips opening the editor, useful to quick save a clipboard snippet.",
)
@click.option(
    "-e",
    "--edit",
    "force_editor",
    type=bool,
    is_flag=True,
    default=False,
    help="Opens editor.",
)
@click.pass_context
def cli(
    ctx: click.Context,
    title: Optional[str] = None,
    clipboard_flag: bool = False,
    debug: bool = False,
    custom_path: Optional[Path] = None,
    no_edit: bool = False,
    force_editor: bool = False,
) -> int:
    r"""
    Take note CLI program, quick depositing of notes for those that prefer using the terminal.

    Configuration files are stored in folder ".tn", local options overwrite globals.
    Config directory path can be overwritten by setting the TN_ENV value.

    Filename of note is generated from config, if title option is not included
    then the default short name is used.

    \b
    Example
    ----------
    `tn -t "Title of a normal note"`
        Note will use basic template and an editor will open.

    """
    # Check for local config
    local = Path.cwd() / APP_DIR_NAME
    app_dir = local if local.exists() else GLOBAL_DIR
    first_time = not app_dir.exists()

    if first_time:
        initialise_app_dir(app_dir, CONFIG_FILE_NAME, CONFIG_TEMPLATE, DEFAULT_TEMPLATES_FOLDER, False)
        return  # Don't continue after generating config

    settings = fetch_settings(GLOBAL_CONFIG, local / CONFIG_FILE_NAME)
    settings["APP_DIR"] = app_dir

    app = App(settings, debug)
    app.filename = title
    app.editor = not no_edit

    app.echo("Take note!", level=0, fg="magenta")

    if custom_path is not None:
        app.settings["SAVE_PATH_NOTES"] = custom_path
        app.echo(f"Saving to output: {custom_path}", level=1)

    if clipboard_flag:
        app.data["clipboard"] = pyperclip.paste()

    if ctx.invoked_subcommand is not None:
        # Pass settings into context object for other commands
        ctx.obj = app
    else:
        app.open_editor(force_editor)

        write_and_close(app)


if __name__ == "__main__":
    cli()
