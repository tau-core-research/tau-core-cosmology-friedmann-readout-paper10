#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/low_z_pantheon_directional_web_anisotropy_policy_v1.csv"
WEB = ROOT / "data/derived/low_z_pantheon_directional_web_anisotropy_v1.csv"
SUMMARY = ROOT / "data/derived/low_z_pantheon_directional_web_anisotropy_v1_summary.csv"
CLAIM_BOUNDARY = "directional_web_anisotropy_source_side_not_scoring_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    policy = read_one(POLICY)
    rows = read_rows(WEB)
    summary = read_one(SUMMARY)
    require(policy["status"] == "DIRECTIONAL_WEB_ANISOTROPY_SOURCE_SIDE_NOT_SCORING", "bad policy")
    require(policy["endpoint_replay_allowed"] == "false", "policy must not authorize replay")
    require(policy["endpoint_validation_claimed"] == "false", "policy must not claim validation")
    require(summary["status"] == "DIRECTIONAL_WEB_ANISOTROPY_BUILT_SOURCE_SIDE_NOT_SCORING", "bad status")
    require(summary["rows"] == str(len(rows)), "row count mismatch")
    require(summary["rows"] == "424", "expected 424 low-z rows")
    require(summary["partial_path_scope_rows"] == "12", "expected 12 partial path-scope rows")
    require(int(summary["nonempty_web_cone_rows"]) > 0, "expected at least one nonempty cone")
    require(int(summary["quadrupole_ready_rows"]) > 0, "expected at least one quadrupole-ready row")
    require(summary["endpoint_replay_allowed"] == "false", "summary must not authorize replay")
    require(summary["endpoint_validation_claimed"] == "false", "summary must not claim validation")
    require(summary["physical_lensing_path_weight_claimed"] == "false", "summary must not claim physical path")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    required = [
        "web_cone_count",
        "web_density_mean",
        "web_dipole_amplitude_rad",
        "web_quadrupole_q",
        "web_quadrupole_angle_rad",
        "web_quadrupole_xx_minus_yy",
        "web_quadrupole_xy2",
    ]
    for row in rows:
        require(row["endpoint_replay_allowed"] == "false", "row must not authorize replay")
        require(row["endpoint_validation_claimed"] == "false", "row must not claim validation")
        require(row["contains_distance_residuals"] == "false", "row must not contain residuals")
        require(row["contains_fit_statistics"] == "false", "row must not contain fit statistics")
        require(row["physical_lensing_path_weight_claimed"] == "false", "row must not claim physical path")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
        for key in required:
            require(key in row, f"missing field: {key}")
        count = int(row["web_cone_count"])
        require(count >= 0, "web count must be nonnegative")
        if count > 0:
            float(row["web_density_mean"])
            float(row["web_dipole_amplitude_rad"])
        if count >= 3:
            q = float(row["web_quadrupole_q"])
            require(0.0 <= q <= 1.0 + 1e-9, "quadrupole q must be in [0, 1]")
            float(row["web_quadrupole_angle_rad"])
            float(row["web_quadrupole_xx_minus_yy"])
            float(row["web_quadrupole_xy2"])
    print(
        "PAPER10_DIRECTIONAL_WEB_ANISOTROPY_VALIDATED "
        f"rows={summary['rows']} quadrupole_ready={summary['quadrupole_ready_rows']} "
        f"partial_ready={summary['partial_path_scope_quadrupole_ready_rows']}"
    )


if __name__ == "__main__":
    main()
