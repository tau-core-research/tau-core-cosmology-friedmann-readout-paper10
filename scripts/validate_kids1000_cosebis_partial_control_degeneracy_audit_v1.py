#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_partial_control_degeneracy_audit_policy_v1.csv"
PAIR_GRID = ROOT / "data" / "derived" / "kids1000_cosebis_partial_control_degeneracy_audit_v1_pair_grid.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_partial_control_degeneracy_audit_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def main() -> None:
    policy = read_one(POLICY)
    summary = read_one(SUMMARY)
    with PAIR_GRID.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if policy["status"] != "PARTIAL_CONTROL_DEGENERACY_AUDIT_NOT_ENDPOINT_VALIDATION":
        raise SystemExit("unexpected degeneracy audit policy status")
    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("degeneracy audit policy must keep endpoint scoring disabled")
    if "kids_data_vector_values" not in policy["forbidden_inputs"]:
        raise SystemExit("data vector values must be forbidden for degeneracy audit")
    if summary["status"] != "PARTIAL_CONTROL_DEGENERACY_AUDIT_BUILT_NOT_ENDPOINT_VALIDATION":
        raise SystemExit("unexpected degeneracy audit summary status")
    if summary["claim_boundary"] != policy["claim_boundary"]:
        raise SystemExit("claim boundary mismatch")
    if summary["uses_kids_data_vector_values"] != "false":
        raise SystemExit("degeneracy audit must not use KiDS data-vector values")
    if summary["uses_kids_covariance_for_metric_only"] != "true":
        raise SystemExit("degeneracy audit must disclose covariance metric use")
    if summary["uses_posterior_chains"] != "false" or summary["uses_posthoc_selection"] != "false":
        raise SystemExit("degeneracy audit must not use posterior chains or posthoc selection")
    if summary["endpoint_scoring_allowed"] != "false" or summary["endpoint_validation_claimed"] != "false":
        raise SystemExit("degeneracy audit must not claim endpoint validation")
    if summary["branch_degeneracy_detected"] != "true":
        raise SystemExit("degeneracy audit must detect the partial-control degeneracy")
    if summary["positive_effective_rank_tol_1e_minus_8"] != "1":
        raise SystemExit("positive partial-control branches must be effectively rank one")
    if float(summary["min_positive_abs_covariance_inverse_cosine"]) < 0.999999999:
        raise SystemExit("positive branch covariance-metric cosine is not sufficiently degenerate")
    if float(summary["max_positive_relative_shape_residual"]) > 1e-9:
        raise SystemExit("positive branch shape residual is too large for the frozen audit")
    if len(rows) != 10:
        raise SystemExit("five nonzero branches should produce ten pair rows")
    for row in rows:
        if row["claim_boundary"] != policy["claim_boundary"]:
            raise SystemExit("pair-grid claim boundary mismatch")
        if row["endpoint_scoring_allowed"] != "false":
            raise SystemExit("pair-grid endpoint scoring must remain disabled")
        if row["uses_kids_data_vector_values"] != "false":
            raise SystemExit("pair-grid must not use KiDS data-vector values")
        if row["uses_kids_covariance_for_metric_only"] != "true":
            raise SystemExit("pair-grid must disclose covariance metric use")
        if row["uses_posterior_chains"] != "false" or row["uses_posthoc_selection"] != "false":
            raise SystemExit("pair-grid must not use posterior chains or posthoc selection")
    print(
        "PAPER10_KIDS1000_COSEBIS_PARTIAL_CONTROL_DEGENERACY_AUDIT_V1_VALIDATED "
        f"positive_rank={summary['positive_effective_rank_tol_1e_minus_8']} "
        "endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()
