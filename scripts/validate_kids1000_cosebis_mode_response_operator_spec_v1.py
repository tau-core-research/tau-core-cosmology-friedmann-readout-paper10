#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_mode_response_operator_spec_policy_v1.csv"
LEDGER = ROOT / "data" / "derived" / "kids1000_cosebis_mode_response_operator_spec_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_mode_response_operator_spec_v1_summary.csv"


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
    rows = read_rows(LEDGER)
    summary = read_one(SUMMARY)
    if policy["status"] != "MODE_RESPONSE_OPERATOR_SPEC_POLICY_FROZEN":
        raise SystemExit("unexpected mode-response operator spec policy status")
    if policy["uses_kids_data_vector_values"] != "false":
        raise SystemExit("policy must not use KiDS data-vector values")
    if policy["uses_fit_statistics"] != "false":
        raise SystemExit("policy must not use fit statistics")
    if policy["uses_random_noise"] != "false":
        raise SystemExit("policy must not use random noise")
    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("policy must remain non-scoring")
    if summary["status"] != "MODE_RESPONSE_OPERATOR_SPEC_COMPLETE_NOT_DERIVED":
        raise SystemExit("unexpected summary status")
    if summary["operator_spec_verdict"] != "operator_requirements_frozen_but_survey_native_mode_response_not_derived":
        raise SystemExit("unexpected operator spec verdict")
    if summary["mode_response_operator_derived"] != "false":
        raise SystemExit("mode-response operator must not be marked derived")
    if summary["open_blocker_count"] != "2":
        raise SystemExit("expected two open blockers")
    if summary["endpoint_validation_claimed"] != "false":
        raise SystemExit("operator spec must not claim validation")
    if len(rows) != 8 or summary["requirements"] != "8":
        raise SystemExit("requirement row count mismatch")
    by_id = {row["requirement_id"]: row for row in rows}
    expected_ids = {
        "R1_domain_path_observable",
        "R2_codomain_cosebis_rows",
        "R3_linearity_before_endpoint_amplitude",
        "R4_mode_response_from_source_operator",
        "R5_pair_redshift_path_separation",
        "R6_no_data_vector_or_fit_feedback",
        "R7_gauge_or_mask_null_safety",
        "R8_standard_lensing_null_limit",
    }
    if set(by_id) != expected_ids:
        raise SystemExit("unexpected requirement ids")
    if by_id["R4_mode_response_from_source_operator"]["status"] != "OPEN_BLOCKER":
        raise SystemExit("mode response from source operator must remain open")
    if by_id["R7_gauge_or_mask_null_safety"]["status"] != "OPEN_BLOCKER":
        raise SystemExit("gauge/null operator safety must remain open")
    if by_id["R6_no_data_vector_or_fit_feedback"]["status"] != "SATISFIED":
        raise SystemExit("no-feedback requirement should be satisfied")
    for row in rows:
        if row["claim_boundary"] != policy["claim_boundary"]:
            raise SystemExit("claim boundary mismatch")
        if not row["dimension_check"]:
            raise SystemExit("missing dimension check")
        if not row["limit_check"]:
            raise SystemExit("missing limit check")
    for key in [
        "uses_kids_data_vector_values",
        "uses_fit_statistics",
        "uses_random_noise",
        "endpoint_scoring_allowed",
        "endpoint_validation_claimed",
    ]:
        if summary[key] != "false":
            raise SystemExit(f"summary {key} must be false")
    print(
        "PAPER10_KIDS1000_COSEBIS_MODE_RESPONSE_OPERATOR_SPEC_V1_VALIDATED "
        f"verdict={summary['operator_spec_verdict']}"
    )


if __name__ == "__main__":
    main()
