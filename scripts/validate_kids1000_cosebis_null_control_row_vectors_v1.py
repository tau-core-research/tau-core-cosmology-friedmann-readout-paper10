#!/usr/bin/env python3
from __future__ import annotations

import csv
import gzip
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/kids1000_cosebis_null_control_row_vectors_v1.csv.gz"
SUMMARY = ROOT / "data/derived/kids1000_cosebis_null_control_row_vectors_v1_summary.csv"
DOC = ROOT / "docs/kids1000_cosebis_null_control_row_vectors_v1.md"
CLAIM_BOUNDARY = "kids1000_cosebis_null_control_row_vectors_not_scoring_not_validation"

EXPECTED_DRAWS = {
    "sky_rotation": 4,
    "tomographic_pair_shuffle": 1000,
    "wrong_channel_activation": 2,
    "web_path_sign_flip": 2,
}


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", newline="") as f:
        return list(csv.DictReader(f))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    rows = read_rows(OUT)
    summary_rows = read_rows(SUMMARY)
    require(len(summary_rows) == 1, "summary must contain exactly one row")
    summary = summary_rows[0]

    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    require(summary["status"] == "KIDS1000_COSEBIS_NULL_CONTROL_ROW_VECTORS_BUILT_NOT_SCORED", "unexpected status")
    require(summary["control_draw_count"] == str(sum(EXPECTED_DRAWS.values())), "unexpected control draw count")
    require(summary["rows_per_control"] == "300", "rows_per_control must be 300")
    require(summary["total_row_vector_rows"] == str(300 * sum(EXPECTED_DRAWS.values())), "unexpected total row count")
    require(len(rows) == int(summary["total_row_vector_rows"]), "row count does not match summary")
    for key in [
        "contains_control_scores",
        "contains_predictions",
        "contains_residuals",
        "contains_fit_statistics",
        "uses_kids_data_vector_values",
        "uses_posterior_chains",
        "uses_posthoc_control_selection",
        "uses_posthoc_control_multiplicity",
        "endpoint_scoring_allowed",
        "endpoint_validation_claimed",
    ]:
        require(summary[key] == "false", f"summary must keep {key}=false")

    families = Counter()
    rows_per_control: dict[str, int] = defaultdict(int)
    values_by_control: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
        require(row["control_row_vector_computed"] == "true", "row vector computed flag missing")
        for key in [
            "contains_control_scores",
            "contains_prediction",
            "contains_residual",
            "contains_fit_statistic",
            "uses_kids_data_vector_values",
            "uses_posterior_chains",
            "uses_posthoc_control_selection",
            "uses_posthoc_control_multiplicity",
            "endpoint_scoring_allowed",
            "endpoint_validation_claimed",
        ]:
            require(row[key] == "false", f"row must keep {key}=false")
        family = row["control_family"]
        require(family in EXPECTED_DRAWS, f"unexpected family: {family}")
        control_id = row["control_index_one_based"]
        rows_per_control[control_id] += 1
        values_by_control[control_id].append(float(row["control_theory_value"]))
    for control_id, count in rows_per_control.items():
        require(count == 300, f"control {control_id} has {count} rows")
    seen_control_families = {}
    for row in rows:
        seen_control_families.setdefault(row["control_index_one_based"], row["control_family"])
    for family in seen_control_families.values():
        families[family] += 1
    require(dict(families) == EXPECTED_DRAWS, f"unexpected family counts: {dict(families)}")
    require(any(any(value != 0 for value in values) for values in values_by_control.values()), "all controls are zero")

    text = DOC.read_text()
    for marker in [CLAIM_BOUNDARY, "300-row COSEBIs basis", "gzip-compressed CSV"]:
        require(marker in text, f"doc missing marker: {marker}")

    print(
        "PAPER10_KIDS1000_COSEBIS_NULL_CONTROL_ROW_VECTORS_V1_VALIDATED "
        f"rows={len(rows)}"
    )


if __name__ == "__main__":
    main()
