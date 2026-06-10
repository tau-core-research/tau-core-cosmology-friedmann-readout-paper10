#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "void_channel_remediation_policy_v1.csv"
GATE = ROOT / "data" / "derived" / "void_channel_remediation_gate_v1.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    policy = read_one(POLICY)
    gate = read_one(GATE)

    require(gate["gate_id"] == "VOID_CHANNEL_REMEDIATION_GATE_V1", "gate id mismatch")
    require(gate["policy_id"] == policy["policy_id"], "policy id mismatch")
    require(gate["endpoint_scoring_allowed"] == "false", "gate must not allow endpoint scoring")
    require(gate["physical_validation_claimed"] == "false", "gate must not claim validation")
    require(gate["full_pantheon_void_endpoint_reopen_allowed"] == "false", "full endpoint must remain blocked")
    require(gate["low_z_scope_endpoint_allowed_now"] == "false", "low-z scope must not be silently opened")
    require(
        gate["source_basis_rebuild_required_for_full_scope"] == "true",
        "full-scope source-basis rebuild requirement must be explicit",
    )
    require(
        gate["void_channel_quarantined_from_full_distance_endpoint"] == "true",
        "void channel must remain quarantined from full-distance endpoint",
    )
    require(
        gate["selected_route"] == "NO_ROUTE_SELECTED_NO_ENDPOINT_REOPEN",
        "no remediation route should be selected by this gate",
    )
    require(gate["route_status"] == "ENDPOINT_REOPEN_BLOCKED", "endpoint reopen status mismatch")
    require(
        gate["claim_boundary"] == "void_channel_remediation_gate_not_scoring_not_validation",
        "claim boundary mismatch",
    )
    require(float(gate["void_catalog_z_support_max_proxy"]) < 0.2, "void support should remain low-z")
    require(float(gate["pantheon_z_max"]) > 2.0, "parent scope should remain full Pantheon")
    require(float(gate["void_active_fraction"]) < 0.5, "void active fraction should remain limited")
    print(
        "PAPER10_VOID_CHANNEL_REMEDIATION_GATE_V1_VALIDATED "
        f"route_status={gate['route_status']} "
        "claim_boundary=not_scoring_not_validation"
    )


if __name__ == "__main__":
    main()
