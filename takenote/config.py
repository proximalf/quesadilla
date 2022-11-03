from pathlib import Path
from dynaconf import Dynaconf, Validator, loaders

validators = [
    Validator("save_path_notes", must_exist=True, default="./"),
    Validator("append_notes.example", default="./appendexample"),
]


def config_file(filepath: Path, force_generate: bool = True) -> None:
    """
    Creates a config file if it does not currently exist.
    """
    settings = Dynaconf(
        envvar_prefix="DYNACONF",
        settings_files=filepath,
        validators=validators,
    )
    if not filepath.exists() and force_generate:
        filepath.parent.mkdir(parents=True, exist_ok=True)
        loaders.write(str(filepath), settings.as_dict())

    return settings
