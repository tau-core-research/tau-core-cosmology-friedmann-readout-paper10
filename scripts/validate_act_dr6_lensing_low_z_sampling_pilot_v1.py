#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "derived" / "act_dr6_lensing_low_z_sampling_pilot_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "act_dr6_lensing_low_z_sampling_pilot_v1_summary.csv"
CLAIM_BOUNDARY = "act_dr6_lensing_low_z_sampling_pilot_source_side_not_endpoint_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def is_float(value: str) -> bool:
    try:
        float(value)
        return True
    except ValueError:
        return False


def main() -> None:
    rows = read_rows(OUT)
    summary_rows = read_rows(SUMMARY)
    if len(summary_rows) != 1:
        raise SystemExit("expected one ACT low-z sampling summary row")
    summary = summary_rows[0]
    if not rows:
        raise SystemExit("ACT low-z sampling pilot is empty")
    if summary["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("summary claim boundary mismatch")
    if int(summary["source_rows"]) != len(rows):
        raise SystemExit("summary source row count mismatch")
    if summary["endpoint_replay_allowed"] != "false":
        raise SystemExit("summary must not allow endpoint replay")
    if summary["endpoint_validation_claimed"] != "false":
        raise SystemExit("summary must not claim endpoint validation")
    if summary["physical_lensing_path_weight_claimed"] != "false":
        raise SystemExit("summary must not claim physical lensing path weights")
    if summary["contains_distance_residuals"] != "false":
        raise SystemExit("summary must not contain distance residuals")
    if summary["contains_fit_statistics"] != "false":
        raise SystemExit("summary must not contain fit statistics")
    if int(summary["baseline_sample_finite_count"]) != len(rows):
        raise SystemExit("baseline samples must be finite for every row")
    if int(summary["curl_sample_finite_count"]) != len(rows):
        raise SystemExit("curl samples must be finite for every row")
    if int(summary["diff_f150_f090_sample_finite_count"]) != len(rows):
        raise SystemExit("diff null-control samples must be finite for every row")
    if int(summary["mask_positive_count"]) + int(summary["mask_zero_count"]) != len(rows):
        raise SystemExit("mask coverage counts do not sum to source rows")
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
        for field in (
            "baseline_kappa_lr",
            "curl_kappa_lr",
            "diff_f150_f090_kappa_lr",
            "baseline_mask_nside4096",
        ):
            if not is_float(row[field]):
                raise SystemExit(f"non-numeric sampled field: {field}")
    print(
        "ACT_DR6_LENSING_LOW_Z_SAMPLING_PILOT_V1_VALIDATED "
        f"rows={summary['source_rows']} endpoint=false"
    )


if __name__ == "__main__":
    main()
