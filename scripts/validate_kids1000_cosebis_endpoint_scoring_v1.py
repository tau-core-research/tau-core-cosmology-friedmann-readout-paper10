#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUN_MANIFEST = ROOT / "data" / "source_manifest" / "kids1000_cosebis_endpoint_scoring_run_v1.csv"
READINESS = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_scoring_readiness_v1_summary.csv"
GEOMETRY = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_family_geometry_audit_v1_summary.csv"
RESULTS = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_scoring_v1_results.csv"
RESIDUALS = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_scoring_v1_residuals.csv"
GRID = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_scoring_v1_grid.csv"
NULL_CONTROLS = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_scoring_v1_null_controls.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_scoring_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def require_false(row: dict[str, str], key: str) -> None:
    if row.get(key) != "false":
        raise SystemExit(f"{key} must be false")


def require_true(row: dict[str, str], key: str) -> None:
    if row.get(key) != "true":
        raise SystemExit(f"{key} must be true")


def finite_float(value: str, key: str) -> float:
    out = float(value)
    if not math.isfinite(out):
        raise SystemExit(f"{key} must be finite")
    return out


def main() -> None:
    run = read_one(RUN_MANIFEST)
    readiness = read_one(READINESS)
    geometry = read_one(GEOMETRY)
    result = read_one(RESULTS)
    summary = read_one(SUMMARY)
    grid = read_rows(GRID)
    residuals = read_rows(RESIDUALS)
    nulls = read_rows(NULL_CONTROLS)

    if run["status"] != "ENDPOINT_SCORING_APPROVED_RUN_V1":
        raise SystemExit("unexpected endpoint scoring run status")
    require_true(run, "endpoint_scoring_allowed")
    require_true(run, "explicit_user_approval_recorded")
    if readiness["first_blocker"] != "none" or readiness["blocking_component_count"] != "0":
        raise SystemExit("endpoint scoring run requires no readiness blockers")
    if geometry["endpoint_family_geometry_passed"] != "true":
        raise SystemExit("endpoint family geometry must pass before scoring")

    if summary["status"] != "KIDS1000_COSEBIS_ENDPOINT_SCORING_RUN_V1_COMPLETE":
        raise SystemExit("unexpected endpoint scoring summary status")
    require_true(summary, "endpoint_scoring_executed")
    require_false(summary, "endpoint_validation_claimed")
    require_true(summary, "uses_kids_data_vector_values_for_scoring")
    require_false(summary, "uses_kids_data_vector_values_for_source_selection")
    require_false(summary, "uses_posterior_chains")
    require_false(summary, "uses_posthoc_selection")

    if len(grid) != 2:
        raise SystemExit("endpoint scoring grid must contain baseline and candidate rows")
    if {row["branch_type"] for row in grid} != {"baseline", "candidate"}:
        raise SystemExit("endpoint scoring grid must contain exactly baseline and candidate")
    if len(residuals) != 300:
        raise SystemExit("endpoint residual table must contain 300 retained COSEBIs rows")
    if len(nulls) != 1008:
        raise SystemExit("endpoint null-control table must contain 1008 controls")

    for row in [result, summary, *residuals, *nulls]:
        require_true(row, "uses_kids_data_vector_values_for_scoring")
        require_false(row, "uses_kids_data_vector_values_for_source_selection")
    for row in [result, summary]:
        require_false(row, "uses_posterior_chains")
        require_false(row, "uses_posthoc_selection")
        require_false(row, "endpoint_validation_claimed")

    delta_chi2 = finite_float(result["candidate_delta_chi2_vs_baseline"], "candidate_delta_chi2_vs_baseline")
    delta_aic = finite_float(result["candidate_delta_aic_vs_baseline"], "candidate_delta_aic_vs_baseline")
    tail_chi2 = finite_float(result["plus_one_tail_fraction_chi2"], "plus_one_tail_fraction_chi2")
    tail_aic = finite_float(result["plus_one_tail_fraction_aic"], "plus_one_tail_fraction_aic")
    rank_chi2 = int(result["candidate_rank_by_chi2"])
    rank_aic = int(result["candidate_rank_by_aic"])
    if rank_chi2 < 1 or rank_chi2 > len(nulls) + 1:
        raise SystemExit("candidate chi2 rank is out of range")
    if rank_aic < 1 or rank_aic > len(nulls) + 1:
        raise SystemExit("candidate AIC rank is out of range")
    if not (0.0 < tail_chi2 <= 1.0 and 0.0 < tail_aic <= 1.0):
        raise SystemExit("plus-one tail fractions must be in (0,1]")
    expected_tail_chi2 = (int(result["chi2_nulls_better_than_candidate"]) + 1.0) / (len(nulls) + 1.0)
    expected_tail_aic = (int(result["aic_nulls_better_than_candidate"]) + 1.0) / (len(nulls) + 1.0)
    if abs(tail_chi2 - expected_tail_chi2) > 1e-12:
        raise SystemExit("chi2 tail fraction mismatch")
    if abs(tail_aic - expected_tail_aic) > 1e-12:
        raise SystemExit("AIC tail fraction mismatch")
    if summary["candidate_delta_chi2_vs_baseline"] != result["candidate_delta_chi2_vs_baseline"]:
        raise SystemExit("summary/result delta chi2 mismatch")
    if summary["candidate_delta_aic_vs_baseline"] != result["candidate_delta_aic_vs_baseline"]:
        raise SystemExit("summary/result delta AIC mismatch")
    if result["claim_boundary"] != run["claim_boundary"]:
        raise SystemExit("result claim boundary mismatch")
    if summary["claim_boundary"] != run["claim_boundary"]:
        raise SystemExit("summary claim boundary mismatch")

    print(
        "PAPER10_KIDS1000_COSEBIS_ENDPOINT_SCORING_V1_VALIDATED "
        f"delta_chi2={delta_chi2:.12g} delta_aic={delta_aic:.12g} "
        f"rank_chi2={rank_chi2}/{len(nulls) + 1} "
        f"tail_chi2={tail_chi2:.12g}"
    )


if __name__ == "__main__":
    main()
