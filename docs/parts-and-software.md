# Parts And Software List

This project is aimed at a universal OBD2 diagnostic tool: generic OBD2 on normal 1996+ vehicles first, then deeper CAN and manufacturer-specific support later.

Important reality check: no free tool truly reads every module on every vehicle. Generic emissions OBD2 is standardized. ABS, airbag, body modules, transmission details, bidirectional tests, key programming, and manufacturer enhanced PIDs are usually brand-specific.

## Recommended Hardware

| Priority | Part | Why You Need It | Notes |
| --- | --- | --- | --- |
| Required | Laptop or Raspberry Pi | Runs the diagnostic app | Mac is fine for development. Raspberry Pi is better for a dedicated garage tool. |
| Required | Quality USB OBD2 adapter | Talks to normal OBD2 cars | USB is more stable than Bluetooth for development. Avoid the cheapest ELM327 clones. |
| Recommended | OBDLink SX or OBDLink EX | Reliable STN-based USB adapter | Better than random ELM327 clones. EX is popular with Ford/FORScan work. |
| Recommended | vLinker FS USB | Ford-friendly adapter option | Good option if you want FORScan/Ford-family support. |
| Recommended | USB-C to USB-A adapter | Connects USB OBD adapter to modern Mac/Pi | Only needed if the host lacks USB-A. |
| Recommended | OBD2 extension cable | Keeps stress off the car port | Get a short, good-quality extension. |
| Recommended | OBD2 breakout box | Safer probing and CAN testing | Lets you access pins without stabbing the car harness. |
| Recommended | Bench 12 V power supply | Bench testing adapters and modules | Use fused leads. 5 A is plenty for basic bench electronics. |
| Recommended | Multimeter | Basic voltage/ground checks | Already useful for car wiring work. |
| Later | CANable, CANtact, CANtact Pro, or CANable-compatible adapter | Raw CAN sniffing through SocketCAN/SavvyCAN | Needed for reverse engineering, not required for basic OBD2. |
| Later | CAN FD adapter | Modern vehicles using CAN FD | Only needed once the project supports CAN FD. |
| Later | J2534 PassThru adapter | Better OEM-style diagnostic path | More expensive, but useful for serious multi-brand work. |
| Optional | Rugged case/enclosure | Makes it garage-friendly | Useful once the Pi version exists. |
| Optional | Small touchscreen | Standalone scan tool display | Good for a Raspberry Pi build. |

## OBD2 Port Pins To Care About

| Pin | Purpose | Notes |
| --- | --- | --- |
| 4 | Chassis ground | Adapter ground reference. |
| 5 | Signal ground | Adapter/signal ground reference. |
| 6 | CAN High | Modern OBD2 CAN. |
| 14 | CAN Low | Modern OBD2 CAN. |
| 7 | K-Line | Older ISO 9141 / KWP2000 vehicles. |
| 2 | J1850 Bus+ | Older Ford/GM era vehicles. |
| 10 | J1850 Bus- | Used on J1850 PWM. |
| 16 | Battery positive | Usually constant 12 V. Use care. |

## Best Free / Open Software Stack

| Software | Cost | Use | Why It Belongs |
| --- | --- | --- | --- |
| Python | Free/open source | Main app language | Cross-platform and easy to run on Mac, Windows, Linux, and Raspberry Pi. |
| python-OBD | Free/open source | Generic OBD2 PID reads through ELM327/STN adapters | Good starting library for Mode 01 live data and basic diagnostics. |
| pySerial | Free/open source | Serial adapter communication | Needed for USB/Bluetooth serial adapters. |
| Rich | Free/open source | Nice command-line output | Makes tables, warnings, and scan output readable. |
| Click | Free/open source | Command-line commands | Keeps `scan`, `codes`, `record`, and future tools clean. |
| pytest | Free/open source | Tests | Keeps the scanner from breaking as features grow. |
| Ruff | Free/open source | Lint/format checks | Fast code cleanup. |
| SocketCAN | Free/open source | Linux CAN interface layer | Best path for Raspberry Pi raw CAN support. |
| can-utils | Free/open source | `candump`, `cansend`, CAN testing | Required for serious Linux CAN debugging. |
| python-can | Free/open source | Python CAN support | Lets this project talk to SocketCAN and other CAN adapters later. |
| SavvyCAN | Free/open source | CAN capture, plotting, reverse engineering | Best free visual tool for raw CAN work. |
| Wireshark | Free/open source | Packet/capture inspection | Useful for SocketCAN captures and protocol inspection. |
| ELM327-emulator | Free/open source | Testing without a car | Lets development continue on a bench or laptop. |
| SQLite | Free/open source | Local scan history | Good for stored scans, vehicle profiles, and logs. |
| DuckDB | Free/open source | Fast log analysis | Useful later for big test-drive logs. |
| Grafana | Free/open source core | Dashboards/log review | Optional later if you want garage analytics. |

