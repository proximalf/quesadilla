poetry update
poetry export -f requirements.txt --output requirements.txt
python -m pip install -r requirements.txt

poetry install

#poetry build
#python -m pip install dist/takenote-*-py3-*.whl -e .

python -m takenote --help