#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/source_manifest/joint_best_justified_kernel_manifest_v1.csv"
RESULTS = ROOT / "data/derived/joint_best_justified_kernel_score_v1.csv"
CONTROLS = ROOT / "data/derived/joint_best_justified_kernel_score_v1_controls.csv"
LOO = ROOT / "data/derived/joint_best_justified_kernel_score_v1_leave_one_channel.csv"
SUMMARY = ROOT / "data/derived/joint_best_justified_kernel_score_v1_summary.csv"
DOC = ROOT / "docs/joint_best_justified_kernel_score_v1.md"
CLAIM_BOUNDARY = "joint_best_justified_kernel_prevalidation_not_joint_likelihood"
GATES = ["g_src", "g_tr", "g_norm", "g_ctrl", "g_leak", "g_dim", "g_proj"]
FORBIDDEN = {
    "endpoint_residual",
    "fit_improvement",
    "posterior",
    "post_score_control_rank",
}


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
    manifest = read_rows(MANIFEST)
    results = read_rows(RESULTS)
    controls = read_rows(CONTROLS)
    loo = read_rows(LOO)
    summary = read_one(SUMMARY)
    if not DOC.exists():
        raise SystemExit("missing joint best-justified kernel doc")

    if len(manifest) < 7:
        raise SystemExit("manifest must include all current joint channels")
    result_channels = {row["channel_id"] for row in results}
    manifest_channels = {row["channel_id"] for row in manifest}
    if result_channels != manifest_channels:
        raise SystemExit("manifest/result channel mismatch")

    positive = []
    q_sum = 0.0
    for row in manifest:
        if row["claim_boundary"] != CLAIM_BOUNDARY:
            raise SystemExit(f"bad manifest claim boundary for {row['channel_id']}")
        for flag in ["endpoint_validation_claimed", "cosmological_validation_claimed"]:
            if row[flag] != "false":
                raise SystemExit(f"{flag} must remain false for {row['channel_id']}")
        for key in GATES:
            val = float(row[key])
            if not (0.0 <= val <= 1.0):
                raise SystemExit(f"{key} outside [0,1] for {row['channel_id']}")
        forbidden_fields = row["forbidden_endpoint_fields"].lower()
        for marker in FORBIDDEN:
            if marker not in forbidden_fields:
                raise SystemExit(f"missing forbidden marker {marker} for {row['channel_id']}")
        q = float(row["Q_i"])
        q_sum += q
        if row["positive_support_allowed"] == "true":
            positive.append(row["channel_id"])
            if q <= 0.0:
                raise SystemExit(f"positive support row has zero Q_i: {row['channel_id']}")
        else:
            if q != 0.0:
                raise SystemExit(f"non-positive support row must have Q_i=0: {row['channel_id']}")

    if q_sum <= 0.0:
        raise SystemExit("Q_i sum must be positive")
    if len(positive) < 2:
        raise SystemExit("best-justified kernel needs at least two positive-support channels")

    weight_sum = 0.0
    for row in results:
        if row["claim_boundary"] != CLAIM_BOUNDARY:
            raise SystemExit(f"bad result claim boundary for {row['channel_id']}")
        for flag in ["endpoint_validation_claimed", "cosmological_validation_claimed"]:
            if row[flag] != "false":
                raise SystemExit(f"{flag} must remain false for {row['channel_id']}")
        weight = float(row["w_i"])
        if row["included_in_best_justified_kernel"] == "true":
            weight_sum += weight
            if row["channel_id"] not in positive:
                raise SystemExit(f"included channel not positive-support: {row['channel_id']}")
        else:
            if weight != 0.0:
                raise SystemExit(f"excluded channel has nonzero weight: {row['channel_id']}")
    if abs(weight_sum - 1.0) > 1e-6:
        raise SystemExit(f"positive-support weights must sum to 1, got {weight_sum}")

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
    if int(summary["positive_support_channels"]) != len(positive):
        raise SystemExit("positive support count mismatch")
    if int(summary["leave_one_total_count"]) != len(loo):
        raise SystemExit("leave-one count mismatch")
    if int(summary["combined_control_count"]) != len(controls):
        raise SystemExit("combined control count mismatch")
    for key in ["exact_sign_flip_one_sided_p_ge_observed", "combined_control_one_sided_p_ge_observed"]:
        p = float(summary[key])
        if not (0.0 <= p <= 1.0):
            raise SystemExit(f"invalid p-value {key}")
    if "VALIDATION" in summary["verdict"] and "NOT_VALIDATION" not in summary["verdict"]:
        raise SystemExit("verdict risks validation overclaim")

    print(
        "JOINT_BEST_JUSTIFIED_KERNEL_SCORE_V1_VALIDATED "
        f"positive_support={summary['positive_support_channels']} "
        f"normalized_score={summary['normalized_score']} "
        f"claim_boundary={CLAIM_BOUNDARY}"
    )


if __name__ == "__main__":
    main()
