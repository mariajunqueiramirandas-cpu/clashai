"""Command-line entry point: `python -m clashai` or `clashai`."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

import cv2
from dotenv import load_dotenv

from clashai.device import Device


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(prog="clashai")
    parser.add_argument("--device", default=os.getenv("CLASHAI_DEVICE"), help="ADB serial")
    sub = parser.add_subparsers(dest="command", required=True)
    shot = sub.add_parser("screenshot", help="save a screenshot from the device")
    shot.add_argument("-o", "--output", default="screenshots/screen.png")
    args = parser.parse_args()

    device = Device(args.device)
    if args.command == "screenshot":
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(out), device.screenshot())
        print(f"Saved {out} from {device.serial}")


if __name__ == "__main__":
    main()
