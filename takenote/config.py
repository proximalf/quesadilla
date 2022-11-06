from pathlib import Path
from dynaconf import Dynaconf, Validator

validators = [
    Validator("save_path_notes", must_exist=True, default="./"),
]

# Config template location.
CONFIG_TEMPLATE = Path(__file__).parent / "conf/default-config.toml"


def generate_config_file(filepath: Path) -> None:
    """
    Creates a config file from template if it does not currently exist.
    """

    with open(CONFIG_TEMPLATE, "r") as template:
        with open(filepath, "w") as file:
            file.write(template.read())


def config_file(filepath: Path) -> Dynaconf:
    """
    returns an existing config file.
    """
    settings = Dynaconf(
        envvar_prefix="DYNACONF",
        settings_files=filepath,
        validators=validators,
    )
    return settings
