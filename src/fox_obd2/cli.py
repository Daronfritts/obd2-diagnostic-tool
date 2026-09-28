from __future__ import annotations

from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from fox_obd2.adapters import available_ports, connect
from fox_obd2.commands import clear_trouble_codes, collect_snapshot, save_snapshot, stream_snapshots

console = Console()


@click.group()
def main() -> None:
    """Fox OBD2 diagnostic tool."""


@main.command()
def detect() -> None:
    """List serial ports that may contain OBD2 adapters."""
    ports = available_ports()

    if not ports:
        console.print("[yellow]No serial ports found.[/yellow]")
        return

    table = Table(title="Detected Serial Ports")
    table.add_column("Port")

    for port in ports:
        table.add_row(port)

    console.print(table)


@main.command()
@click.option("--port", help="Serial port for the OBD2 adapter, like /dev/ttyUSB0 or COM3.")
@click.option("--fast/--no-fast", default=False, help="Enable faster python-OBD polling.")
@click.option("--save", type=click.Path(path_type=Path), help="Save a JSON diagnostic snapshot.")
def scan(port: str | None, fast: bool, save: Path | None) -> None:
    """Read common live data and diagnostic codes."""
    connection = connect(port=port, fast=fast)

    if not connection.is_connected():
        raise click.ClickException("Could not connect to the OBD2 adapter.")

    snapshot = collect_snapshot(connection)

    console.print(f"[bold]Adapter:[/bold] {snapshot.adapter_port or 'auto'}")
    console.print(f"[bold]Protocol:[/bold] {snapshot.protocol or 'unknown'}")
    console.print(f"[bold]VIN:[/bold] {snapshot.vehicle_vin or 'unavailable'}\n")

    table = Table(title="OBD2 Live Data")
    table.add_column("PID")
    table.add_column("Value")

    for reading in snapshot.readings:
        status = reading.value if reading.supported else "[dim]unsupported[/dim]"
        table.add_row(reading.name, status)

    console.print(table)

    if snapshot.trouble_codes:
        console.print("\n[bold red]Trouble Codes[/bold red]")
        for code in snapshot.trouble_codes:
            console.print(f"- {code}")
    else:
        console.print("\n[green]No stored trouble codes reported.[/green]")

    if save:
        save_snapshot(snapshot, save)
        console.print(f"\nSaved snapshot to {save}")


@main.command()
@click.option("--port", help="Serial port for the OBD2 adapter, like /dev/ttyUSB0 or COM3.")
@click.option("--fast/--no-fast", default=False, help="Enable faster python-OBD polling.")
@click.option("--clear", "should_clear", is_flag=True, help="Clear trouble codes after reading them.")
def codes(port: str | None, fast: bool, should_clear: bool) -> None:
    """Read stored trouble codes, with optional clearing."""
    connection = connect(port=port, fast=fast)

    if not connection.is_connected():
        raise click.ClickException("Could not connect to the OBD2 adapter.")

    snapshot = collect_snapshot(connection, commands=[])

    if snapshot.trouble_codes:
        console.print("[bold red]Trouble Codes[/bold red]")
        for code in snapshot.trouble_codes:
            console.print(f"- {code}")
    else:
        console.print("[green]No stored trouble codes reported.[/green]")

    if should_clear:
        click.confirm("Clear stored trouble codes now?", abort=True)
        if clear_trouble_codes(connection):
            console.print("[green]Clear-code command sent.[/green]")
        else:
            console.print("[yellow]Clear-code command was not accepted or returned no response.[/yellow]")


@main.command()
@click.option("--port", help="Serial port for the OBD2 adapter, like /dev/ttyUSB0 or COM3.")
@click.option("--fast/--no-fast", default=False, help="Enable faster python-OBD polling.")
@click.option("--output", type=click.Path(path_type=Path), default=Path("snapshots/live.jsonl"))
@click.option("--interval", type=float, default=1.0, show_default=True, help="Seconds between samples.")
@click.option("--samples", type=int, default=60, show_default=True, help="Number of samples to record.")
def record(port: str | None, fast: bool, output: Path, interval: float, samples: int) -> None:
    """Record repeated live-data snapshots as JSON Lines."""
    if interval <= 0:
        raise click.ClickException("--interval must be greater than zero.")
    if samples <= 0:
        raise click.ClickException("--samples must be greater than zero.")

    connection = connect(port=port, fast=fast)

    if not connection.is_connected():
        raise click.ClickException("Could not connect to the OBD2 adapter.")

    stream_snapshots(connection, output, interval_seconds=interval, samples=samples)
    console.print(f"[green]Recorded {samples} samples to {output}[/green]")
