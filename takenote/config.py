from pathlib import Path
from dynaconf import Dynaconf, Validator, loaders

USER_CONFIG_FILE = Path("./settings.toml")

validators = [Validator("save_path_notes", must_exist=True, default="/tmp")]

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=USER_CONFIG_FILE,
    validators=validators,
)


def create_config_file() -> None:
    """
    Creates a config file if it does not currently exist. Fle is in .toml format
    """
    if not USER_CONFIG_FILE.exists():
        USER_CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        loaders.write(str(USER_CONFIG_FILE), settings.as_dict())
