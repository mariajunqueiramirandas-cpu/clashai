# clashai

A Clash Royale bot. Work in progress.

## Setup

Requires Python 3.10+.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

## crforge simulator

Install Git and JDK 21. From the repository root, with the Python environment above active, run

```bash
clashai sim-setup
clashai sim-smoke --seed 42
```

Setup pins crforge to `v16.635.1-range-16.635.1-16.635.9` and builds the `16.635.8` game tables.
The engine, Gradle cache, and game tables live in the ignored `.crforge/` directory. The Python
binding is installed into the active environment.

The first setup downloads dependencies and fetches assets from the game's CDN to build the tables.
To use a local copy of the CDN layout, pass `--asset-source file:///path/to/cdn/`. On networks that
require a proxy for Java, set `http.proxyHost`, `http.proxyPort`, `https.proxyHost`, and
`https.proxyPort` in `JAVA_TOOL_OPTIONS` before setup.

Use `clashai.simulator.make_env(deck, opponent_deck)` to open a Gymnasium environment from Python.
Each deck is a sequence of eight crforge card names. The environment's action mask is available as
`info["action_mask"]` after `reset()` and `step()`.

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
