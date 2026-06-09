#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_tomographic_control_plausibility_audit_policy_v1.csv"
AUDIT = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_control_plausibility_audit_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_control_plausibility_audit_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    policy = read_one(POLICY)
    rows = read_rows(AUDIT)
    summary = read_one(SUMMARY)

    if policy["status"] != "TOMOGRAPHIC_CONTROL_PLAUSIBILITY_AUDIT_POLICY_FROZEN":
        raise SystemExit("unexpected plausibility policy status")
    if policy["computes_new_scores"] != "false":
        raise SystemExit("plausibility audit must not compute new scores")
    if summary["status"] != "TOMOGRAPHIC_CONTROL_PLAUSIBILITY_AUDIT_BUILT":
        raise SystemExit("unexpected plausibility summary status")
    if summary["audited_top_control_count"] != "25" or len(rows) != 25:
        raise SystemExit("audit should contain top 25 controls")
    if summary["better_than_candidate_audited_count"] != "3":
        raise SystemExit("expected three better-than-candidate controls in the top audit")
    if summary["accepted_physical_alternative_count"] != "0":
        raise SystemExit("no tomographic control should be accepted as a physical alternative")
    if summary["candidate_tomographic_caveat_active"] != "true":
        raise SystemExit("tomographic caveat should remain active")
    if summary["tomographic_controls_refute_endpoint_signal"] != "false":
        raise SystemExit("controls should not be classified as refuting the endpoint signal")
    if summary["tomographic_controls_block_validation"] != "true":
        raise SystemExit("controls should block validation")
    expected_verdict = "better_tomographic_controls_are_control_only_or_source_systematic_candidates_not_physical_alternatives"
    if summary["verdict"] != expected_verdict:
        raise SystemExit("unexpected plausibility verdict")

    better = [row for row in rows if row["beats_candidate_chi2"] == "true"]
    if len(better) != 3:
        raise SystemExit("expected three better controls in audited top rows")
    statuses = {row["physical_alternative_status"] for row in better}
    if statuses != {"CONTROL_ONLY", "CONDITIONAL_SOURCE_SYSTEMATIC"}:
        raise SystemExit("better controls should be control-only or conditional source systematic")
    if not any(row["control_family"] == "bin_label_permutation" for row in better):
        raise SystemExit("one better control should be a bin-label permutation")
    if not any(row["control_family"] == "auto_cross_preserving_shuffle" for row in better):
        raise SystemExit("better controls should include auto/cross preserving shuffles")
    for row in rows:
        if row["computes_new_scores"] != "false":
            raise SystemExit("audit rows must not compute new scores")
        if row["uses_kids_data_vector_values_for_source_selection"] != "false":
            raise SystemExit("audit rows must not use endpoint data for source selection")
        if row["endpoint_validation_claimed"] != "false":
            raise SystemExit("audit rows must not claim validation")
        if row["claim_boundary"] != policy["claim_boundary"]:
            raise SystemExit("claim boundary mismatch")
    if summary["claim_boundary"] != policy["claim_boundary"]:
        raise SystemExit("summary claim boundary mismatch")
    print(
        "PAPER10_KIDS1000_COSEBIS_TOMOGRAPHIC_CONTROL_PLAUSIBILITY_AUDIT_V1_VALIDATED "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()
