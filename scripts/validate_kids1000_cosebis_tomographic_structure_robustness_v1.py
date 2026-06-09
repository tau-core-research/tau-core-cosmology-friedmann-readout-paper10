#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_tomographic_structure_robustness_policy_v1.csv"
CONTROLS = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_structure_robustness_v1_controls.csv"
FAMILY = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_structure_robustness_v1_family_summary.csv"
TOP = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_structure_robustness_v1_top_controls.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_structure_robustness_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    policy = read_one(POLICY)
    controls = read_rows(CONTROLS)
    family = read_rows(FAMILY)
    top = read_rows(TOP)
    summary = read_one(SUMMARY)

    if policy["status"] != "TOMOGRAPHIC_STRUCTURE_ROBUSTNESS_POLICY_FROZEN":
        raise SystemExit("unexpected robustness policy status")
    if policy["endpoint_validation_claimed"] != "false":
        raise SystemExit("policy must not claim validation")
    if summary["status"] != "KIDS1000_COSEBIS_TOMOGRAPHIC_STRUCTURE_ROBUSTNESS_COMPLETE":
        raise SystemExit("unexpected robustness summary status")
    if summary["control_count"] != "1119":
        raise SystemExit("robustness run must contain 1119 controls")
    if len(controls) != 1119:
        raise SystemExit("controls CSV row count mismatch")
    if len(family) != 2:
        raise SystemExit("family summary should contain two control families")
    if len(top) != 25:
        raise SystemExit("top control table should contain 25 rows")
    by_family = {row["control_family"]: row for row in family}
    if by_family["bin_label_permutation"]["control_count"] != "119":
        raise SystemExit("bin-label permutation count should be 119")
    if by_family["auto_cross_preserving_shuffle"]["control_count"] != "1000":
        raise SystemExit("auto/cross preserving shuffle count should be 1000")
    better_count = int(summary["controls_better_than_candidate_chi2"])
    if int(summary["candidate_rank_by_chi2"]) != better_count + 1:
        raise SystemExit("candidate rank should equal better_count + 1")
    expected_tail = (better_count + 1.0) / (len(controls) + 1.0)
    if abs(float(summary["plus_one_tail_fraction_chi2"]) - expected_tail) > 1e-12:
        raise SystemExit("plus-one tail fraction mismatch")
    for row in [summary, *controls, *family, *top]:
        if row["endpoint_validation_claimed"] != "false":
            raise SystemExit("robustness rows must not claim validation")
        if row["claim_boundary"] != policy["claim_boundary"]:
            raise SystemExit("claim boundary mismatch")
    for row in controls:
        if row["uses_kids_data_vector_values_for_scoring"] != "true":
            raise SystemExit("robustness controls should record scoring data use")
        if row["uses_kids_data_vector_values_for_source_selection"] != "false":
            raise SystemExit("robustness controls must not use data values for source selection")
    print(
        "PAPER10_KIDS1000_COSEBIS_TOMOGRAPHIC_STRUCTURE_ROBUSTNESS_V1_VALIDATED "
        f"rank_chi2={summary['candidate_rank_by_chi2']}/{len(controls) + 1} "
        f"tail_chi2={summary['plus_one_tail_fraction_chi2']} "
        f"families_with_better={summary['families_with_better_than_candidate']}"
    )


if __name__ == "__main__":
    main()
