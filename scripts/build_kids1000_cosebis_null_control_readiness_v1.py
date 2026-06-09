#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_null_control_policy_v1.csv"
MAPPING = ROOT / "data" / "derived" / "kids1000_cosebis_web_path_mapping_readiness_v1_summary.csv"
REPLAY = ROOT / "data" / "derived" / "kids1000_cosebis_null_control_theory_replay_v1_summary.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_null_control_readiness_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_null_control_readiness_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def main() -> None:
    policy = read_one(POLICY)
    mapping = read_one(MAPPING)
    replay = read_one(REPLAY)
    if policy["endpoint_scoring_allowed"].lower() != "false":
        raise SystemExit("COSEBIs null-control policy must remain endpoint disabled")
    if mapping["current_mapping_computed"].lower() != "true":
        raise SystemExit("source-frozen web/path mapping basis must exist before null controls are declared ready")
    if mapping["contains_theory_vector"].lower() != "false":
        raise SystemExit("null-control readiness must precede theory-vector construction")
    if replay["current_control_theory_replay_executed"].lower() != "true":
        raise SystemExit("null-control theory replay must exist before controls are ready")
    if replay["contains_control_scores"].lower() != "false":
        raise SystemExit("null-control theory replay must not contain scores")

    families = policy["control_families"].split(";")
    replay_draws = replay["control_draw_count"]
    rows: list[dict[str, str]] = []
    for family in families:
        rows.append(
            {
                "policy_id": policy["policy_id"],
                "parent_policy": policy["parent_policy"],
                "selected_statistic": policy["selected_statistic"],
                "control_family": family,
                "control_status": "THEORY_REPLAY_EXECUTED_NOT_SCORED",
                "target_rows": mapping["target_rows"],
                "requires_seed_policy": "true",
                "requires_multiplicity_policy": "true",
                "current_control_executed": "true",
                "contains_theory_vector": "true",
                "contains_control_scores": "false",
                "contains_predictions": "false",
                "contains_residuals": "false",
                "contains_fit_statistics": "false",
                "uses_kids_data_vector_values": "false",
                "uses_posterior_chains": "false",
                "uses_posthoc_control_selection": "false",
                "endpoint_scoring_allowed": "false",
                "replay_artifact": "data/derived/kids1000_cosebis_null_control_theory_replay_v1_summary.csv",
                "claim_boundary": "kids1000_cosebis_null_control_readiness_not_validation",
            }
        )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "policy_id": policy["policy_id"],
        "status": "KIDS1000_COSEBIS_NULL_CONTROL_READINESS_BUILT_THEORY_REPLAY_NOT_SCORED",
        "selected_statistic": policy["selected_statistic"],
        "control_family_count": str(len(rows)),
        "control_families": policy["control_families"],
        "control_draw_count": replay_draws,
        "target_rows": mapping["target_rows"],
        "current_controls_executed": "true",
        "contains_theory_vector": "true",
        "contains_control_scores": "false",
        "contains_predictions": "false",
        "contains_residuals": "false",
        "contains_fit_statistics": "false",
        "uses_kids_data_vector_values": "false",
        "uses_posterior_chains": "false",
        "uses_posthoc_control_selection": "false",
        "endpoint_scoring_allowed": "false",
        "replay_artifact": "data/derived/kids1000_cosebis_null_control_theory_replay_v1_summary.csv",
        "claim_boundary": "kids1000_cosebis_null_control_readiness_not_validation",
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_NULL_CONTROL_READINESS_V1_BUILT "
        f"controls={len(rows)} replay_executed=true endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()
