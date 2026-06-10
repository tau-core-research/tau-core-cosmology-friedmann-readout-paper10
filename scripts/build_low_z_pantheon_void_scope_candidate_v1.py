#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "low_z_pantheon_void_scope_candidate_policy_v1.csv"
GATE = ROOT / "data" / "derived" / "void_channel_remediation_gate_v1.csv"
DESIGN = ROOT / "data" / "derived" / "pantheon_void_web_source_native_design_matrix_v1.csv"
OUT_MASK = ROOT / "data" / "derived" / "low_z_pantheon_void_scope_candidate_v1_row_mask.csv"
OUT_SUMMARY = ROOT / "data" / "derived" / "low_z_pantheon_void_scope_candidate_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    policy = read_one(POLICY)
    gate = read_one(GATE)
    design = read_rows(DESIGN)

    if policy["endpoint_scoring_allowed"].lower() != "false":
        raise SystemExit("low-z scope policy must not allow endpoint scoring")
    if gate["route_status"] != "ENDPOINT_REOPEN_BLOCKED":
        raise SystemExit("parent remediation gate must remain endpoint-blocked")
    if gate["low_z_scope_endpoint_allowed_now"] != "false":
        raise SystemExit("parent gate must not silently allow low-z endpoint")
    if policy["route_id"] != gate["allowed_route_low_z_scope"]:
        raise SystemExit("low-z route mismatch")

    z_max = float(gate["void_catalog_z_support_max_proxy"])
    mask_rows: list[dict[str, str]] = []
    included_z: list[float] = []
    included_void: list[float] = []
    for row in design:
        z = float(row["zHD"])
        void_basis = float(row["W_void_source_native_basis"])
        included = z <= z_max and void_basis > 0.0
        reason = "included_low_z_void_supported" if included else "outside_low_z_void_support_or_zero_void_basis"
        if included:
            included_z.append(z)
            included_void.append(void_basis)
        mask_rows.append(
            {
                "scope_id": policy["policy_id"],
                "CID": row["CID"],
                "source_row_index": row["source_row_index"],
                "zHD": row["zHD"],
                "W_void_source_native_basis": row["W_void_source_native_basis"],
                "W_web_source_native_basis": row["W_web_source_native_basis"],
                "included": str(included).lower(),
                "selection_reason": reason,
                "endpoint_scoring_allowed": "false",
                "physical_validation_claimed": "false",
            }
        )

    included_rows = len(included_z)
    excluded_rows = len(mask_rows) - included_rows
    summary = [
        {
            "scope_id": policy["policy_id"],
            "parent_gate_id": policy["parent_gate_id"],
            "route_id": policy["route_id"],
            "scope_status": policy["scope_status"],
            "row_rule_id": policy["row_rule_id"],
            "total_parent_pantheon_rows": str(len(mask_rows)),
            "included_rows": str(included_rows),
            "excluded_rows": str(excluded_rows),
            "included_fraction": f"{included_rows / len(mask_rows):.12g}",
            "z_support_max": f"{z_max:.12g}",
            "min_included_zHD": f"{min(included_z):.12g}" if included_z else "",
            "max_included_zHD": f"{max(included_z):.12g}" if included_z else "",
            "mean_included_void_basis": f"{sum(included_void) / included_rows:.12g}" if included_rows else "",
            "endpoint_scoring_allowed": "false",
            "physical_validation_claimed": "false",
            "candidate_endpoint_run_allowed_now": "false",
            "requires_separate_authorization_before_scoring": "true",
            "forbidden_inputs": policy["forbidden_inputs"],
            "claim_boundary": policy["claim_boundary"],
        }
    ]

    write_csv(OUT_MASK, mask_rows)
    write_csv(OUT_SUMMARY, summary)
    print(
        "PAPER10_LOW_Z_PANTHEON_VOID_SCOPE_CANDIDATE_V1_BUILT "
        f"included={included_rows} z_max={z_max:.12g} "
        "claim_boundary=not_scoring_not_validation"
    )


if __name__ == "__main__":
    main()
