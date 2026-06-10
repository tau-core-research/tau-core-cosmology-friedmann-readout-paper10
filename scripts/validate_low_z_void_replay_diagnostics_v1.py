#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "data" / "derived" / "low_z_void_replay_diagnostics_v1_summary.csv"
BRANCHES = ROOT / "data" / "derived" / "low_z_void_replay_diagnostics_v1_branch_summary.csv"
PROFILE = ROOT / "data" / "derived" / "low_z_void_replay_diagnostics_v1_profile.csv"


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
    branches = read_rows(BRANCHES)
    profile = read_rows(PROFILE)

    require(summary["diagnostic_id"] == "LOW_Z_VOID_REPLAY_DIAGNOSTICS_V1", "diagnostic id mismatch")
    require(summary["physical_validation_claimed"] == "false", "diagnostic must not claim validation")
    require(summary["claim_boundary"] == "low_z_void_replay_diagnostic_not_validation", "claim boundary mismatch")
    require(summary["diagnosis"] == "grid_edge_pressure_and_shuffled_control_beats_candidate", "diagnosis changed")
    require(int(summary["n_rows"]) == 424, "diagnostic row count changed")
    require(float(summary["shuffled_minus_candidate_chi2"]) < 0.0, "shuffled control should remain better in chi2")
    require(summary["candidate_omega_m_at_grid_edge"] == "true", "candidate omega_m edge pressure should remain recorded")
    require(summary["candidate_omega_void_at_grid_edge"] == "true", "candidate omega_void edge pressure should remain recorded")
    require(int(summary["void_basis_unique_rounded_1e8"]) > 1, "void basis should not collapse to one value")
    require(len(profile) == 424, "profile must retain the frozen low-z row count")
    branch_names = {row["branch"] for row in branches}
    required = {
        "baseline_only",
        "void_only",
        "wrong_void_sign",
        "wrong_void_threshold",
        "deterministic_shuffled_void_within_low_z_mask",
        "zero_void_amplitude",
    }
    require(required <= branch_names, f"missing branch diagnostics: {sorted(required - branch_names)}")
    require(all(row["claim_boundary"] == "low_z_void_replay_diagnostic_not_validation" for row in branches), "branch claim boundary mismatch")
    print(
        "PAPER10_LOW_Z_VOID_REPLAY_DIAGNOSTICS_V1_VALIDATED "
        f"diagnosis={summary['diagnosis']} "
        "claim_boundary=diagnostic_not_validation"
    )


if __name__ == "__main__":
    main()
