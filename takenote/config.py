import os
from pathlib import Path
from typing import Any, Dict, List, Optional
from dynaconf import Dynaconf, Validator
from loguru import logger

CONFIG_FILE_NAME: str = "takenote-config.toml"
APP_DIR_NAME: str = ".tn"
tn_env: Optional[str] = os.environ.get("TN_ENV")
logger.info(f"TN_ENV: {tn_env}", level=3 if tn_env is None else 0, fg="red")

GLOBAL_DIR: Path = Path(tn_env) if tn_env is not None else Path.home() / APP_DIR_NAME  # type: ignore

GLOBAL_CONFIG: Path = GLOBAL_DIR / CONFIG_FILE_NAME

# Config template location.
DEFAULT_TEMPLATES_FOLDER: Path = Path(__file__).parent / "resources/default-templates"
CONFIG_TEMPLATE: Path = Path(__file__).parent / "resources/default-config.toml"


def fetch_settings(global_config: Path, local_config: Path) -> Dict[str, Any]:
    """
    Fetch settings. local config is checked to exist, else uses global.

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
    Return an existing config file. Requires a list of files for input.
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
        Validator("DEBUG", must_exist=True, default=False),
        Validator("DEFAULT_TEMPLATE", must_exist=True, default=None),
    ]

    settings = Dynaconf(
        envvar_prefix="TN",
        settings_files=filepaths,
        validators=validators,
    )
    return settings
