#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "derived" / "act_dr6_lensing_path_weight_candidate_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "act_dr6_lensing_path_weight_candidate_v1_summary.csv"
DOC = ROOT / "docs" / "act_dr6_lensing_path_weight_candidate_v1.md"
CLAIM_BOUNDARY = "act_dr6_lensing_path_weight_candidate_source_side_not_endpoint_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    rows = read_rows(OUT)
    summary_rows = read_rows(SUMMARY)
    if len(summary_rows) != 1:
        raise SystemExit("expected one ACT path-weight candidate summary row")
    summary = summary_rows[0]
    if int(summary["source_rows"]) != len(rows):
        raise SystemExit("source row count mismatch")
    if int(summary["mask_positive_rows"]) <= 0:
        raise SystemExit("path-weight candidate has no mask-positive rows")
    if summary["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("summary claim boundary mismatch")
    for field in (
        "endpoint_replay_allowed",
        "endpoint_validation_claimed",
        "physical_lensing_path_weight_claimed",
        "contains_distance_residuals",
        "contains_fit_statistics",
    ):
        if summary[field] != "false":
            raise SystemExit(f"summary field must remain false: {field}")
    for row in rows:
        if row["claim_boundary"] != CLAIM_BOUNDARY:
            raise SystemExit("row claim boundary mismatch")
        for field in (
            "endpoint_replay_allowed",
            "endpoint_validation_claimed",
            "physical_lensing_path_weight_claimed",
            "contains_distance_residuals",
            "contains_fit_statistics",
        ):
            if row[field] != "false":
                raise SystemExit(f"row field must remain false: {field}")
        if row["mask_positive"] == "false" and row["w_act_baseline_candidate"] != "0":
            raise SystemExit("outside-mask rows must carry zero ACT baseline candidate weight")
    text = DOC.read_text()
    for marker in ["endpoint replay", "null controls", CLAIM_BOUNDARY]:
        if marker not in text:
            raise SystemExit(f"doc missing marker: {marker}")
    print(
        "ACT_DR6_LENSING_PATH_WEIGHT_CANDIDATE_V1_VALIDATED "
        f"rows={summary['source_rows']} endpoint=false"
    )


if __name__ == "__main__":
    main()
