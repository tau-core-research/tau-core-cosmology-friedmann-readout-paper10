#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUN_MANIFEST = ROOT / "data/source_manifest/paper10_desi_shape_row2_authorized_replay_run_v1.csv"
AUTH_SUMMARY = ROOT / "data/derived/paper10_desi_shape_row2_replay_authorization_review_response_v1_summary.csv"
GRID = ROOT / "data/derived/paper10_desi_shape_row2_authorized_replay_v1_grid.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_shape_row2_authorized_replay_v1_summary.csv"
DOC = ROOT / "docs/paper10_desi_shape_row2_authorized_replay_v1.md"
CLAIM_BOUNDARY = "paper10_desi_shape_row2_authorized_replay_permission_only_not_validation"
BRANCHES = {
    "candidate_CLOCK_SLOPE_SHAPE_ROW2",
    "control_redshift_order_shuffle_ROW2",
    "control_wrong_time_basis_rank_reverse_ROW2",
    "control_cc_window_stress_ROW2",
    "control_rd_prior_stress_ROW2",
}


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    run = read_one(RUN_MANIFEST)
    auth = read_one(AUTH_SUMMARY)
    summary = read_one(SUMMARY)
    grid = read_rows(GRID)
    require(run["status"] == "ROW2_PERMISSION_ONLY_REPLAY_AUTHORIZED_NOT_VALIDATION", "bad run manifest")
    require(auth["verdict"] == "GO_DESI_SHAPE_ROW2_REPLAY_PERMISSION_ONLY", "missing Row2 authorization")
    require(auth["endpoint_replay_allowed"] == "true", "authorization must allow replay")
    require(auth["endpoint_validation_claimed"] == "false", "authorization must not claim validation")
    require(auth["physical_validation_claimed"] == "false", "authorization must not claim physical validation")
    require(summary["status"] == "ROW2_AUTHORIZED_REPLAY_PERMISSION_ONLY_NOT_VALIDATION", "bad summary status")
    require(summary["authorization_verdict"] == auth["verdict"], "authorization verdict mismatch")
    require(summary["shape_row"] == "2", "must be Row2-only")
    require(summary["branch_count"] == str(len(BRANCHES)), "branch count mismatch")
    require(set(row["branch"] for row in grid) == BRANCHES, "branch set mismatch")
    require(summary["endpoint_replay_allowed"] == "true", "summary must record permission-only replay")
    require(summary["endpoint_validation_claimed"] == "false", "summary must not claim endpoint validation")
    require(summary["physical_validation_claimed"] == "false", "summary must not claim physical validation")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    for row in grid:
        require(row["shape_row"] == "2", "grid must be Row2-only")
        require(row["endpoint_replay_allowed"] == "true", "grid must record permission-only replay")
        require(row["endpoint_validation_claimed"] == "false", "grid must not claim endpoint validation")
        require(row["physical_validation_claimed"] == "false", "grid must not claim physical validation")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "grid claim boundary mismatch")
        float(row["shape_value"])
        float(row["shape_sigma"])
        float(row["shape_quadratic_score"])
    for key in [
        "row2_shape_value",
        "row2_shape_sigma",
        "candidate_shape_quadratic_score",
        "best_control_shape_quadratic_score",
        "delta_candidate_minus_best_control_score",
    ]:
        float(summary[key])
    require(
        summary["verdict"]
        in {
            "row2_permission_replay_candidate_exceeds_all_row2_controls_not_validation",
            "row2_permission_replay_candidate_not_control_resistant_not_validation",
        },
        "bad verdict",
    )
    require(DOC.exists() and DOC.stat().st_size > 0, "missing replay doc")
    print(
        "PAPER10_DESI_SHAPE_ROW2_AUTHORIZED_REPLAY_VALIDATED "
        f"verdict={summary['verdict']} "
        f"candidate_score={summary['candidate_shape_quadratic_score']}"
    )


if __name__ == "__main__":
    main()
