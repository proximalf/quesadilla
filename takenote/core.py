from pathlib import Path

from takenote.template.functions import fetch_template


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
