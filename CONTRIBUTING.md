# Contributing

## Set up the Development environment

To install the development environment, please follow these steps, preferably in a Python 3.8 virtual environment.

```bash
pip install -e ".[dev]"
pre-commit install
pre-commit run --all-files
```

## Building

```bash
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

The repository has pylint as linter. To run pylint checks, execute:

```bash
pylint src
```

## PR names

The PR titles should follow these [guidelines](https://www.conventionalcommits.org/en/v1.0.0/)
