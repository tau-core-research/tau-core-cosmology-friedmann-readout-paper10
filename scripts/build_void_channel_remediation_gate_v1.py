#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "void_channel_remediation_policy_v1.csv"
BASIS_AUDIT = ROOT / "data" / "derived" / "void_source_basis_audit_v1_summary.csv"
OUT = ROOT / "data" / "derived" / "void_channel_remediation_gate_v1.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def write_one(path: Path, row: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(row.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(row)


def main() -> None:
    policy = read_one(POLICY)
    audit = read_one(BASIS_AUDIT)

    if policy["endpoint_scoring_allowed"].lower() != "false":
        raise SystemExit("remediation policy must not allow endpoint scoring")
    if audit["endpoint_scoring_allowed"].lower() != "false":
        raise SystemExit("basis audit must not allow endpoint scoring")
    if policy["source_basis_limitation"] != audit["source_basis_limitation"]:
        raise SystemExit("policy/audit source-basis limitation mismatch")

    z_support_max = float(audit["void_catalog_z_support_max_proxy"])
    pantheon_z_max = float(audit["pantheon_z_max"])
    void_active_fraction = float(audit["void_active_fraction"])

    route_status = "ENDPOINT_REOPEN_BLOCKED"
    recommended_next_action = (
        "select_predeclared_low_z_scope_or_rebuild_void_source_basis_before_any_new_endpoint"
    )
    if z_support_max >= 0.2 or void_active_fraction >= 0.5:
        route_status = "REVIEW_REQUIRED_UNEXPECTED_SUPPORT"
        recommended_next_action = "manual_review_required_before_endpoint_decision"

    row = {
        "gate_id": "VOID_CHANNEL_REMEDIATION_GATE_V1",
        "policy_id": policy["policy_id"],
        "parent_audit_id": audit["audit_id"],
        "source_basis_limitation": audit["source_basis_limitation"],
        "pantheon_z_max": audit["pantheon_z_max"],
        "void_catalog_z_support_max_proxy": audit["void_catalog_z_support_max_proxy"],
        "void_active_fraction": audit["void_active_fraction"],
        "allowed_route_low_z_scope": policy["allowed_route_low_z_scope"],
        "allowed_route_full_scope_rebuild": policy["allowed_route_full_scope_rebuild"],
        "allowed_route_quarantine": policy["allowed_route_quarantine"],
        "selected_route": policy["selected_route"],
        "route_status": route_status,
        "full_pantheon_void_endpoint_reopen_allowed": "false",
        "low_z_scope_endpoint_allowed_now": "false",
        "source_basis_rebuild_required_for_full_scope": "true",
        "void_channel_quarantined_from_full_distance_endpoint": "true",
        "endpoint_scoring_allowed": "false",
        "physical_validation_claimed": "false",
        "recommended_next_action": recommended_next_action,
        "claim_boundary": policy["claim_boundary"],
    }

    if pantheon_z_max <= 2.0:
        raise SystemExit("expected full Pantheon scope in parent audit")

    write_one(OUT, row)
    print(
        "PAPER10_VOID_CHANNEL_REMEDIATION_GATE_V1_BUILT "
        f"route_status={route_status} "
        f"z_support_max={row['void_catalog_z_support_max_proxy']} "
        "claim_boundary=not_scoring_not_validation"
    )


if __name__ == "__main__":
    main()
