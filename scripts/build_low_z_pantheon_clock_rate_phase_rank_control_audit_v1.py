#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from collections import Counter
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "data/source_manifest/low_z_pantheon_clock_rate_phase_rank_control_audit_v1.csv"
CANDIDATE = ROOT / "data/derived/low_z_pantheon_time_readout_clock_rate_phase_candidate_v1.csv"
SCREEN_SUMMARY = ROOT / "data/derived/low_z_pantheon_clock_rate_phase_fast_screen_v1_summary.csv"
SCREEN_FAMILY = ROOT / "data/derived/low_z_pantheon_clock_rate_phase_fast_screen_v1_family_summary.csv"
DETAIL = ROOT / "data/derived/low_z_pantheon_clock_rate_phase_rank_control_audit_v1.csv"
SUMMARY = ROOT / "data/derived/low_z_pantheon_clock_rate_phase_rank_control_audit_v1_summary.csv"
CLAIM_BOUNDARY = "clock_rate_phase_rank_control_audit_source_side_not_scoring_not_validation"


FAMILIES = {
    "clock_level": "W_time_clock_level_basis",
    "clock_slope": "W_time_clock_slope_basis",
    "clock_phase": "W_time_clock_phase_basis",
}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"expected one row in {path.relative_to(ROOT)}, got {len(rows)}")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def fmt(value: float) -> str:
    if not math.isfinite(value):
        return ""
    return f"{value:.12g}"


def average_ranks(values: np.ndarray) -> np.ndarray:
    order = np.argsort(values, kind="mergesort")
    ranks = np.empty(len(values), dtype=float)
    sorted_values = values[order]
    start = 0
    while start < len(values):
        end = start + 1
        while end < len(values) and sorted_values[end] == sorted_values[start]:
            end += 1
        average_rank = 0.5 * (start + end - 1)
        ranks[order[start:end]] = average_rank
        start = end
    return ranks


def pearson(a: np.ndarray, b: np.ndarray) -> float:
    if len(a) != len(b) or len(a) < 2:
        return math.nan
    aa = a - np.mean(a)
    bb = b - np.mean(b)
    denom = float(np.linalg.norm(aa) * np.linalg.norm(bb))
    if denom == 0.0:
        return math.nan
    return float(np.dot(aa, bb) / denom)


def spearman(a: np.ndarray, b: np.ndarray) -> float:
    return pearson(average_ranks(a), average_ranks(b))


def rank_reverse(values: np.ndarray) -> np.ndarray:
    order = np.argsort(values)
    out = np.array(values, copy=True)
    out[order] = values[order[::-1]]
    return out


