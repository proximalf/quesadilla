from pathlib import Path
from typing import List
from dynaconf import Dynaconf, Validator

validators = [
    Validator("EDITOR", must_exist=True, default=None),
    Validator("EXTENSION", must_exist=True, default="md"),
    Validator("SAVE_PATH_NOTES", must_exist=True, default="./"),
    Validator("TEMPLATES_DIR", must_exist=True, default="./templates"),
    Validator("FORMAT.title", must_exist=True, default={"long": "{{ title }}", "short": "new-note"}),
    Validator("VERBOSITY_LEVEL", must_exist=True, default=1),
]


def generate_config_file(template_file: Path, filepath: Path) -> None:
    """
    Creates a config file from template if it does not currently exist.

    Parameters
    ----------
    template_file: Path
        Template file to write to file.
    filepath: Path
        File path to save file to.
    """

    with open(template_file, "r") as template:
        with open(filepath, "w") as file:
            file.write(template.read())


def config_file(filepaths: List[Path]) -> Dynaconf:
    """
    Returns an existing config file. Requires a list of files for input.

    Parameters
    ----------
    filepaths: List[Path]
        List of config file paths.

    Returns
    ----------
    Dict[str, Any]
        Settings object from Dynaconf.
    """
    settings = Dynaconf(
        envvar_prefix="TN",
        settings_files=filepaths,
        validators=validators,
    )
    return settings
