#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/source_manifest/paper10_desi_time_level_control_seed_manifest_v1.csv"
CONTROL_SUITE = ROOT / "data/derived/paper10_time_level_endpoint_control_suite_protocol_v1_summary.csv"
HIGH_Z_POLICY = ROOT / "data/derived/paper10_desi_dr2_high_z_bao_policy_v1_summary.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_time_level_control_seed_manifest_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_time_level_control_seed_manifest_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, row: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(row.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(row)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    rows = read_rows(MANIFEST)
    control_suite = read_one(CONTROL_SUITE)
    high_z = read_one(HIGH_Z_POLICY)
    expected = control_suite["control_family_count"]
    expected_families = {
        "rd_off_control",
        "external_prior_width_stress",
        "wrong_prior_control",
        "BAO_pair_drop_control",
        "CC_match_window_stress",
        "level_slope_swap_control",
        "redshift_order_shuffle_control",
    }
    require(control_suite["verdict"] == "time_level_endpoint_control_suite_declared_but_not_replayed", "control suite not declared")
    require(high_z["verdict"] == "high_z_lya_row_predeclared_excluded_from_first_cc_matched_time_endpoint", "high-z policy not frozen")
    require(len(rows) == int(expected), "seed manifest must contain exactly the declared control count")
    require({row["control_family"] for row in rows} == expected_families, "control families do not match declared suite")
    require(len({row["seed"] for row in rows}) == len(rows), "control seeds must be unique")
    require({row["deterministic_transform_scope"] for row in rows} == {"first_CC_matched_DESI_5row_scope"}, "bad transform scope")
    for row in rows:
        require(row["status"] == "SOURCE_SIDE_CONTROL_SEED_MANIFEST_FROZEN_NOT_REPLAY_NOT_VALIDATION", "bad status")
        require(row["parent_control_suite"] == "PAPER10_TIME_LEVEL_ENDPOINT_CONTROL_SUITE_PROTOCOL_V1", "bad parent control suite")
        require(row["parent_high_z_policy"] == high_z["policy_id"], "bad parent high-z policy")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "bad claim boundary")
        for forbidden in [
            "endpoint_scores",
            "fit_statistics",
            "posthoc_control_selection",
            "posthoc_seed_selection",
            "posthoc_control_family_drop",
            "Pantheon_distance_residuals",
            "late_time_fit_parameters",
        ]:
            require(forbidden in row["forbidden_use"], f"missing forbidden use: {forbidden}")
        for field in ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"]:
            require(row[field] == "false", f"{field} must remain false")

    summary = {
        "seed_manifest_id": rows[0]["seed_manifest_id"],
        "status": "DESI_TIME_LEVEL_CONTROL_SEED_MANIFEST_FROZEN_NOT_REPLAY_NOT_VALIDATION",
        "parent_control_suite": rows[0]["parent_control_suite"],
        "parent_high_z_policy": rows[0]["parent_high_z_policy"],
        "control_family_count": str(len(rows)),
        "deterministic_seed_min": min(row["seed"] for row in rows),
        "deterministic_seed_max": max(row["seed"] for row in rows),
        "transform_scope": "first_CC_matched_DESI_5row_scope",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
        "verdict": "desi_time_level_control_seed_manifest_frozen_not_replayed",
    }
    write_csv(SUMMARY, summary)
    print(f"PAPER10_DESI_TIME_LEVEL_CONTROL_SEED_MANIFEST_VALIDATED verdict={summary['verdict']}")


if __name__ == "__main__":
    main()
