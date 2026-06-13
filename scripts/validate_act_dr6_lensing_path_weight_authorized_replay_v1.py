#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUTH_SUMMARY = (
    ROOT / "data" / "derived" / "act_dr6_lensing_path_weight_replay_authorization_review_response_v1_summary.csv"
)
GRID = ROOT / "data" / "derived" / "act_dr6_lensing_path_weight_authorized_replay_v1_grid.csv"
SUMMARY = ROOT / "data" / "derived" / "act_dr6_lensing_path_weight_authorized_replay_v1_summary.csv"
CLAIM_BOUNDARY = "act_dr6_lensing_path_weight_authorized_replay_permission_only_not_validation"
BRANCHES = {
    "baseline_only",
    "candidate",
    "off",
    "wrong_sign",
    "curl_null",
    "diff_f150_f090_null",
    "deterministic_shuffle",
    "rank_reverse",
}


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"expected one row in {path.relative_to(ROOT)}")
    return rows[0]


def main() -> None:
    auth = read_one(AUTH_SUMMARY)
    summary = read_one(SUMMARY)
    grid = read_rows(GRID)
    if auth["permission_only_replay_authorized"] != "true":
        raise SystemExit("missing permission-only authorization")
    if summary["status"] != "ACT_DR6_LENSING_PATH_WEIGHT_AUTHORIZED_REPLAY_PERMISSION_ONLY_NOT_VALIDATION":
        raise SystemExit("bad replay summary status")
    if summary["authorization_verdict"] != auth["verdict"]:
        raise SystemExit("authorization verdict mismatch")
    if set(row["branch"] for row in grid) != BRANCHES:
        raise SystemExit("branch set mismatch")
    for key in ("permission_only_replay_authorized",):
        if summary[key] != "true":
            raise SystemExit(f"summary must keep {key}=true")
    for key in ("endpoint_validation_claimed", "physical_lensing_path_weight_claimed"):
        if summary[key] != "false":
            raise SystemExit(f"summary must keep {key}=false")
    if summary["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("summary claim boundary mismatch")
    for row in grid:
        if row["permission_only_replay_authorized"] != "true":
            raise SystemExit("grid rows must record permission-only authorization")
        if row["endpoint_validation_claimed"] != "false":
            raise SystemExit("grid rows must not claim validation")
        if row["physical_lensing_path_weight_claimed"] != "false":
            raise SystemExit("grid rows must not claim physical lensing path weight")
        if row["claim_boundary"] != CLAIM_BOUNDARY:
            raise SystemExit("grid claim boundary mismatch")
        float(row["chi2_act_path"]) if row["chi2_act_path"] != "inf" else float("inf")
        float(row["aic_act_path"]) if row["aic_act_path"] != "inf" else float("inf")
    print(
        "ACT_DR6_LENSING_PATH_WEIGHT_AUTHORIZED_REPLAY_VALIDATED "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()
