#!/usr/bin/env python3
from __future__ import annotations

import csv
import random
import statistics
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOW_Z_MASK = ROOT / "data" / "derived" / "low_z_pantheon_void_scope_candidate_v1_row_mask.csv"
CONTROL_AUDIT = ROOT / "data" / "derived" / "void_source_basis_refinement_control_dominance_audit_v1_summary.csv"
OUT = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_void_morphology_values.csv"
SUMMARY = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_void_morphology_values_summary.csv"

SEED = 20260610
COMPONENT_ID = "V2_VOID_MORPHOLOGY"
CLAIM_BOUNDARY = "v2_void_morphology_source_values_frozen_weak_negative_not_scoring_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def quantile_ranks(values: list[float]) -> list[float]:
    if len(values) == 1:
        return [0.0]
    order = sorted(range(len(values)), key=lambda idx: (values[idx], idx))
    ranks = [0.0] * len(values)
    denom = len(values) - 1
    for rank, idx in enumerate(order):
        ranks[idx] = rank / denom
    return ranks


def fmt(value: float) -> str:
    return f"{value:.12g}"


def main() -> None:
    rows = [row for row in read_rows(LOW_Z_MASK) if row["included"] == "true"]
    audit = read_one(CONTROL_AUDIT)
    if not rows:
        raise SystemExit("no included low-z rows found")
    if audit["verdict"] != "candidate_signal_not_source_specific_shuffled_control_dominates_without_redshift_leak":
        raise SystemExit("unexpected control-dominance verdict; refusing to hide weak negative")
    values = [float(row["W_void_source_native_basis"]) for row in rows]
    mean = statistics.fmean(values)
    stdev = statistics.pstdev(values)
    ranks = quantile_ranks(values)
    shuffled_values = values[:]
    random.Random(SEED).shuffle(shuffled_values)
    q25_cut = sorted(values)[int(0.25 * (len(values) - 1))]
    q75_cut = sorted(values)[int(0.75 * (len(values) - 1))]

    out_rows: list[dict[str, str]] = []
    for row, raw, rank, shuffled in zip(rows, values, ranks, shuffled_values, strict=True):
        centered = raw - mean
        out_rows.append(
            {
                "component_id": COMPONENT_ID,
                "channel_id": "W_VOID_MATURITY",
                "source_scope": "LOW_Z_PANTHEON_VOID_SCOPE_CANDIDATE_POLICY_V1_INCLUDED_ROWS",
                "CID": row["CID"],
                "source_row_index": row["source_row_index"],
                "zHD": row["zHD"],
                "W_void_source_native_basis": fmt(raw),
                "W_void_centered": fmt(centered),
                "W_void_abs_centered": fmt(abs(centered)),
                "W_void_rank_quantile": fmt(rank),
                "void_off_control": "0",
                "void_wrong_sign_control": fmt(-raw),
                "void_deterministic_row_shuffle_control": fmt(shuffled),
                "void_low_quartile_control": "1" if raw <= q25_cut else "0",
                "void_high_quartile_control": "1" if raw >= q75_cut else "0",
                "deterministic_shuffle_seed": str(SEED),
                "weak_negative_status_inherited": "true",
                "control_dominance_verdict": audit["verdict"],
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "contains_endpoint_scores": "false",
                "contains_distance_residuals": "false",
                "contains_fit_statistics": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    summary = [
        {
            "component_id": COMPONENT_ID,
            "status": "V2_VOID_MORPHOLOGY_VALUES_FROZEN_WEAK_NEGATIVE_NOT_ENDPOINT_READY",
            "source_artifact": str(LOW_Z_MASK.relative_to(ROOT)),
            "control_audit_artifact": str(CONTROL_AUDIT.relative_to(ROOT)),
            "output_artifact": str(OUT.relative_to(ROOT)),
            "n_rows": str(len(out_rows)),
            "void_nonzero_count": str(sum(1 for value in values if value != 0.0)),
            "void_min": fmt(min(values)),
            "void_max": fmt(max(values)),
            "void_mean": fmt(mean),
            "void_std": fmt(stdev),
            "deterministic_shuffle_seed": str(SEED),
            "weak_negative_status_inherited": "true",
            "control_dominance_verdict": audit["verdict"],
            "candidate_improves_chi2_over_baseline": audit["candidate_improves_chi2_over_baseline"],
            "candidate_loses_aic_to_baseline": audit["candidate_loses_aic_to_baseline"],
            "best_control_beats_candidate_chi2": audit["best_control_beats_candidate_chi2"],
            "best_control_is_row_shuffle": audit["best_control_is_row_shuffle"],
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "contains_endpoint_scores": "false",
            "contains_distance_residuals": "false",
            "contains_fit_statistics": "false",
            "verdict": "void_morphology_values_frozen_but_weak_negative_preserved",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(OUT, out_rows)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_V2_VOID_MORPHOLOGY_VALUES_BUILT "
        f"rows={len(out_rows)} weak_negative_status_inherited=true endpoint_replay_allowed=false"
    )


if __name__ == "__main__":
    main()
