from pathlib import Path

from ..__version__ import __version__
from ..note.template.functions import fetch_template


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


def generate_template_folder(template_folder: Path, dirpath: Path) -> None:
    """
    Generates template folder from example, and saves the templates
    under dirpath.

    Parameters
    ----------
    template_folder: Path
        Template folder to generate new folder from
    dirpath: Path
        Path to folder to be templated.
    """
    if not dirpath.exists():
        dirpath.mkdir(parents=True)

    for template_file in template_folder.glob("*"):
        with open(template_file, "r") as template:
            with open(dirpath / template_file.name, "w") as file:
                file.write(template.read())


def generate_config_file(template_file: Path, filepath: Path, version: str) -> None:
    """
    Creates a config file from template if it does not currently exist.

    Parameters
    ----------
    template_file: Path
        Template file to write to file.
    filepath: Path
        File path to save file to.
    version: str
        String of app version to add to config.
    """
    template = fetch_template(template_file)
    with open(filepath, "w") as file:
        file.write(template.render(version=version))
