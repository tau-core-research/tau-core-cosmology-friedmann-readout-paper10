#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_best_justified_kernel_robustness_v1.csv"
CONTROLS = ROOT / "data/derived/joint_best_justified_kernel_robustness_v1_controls.csv"
SUMMARY = ROOT / "data/derived/joint_best_justified_kernel_robustness_v1_summary.csv"
DOC = ROOT / "docs/joint_best_justified_kernel_robustness_v1.md"
CLAIM_BOUNDARY = "joint_best_justified_kernel_robustness_prevalidation_not_joint_likelihood"
AGGREGATE_ID = "JOINT_BEST_JUSTIFIED_KERNEL_ROBUSTNESS_V1"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    detail = read_rows(OUT)
    controls = read_rows(CONTROLS)
    summary_rows = read_rows(SUMMARY)
    if not DOC.exists():
        raise SystemExit("missing robustness doc")
    if len(summary_rows) < 2:
        raise SystemExit("summary must contain scheme rows and aggregate row")

    for row in detail:
        if row["claim_boundary"] != CLAIM_BOUNDARY:
            raise SystemExit(f"bad detail claim boundary for {row['scheme_id']} {row['channel_id']}")
    for row in controls:
        if row["claim_boundary"] != CLAIM_BOUNDARY:
            raise SystemExit(f"bad control claim boundary for {row['control_id']}")
        p = row.get("control_score")
        if p is None:
            raise SystemExit("control row missing score")

    aggregate = None
    scheme_rows = []
    for row in summary_rows:
        if row.get("robustness_id") == AGGREGATE_ID:
            aggregate = row
        else:
            scheme_rows.append(row)
    if aggregate is None:
        raise SystemExit("missing aggregate summary row")

    for row in scheme_rows:
        if row["claim_boundary"] != CLAIM_BOUNDARY:
            raise SystemExit(f"bad scheme claim boundary for {row['scheme_id']}")
        for flag in ["endpoint_validation_claimed", "cosmological_validation_claimed"]:
            if row[flag] != "false":
                raise SystemExit(f"{flag} must remain false for {row['scheme_id']}")
        if int(row["active_channels"]) < 2:
            raise SystemExit("each robustness scheme needs at least two active channels")
        for key in ["exact_sign_flip_one_sided_p_ge_observed", "combined_control_one_sided_p_ge_observed"]:
            p = float(row[key])
            if not (0.0 <= p <= 1.0):
                raise SystemExit(f"invalid p value {key} for {row['scheme_id']}")

    for flag in ["joint_likelihood_claimed", "endpoint_validation_claimed", "cosmological_validation_claimed"]:
        if aggregate[flag] != "false":
            raise SystemExit(f"aggregate {flag} must remain false")
    if aggregate["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("aggregate claim boundary mismatch")
    if int(aggregate["schemes_tested"]) != len(scheme_rows):
        raise SystemExit("scheme count mismatch")
    if int(aggregate["positive_scheme_count"]) != sum(
        1 for row in scheme_rows if row["positive_score"] == "true"
    ):
        raise SystemExit("positive scheme count mismatch")
    if "VALIDATION" in aggregate["verdict"] and "NOT_VALIDATION" not in aggregate["verdict"]:
        raise SystemExit("aggregate verdict risks validation overclaim")

    print(
        "JOINT_BEST_JUSTIFIED_KERNEL_ROBUSTNESS_V1_VALIDATED "
        f"schemes={aggregate['schemes_tested']} "
        f"positive={aggregate['positive_scheme_count']} "
        f"claim_boundary={CLAIM_BOUNDARY}"
    )


if __name__ == "__main__":
    main()
