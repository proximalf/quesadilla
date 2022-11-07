from pathlib import Path
from typing import List
from dynaconf import Dynaconf, Validator

validators = [
    Validator("SAVE_PATH_NOTES", must_exist=True, default="./"),
    Validator("VERBOSITY_LEVEL", must_exist=True, default=1),
]

# Config template location.
CONFIG_TEMPLATE = Path(__file__).parent / "conf/default-config.toml"


def generate_config_file(filepath: Path) -> None:
    """
    Creates a config file from template if it does not currently exist.

    Parameters
    ----------
    filepath: Path
        File path to save file to.
    """

    with open(CONFIG_TEMPLATE, "r") as template:
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
