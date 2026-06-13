#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/source_manifest/joint_multichannel_endpoint_manifest_v1.csv"
RESULTS = ROOT / "data/derived/joint_multichannel_endpoint_candidate_v1.csv"
SUMMARY = ROOT / "data/derived/joint_multichannel_endpoint_candidate_v1_summary.csv"
DOC = ROOT / "docs/joint_multichannel_endpoint_candidate_v1.md"
CLAIM_BOUNDARY = "joint_multichannel_endpoint_candidate_preflight_not_validation"


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
    manifest_rows = read_rows(MANIFEST)
    rows = read_rows(RESULTS)
    summary = read_one(SUMMARY)
    if not DOC.exists():
        raise SystemExit("missing joint candidate documentation")
    if len(rows) != len(manifest_rows):
        raise SystemExit("joint results do not match manifest row count")
    if int(summary["channels_scored"]) != len(rows):
        raise SystemExit("summary channel count mismatch")
    if summary["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("summary claim boundary mismatch")
    for flag in ["joint_endpoint_claimed", "endpoint_validation_claimed", "cosmological_validation_claimed"]:
        if summary[flag] != "false":
            raise SystemExit(f"summary {flag} must remain false")
    weighted_sum = 0.0
    abs_weight = 0.0
    seen = set()
    for row in rows:
        if row["channel_id"] in seen:
            raise SystemExit(f"duplicate channel: {row['channel_id']}")
        seen.add(row["channel_id"])
        if row["claim_boundary"] != CLAIM_BOUNDARY:
            raise SystemExit(f"bad claim boundary for {row['channel_id']}")
        for flag in [
            "endpoint_residual_fields_used",
            "joint_endpoint_claimed",
            "endpoint_validation_claimed",
            "cosmological_validation_claimed",
        ]:
            if row[flag] != "false":
                raise SystemExit(f"{flag} must remain false for {row['channel_id']}")
        score = float(row["bounded_channel_score"])
        if score < -1.0000001 or score > 1.0000001:
            raise SystemExit(f"bounded score out of range for {row['channel_id']}")
        weight = float(row["channel_weight"])
        weighted = float(row["weighted_channel_score"])
        if abs(weight * score - weighted) > 1e-6:
            raise SystemExit(f"weighted score mismatch for {row['channel_id']}")
        weighted_sum += weighted
        abs_weight += abs(weight)
        if not (ROOT / row["source_artifact"]).exists():
            raise SystemExit(f"missing source artifact for {row['channel_id']}")
    if abs(weighted_sum - float(summary["joint_weighted_sum"])) > 1e-6:
        raise SystemExit("joint weighted sum mismatch")
    expected_norm = weighted_sum / abs_weight if abs_weight else 0.0
    if abs(expected_norm - float(summary["normalized_joint_score"])) > 1e-6:
        raise SystemExit("normalized joint score mismatch")
    if "VALIDATION" in summary["verdict"] and "PREVALIDATION" not in summary["verdict"]:
        raise SystemExit("verdict risks validation overclaim")
    print(
        "JOINT_MULTICHANNEL_ENDPOINT_CANDIDATE_V1_VALIDATED "
        f"channels={summary['channels_scored']} normalized_joint_score={summary['normalized_joint_score']} "
        f"claim_boundary={CLAIM_BOUNDARY}"
    )


if __name__ == "__main__":
    main()
