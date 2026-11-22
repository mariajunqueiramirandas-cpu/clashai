"""Command-line entry point: `python -m clashai` or `clashai`."""

import argparse
from contextlib import closing
from subprocess import CalledProcessError

from clashai.simulator import DATA_VERSION, SMOKE_DECK, make_env, setup_crforge


def _smoke_match(seed: int) -> None:
    with closing(make_env(SMOKE_DECK, SMOKE_DECK)) as env:
        env.action_space.seed(seed)
        _, info = env.reset(seed=seed)
        while True:
            action = env.action_space.sample(mask=info["action_mask"])
            _, _, terminated, truncated, info = env.step(action)
            if truncated:
                if info["fault"] != "none":
                    raise RuntimeError(f"crforge battle fault: {info['fault_message']}")
                raise RuntimeError("crforge battle reached the tick limit before a result.")
            if terminated:
                winner = info["winner"]
                tick = info["tick"]
                result = "draw" if winner == env.schema.winner_draw else f"seat {winner} won"
                print(f"crforge {DATA_VERSION} completed a match at tick {tick} ({result}).")
                return


def main() -> None:
    parser = argparse.ArgumentParser(prog="clashai", description="Clash Royale AI tools")
    commands = parser.add_subparsers(dest="command")
    setup = commands.add_parser("sim-setup", help="Install the pinned crforge simulator")
    setup.add_argument(
        "--asset-source", default="cdn", help="The game's CDN or a file:// URI to a local mirror"
    )
    smoke = commands.add_parser("sim-smoke", help="Play one seeded crforge match")
    smoke.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    try:
        if args.command == "sim-setup":
            setup_crforge(asset_source=args.asset_source)
        elif args.command == "sim-smoke":
            _smoke_match(args.seed)
        else:
            parser.print_help()
    except (CalledProcessError, OSError, RuntimeError, ValueError) as exc:
        parser.exit(1, f"clashai: {exc}\n")


if __name__ == "__main__":
    main()