Sources worth knowing: python-OBD is made for OBD-II data from ELM327-style adapters, SocketCAN is the Linux kernel CAN networking stack, SavvyCAN is a cross-platform CAN capture/reverse-engineering tool, and Wireshark is a free/open-source packet analyzer.

## Useful Free Or Free-Tier Vehicle Software

| Software | Brand Coverage | Cost Notes | Use |
| --- | --- | --- | --- |
| FORScan | Ford, Mazda, Lincoln, Mercury | Free/basic options, paid license for some functions | Best Ford-family practical diagnostic/config tool. Great reference for Ford behavior. |
| Torque Lite | Generic OBD2 Android | Free version | Quick sanity check with cheap adapters. |
| Car Scanner ELM OBD2 | Generic OBD2 mobile app | Free with paid extras | Good phone-based comparison tool. |
| OBD Auto Doctor | Generic OBD2 | Free/basic with paid upgrade | Useful for comparing generic PID behavior. |
| OEM service info sites | Brand-specific | Often paid | Needed for real enhanced diagnostics, pinouts, and module procedures. |

## Adapter Strategy

Start with one solid USB OBD2 adapter and one raw CAN adapter.

Best first buy:

1. OBDLink SX or OBDLink EX USB adapter.
2. OBD2 extension cable.
3. OBD2 breakout box.

Best later buy:

1. CANable/CANtact-style SocketCAN adapter.
2. CAN FD adapter if you start testing newer vehicles.
3. J2534 adapter if you want to chase OEM-level support.

## What The Tool Should Support First

| Feature | Priority | Notes |
| --- | --- | --- |
| Adapter auto-detect | High | USB serial first. |
| VIN read | High | Works on many OBD2 vehicles, but not all. |
| Protocol read | High | Shows CAN, ISO, KWP, J1850, etc. |
| Stored codes | High | Generic DTC read. |
| Pending codes | High | Needed for emissions/driveability. |
| Clear codes | High | Require confirmation before clearing. |
| Live data | High | RPM, coolant, speed, trims, O2, throttle, voltage. |
| Freeze frame | Medium | Important for diagnosing why a code set. |
| Mode 06 tests | Medium | Useful but more complex to present clearly. |
| CSV/JSON logs | High | Critical for test drives. |
| Vehicle profiles | Medium | Save supported PID list by vehicle/VIN. |
| Raw CAN capture | Later | Needs SocketCAN adapter and safety limits. |
| Manufacturer enhanced PIDs | Later | Brand-specific, not universal. |
| Bidirectional control | Much later | Risky. Needs guardrails and vehicle-specific logic. |

## What Will Not Be Universal For Free

These are the areas where cheap/free tools usually fall short:

- ABS, airbag, BCM, HVAC, radio, immobilizer, and other non-engine modules.
- Manufacturer enhanced PIDs.
- Bidirectional tests like commanding fans, pumps, solenoids, windows, locks, or relearns.
- Key programming, security access, and module coding.
- Accurate definitions for every CAN signal without reverse engineering or paid data.

The realistic plan is:

1. Build excellent generic OBD2.
2. Add raw CAN logging.
3. Add vehicle profiles.
4. Add brand-specific plugins one brand at a time.

## Safety Rules

- Do not send random CAN frames on a real vehicle.
- Use listen-only mode for CAN sniffing when possible.
- Never run bidirectional tests unless the car is safe, parked, and the function is understood.
- Keep a battery charger on the vehicle during long diagnostic sessions.
- Do not clear codes before saving a scan report.
- On modern vehicles, assume modules can wake up unexpectedly when the OBD port is powered.

## Foxbody Note

The 1988 Mustang is not factory OBD2. For your Foxbody, this project should eventually use separate data adapters:

- Generic OBD2 adapter for normal OBD2 cars.
- Microsquirt serial adapter for the Mustang ECU.
- BCM/Pico serial or CAN adapter for body-control data.
- Optional raw CAN adapter for future add-ons.
