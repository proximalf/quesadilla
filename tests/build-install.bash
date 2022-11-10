rm dist/*

poetry update
poetry export -f requirements.txt --output requirements.txt
python -m pip install -r requirements.txt

poetry install
# python -m takenote --help

# Takenote entry point as denoted in the pyproject file.
tn --help


# Build wheel for install.
poetry build -f wheel
# Remove version
# python -m pip uninstall takenote -y
# Install new one
# python -m pip install dist/takenote-*-py3-*.whl
