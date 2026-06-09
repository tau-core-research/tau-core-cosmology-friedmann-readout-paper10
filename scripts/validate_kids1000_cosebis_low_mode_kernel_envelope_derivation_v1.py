#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_low_mode_kernel_envelope_derivation_policy_v1.csv"
MODE_WEIGHTS = ROOT / "data" / "derived" / "kids1000_cosebis_low_mode_kernel_envelope_derivation_v1_mode_weights.csv"
LEDGER = ROOT / "data" / "derived" / "kids1000_cosebis_low_mode_kernel_envelope_derivation_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_low_mode_kernel_envelope_derivation_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    policy = read_one(POLICY)
    weights = read_rows(MODE_WEIGHTS)
    ledger = read_rows(LEDGER)
    summary = read_one(SUMMARY)
    if policy["status"] != "LOW_MODE_KERNEL_ENVELOPE_DERIVATION_POLICY_FROZEN":
        raise SystemExit("unexpected kernel derivation policy status")
    if policy["uses_kids_data_vector_values"] != "false" or policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("kernel derivation policy must remain non-scoring and data-vector-free")
    if summary["status"] != "LOW_MODE_KERNEL_ENVELOPE_CONDITIONAL_DERIVATION_COMPLETE":
        raise SystemExit("unexpected kernel derivation summary status")
    if summary["derivation_verdict"] != "conditional_log_band_power_envelope_derives_n_minus_half_shape_but_covariant_kernel_blocker_remains":
        raise SystemExit("unexpected derivation verdict")
    if summary["endpoint_validation_claimed"] != "false":
        raise SystemExit("kernel derivation must not claim validation")
    if summary["open_blocker_count"] != "1":
        raise SystemExit("kernel derivation must preserve the covariant-kernel blocker")
    if len(weights) != 20 or summary["mode_count"] != "20":
        raise SystemExit("mode weights must cover modes 1..20")
    if [row["mode"] for row in weights] != [str(i) for i in range(1, 21)]:
        raise SystemExit("mode weights must be ordered over modes 1..20")
    if abs(float(summary["mean_unit_mode_weight"]) - 1.0) > 1e-12:
        raise SystemExit("unit-mean mode weights changed")
    if float(weights[0]["unit_mean_mode_weight"]) <= float(weights[-1]["unit_mean_mode_weight"]):
        raise SystemExit("low-mode carrier must downweight high modes")
    if weights[0]["unit_mean_mode_weight"] != summary["matches_frozen_theory_vector_max_weight"]:
        raise SystemExit("derived max weight must match frozen theory-vector summary")
    if weights[-1]["unit_mean_mode_weight"] != summary["matches_frozen_theory_vector_min_weight"]:
        raise SystemExit("derived min weight must match frozen theory-vector summary")
    statuses = [row["status"] for row in ledger]
    if statuses.count("ASSUMPTION") != 2:
        raise SystemExit("kernel derivation should expose two assumptions")
    if statuses.count("DERIVED_CONDITIONAL") != 2:
        raise SystemExit("kernel derivation should expose two conditional steps")
    if statuses.count("DEFINITION") != 1 or statuses.count("LIMIT_CHECK") != 1:
        raise SystemExit("kernel derivation should expose definition and limit check")
    if statuses.count("OPEN_BLOCKER") != 1:
        raise SystemExit("kernel derivation should preserve one blocker")
    for row in [summary, *weights, *ledger]:
        if row["claim_boundary"] != policy["claim_boundary"]:
            raise SystemExit("claim boundary mismatch")
    print(
        "PAPER10_KIDS1000_COSEBIS_LOW_MODE_KERNEL_ENVELOPE_DERIVATION_V1_VALIDATED "
        f"verdict={summary['derivation_verdict']}"
    )


if __name__ == "__main__":
    main()
