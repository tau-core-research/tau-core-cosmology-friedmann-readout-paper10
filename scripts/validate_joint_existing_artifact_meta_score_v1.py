#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "data/derived/joint_existing_artifact_meta_score_v1.csv"
SUMMARY = ROOT / "data/derived/joint_existing_artifact_meta_score_v1_summary.csv"
DOC = ROOT / "docs/joint_existing_artifact_meta_score_v1.md"
CLAIM_BOUNDARY = "joint_existing_artifact_meta_score_prevalidation_not_cosmological_validation"


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
    rows = read_rows(LEDGER)
    summary = read_one(SUMMARY)
    if not DOC.exists():
        raise SystemExit("missing documentation")
    if len(rows) < 5:
        raise SystemExit("meta-score must audit at least five channels")
    if summary["meta_score_id"] != "JOINT_EXISTING_ARTIFACT_META_SCORE_V1":
        raise SystemExit("summary meta score id mismatch")
    if int(summary["channels_audited"]) != len(rows):
        raise SystemExit("summary channel count mismatch")
    for row in rows:
        if row["claim_boundary"] != CLAIM_BOUNDARY:
            raise SystemExit(f"bad claim boundary for {row['channel_id']}")
        for field in [
            "endpoint_validation_claimed",
            "physical_validation_claimed",
            "cosmological_validation_claimed",
            "dark_sector_verdict_allowed",
        ]:
            if row[field] != "false":
                raise SystemExit(f"{field} must remain false for {row['channel_id']}")
        artifact = ROOT / row["source_artifact"]
        if not artifact.exists():
            raise SystemExit(f"missing source artifact for {row['channel_id']}: {row['source_artifact']}")
        float(row["meta_weight"])
    for field in [
        "joint_endpoint_claimed",
        "endpoint_validation_claimed",
        "physical_validation_claimed",
        "cosmological_validation_claimed",
        "dark_sector_verdict_allowed",
    ]:
        if summary[field] != "false":
            raise SystemExit(f"summary {field} must remain false")
    if summary["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("summary claim boundary mismatch")
    net = sum(float(row["meta_weight"]) for row in rows)
    if abs(net - float(summary["net_meta_weight"])) > 1e-9:
        raise SystemExit("net meta weight mismatch")
    if "VALIDATION" in summary["verdict"] and "NOT_VALIDATION" not in summary["verdict"]:
        raise SystemExit("verdict wording risks validation overclaim")
    print(
        "JOINT_EXISTING_ARTIFACT_META_SCORE_V1_VALIDATED "
        f"channels={summary['channels_audited']} net_meta_weight={summary['net_meta_weight']} "
        f"claim_boundary={CLAIM_BOUNDARY}"
    )


if __name__ == "__main__":
    main()
