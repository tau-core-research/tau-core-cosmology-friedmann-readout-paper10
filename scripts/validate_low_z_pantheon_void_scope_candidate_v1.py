#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "low_z_pantheon_void_scope_candidate_policy_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "low_z_pantheon_void_scope_candidate_v1_summary.csv"
MASK = ROOT / "data" / "derived" / "low_z_pantheon_void_scope_candidate_v1_row_mask.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    policy = read_one(POLICY)
    summary = read_one(SUMMARY)
    rows = read_rows(MASK)
    included = [row for row in rows if row["included"] == "true"]
    excluded = [row for row in rows if row["included"] == "false"]

    require(policy["endpoint_scoring_allowed"] == "false", "policy must not allow endpoint scoring")
    require(summary["endpoint_scoring_allowed"] == "false", "summary must not allow endpoint scoring")
    require(summary["physical_validation_claimed"] == "false", "summary must not claim validation")
    require(summary["candidate_endpoint_run_allowed_now"] == "false", "candidate endpoint must not be allowed now")
    require(
        summary["requires_separate_authorization_before_scoring"] == "true",
        "separate authorization must be required before scoring",
    )
    require(
        summary["claim_boundary"] == "low_z_void_scope_candidate_not_scoring_not_validation",
        "claim boundary mismatch",
    )
    require(int(summary["included_rows"]) == len(included), "included row count mismatch")
    require(int(summary["excluded_rows"]) == len(excluded), "excluded row count mismatch")
    require(len(included) > 0, "low-z scope candidate should include at least one row")
    require(len(included) < len(rows), "low-z scope candidate should be narrower than full Pantheon")
    z_support_max = float(summary["z_support_max"])
    require(z_support_max < 0.2, "low-z support max must remain low-z")
    require(all(float(row["zHD"]) <= z_support_max for row in included), "included rows exceed z support")
    require(all(float(row["W_void_source_native_basis"]) > 0.0 for row in included), "included rows need positive void basis")
    require({row["endpoint_scoring_allowed"] for row in rows} == {"false"}, "mask must not allow scoring")
    require({row["physical_validation_claimed"] for row in rows} == {"false"}, "mask must not claim validation")
    forbidden = summary["forbidden_inputs"]
    for marker in ["residuals", "chi2", "AIC", "BIC", "endpoint_rank", "fit_improvement_flags"]:
        require(marker in forbidden, f"missing forbidden input marker: {marker}")
    print(
        "PAPER10_LOW_Z_PANTHEON_VOID_SCOPE_CANDIDATE_V1_VALIDATED "
        f"included={len(included)} z_max={z_support_max:.12g} "
        "claim_boundary=not_scoring_not_validation"
    )


if __name__ == "__main__":
    main()
