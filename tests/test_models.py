from fox_obd2.models import DiagnosticReading, DiagnosticSnapshot


def test_snapshot_serializes_readings() -> None:
    snapshot = DiagnosticSnapshot(
        adapter_port="/dev/ttyUSB0",
        protocol="ISO 15765-4 CAN",
        vehicle_vin="1FAFP42X0XF000000",
        readings=[DiagnosticReading(name="RPM", value="850 rpm")],
        trouble_codes=["P0300: Random/multiple cylinder misfire detected"],
    )

    data = snapshot.to_json_dict()

    assert data["adapter_port"] == "/dev/ttyUSB0"
    assert data["protocol"] == "ISO 15765-4 CAN"
    assert data["vehicle_vin"] == "1FAFP42X0XF000000"
    assert data["readings"] == [{"name": "RPM", "value": "850 rpm", "supported": True}]
    assert data["trouble_codes"] == ["P0300: Random/multiple cylinder misfire detected"]
