from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class DiagnosticReading:
    name: str
    value: str
    supported: bool = True


@dataclass(frozen=True)
class DiagnosticSnapshot:
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    adapter_port: str | None = None
    protocol: str | None = None
    vehicle_vin: str | None = None
    readings: list[DiagnosticReading] = field(default_factory=list)
    trouble_codes: list[str] = field(default_factory=list)

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "created_at": self.created_at.isoformat(),
            "adapter_port": self.adapter_port,
            "protocol": self.protocol,
            "vehicle_vin": self.vehicle_vin,
            "readings": [reading.__dict__ for reading in self.readings],
            "trouble_codes": self.trouble_codes,
        }
