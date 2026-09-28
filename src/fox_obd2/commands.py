from __future__ import annotations

import json
from pathlib import Path
from time import sleep

import obd

from fox_obd2.models import DiagnosticReading, DiagnosticSnapshot


DEFAULT_LIVE_COMMANDS = [
    obd.commands.RPM,
    obd.commands.SPEED,
    obd.commands.COOLANT_TEMP,
    obd.commands.THROTTLE_POS,
    obd.commands.INTAKE_TEMP,
    obd.commands.CONTROL_MODULE_VOLTAGE,
    obd.commands.FUEL_STATUS,
    obd.commands.SHORT_FUEL_TRIM_1,
    obd.commands.LONG_FUEL_TRIM_1,
    obd.commands.O2_SENSORS,
    obd.commands.RUN_TIME,
]


def _adapter_value(connection: obd.OBD, name: str) -> str | None:
    value = getattr(connection, name, None)
    if value is None:
        return None

    if callable(value):
        value = value()

    return None if value is None else str(value)


def _string_value(connection: obd.OBD, command: obd.OBDCommand) -> str | None:
    if not connection.supports(command):
        return None

    response = connection.query(command)
    if response.is_null():
        return None

    return str(response.value)


def _trouble_codes(connection: obd.OBD) -> list[str]:
    response = connection.query(obd.commands.GET_DTC)
    if response.is_null():
        return []

    return [f"{code}: {desc}" for code, desc in response.value]


def collect_snapshot(
    connection: obd.OBD,
    commands: list[obd.OBDCommand] | None = None,
) -> DiagnosticSnapshot:
    command_list = DEFAULT_LIVE_COMMANDS if commands is None else commands
    readings: list[DiagnosticReading] = []

    for command in command_list:
        if not connection.supports(command):
            readings.append(DiagnosticReading(name=command.name, value="unsupported", supported=False))
            continue

        response = connection.query(command)
        readings.append(
            DiagnosticReading(
                name=command.name,
                value="unsupported" if response.is_null() else str(response.value),
                supported=not response.is_null(),
            )
        )

    return DiagnosticSnapshot(
        adapter_port=_adapter_value(connection, "port_name"),
        protocol=_adapter_value(connection, "protocol_name"),
        vehicle_vin=_string_value(connection, obd.commands.VIN),
        readings=readings,
        trouble_codes=_trouble_codes(connection),
    )


def save_snapshot(snapshot: DiagnosticSnapshot, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(snapshot.to_json_dict(), indent=2), encoding="utf-8")


def clear_trouble_codes(connection: obd.OBD) -> bool:
    response = connection.query(obd.commands.CLEAR_DTC)
    return not response.is_null()


def stream_snapshots(
    connection: obd.OBD,
    output_path: Path,
    interval_seconds: float,
    samples: int,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as output_file:
        for index in range(samples):
            snapshot = collect_snapshot(connection)
            output_file.write(json.dumps(snapshot.to_json_dict()) + "\n")
            output_file.flush()

            if index < samples - 1:
                sleep(interval_seconds)
