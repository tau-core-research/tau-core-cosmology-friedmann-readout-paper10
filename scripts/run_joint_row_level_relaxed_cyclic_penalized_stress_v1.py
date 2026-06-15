#!/usr/bin/env python3
from __future__ import annotations

import csv
import statistics
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data" / "derived"
DOCS = ROOT / "docs"

PENALTY_VALUES = DERIVED / "joint_row_level_numeric_penalty_values_v1.csv"
BASE_T = DERIVED / "joint_numeric_t_joint_ledger_v1_summary.csv"
LAMBDA = DERIVED / "joint_row_level_numeric_lambda_blocker_status_v1_summary.csv"
OUT = DERIVED / "joint_row_level_relaxed_cyclic_penalized_stress_v1.csv"
SUMMARY = DERIVED / "joint_row_level_relaxed_cyclic_penalized_stress_v1_summary.csv"
DOC = DOCS / "joint_row_level_relaxed_cyclic_penalized_stress_v1.md"
CLAIM_BOUNDARY = "joint_row_level_relaxed_cyclic_penalized_stress_not_validation"

CHANNEL_ORDER = [
    "desi_shape_time_readout",
    "kids_lensing_cosebis_low_mode",
    "observer_path_basis_low_z",
]


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def f(value: str) -> float:
    return float(value)


def sorted_controls(rows: list[dict[str, str]], channel: str) -> list[dict[str, str]]:
    controls = [row for row in rows if row["channel_id"] == channel and row["row_type"] == "matched_control"]
    return sorted(controls, key=lambda r: (r["control_family"], r["control_id"]))


