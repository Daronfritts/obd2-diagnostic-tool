# Fox OBD2 Diagnostic Tool

A Python-based OBD2 diagnostic tool for reading live data, trouble codes, and vehicle health snapshots from ELM327/STN-compatible adapters.

This project is meant to start simple and grow into a practical diagnostic companion for garage use, Raspberry Pi use, and future dashboard/BCM integration work.

## Goals

- Connect to common USB, Bluetooth, or Wi-Fi OBD2 adapters.
- Auto-detect the vehicle protocol when the adapter supports it.
- Read and clear diagnostic trouble codes.
- Stream useful live PIDs like RPM, coolant temp, voltage, throttle position, fuel trims, and vehicle speed.
- Save timestamped diagnostic snapshots.
- Keep the core logic separate from future UI work.

## Important Note

Your 1988 Foxbody Mustang is not factory OBD2. This tool is for:

- Other OBD2 vehicles.
- Engine swaps or aftermarket ECUs that expose OBD2-style data.
- Future expansion where OBD2, CAN, Microsquirt logs, or custom BCM data may be displayed together.

For Microsquirt/MS2 data, this project should use a separate adapter layer instead of pretending it is standard OBD2.

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
fox-obd2 scan
```

If your adapter is not auto-detected:

```bash
fox-obd2 scan --port /dev/ttyUSB0
```

Other starter commands:

```bash
fox-obd2 detect
fox-obd2 codes
fox-obd2 codes --clear
fox-obd2 record --output snapshots/test-drive.jsonl --interval 1 --samples 300
```

## What "Any Car" Means

The target is any normal OBD2-compliant vehicle, which generally means:

- 1996+ gas vehicles in the US.
- 2008+ light diesel vehicles in the US.
- Vehicles using common OBD2 protocols through a proper adapter.

The tool should gracefully handle unsupported PIDs because every car exposes a different set of data. A good scanner asks what the vehicle supports, then shows the data that actually exists.

## Project Layout

```text
src/fox_obd2/
  cli.py          Command-line entry point
  adapters.py     OBD2 adapter connection helpers
  commands.py     High-level diagnostic commands
  models.py       Shared data models

config/
  pids.example.toml

docs/
  roadmap.md
  hardware.md
```

## First Milestone

1. Confirm connection to an ELM327 adapter.
2. Read basic live data.
3. Read stored and pending trouble codes.
4. Save a diagnostic snapshot as JSON.
5. Add a simple Raspberry Pi friendly display mode.
