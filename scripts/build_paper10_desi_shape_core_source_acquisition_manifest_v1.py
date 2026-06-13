#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_shape_core_source_acquisition_manifest_policy_v1.csv"
ROW_AUDIT = ROOT / "data/derived/paper10_desi_shape_row_sensitivity_source_audit_v1.csv"
ROW_AUDIT_SUMMARY = ROOT / "data/derived/paper10_desi_shape_row_sensitivity_source_audit_v1_summary.csv"
OUT = ROOT / "data/derived/paper10_desi_shape_core_source_acquisition_manifest_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_shape_core_source_acquisition_manifest_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_shape_core_source_acquisition_manifest_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required input: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def one_row(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def target_priority(row: dict[str, str]) -> str:
    if row["source_caveat"] != "no_major_source_caveat_in_current_manifest":
        return "P0"
    if row["sensitivity_class"] == "core_sensitive":
        return "P1"
    return "P2"


def required_source(row: dict[str, str]) -> str:
    if row["source_caveat"] != "no_major_source_caveat_in_current_manifest":
        return (
            "independent_clock_or_source_native_shape_support_for_same_radial_interval_"
            "not_reusing_the_single_reference_family_pair"
        )
    return (
        "confirmatory_independent_clock_or_source_native_shape_support_for_core_sensitive_"
        "interval_without_endpoint_residuals"
    )


def main() -> None:
    policy = one_row(POLICY)
    if policy["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("bad shape-core acquisition policy claim boundary")
    for field in ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"]:
        if policy[field] != "false":
            raise SystemExit(f"policy {field} must remain false")

    audit_summary = one_row(ROW_AUDIT_SUMMARY)
    if audit_summary["core_sensitive_rows"] != "1;2":
        raise SystemExit("shape-core acquisition expects core-sensitive rows 1;2")
    if audit_summary["endpoint_validation_claimed"] != "false":
        raise SystemExit("shape-core acquisition requires non-validation audit summary")

    audit_rows = read_rows(ROW_AUDIT)
    core_rows = [row for row in audit_rows if row["sensitivity_class"] == "core_sensitive"]
    if [row["shape_row"] for row in core_rows] != ["1", "2"]:
        raise SystemExit("shape-core acquisition must freeze rows 1 and 2")

    rows: list[dict[str, str]] = []
    for row in core_rows:
        priority = target_priority(row)
        rows.append(
            {
                "manifest_id": policy["manifest_id"],
                "target_id": f"DESI_SHAPE_ROW_{row['shape_row']}_CORE_SUPPORT",
                "priority": priority,
                "shape_row": row["shape_row"],
                "radial_interval": row["radial_interval"],
                "z_left": row["z_left"],
                "z_right": row["z_right"],
                "z_mid": row["z_mid"],
                "current_shape_value": row["shape_value"],
                "dependency_loss_fraction_when_dropped": row["dependency_loss_fraction_when_dropped"],
                "current_source_caveat": row["source_caveat"],
                "current_left_reference": row["left_cc_reference"],
                "current_right_reference": row["right_cc_reference"],
                "required_new_source": required_source(row),
                "acceptable_source_types": "peer_reviewed_CC_Hz;public_CC_compilation;source_native_BAO_CC_shape_support;independent_time_readout_shape_observable",
                "minimum_quality_rule": "must_provide_z_or_bin_center;value_or_shape_constraint;uncertainty_or_covariance;method;citation_or_release_id;no_endpoint_residual_use",
                "preferred_z_window": f"{row['z_left']}<=z<= {row['z_right']} or direct support for z_mid={row['z_mid']}",
                "hard_no_endpoint_leakage_rule": "true",
                "source_fetch_status": "not_fetched",
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(OUT, rows)

    summary = [
        {
            "manifest_id": policy["manifest_id"],
            "status": "DESI_SHAPE_CORE_SOURCE_ACQUISITION_MANIFEST_FROZEN_NOT_FETCHED_NOT_VALIDATION",
            "target_count": str(len(rows)),
            "p0_targets": ";".join(row["target_id"] for row in rows if row["priority"] == "P0"),
            "p1_targets": ";".join(row["target_id"] for row in rows if row["priority"] == "P1"),
            "core_sensitive_rows": audit_summary["core_sensitive_rows"],
            "caveated_core_sensitive_rows": audit_summary["caveated_core_sensitive_rows"],
            "source_fetch_completed": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
            "verdict": "shape_core_source_targets_frozen_sources_not_attached_not_validation",
            "recommended_next_action": "fetch_or_review_independent_shape_support_for_row2_first_then_row1",
        }
    ]
    write_csv(SUMMARY, summary)
    print(f"wrote {OUT.relative_to(ROOT)}")
    print(f"wrote {SUMMARY.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
