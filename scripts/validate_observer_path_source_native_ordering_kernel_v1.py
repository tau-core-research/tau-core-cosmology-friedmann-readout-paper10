#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/observer_path_source_native_ordering_kernel_v1.csv"
SUMMARY = ROOT / "data/derived/observer_path_source_native_ordering_kernel_v1_summary.csv"
DOC = ROOT / "docs/observer_path_source_native_ordering_kernel_v1.md"
CLAIM_BOUNDARY = "observer_path_source_native_ordering_kernel_source_side_not_endpoint"
KERNELS = [
    "K_order_metric_environment",
    "K_order_los_web_gate",
    "K_order_void_web_los_balanced",
    "K_order_metric_los_skyz",
    "K_order_metric_observer_x_z",
    "K_order_metric_environment_gradient",
]


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    rows = read_rows(OUT)
    summary_rows = read_rows(SUMMARY)
    if len(rows) != 12:
        raise SystemExit("ordering kernel must use the frozen 12-row scope")
    if len(summary_rows) != 1:
        raise SystemExit("summary must contain exactly one row")
    for row in rows + summary_rows:
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
    for row in rows:
        for kernel in KERNELS:
            value = float(row[kernel])
            if not -1.0 < value < 1.0:
                raise SystemExit(f"{kernel} out of bounded range")
            if f"{kernel}_raw" not in row:
                raise SystemExit(f"missing raw column for {kernel}")
    summary = summary_rows[0]
    if summary["kernel_family_count"] != str(len(KERNELS)):
        raise SystemExit("kernel family count mismatch")
    text = DOC.read_text()
    for marker in ["not endpoint replay", "rank-reversal control", CLAIM_BOUNDARY]:
        if marker not in text:
            raise SystemExit(f"doc missing marker: {marker}")
    print(
        "OBSERVER_PATH_SOURCE_NATIVE_ORDERING_KERNEL_V1_VALIDATED "
        f"rows={len(rows)} families={summary['kernel_family_count']}"
    )


if __name__ == "__main__":
    main()
