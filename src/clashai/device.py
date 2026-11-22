"""Thin wrapper around ADB for controlling the emulator."""

from __future__ import annotations

import numpy as np
from adbutils import AdbDevice, adb


class Device:
    def __init__(self, serial: str | None = None) -> None:
        if serial:
            adb.connect(serial)  # needed for network-attached emulators (127.0.0.1:port)
        self._dev: AdbDevice = adb.device(serial=serial or None)

    @property
    def serial(self) -> str:
        return self._dev.serial

    def screenshot(self) -> np.ndarray:
        """Return the current screen as a BGR numpy array (OpenCV format)."""
        rgb = np.asarray(self._dev.screenshot().convert("RGB"))
        return rgb[:, :, ::-1].copy()

    def tap(self, x: int, y: int) -> None:
        self._dev.click(x, y)

    def swipe(self, x1: int, y1: int, x2: int, y2: int, duration: float = 0.2) -> None:
        self._dev.swipe(x1, y1, x2, y2, duration)
