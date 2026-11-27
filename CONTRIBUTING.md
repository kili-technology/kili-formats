# Contributing

## Set up the Development environment

To install the development environment, please follow these steps, preferably in a Python 3.10 virtual environment.

```bash
pip install -e ".[dev]"
pre-commit install
pre-commit run --all-files
```

## Building

```bash
pip install build
python -m build
```

## Testing

To test a feature,
you can run

```bash
pytest tests/<TEST_TO_RUN>.py
```

to run all tests, simply run `pytest tests`

## Linting

`pre-commit` runs Ruff, pyupgrade, isort and Black. Pylint (which must score 10.00/10) and Pyright run in CI only:

```bash
pylint --rcfile=.pylintrc src/kili_formats
pyright src
```

## PR names

The PR titles should follow these [guidelines](https://www.conventionalcommits.org/en/v1.0.0/)