def main() -> None:
    run = read_one(RUN)
    if run["status"] != "SOURCE_SIDE_DIAGNOSTIC_AUDIT_NOT_REPLAY_NOT_VALIDATION":
        raise SystemExit("bad audit run status")
    for field in ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"]:
        if run[field] != "false":
            raise SystemExit(f"{field} must be false")
    if run["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("bad audit claim boundary")

    candidate_rows = read_rows(CANDIDATE)
    screen_summary = read_one(SCREEN_SUMMARY)
    family_summary = {row["family_id"]: row for row in read_rows(SCREEN_FAMILY)}
    if len(candidate_rows) != 424:
        raise SystemExit(f"expected 424 candidate rows, got {len(candidate_rows)}")
    if screen_summary["verdict"] != "clock_rate_phase_fast_screen_not_control_resistant":
        raise SystemExit("rank-control audit expects the failed fast-screen verdict")

    z = np.array([float(row["zHD"]) for row in candidate_rows], dtype=float)
    source_index = np.array([float(row["source_row_index"]) for row in candidate_rows], dtype=float)
    cc_bins = [row["assigned_cc_bin_index"] for row in candidate_rows]
    bin_counts = Counter(cc_bins)
    bin_count_string = ";".join(f"{key}:{bin_counts[key]}" for key in sorted(bin_counts, key=lambda x: int(x)))
    cc_refs = sorted({row["assigned_cc_reference"] for row in candidate_rows})
    detail_rows: list[dict[str, str]] = []

    rank_control_dominance_flags: list[bool] = []
    for family_id, column in FAMILIES.items():
        values = np.array([float(row[column]) for row in candidate_rows], dtype=float)
        reversed_values = rank_reverse(values)
        unique_values = sorted({float(value) for value in values})
        p_z = pearson(values, z)
        s_z = spearman(values, z)
        p_idx = pearson(values, source_index)
        s_idx = spearman(values, source_index)
        p_rev = pearson(values, reversed_values)
        s_rev = spearman(values, reversed_values)
        family = family_summary[family_id]
        absolute_order_corr = max(abs(v) for v in [p_z, s_z, p_idx, s_idx] if math.isfinite(v))
        rank_control_dominates = (
            family["best_control_branch"] == "rank_reverse"
            and int(family["controls_better_than_candidate_chi2"]) > 0
        )
        rank_control_dominance_flags.append(rank_control_dominates)
        detail_rows.append(
            {
                "run_id": run["run_id"],
                "family_id": family_id,
                "basis_column": column,
                "n_rows": str(len(candidate_rows)),
                "assigned_cc_bin_count": str(len(bin_counts)),
                "assigned_cc_bin_counts": bin_count_string,
                "unique_basis_value_count": str(len(unique_values)),
                "basis_min": fmt(float(np.min(values))),
                "basis_max": fmt(float(np.max(values))),
                "basis_mean": fmt(float(np.mean(values))),
                "basis_std": fmt(float(np.std(values))),
                "pearson_with_zHD": fmt(p_z),
                "spearman_with_zHD": fmt(s_z),
                "pearson_with_source_row_index": fmt(p_idx),
                "spearman_with_source_row_index": fmt(s_idx),
                "pearson_with_rank_reverse_control": fmt(p_rev),
                "spearman_with_rank_reverse_control": fmt(s_rev),
                "absolute_order_correlation_max": fmt(absolute_order_corr),
                "best_local_control_branch": family["best_control_branch"],
                "controls_better_than_candidate_chi2": family["controls_better_than_candidate_chi2"],
                "family_survives_local_controls": family["family_survives_local_controls"],
                "rank_control_dominance_flag": "true" if rank_control_dominates else "false",
                "diagnostic_interpretation": (
                    "coarse_low_z_cc_bin_basis_rank_reverse_local_control_dominates"
                    if rank_control_dominates
                    else "coarse_low_z_cc_bin_basis_rank_reverse_not_local_best"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(DETAIL, detail_rows)

    best_candidate = screen_summary["best_candidate_family"]
    best_control = f"{screen_summary['best_global_control_branch']}/{screen_summary['best_global_control_family']}"
    all_rank_control_dominated = all(rank_control_dominance_flags)
    verdict = (
        "low_cc_bin_count_rank_control_dominance_confirmed_not_validation"
        if all_rank_control_dominated
        else "low_cc_bin_count_rank_control_dominance_incomplete_not_validation"
    )
    summary_rows = [
        {
            "run_id": run["run_id"],
            "status": "SOURCE_SIDE_DIAGNOSTIC_AUDIT_COMPLETE_NOT_REPLAY_NOT_VALIDATION",
            "n_rows": str(len(candidate_rows)),
            "assigned_cc_bin_count": str(len(bin_counts)),
            "assigned_cc_bin_counts": bin_count_string,
            "assigned_cc_references": ";".join(cc_refs),
            "best_candidate_family_from_fast_screen": best_candidate,
            "best_global_control_from_fast_screen": best_control,
            "controls_better_than_candidate_chi2": screen_summary["controls_better_than_candidate_chi2"],
            "candidate_delta_chi2_minus_baseline": screen_summary["delta_chi2_candidate_minus_baseline"],
            "candidate_delta_chi2_minus_best_global_control": screen_summary[
                "delta_chi2_candidate_minus_best_global_control"
            ],
            "max_unique_basis_value_count": str(max(int(row["unique_basis_value_count"]) for row in detail_rows)),
            "min_absolute_order_correlation_max": fmt(
                min(float(row["absolute_order_correlation_max"]) for row in detail_rows)
            ),
            "all_families_rank_control_dominated": "true" if all_rank_control_dominated else "false",
            "diagnostic_interpretation": (
                "the_clock_rate_phase_basis_is_too_coarse_for_replay_and_rank_reverse_dominates_local_controls"
                if all_rank_control_dominated
                else "the_clock_rate_phase_basis_is_coarse_but_rank_reverse_does_not_dominate_all_local_controls"
            ),
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
            "verdict": verdict,
        }
    ]
    write_csv(SUMMARY, summary_rows)
    print(
        "PAPER10_CLOCK_RATE_PHASE_RANK_CONTROL_AUDIT_BUILT "
        f"cc_bins={summary_rows[0]['assigned_cc_bin_count']} "
        f"verdict={verdict}"
    )


if __name__ == "__main__":
    main()
