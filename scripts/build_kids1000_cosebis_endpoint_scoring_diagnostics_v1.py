#!/usr/bin/env python3
from __future__ import annotations

import csv
import statistics
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_endpoint_scoring_diagnostics_policy_v1.csv"
RESULTS = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_scoring_v1_results.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_scoring_v1_summary.csv"
NULLS = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_scoring_v1_null_controls.csv"
OUT_FAMILY = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_scoring_diagnostics_v1_family_summary.csv"
OUT_TOP = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_scoring_diagnostics_v1_top_nulls.csv"
OUT_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_scoring_diagnostics_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def fmt(value: float) -> str:
    return f"{value:.12e}"


def main() -> None:
    policy = read_one(POLICY)
    result = read_one(RESULTS)
    score_summary = read_one(SUMMARY)
    nulls = read_rows(NULLS)

    if policy["parent_endpoint_scoring_run"] != result["run_id"]:
        raise SystemExit("diagnostics policy parent run mismatch")
    if policy["endpoint_validation_claimed"] != "false":
        raise SystemExit("diagnostics policy must not claim validation")
    if score_summary["endpoint_scoring_executed"] != "true":
        raise SystemExit("endpoint scoring must be executed before diagnostics")
    if score_summary["endpoint_validation_claimed"] != "false":
        raise SystemExit("endpoint scoring summary must not claim validation")
    if len(nulls) != int(result["null_control_count"]):
        raise SystemExit("null-control count mismatch")

    candidate_delta = float(result["candidate_delta_chi2_vs_baseline"])
    candidate_aic_delta = float(result["candidate_delta_aic_vs_baseline"])

    by_family: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in nulls:
        by_family[row["control_family"]].append(row)

    family_rows: list[dict[str, str]] = []
    for family in sorted(by_family):
        rows = by_family[family]
        delta = [float(row["delta_chi2_vs_baseline"]) for row in rows]
        delta_aic = [float(row["delta_aic_vs_baseline"]) for row in rows]
        beats_chi2 = sum(value < candidate_delta for value in delta)
        beats_aic = sum(value < candidate_aic_delta for value in delta_aic)
        family_rows.append(
            {
                "policy_id": policy["policy_id"],
                "run_id": result["run_id"],
                "control_family": family,
                "control_count": str(len(rows)),
                "min_delta_chi2_vs_baseline": fmt(min(delta)),
                "median_delta_chi2_vs_baseline": fmt(float(statistics.median(delta))),
                "mean_delta_chi2_vs_baseline": fmt(float(statistics.mean(delta))),
                "max_delta_chi2_vs_baseline": fmt(max(delta)),
                "min_delta_aic_vs_baseline": fmt(min(delta_aic)),
                "median_delta_aic_vs_baseline": fmt(float(statistics.median(delta_aic))),
                "mean_delta_aic_vs_baseline": fmt(float(statistics.mean(delta_aic))),
                "candidate_delta_chi2_vs_baseline": fmt(candidate_delta),
                "candidate_delta_aic_vs_baseline": fmt(candidate_aic_delta),
                "controls_better_than_candidate_chi2": str(beats_chi2),
                "controls_better_than_candidate_aic": str(beats_aic),
                "family_has_better_than_candidate": str(beats_chi2 > 0 or beats_aic > 0).lower(),
                "uses_kids_data_vector_values_for_scoring": "true",
                "uses_kids_data_vector_values_for_source_selection": "false",
                "endpoint_validation_claimed": "false",
                "claim_boundary": policy["claim_boundary"],
            }
        )

    top_sorted = sorted(nulls, key=lambda row: float(row["chi2"]))
    top_rows: list[dict[str, str]] = []
    for rank, row in enumerate(top_sorted[:25], start=1):
        top_rows.append(
            {
                "policy_id": policy["policy_id"],
                "run_id": result["run_id"],
                "null_rank_by_chi2": str(rank),
                "control_index_one_based": row["control_index_one_based"],
                "control_family": row["control_family"],
                "operator": row["operator"],
                "seed": row["seed"],
                "amplitude": row["amplitude"],
                "chi2": row["chi2"],
                "delta_chi2_vs_baseline": row["delta_chi2_vs_baseline"],
                "aic": row["aic"],
                "delta_aic_vs_baseline": row["delta_aic_vs_baseline"],
                "beats_candidate_chi2": row["beats_candidate_chi2"],
                "beats_candidate_aic": row["beats_candidate_aic"],
                "candidate_rank_by_chi2": result["candidate_rank_by_chi2"],
                "candidate_rank_by_aic": result["candidate_rank_by_aic"],
                "endpoint_validation_claimed": "false",
                "claim_boundary": policy["claim_boundary"],
            }
        )

    families_with_better = sorted(
        row["control_family"] for row in family_rows if row["family_has_better_than_candidate"] == "true"
    )
    diagnostic_verdict = (
        "candidate_low_tail_but_not_absolute_winner_tomographic_shuffle_controls_dominate"
        if families_with_better == ["tomographic_pair_shuffle"]
        else "candidate_low_tail_with_multiple_better_control_families"
        if families_with_better
        else "candidate_absolute_winner_against_predeclared_controls"
    )
    summary_rows = [
        {
            "policy_id": policy["policy_id"],
            "run_id": result["run_id"],
            "status": "KIDS1000_COSEBIS_ENDPOINT_SCORING_DIAGNOSTICS_BUILT",
            "selected_statistic": policy["selected_statistic"],
            "candidate_delta_chi2_vs_baseline": result["candidate_delta_chi2_vs_baseline"],
            "candidate_delta_aic_vs_baseline": result["candidate_delta_aic_vs_baseline"],
            "candidate_rank_by_chi2": result["candidate_rank_by_chi2"],
            "candidate_rank_by_aic": result["candidate_rank_by_aic"],
            "null_control_count": result["null_control_count"],
            "better_than_candidate_chi2_count": result["chi2_nulls_better_than_candidate"],
            "better_than_candidate_aic_count": result["aic_nulls_better_than_candidate"],
            "families_with_better_than_candidate": ";".join(families_with_better) if families_with_better else "none",
            "top_null_family": top_rows[0]["control_family"],
            "top_null_operator": top_rows[0]["operator"],
            "diagnostic_verdict": diagnostic_verdict,
            "endpoint_validation_claimed": "false",
            "uses_kids_data_vector_values_for_scoring": "true",
            "uses_kids_data_vector_values_for_source_selection": "false",
            "uses_posterior_chains": "false",
            "uses_posthoc_source_selection": "false",
            "claim_boundary": policy["claim_boundary"],
        }
    ]

    write_csv(OUT_FAMILY, family_rows)
    write_csv(OUT_TOP, top_rows)
    write_csv(OUT_SUMMARY, summary_rows)
    print(
        "PAPER10_KIDS1000_COSEBIS_ENDPOINT_SCORING_DIAGNOSTICS_V1_BUILT "
        f"verdict={diagnostic_verdict} families_with_better={summary_rows[0]['families_with_better_than_candidate']}"
    )


if __name__ == "__main__":
    main()
