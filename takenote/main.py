import os
from pathlib import Path
from typing import Optional
import click
import pyperclip

from takenote.template import apply_template, filename_from_format
from takenote.cli import initialise_app_dir, fetch_settings, new_note, append_note, output

CONFIG_FILE_NAME: str = "takenote-config.toml"
APP_DIR_NAME: str = ".tn"
tn_env: Optional[str] = os.environ.get("TN_ENV")
# Echo if ENV has been set.
output.echo(f"TN_ENV: {tn_env}", level=3 if tn_env is None else 0, fg="red")

GLOBAL_DIR: Path = Path(tn_env) if tn_env is not None else Path.home() / APP_DIR_NAME  # type: ignore


GLOBAL_CONFIG: Path = GLOBAL_DIR / CONFIG_FILE_NAME


# Config template location.
DEFAULT_TEMPLATES_FOLDER: Path = Path(__file__).parent / "resources/default-templates"
CONFIG_TEMPLATE: Path = Path(__file__).parent / "resources/default-config.toml"


@click.group(invoke_without_command=True)
@click.option("-t", "--title", "title", type=str, required=False, default=None, help="Title of note.")
@click.option(
    "-n",
    "--note",
    "note",
    type=str,
    default=None,
    help="Use the given string as the contents of the note.",
)
@click.option(
    "-lc",
    "--generate-local",
    "generate_local_config",
    is_flag=True,
    default=False,
    help=f"Use to generate a local config folder, {APP_DIR_NAME}",
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
    "-v", "--verbose", "verbose", count=True, help="Set the verbosity level. Default is 0 level. Can be set in config."
)
@click.option(
    "-at",
    "--template",
    "template",
    type=str,
    default=None,
    help="Provide a key to apply a corresponding template to a note.",
)
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
    "-e",
    "--edit",
    "force_editor",
    type=bool,
    is_flag=True,
    default=False,
    help="Open editor - options are applied and can be edited after.",
)
@click.pass_context
def cli(
    ctx: click.Context,
    title: Optional[str] = None,
    note: Optional[str] = None,
    generate_local_config: bool = False,
    custom_path: Optional[Path] = None,
    verbose: int = 0,
    template: Optional[str] = None,
    clipboard_flag: bool = False,
    force_editor: bool = False,
) -> int:
    """
    Take note CLI program, for those that prefer using the terminal.
    The note has to be wrapped in quotes for single line.

    Configuration files are stored in folder ".tn", local options overwrite globals.

    Filename of note is generated from config.

    `--force-editor` can be used along side `--note` as the option opens an editor
    after templates have been applied.

    \b
    Example
    ----------
    tn --generate-local/-lc # Generate config in local directory

    tn --title/-t "Title" # Opens your favourite editor and saves note on close

    tn --title/-t "Title" --note/-n "Note String"
    tn --note/-n "Note" # Filename is generated from config

    tn a KEY -n "Note String"
    """
    first_time = not GLOBAL_DIR.exists()

    # Check for local config
    local = Path.cwd() / APP_DIR_NAME
    app_dir = local if not local.exists() and generate_local_config else GLOBAL_DIR
    initialise_app_dir(app_dir, CONFIG_FILE_NAME, CONFIG_TEMPLATE, DEFAULT_TEMPLATES_FOLDER, generate_local_config)

    if generate_local_config or first_time:
        return 0  # Don't continue after generating config

    settings = fetch_settings(GLOBAL_CONFIG, local / CONFIG_FILE_NAME)

    output.level = verbose if verbose != 0 else settings["VERBOSITY_LEVEL"]
    output.echo("Take note!", level=0, fg="magenta")

    if ctx.invoked_subcommand is not None:
        # Pass settings into context object for other commands
        ctx.obj = settings
    else:
        if custom_path is not None:
            settings["SAVE_PATH_NOTES"] = custom_path
            output.echo(f"Saving to output: {custom_path}", level=3)

        clipboard: Optional[str] = None
        if clipboard_flag:
            clipboard = pyperclip.paste()

        filename_format = "short" if title is None else "long"
        filename = filename_from_format(settings["FORMAT"]["filename"][filename_format], title)

        if note is None:
            note = click.edit(editor=settings["EDITOR"])

        if template is not None and note is not None:
            template_dir = app_dir / settings["TEMPLATES_DIR"]
            template_path = template_dir / settings["TEMPLATES"][template]
            output.echo(f"Applying template: {template}", level=3)
            note = apply_template(template_path, note, filename, clipboard)

        if force_editor:
            click.edit(text=note, editor=settings["EDITOR"])

        try:
            if note is None:
                output.echo("No note saved!", level=0, fg="red")
                return 1
            else:
                new_note(settings, note, f"{filename}.{settings['EXTENSION']}")
                output.echo("Success!", level=1)
                return 0
        except FileExistsError as e:
            output.echo(f"File already exists: {e}")
        except Exception as e:
            output.echo(f"Error occured:\n{e}", level=0, fg="red")
        return 1


@cli.command("a")
@click.argument("append_key", type=str, default=None, required=True)
@click.option(
    "-n",
    "--note",
    "note",
    type=str,
    default=None,
    help="Use the given string as the contents of the note.",
)
@click.option(
    "-p",
    "--path",
    "custom_path",
    type=Path,
    default=None,
    help="A specifed path to append a note to, takes precedence over defined settings.",
)
@click.pass_context
def append(ctx: click.Context, append_key: str, note: str, custom_path: Path) -> None:
    """
    Append to note. Keys for notes to be appended to are set in the config file.
    Option "--note/-n" is provided and has same function.

    \b
    Example
    ----------
    tn a KEY # Opens editor

    tn a KEY --path "./path/of/appendable/note.md"
    """

    # Get settings from context.
    settings = ctx.obj

    if custom_path is not None:
        settings["SAVE_PATH_NOTES"] = custom_path
        output.echo(f"Saving to output: {custom_path}", level=3)

    if note is None:
        note = click.edit(editor=settings["EDITOR"])

    try:
        if note is None:
            output.echo("Note not appended!", level=0, fg="red")
            return 1
        else:
            append_note(settings, append_key, note)
            output.echo("Success!", level=1)
            return 0
    except Exception as e:
        output.echo(f"Error occured:\n{e}", level=0, fg="red")
    return 0


if __name__ == "__main__":
    cli()
