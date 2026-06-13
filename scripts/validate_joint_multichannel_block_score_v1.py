#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "data/derived/joint_multichannel_block_score_v1.csv"
CONTROLS = ROOT / "data/derived/joint_multichannel_block_score_v1_controls.csv"
LOO = ROOT / "data/derived/joint_multichannel_block_score_v1_leave_one_channel.csv"
SUMMARY = ROOT / "data/derived/joint_multichannel_block_score_v1_summary.csv"
DOC = ROOT / "docs/joint_multichannel_block_score_v1.md"
CLAIM_BOUNDARY = "joint_multichannel_block_score_prevalidation_not_joint_likelihood"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def main() -> None:
    rows = read_rows(RESULTS)
    controls = read_rows(CONTROLS)
    loo = read_rows(LOO)
    summary = read_one(SUMMARY)
    if not DOC.exists():
        raise SystemExit("missing joint block-score documentation")
    for row in rows:
        if row["claim_boundary"] != CLAIM_BOUNDARY:
            raise SystemExit(f"bad claim boundary for {row['channel_id']}")
        for flag in ["endpoint_validation_claimed", "cosmological_validation_claimed"]:
            if row[flag] != "false":
                raise SystemExit(f"{flag} must remain false for {row['channel_id']}")
    for row in controls:
        if row["claim_boundary"] != CLAIM_BOUNDARY:
            raise SystemExit(f"bad control claim boundary for {row['control_id']}")
    for row in loo:
        if row["claim_boundary"] != CLAIM_BOUNDARY:
            raise SystemExit(f"bad leave-one claim boundary for {row['dropped_channel_id']}")
    for flag in ["joint_likelihood_claimed", "endpoint_validation_claimed", "cosmological_validation_claimed"]:
        if summary[flag] != "false":
            raise SystemExit(f"summary {flag} must remain false")
    if summary["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("summary claim boundary mismatch")
    nonzero = sum(1 for row in rows if row["included_in_block_score"] == "true")
    if int(summary["nonzero_weight_channels"]) != nonzero:
        raise SystemExit("nonzero channel count mismatch")
    if int(summary["leave_one_total_count"]) != len(loo):
        raise SystemExit("leave-one count mismatch")
    if int(summary["combined_control_count"]) != len(controls):
        raise SystemExit("control count mismatch")
    p_sign = float(summary["exact_sign_flip_one_sided_p_ge_observed"])
    if not (0.0 <= p_sign <= 1.0):
        raise SystemExit("invalid sign-flip p-value")
    if "VALIDATION" in summary["verdict"] and "PREVALIDATION" not in summary["verdict"]:
        raise SystemExit("verdict risks validation overclaim")
    print(
        "JOINT_MULTICHANNEL_BLOCK_SCORE_V1_VALIDATED "
        f"block_normalized_score={summary['block_normalized_score']} "
        f"claim_boundary={CLAIM_BOUNDARY}"
    )


if __name__ == "__main__":
    main()
