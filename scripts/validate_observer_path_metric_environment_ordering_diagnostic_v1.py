#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/observer_path_metric_environment_ordering_diagnostic_v1.csv"
PAIRWISE = ROOT / "data/derived/observer_path_metric_environment_ordering_diagnostic_v1_pairwise.csv"
SUMMARY = ROOT / "data/derived/observer_path_metric_environment_ordering_diagnostic_v1_summary.csv"
DOC = ROOT / "docs/observer_path_metric_environment_ordering_diagnostic_v1.md"
CLAIM_BOUNDARY = "observer_path_metric_environment_ordering_diagnostic_source_side_not_endpoint"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    rows = read_rows(OUT)
    pairwise = read_rows(PAIRWISE)
    summary_rows = read_rows(SUMMARY)
    if len(rows) != 12:
        raise SystemExit("ordering diagnostic must retain the frozen 12-row scope")
    if len(pairwise) < 6:
        raise SystemExit("expected source-side pairwise diagnostics")
    if len(summary_rows) != 1:
        raise SystemExit("summary must contain exactly one row")
    for table in [rows, pairwise, summary_rows]:
        for row in table:
            if row["claim_boundary"] != CLAIM_BOUNDARY:
                raise SystemExit("claim boundary mismatch")
            for key in [
                "endpoint_replay_allowed",
                "endpoint_validation_claimed",
                "contains_endpoint_scores",
                "contains_distance_residuals",
                "physical_lensing_path_weight_claimed",
            ]:
                if row[key] != "false":
                    raise SystemExit(f"{key} must remain false")
    summary = summary_rows[0]
    if summary["best_control_branch"] != "rank_reverse":
        raise SystemExit("diagnostic must preserve the rank_reverse failure mode")
    if float(summary["delta_chi2_candidate_minus_best_control"]) <= 0.0:
        raise SystemExit("diagnostic expected candidate to remain worse than best control")
    text = DOC.read_text()
    for marker in ["not endpoint replay", "rank-reversal control", CLAIM_BOUNDARY]:
        if marker not in text:
            raise SystemExit(f"doc missing marker: {marker}")
    print(
        "OBSERVER_PATH_METRIC_ENVIRONMENT_ORDERING_DIAGNOSTIC_V1_VALIDATED "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()
