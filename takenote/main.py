import os
from pathlib import Path
from typing import Optional
import click

from takenote.templates import apply_template, title_from_format
from takenote.cli import initialise_app_dir, fetch_settings, new_note, append_note, output

CONFIG_FILE_NAME: str = "takenote-config.toml"
APP_DIR_NAME: str = ".tn"
tn_env: Optional[str] = os.environ.get("TN_ENV")
GLOBAL_DIR: Path = Path(tn_env) if "TN_ENV" in os.environ else Path.home() / APP_DIR_NAME  # type: ignore
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
    help="Contents of note.",
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
    help="Provide a key to apply a corrasponding template to a note.",
)
@click.pass_context
def cli(
    ctx: click.Context,
    title: Optional[str] = None,
    note: Optional[str] = None,
    generate_config: bool = False,
    custom_path: Optional[Path] = None,
    verbose: int = 0,
    template: Optional[str] = None,
) -> int:
    """
    Take note CLI program, for those that prefer using the terminal.
    The note has to be wrapped in quotes for single line.
    Config file name: takenote-config.toml

    \b
    Example
    ----------
    tn -gc # Generate config in local directory

    tn "Title" # Opens your favourite editor and saves note on close

    tn "Title" -n "Note String"
    tn -n "Note" # Title is auto generated

    tn a KEY -n "Note String"
    """
    # Check for local config
    local = Path.cwd() / APP_DIR_NAME
    app_dir = local if not local.exists() and generate_config else GLOBAL_DIR
    initialise_app_dir(app_dir, CONFIG_FILE_NAME, CONFIG_TEMPLATE, DEFAULT_TEMPLATES_FOLDER)

    if generate_config:
        return 0  # Don't continue after generating config

    settings = fetch_settings(GLOBAL_CONFIG, local / CONFIG_FILE_NAME)

    output.level = verbose if verbose != 0 else settings["VERBOSITY_LEVEL"]
    output.echo("Take note!", {"fg": "magenta"}, level=0)

    if ctx.invoked_subcommand is None:
        if custom_path is not None:
            settings["SAVE_PATH_NOTES"] = custom_path
            output.echo(f"Saving to output: {custom_path}", level=3)

        title = title_from_format(settings["FORMAT"]["title"], title)

        if note is None:
            note = click.edit(editor=settings["EDITOR"])

        if template is not None and note is not None:
            template_dir = app_dir / settings["TEMPLATES_DIR"]
            template_path = template_dir / settings["TEMPLATES"][template]
            output.echo(f"Applying template: {template}", level=3)
            note = apply_template(template_path, note, title)

        try:
            if note is None:
                output.echo("No note saved!", {"fg": "red"}, level=0)
                return 1
            else:
                new_note(settings, note, title)
                output.echo("Success!", level=1)
                return 0
        except Exception as e:
            output.echo(f"Error occured:\n{e}", {"fg": "red"}, level=0)
        return 0
    else:
        ctx.obj = settings


@cli.command("a")
@click.argument("append_key", type=str, default=None, required=True)
@click.option(
    "-n",
    "--note",
    "note",
    type=str,
    default=None,
    help="Contents of note.",
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
def append(ctx, append_key: str, note: str, custom_path: Path):
    """
    Append to note.
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
            output.echo("Note not appended!", {"fg": "red"}, level=0)
            return 1
        else:
            append_note(settings, append_key, note)
            output.echo("Success!", level=1)
            return 0
    except Exception as e:
        output.echo(f"Error occured:\n{e}", {"fg": "red"}, level=0)
    return 0


if __name__ == "__main__":
    cli()
