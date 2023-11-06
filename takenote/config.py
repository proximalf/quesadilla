from pathlib import Path
from typing import Any, Dict, List
from dynaconf import Dynaconf, Validator


def fetch_settings(global_config: Path, local_config: Path) -> Dict[str, Any]:
    """
    Fetches settings. local config is checked to exist, else uses global.

    Parameters
    ----------
    global_config: Path
        Global config file path, loaded before local.
    local_config: Path
        File path to local config file.

    Returns
    ----------
    Dict[str, Any]
        Settings dict, from Dynaconf
    """
    if local_config.exists():
        return config_file([global_config, local_config])
    else:
        return config_file([global_config])


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
