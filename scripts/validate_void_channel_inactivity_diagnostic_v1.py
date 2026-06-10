#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "data" / "derived" / "void_channel_inactivity_diagnostic_v1_summary.csv"
PROFILE = ROOT / "data" / "derived" / "void_channel_inactivity_diagnostic_v1_profile.csv"


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
    summary = read_one(SUMMARY)
    profile = read_rows(PROFILE)
    require(summary["status"] == "DIAGNOSTIC_COMPLETE_NOT_VALIDATION", "status mismatch")
    require(summary["physical_validation_claimed"] == "false", "must not claim validation")
    require(summary["claim_boundary"] == "void_channel_inactivity_diagnostic_not_validation", "claim boundary mismatch")
    require(summary["combined_candidate_void_channel_active_at_best"] == "false", "combined candidate should keep void inactive")
    require(summary["combined_candidate_equals_web_only_chi2"] == "true", "combined candidate should equal web-only")
    require(float(summary["void_nonzero_fraction"]) < float(summary["web_nonzero_fraction"]), "void support should be narrower than web support")
    require(float(summary["best_nonzero_void_delta_chi2_vs_zero"]) > 0.0, "nonzero void amplitudes should not improve over zero")
    require(
        summary["diagnostic_verdict"]
        == "void_basis_has_limited_support_and_nonzero_void_amplitudes_do_not_improve_frozen_profiles",
        "diagnostic verdict changed",
    )
    require({row["physical_validation_claimed"] for row in profile} == {"false"}, "profile rows must not claim validation")
    zero_rows = [row for row in profile if row["omega_void"] == "0"]
    require(len(zero_rows) == 2, "both profiles should contain omega_void=0")
    require(all(float(row["delta_chi2_vs_omega_void_zero"]) == 0.0 for row in zero_rows), "zero rows must define the baseline")
    print(
        "PAPER10_VOID_CHANNEL_INACTIVITY_DIAGNOSTIC_V1_VALIDATED "
        f"void_fraction={summary['void_nonzero_fraction']} "
        f"best_nonzero_delta={summary['best_nonzero_void_delta_chi2_vs_zero']} "
        "claim_boundary=diagnostic_not_validation"
    )


if __name__ == "__main__":
    main()
