# Universal OBD2 Plan

The goal is to build a scanner that works across normal OBD2-compliant cars without needing brand-specific setup first.

## Baseline Coverage

Support these standard OBD2 jobs first:

- Auto-connect to USB/Bluetooth serial adapters.
- Auto-detect vehicle protocol through the adapter.
- Read VIN when supported.
- Read stored, pending, and permanent diagnostic trouble codes.
- Clear diagnostic trouble codes with confirmation.
- Read common live PIDs.
- Log live data to JSON Lines or CSV.

## Supported Adapter Families

Start with ELM327-compatible adapters because they are common, but design around adapter classes so better hardware can be added later.

Good targets:

- OBDLink SX, LX, MX, or MX+.
- STN-based adapters.
- Quality USB ELM327 adapters.

Avoid depending on bargain clone behavior. Many cheap adapters lie about supported commands or freeze under fast polling.

## Protocols To Expect

The adapter should handle protocol negotiation, but the tool should display the protocol once connected.

Common protocols:

- ISO 15765-4 CAN 11-bit/500k
- ISO 15765-4 CAN 29-bit/500k
- ISO 9141-2
- ISO 14230-4 KWP2000
- SAE J1850 PWM
- SAE J1850 VPW

## Data Strategy

Do not assume every PID exists. Query support first, then show:

- Supported live data.
- Unsupported-but-requested data as dim/unsupported.
- Trouble codes separately from live sensor values.

## Later Brand-Specific Expansion

Once the generic scanner is solid, add optional vehicle profiles:

- Ford enhanced PIDs.
- GM enhanced PIDs.
- Chrysler enhanced PIDs.
- Toyota/Honda enhanced PIDs.

These should be optional layers, not required for basic OBD2 scanning.
