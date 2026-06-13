#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/observer_path_metric_lensing_next_gate_v1.csv"
SUMMARY = ROOT / "data/derived/observer_path_metric_lensing_next_gate_v1_summary.csv"
DOC = ROOT / "docs/observer_path_metric_lensing_next_gate_v1.md"
CLAIM_BOUNDARY = "observer_path_metric_lensing_next_gate_not_endpoint_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    rows = read_rows(OUT)
    summary_rows = read_rows(SUMMARY)
    if len(rows) != 6:
        raise SystemExit("next gate must contain six gate rows")
    if len(summary_rows) != 1:
        raise SystemExit("summary must contain one row")
    for table in [rows, summary_rows]:
        for row in table:
            if row["claim_boundary"] != CLAIM_BOUNDARY:
                raise SystemExit("claim boundary mismatch")
            if row["endpoint_validation_claimed"] != "false":
                raise SystemExit("must not claim validation")
    summary = summary_rows[0]
    if summary["physical_metric_lensing_path_product_available"] != "false":
        raise SystemExit("current gate unexpectedly has physical path product")
    if summary["act_dr6_source_side_kappa_sampling_available"] != "true":
        raise SystemExit("current gate should include ACT DR6 source-side sampling")
    if summary["act_dr6_source_frozen_path_weight_candidate_available"] != "true":
        raise SystemExit("current gate should include ACT DR6 source-frozen path-weight candidate")
    if int(summary["act_dr6_mask_positive_rows"]) <= 0:
        raise SystemExit("ACT DR6 source-side sampling has no mask-positive rows")
    if summary["endpoint_replay_allowed"] != "false":
        raise SystemExit("current gate must block endpoint replay")
    if summary["physical_lensing_path_weight_claimed"] != "false":
        raise SystemExit("must not claim physical lensing path weight")
    if summary["verdict"] != "ACT_DR6_PATH_WEIGHT_CANDIDATE_READY_BUT_REVIEW_BLOCKS_REPLAY":
        raise SystemExit("unexpected next-gate verdict")
    text = DOC.read_text()
    for marker in ["not endpoint replay", "ACT DR6 source-frozen path-weight candidate", CLAIM_BOUNDARY]:
        if marker not in text:
            raise SystemExit(f"doc missing marker: {marker}")
    print(
        "OBSERVER_PATH_METRIC_LENSING_NEXT_GATE_V1_VALIDATED "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()
