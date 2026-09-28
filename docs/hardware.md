# Hardware Notes

## Recommended Adapter Types

- USB ELM327 adapter for Raspberry Pi or laptop bench testing.
- OBDLink/STN-based adapters for better reliability than bargain ELM327 clones.
- Bluetooth adapters only when the host device has stable pairing.

## Raspberry Pi Notes

For a Pi install, USB is the easiest first choice:

- Adapter usually appears as `/dev/ttyUSB0` or `/dev/ttyACM0`.
- Add the runtime user to the `dialout` group if the port is permission-blocked.
- Keep the adapter wiring away from ignition noise where possible.

## Foxbody Note

A stock 1988 Mustang does not have OBD2. For the Foxbody project, keep these as separate data sources:

- OBD2 adapter for OBD2 vehicles.
- Microsquirt serial data for the Mustang ECU.
- BCM/Pico serial or CAN data for body control and dashboard features.
