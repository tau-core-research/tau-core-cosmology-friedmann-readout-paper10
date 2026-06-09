#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_endpoint_scoring_diagnostics_policy_v1.csv"
RESULTS = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_scoring_v1_results.csv"
FAMILY = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_scoring_diagnostics_v1_family_summary.csv"
TOP = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_scoring_diagnostics_v1_top_nulls.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_scoring_diagnostics_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    policy = read_one(POLICY)
    result = read_one(RESULTS)
    family = read_rows(FAMILY)
    top = read_rows(TOP)
    summary = read_one(SUMMARY)

    if policy["status"] != "ENDPOINT_SCORING_DIAGNOSTICS_POLICY_FROZEN":
        raise SystemExit("unexpected diagnostics policy status")
    if policy["endpoint_validation_claimed"] != "false":
        raise SystemExit("diagnostics policy must not claim validation")
    if policy["parent_endpoint_scoring_run"] != result["run_id"]:
        raise SystemExit("diagnostics parent run mismatch")
    if summary["status"] != "KIDS1000_COSEBIS_ENDPOINT_SCORING_DIAGNOSTICS_BUILT":
        raise SystemExit("unexpected diagnostics summary status")
    if summary["run_id"] != result["run_id"]:
        raise SystemExit("diagnostics summary run mismatch")
    if summary["endpoint_validation_claimed"] != "false":
        raise SystemExit("diagnostics summary must not claim validation")
    if summary["uses_kids_data_vector_values_for_scoring"] != "true":
        raise SystemExit("diagnostics must record that endpoint scores use KiDS data values")
    if summary["uses_kids_data_vector_values_for_source_selection"] != "false":
        raise SystemExit("diagnostics must not use KiDS data values for source selection")
    if summary["uses_posthoc_source_selection"] != "false":
        raise SystemExit("diagnostics must not enable posthoc source selection")
    if summary["candidate_rank_by_chi2"] != result["candidate_rank_by_chi2"]:
        raise SystemExit("candidate chi2 rank mismatch")
    if summary["candidate_rank_by_aic"] != result["candidate_rank_by_aic"]:
        raise SystemExit("candidate AIC rank mismatch")
    if summary["better_than_candidate_chi2_count"] != result["chi2_nulls_better_than_candidate"]:
        raise SystemExit("better-than-candidate chi2 count mismatch")
    if summary["better_than_candidate_aic_count"] != result["aic_nulls_better_than_candidate"]:
        raise SystemExit("better-than-candidate AIC count mismatch")
    if summary["families_with_better_than_candidate"] != "tomographic_pair_shuffle":
        raise SystemExit("only tomographic_pair_shuffle should contain better controls")
    if summary["diagnostic_verdict"] != "candidate_low_tail_but_not_absolute_winner_tomographic_shuffle_controls_dominate":
        raise SystemExit("unexpected diagnostic verdict")
    if len(family) != 4:
        raise SystemExit("family summary should contain four control families")
    by_family = {row["control_family"]: row for row in family}
    if set(by_family) != {
        "sky_rotation",
        "tomographic_pair_shuffle",
        "web_path_sign_flip",
        "wrong_channel_activation",
    }:
        raise SystemExit("unexpected control-family set")
    if by_family["tomographic_pair_shuffle"]["controls_better_than_candidate_chi2"] != "2":
        raise SystemExit("tomographic shuffle better count should be 2")
    for family_id in ["sky_rotation", "web_path_sign_flip", "wrong_channel_activation"]:
        if by_family[family_id]["controls_better_than_candidate_chi2"] != "0":
            raise SystemExit(f"{family_id} should not beat candidate by chi2")
        if by_family[family_id]["controls_better_than_candidate_aic"] != "0":
            raise SystemExit(f"{family_id} should not beat candidate by AIC")
    if len(top) != 25:
        raise SystemExit("top-null diagnostic should retain top 25 nulls")
    if top[0]["control_family"] != "tomographic_pair_shuffle":
        raise SystemExit("top null should be a tomographic-pair shuffle")
    if top[0]["beats_candidate_chi2"] != "true":
        raise SystemExit("top null should beat candidate")
    for row in [*family, *top, summary]:
        if row["endpoint_validation_claimed"] != "false":
            raise SystemExit("diagnostic rows must not claim validation")
        if row["claim_boundary"] != policy["claim_boundary"]:
            raise SystemExit("diagnostic claim boundary mismatch")
    print(
        "PAPER10_KIDS1000_COSEBIS_ENDPOINT_SCORING_DIAGNOSTICS_V1_VALIDATED "
        f"verdict={summary['diagnostic_verdict']}"
    )


if __name__ == "__main__":
    main()
