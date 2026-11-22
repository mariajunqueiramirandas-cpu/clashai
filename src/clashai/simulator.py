"""Install and use the repository's pinned crforge simulator."""

from __future__ import annotations

import os
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from crforge_env import ClashGymEnv

CRFORGE_URL = "https://github.com/voonhous/crforge.git"
CRFORGE_TAG = "v16.635.1-range-16.635.1-16.635.9"
CRFORGE_COMMIT = "8be539ea0d1de393681299c1d84148fdc5ef013d"
DATA_VERSION = "16.635.8"
DEFAULT_RUNTIME = Path(".crforge")
SMOKE_DECK = ("Knight", "Archer", "Musketeer", "Giant", "MiniPekka", "Fireball", "Arrows", "Zap")


def _check_revision(source: Path) -> None:
    revision = subprocess.check_output(
        ["git", "-C", str(source), "rev-parse", "HEAD"], text=True
    ).strip()
    if revision != CRFORGE_COMMIT:
        raise RuntimeError(f"{source} is at {revision}. Expected crforge {CRFORGE_COMMIT}.")


def setup_crforge(runtime_dir: Path = DEFAULT_RUNTIME, *, asset_source: str = "cdn") -> None:
    """Build the engine and tables locally, then install its Python package."""
    runtime_dir = runtime_dir.resolve()
    runtime_dir.mkdir(parents=True, exist_ok=True)
    source = runtime_dir / "source"
    if not source.exists():
        with TemporaryDirectory(dir=runtime_dir) as temporary:
            checkout = Path(temporary) / "source"
            subprocess.run(
                [
                    "git",
                    "clone",
                    "--depth",
                    "1",
                    "--branch",
                    CRFORGE_TAG,
                    CRFORGE_URL,
                    str(checkout),
                ],
                check=True,
            )
            _check_revision(checkout)
            checkout.rename(source)
    else:
        _check_revision(source)

    wrapper = source / ("gradlew.bat" if os.name == "nt" else "gradlew")
    subprocess.run(
        [
            str(wrapper),
            "--gradle-user-home",
            str(runtime_dir / "gradle"),
            "--no-daemon",
            ":env:installDist",
            ":tables:dataVersionTables",
            f"-Pcrforge.dataVersion={DATA_VERSION}",
            f"-Pcrforge.cache={runtime_dir / 'cache'}",
            f"-Pcrforge.assetSource={asset_source}",
        ],
        cwd=source,
        check=True,
    )
    subprocess.run([sys.executable, "-m", "pip", "install", str(source / "python")], check=True)


def make_env(
    deck: Sequence[str],
    opponent_deck: Sequence[str],
    *,
    runtime_dir: Path = DEFAULT_RUNTIME,
    **options: Any,
) -> ClashGymEnv:
    """Open a crforge Ladder environment using this checkout's engine and tables."""
    install = runtime_dir / "source" / "env" / "build" / "install" / "env"
    tables = runtime_dir / "cache" / "tables" / DATA_VERSION
    setup_hint = "Run `clashai sim-setup` from the repository root."
    if not any((install / "lib").glob("*.jar")) or not (tables / "build.properties").is_file():
        raise RuntimeError(f"The crforge engine or game tables are missing. {setup_hint}")

    try:
        from crforge_env import ClashGymEnv
    except ModuleNotFoundError as exc:
        if exc.name != "crforge_env":
            raise
        raise RuntimeError(f"The crforge Python package is missing. {setup_hint}") from exc

    return ClashGymEnv(deck, opponent_deck, install=install, tables=tables, **options)
