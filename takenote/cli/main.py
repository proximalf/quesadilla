from pathlib import Path
from typing import Union
import sys
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
    TN_ENV,
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
        app.print_contents()
    except Exception as e:
        logger.exception(e)
        app.echo(f"Error occured:\n{e}", level=0, fg="red")
        app.print_contents()


def initialise_logging(
    log_file: Union[str, Path],
    level: str = "INFO",
    write_to_stderr: bool = True,
    write_to_stdout: bool = False,
    debug: bool = False,
):
    """
    Initialise loguru logger with file and stderr and stdout as per their respective flags
    """
    settings = {
        "colorize": True,
        "level": level,
    }
    if debug:
        settings["backtrace"] = True
        settings["diagnose"] = True

    if write_to_stderr:
        logger.add(sys.stderr, **settings)
    if write_to_stdout:
        logger.add(sys.stdout, **settings)

    # write because no point keeping old file, personal preferance.
    # String from config
    logger.add(Path(log_file).expanduser(), mode="w")


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
    """
    Take note CLI, quick depositing of notes for those that prefer using the terminal.

    Configuration files are stored in folder ".tn", local options overwrite globals.
    Config directory path can be overwritten by setting the TN_ENV value.

    Filename of note is generated from config, if title option is not included
    then the default short name is used.

    \b
    Example
    ----------
    `tn -t "Title of a normal note"`
        Note will use basic template and an editor will open.

    `tn t new`
        Basic template note, opens editor.

    `tn -t "Title of templated file" t new`
        Setting the title of a note that uses the `new` template, refer to config.

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

    initialise_logging(**settings["LOGGING"])

    app = App(settings, debug)
    app.filename = title
    app.editor = not no_edit

    if TN_ENV:
        # Output the set env variable "TN_ENV"
        app.echo(f"TN_ENV: {TN_ENV}", level=1, fg="red")
        logger.info(f"TN_ENV: {TN_ENV}")

    app.echo("Take note!", level=0, fg="magenta")

    if custom_path is not None:
        # Overwrite save path
        app.settings["SAVE_PATH_NOTES"] = custom_path
        app.echo(f"Saving to output: {custom_path}", level=1)

    if clipboard_flag:
        # Grab clipboard data
        app.data["clipboard"] = pyperclip.paste()

    if ctx.invoked_subcommand is not None:
        # Pass settings into context object for other commands
        ctx.obj = app
    else:
        app.open_editor(force_editor)

        write_and_close(app)


@cli.command("t", short_help="Templates using keys.")
@click.pass_context
@click.argument("template_key", type=str, default=None, required=False)
@click.option(
    "-k",
    "--keys",
    "print_keys",
    type=bool,
    is_flag=True,
    default=False,
    help="Prints template keys availible, refer to config file to modify keys.",
)
def template(ctx: click.Context, template_key: Optional[str] = None, print_keys: bool = False) -> None:
    """
    Templating command. Refer to config file and default templates for more information.

    Example
    ----------
    `tn t -k`
        Will print keys set in config file
    `tn -t "Template" t new`
        Will create a note using new template and give it a title.
    """
    app: App = ctx.obj
    if print_keys:
        app.print_template_keys()
        return

    if template_key is None:
        app.echo("Error: No template key provided!", fg="")
        return

    try:
        app.set_template(template_key)
        app.echo(f"Applying template: {template_key}", level=2)
    except FileNotFoundError:
        app.echo("ERROR", fg="red")
        app.echo(f"Template {template_key} cannot be applied as file cannot be found.")
        app.echo("Please refer to config file.")
        return
    # Always open after applying template.
    app.open_editor(True)

    write_and_close(app)


@cli.command("config", short_help="Command to open config files.")
@click.pass_context
@click.option(
    "-l",
    "--local",
    "open_local",
    type=bool,
    is_flag=True,
    default=False,
    help="Open local config file, if none exists this is generated.",
)
@click.option(
    "-g",
    "--global",
    "open_global",
    type=bool,
    is_flag=True,
    default=False,
    help="Open global config file.",
)
def config(ctx: click.Context, open_local: bool = False, open_global: bool = False):
    """
    Config command, used to generate and edit local and global config files.
    """
    app: App = ctx.obj

    # Check for local config
    local = Path.cwd() / APP_DIR_NAME
    local_config = local / CONFIG_FILE_NAME

    if open_local:
        app_dir = local if not local.exists() else GLOBAL_DIR
        initialise_app_dir(app_dir, CONFIG_FILE_NAME, CONFIG_TEMPLATE, DEFAULT_TEMPLATES_FOLDER, True)

    app.echo("Editing Config!")

    if local_config.exists():
        app.echo(f"Local: {local_config}")
        click.edit(filename=local_config)
    elif open_global or not local_config:
        app.echo(f"Global: {GLOBAL_CONFIG}")
        click.edit(filename=GLOBAL_CONFIG)