def main() -> None:
    rows = read_rows(PENALTY_VALUES)
    base_t = f(read_one(BASE_T)["numeric_t_joint"])
    lambda_row = f(read_one(LAMBDA)["lambda_row_numeric_value"])
    candidate_rows = [
        row for row in rows if row["row_type"] == "candidate" and row["joint_penalty_contribution_allowed"] == "true"
    ]
    if sorted(row["channel_id"] for row in candidate_rows) != sorted(CHANNEL_ORDER):
        raise SystemExit("candidate rows do not cover the active channels")
    p_candidate = sum(f(row["P_i"]) for row in candidate_rows)
    candidate_penalized = base_t + lambda_row * p_candidate

    controls = {channel: sorted_controls(rows, channel) for channel in CHANNEL_ORDER}
    if any(not controls[channel] for channel in CHANNEL_ORDER):
        raise SystemExit("missing channel controls")

    # Stress-test rule: use the observer/path count as the relaxed control
    # horizon, reuse the smaller DESI list cyclically, and take the first
    # source-sorted KiDS controls. This is deterministic and residual-blind,
    # but it is explicitly not a strict validation control universe.
    horizon = len(controls["observer_path_basis_low_z"])
    stress_rows = []
    for idx in range(horizon):
        selected = {
            "desi_shape_time_readout": controls["desi_shape_time_readout"][idx % len(controls["desi_shape_time_readout"])],
            "kids_lensing_cosebis_low_mode": controls["kids_lensing_cosebis_low_mode"][idx],
            "observer_path_basis_low_z": controls["observer_path_basis_low_z"][idx],
        }
        p_control = sum(f(row["P_i"]) for row in selected.values())
        # There is no authorized per-control T_joint for this relaxed rule.
        # The stress test isolates the row-level penalty contribution by using
        # the same frozen base T_joint for candidate and relaxed controls.
        control_penalized = base_t + lambda_row * p_control
        margin = candidate_penalized - control_penalized
        stress_rows.append(
            {
                "run_id": "JOINT_ROW_LEVEL_RELAXED_CYCLIC_PENALIZED_STRESS_V1",
                "relaxed_index": str(idx + 1),
                "alignment_rule": "observer_horizon_25_with_desi_cyclic_reuse_and_first_25_kids_controls",
                "candidate_T_joint_base": f"{base_t:.12e}",
                "candidate_P_row": f"{p_candidate:.12e}",
                "candidate_T_joint_penalized": f"{candidate_penalized:.12e}",
                "control_T_joint_base": f"{base_t:.12e}",
                "control_P_row": f"{p_control:.12e}",
                "control_T_joint_penalized": f"{control_penalized:.12e}",
                "candidate_minus_control_penalized": f"{margin:.12e}",
                "control_penalty_exceeds_or_equals_candidate_penalty": str(p_control >= p_candidate).lower(),
                "control_ids_by_channel": "|".join(f"{ch}:{selected[ch]['control_id']}" for ch in CHANNEL_ORDER),
                "control_families_by_channel": "|".join(f"{ch}:{selected[ch]['control_family']}" for ch in CHANNEL_ORDER),
                "desi_reuse_index": str((idx % len(controls["desi_shape_time_readout"])) + 1),
                "endpoint_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    stress_rows = sorted(stress_rows, key=lambda r: f(r["control_P_row"]), reverse=True)
    for rank, row in enumerate(stress_rows, start=1):
        row["control_rank_by_penalty_desc"] = str(rank)
    write_csv(OUT, stress_rows)

    margins = [f(row["candidate_minus_control_penalized"]) for row in stress_rows]
    controls_beating = sum(1 for row in stress_rows if row["control_penalty_exceeds_or_equals_candidate_penalty"] == "true")
    summary = {
        "run_id": "JOINT_ROW_LEVEL_RELAXED_CYCLIC_PENALIZED_STRESS_V1",
        "status": "RELAXED_CYCLIC_STRESS_COMPLETE_NOT_VALIDATION",
        "alignment_rule": "observer_horizon_25_with_desi_cyclic_reuse_and_first_25_kids_controls",
        "candidate_T_joint_base": f"{base_t:.12e}",
        "lambda_row": f"{lambda_row:.12e}",
        "candidate_P_row": f"{p_candidate:.12e}",
        "candidate_T_joint_penalized": f"{candidate_penalized:.12e}",
        "relaxed_control_count": str(len(stress_rows)),
        "controls_with_penalty_exceeding_or_equal_candidate": str(controls_beating),
        "fraction_exceeding_or_equal_candidate": f"{controls_beating / len(stress_rows):.12e}",
        "min_candidate_minus_control_penalized": f"{min(margins):.12e}",
        "median_candidate_minus_control_penalized": f"{statistics.median(margins):.12e}",
        "mean_candidate_minus_control_penalized": f"{statistics.mean(margins):.12e}",
        "desi_controls_reused_cyclically": "true",
        "per_control_T_joint_authorized": "false",
        "stress_test_only": "true",
        "endpoint_validation_claimed": "false",
        "verdict": "RELAXED_CYCLIC_STRESS_POSITIVE_NOT_VALIDATION"
        if controls_beating == 0
        else "RELAXED_CYCLIC_STRESS_CAVEATED_CONTROLS_EXCEED_CANDIDATE_NOT_VALIDATION",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(SUMMARY, [summary])

    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Joint row-level relaxed cyclic penalized stress v1",
                "",
                "**Doc class:** relaxed-control stress test.",
                "**Status:** complete; not validation.",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`.",
                "",
                "This is a fast stress test, not a strict endpoint validation.",
                "It keeps the same frozen source-side penalty values but relaxes",
                "the all-channel alignment rule by cyclically reusing the six DESI",
                "shape/time controls across the 25 observer/path controls.",
                "",
                "Because no per-control relaxed `T_joint` statistic has been",
                "authorized for this construction, the test isolates the row-level",
                "penalty term using the same frozen base `T_joint` for candidate and",
                "relaxed controls.",
                "",
                f"Relaxed controls: `{summary['relaxed_control_count']}`.",
                f"Controls whose penalty exceeds/equal candidate: `{summary['controls_with_penalty_exceeding_or_equal_candidate']}`.",
                f"Minimum penalized margin: `{summary['min_candidate_minus_control_penalized']}`.",
                "",
                "The result can motivate a future reviewed relaxed-alignment route,",
                "but it does not replace the strict six-control endpoint replay.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(
        "JOINT_ROW_LEVEL_RELAXED_CYCLIC_PENALIZED_STRESS_V1_COMPLETE "
        f"controls_exceeding={controls_beating}"
    )


if __name__ == "__main__":
    main()
