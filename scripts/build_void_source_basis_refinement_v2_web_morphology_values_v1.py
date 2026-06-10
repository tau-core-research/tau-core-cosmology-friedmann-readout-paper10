#!/usr/bin/env python3
from __future__ import annotations

import csv
import random
import statistics
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOW_Z_MASK = ROOT / "data" / "derived" / "low_z_pantheon_void_scope_candidate_v1_row_mask.csv"
OUT = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_web_morphology_values.csv"
SUMMARY = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_web_morphology_values_summary.csv"

SEED = 20260610
COMPONENT_ID = "V2_WEB_MORPHOLOGY"
CLAIM_BOUNDARY = "v2_web_morphology_source_values_frozen_not_scoring_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


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
    if not rows:
        raise SystemExit("no included low-z rows found")
    values = [float(row["W_web_source_native_basis"]) for row in rows]
    mean = statistics.fmean(values)
    stdev = statistics.pstdev(values)
    ranks = quantile_ranks(values)
    rng = random.Random(SEED)
    shuffled_values = values[:]
    rng.shuffle(shuffled_values)
    q25_cut = sorted(values)[int(0.25 * (len(values) - 1))]
    q75_cut = sorted(values)[int(0.75 * (len(values) - 1))]

    out_rows: list[dict[str, str]] = []
    for row, raw, rank, shuffled in zip(rows, values, ranks, shuffled_values, strict=True):
        centered = raw - mean
        out_rows.append(
            {
                "component_id": COMPONENT_ID,
                "channel_id": "W_WEB_ANISOTROPY",
                "source_scope": "LOW_Z_PANTHEON_VOID_SCOPE_CANDIDATE_POLICY_V1_INCLUDED_ROWS",
                "CID": row["CID"],
                "source_row_index": row["source_row_index"],
                "zHD": row["zHD"],
                "W_web_source_native_basis": fmt(raw),
                "W_web_centered": fmt(centered),
                "W_web_abs_centered": fmt(abs(centered)),
                "W_web_rank_quantile": fmt(rank),
                "web_off_control": "0",
                "web_wrong_sign_control": fmt(-raw),
                "web_deterministic_row_shuffle_control": fmt(shuffled),
                "web_low_quartile_control": "1" if raw <= q25_cut else "0",
                "web_high_quartile_control": "1" if raw >= q75_cut else "0",
                "deterministic_shuffle_seed": str(SEED),
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "contains_endpoint_scores": "false",
                "contains_distance_residuals": "false",
                "contains_fit_statistics": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    nonzero_count = sum(1 for value in values if value != 0.0)
    summary = [
        {
            "component_id": COMPONENT_ID,
            "status": "V2_WEB_MORPHOLOGY_VALUES_FROZEN_NOT_ENDPOINT_READY",
            "source_artifact": str(LOW_Z_MASK.relative_to(ROOT)),
            "output_artifact": str(OUT.relative_to(ROOT)),
            "n_rows": str(len(out_rows)),
            "web_nonzero_count": str(nonzero_count),
            "web_min": fmt(min(values)),
            "web_max": fmt(max(values)),
            "web_mean": fmt(mean),
            "web_std": fmt(stdev),
            "deterministic_shuffle_seed": str(SEED),
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "contains_endpoint_scores": "false",
            "contains_distance_residuals": "false",
            "contains_fit_statistics": "false",
            "verdict": "web_morphology_values_frozen_not_endpoint_ready",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(OUT, out_rows)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_V2_WEB_MORPHOLOGY_VALUES_BUILT "
        f"rows={len(out_rows)} web_nonzero_count={nonzero_count} endpoint_replay_allowed=false"
    )


if __name__ == "__main__":
    main()
