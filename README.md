# clashai

A Clash Royale bot. Work in progress.

## Setup

Requires Python 3.10+.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

## Usage

```bash
clashai                          # or: python -m clashai
```

## Development

```bash
pytest           # run tests
ruff check .     # lint
ruff format .    # format
```

## Project layout

```
src/clashai/   bot code
tests/         pytest tests
```
