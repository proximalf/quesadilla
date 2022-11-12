from pathlib import Path
from typing import List
from dynaconf import Dynaconf, Validator


def config_file(filepaths: List[Path]) -> Dynaconf:
    """
    Returns an existing config file. Requires a list of files for input.
    Files are overwritten based on order in list.

    Parameters
    ----------
    filepaths: List[Path]
        List of config file paths.

    Returns
    ----------
    Dict[str, Any]
        Settings object from Dynaconf.
    """

    validators = [
        Validator("EDITOR", must_exist=True, default=None),
        Validator("EXTENSION", must_exist=True, default="md"),
        Validator("SAVE_PATH_NOTES", must_exist=True, default="./"),
        Validator("TEMPLATES_DIR", must_exist=True, default="./templates"),
        Validator("FORMAT.filename", must_exist=True, default={"long": "{{ title }}", "short": "new-note"}),
        Validator("VERBOSITY_LEVEL", must_exist=True, default=1),
    ]

    settings = Dynaconf(
        envvar_prefix="TN",
        settings_files=filepaths,
        validators=validators,
    )
    return settings
