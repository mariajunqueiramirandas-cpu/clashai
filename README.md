# clashai

A bot that plays Clash Royale. It runs the game in an Android emulator, reads the screen over ADB, and sends taps back.

> ⚠️ Automating gameplay breaks Supercell's Terms of Service and can get an account banned. Use a throwaway account.

## How it works

```
 emulator ──(adb screenshot)──▶ vision (OpenCV) ──▶ decision logic ──(adb tap/swipe)──▶ emulator
```

1. **Capture**: grab a screenshot from the emulator via ADB.
2. **Perceive**: work out the game state (elixir, cards in hand, troops, tower HP) with OpenCV template matching, and later an object-detection model if needed.
3. **Decide**: pick a card and a placement, starting with rules and possibly moving to ML/RL later.
4. **Act**: tap the card, then tap the arena position.

## Requirements

- Python 3.10+
- An Android emulator with Clash Royale installed, e.g. [BlueStacks](https://www.bluestacks.com/), [LDPlayer](https://www.ldplayer.net/), [MEmu](https://www.memuplay.com/), or the Android Studio emulator
- [ADB (Android platform-tools)](https://developer.android.com/tools/releases/platform-tools) on your `PATH`
- ADB enabled in the emulator settings

Use a fixed emulator resolution (for example 720×1280 portrait). Templates and screen coordinates depend on it.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e ".[dev]"

cp .env.example .env             # then set CLASHAI_DEVICE if you have more than one device
adb devices                      # check the emulator shows up
```

## Usage

```bash
clashai screenshot               # saves screenshots/screen.png from the emulator
```

Use screenshots to crop templates (cards, buttons, elixir digits) into `assets/templates/`.

## Project layout

```
src/clashai/
  __main__.py     CLI entry point
  device.py       ADB wrapper: screenshot, tap, swipe
assets/templates/ image templates for OpenCV matching
tests/            pytest tests
```

## Development

```bash
pytest           # run tests
ruff check .     # lint
ruff format .    # format
```

## Roadmap

- [ ] Detect screens: main menu, battle, end of battle
- [ ] Read elixir count
- [ ] Recognise the 4 cards in hand and the next card
- [ ] Map arena tiles to screen coordinates
- [ ] Rule-based play loop
- [ ] Auto-requeue battles
- [ ] Detect troops on the field (YOLO or similar)
