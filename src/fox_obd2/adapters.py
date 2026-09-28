from __future__ import annotations

import obd
from serial.tools import list_ports


def connect(port: str | None = None, fast: bool = False) -> obd.OBD:
    """Open an OBD connection.

    Passing no port lets python-OBD auto-detect common serial adapters.
    """
    return obd.OBD(portstr=port, fast=fast)


def available_ports() -> list[str]:
    """Return visible serial ports that may contain USB/Bluetooth OBD adapters."""
    return [port.device for port in list_ports.comports()]
