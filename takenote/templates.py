from pathlib import Path

# Config template location.
DEFAULT_TEMPLATES_FOLDER = Path(__file__).parent / "resources/default-templates"


def generate_template_folder(filepath: Path) -> None:
    """
    Generates template folder from example
    """
    if not filepath.exists():
        filepath.mkdir(parents=True)

    for template_file in DEFAULT_TEMPLATES_FOLDER.glob("*"):
        with open(template_file, "r") as template:
            with open(filepath / template_file.name, "w") as file:
                file.write(template.read())
