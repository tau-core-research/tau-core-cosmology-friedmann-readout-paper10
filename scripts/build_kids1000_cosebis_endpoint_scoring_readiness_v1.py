#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_endpoint_scoring_readiness_policy_v1.csv"
TOMO = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_mode_inventory_v1_summary.csv"
COV = ROOT / "data" / "derived" / "kids1000_cosebis_covariance_readiness_v1_summary.csv"
INV = ROOT / "data" / "derived" / "kids1000_cosebis_covariance_inversion_readiness_v1_summary.csv"
THEORY = ROOT / "data" / "derived" / "kids1000_cosebis_theory_vector_readiness_v1_summary.csv"
MAPPING = ROOT / "data" / "derived" / "kids1000_cosebis_web_path_mapping_readiness_v1_summary.csv"
PREFLIGHT = ROOT / "data" / "derived" / "kids1000_cosebis_path_mapping_source_preflight_v1_summary.csv"
BLOCKERS = ROOT / "data" / "derived" / "kids1000_cosebis_path_blocker_resolution_order_v1_summary.csv"
NULL_SEEDS = ROOT / "data" / "derived" / "kids1000_cosebis_null_control_seed_inventory_v1_summary.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_scoring_readiness_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_scoring_readiness_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def main() -> None:
    policy = read_one(POLICY)
    tomo = read_one(TOMO)
    cov = read_one(COV)
    inv = read_one(INV)
    theory = read_one(THEORY)
    mapping = read_one(MAPPING)
    preflight = read_one(PREFLIGHT)
    blockers = read_one(BLOCKERS)
    null_seeds = read_one(NULL_SEEDS)

    if policy["current_endpoint_scoring_allowed"] != "false":
        raise SystemExit("endpoint scoring readiness policy must remain scoring-disabled")
    if policy["current_scoring_executed"] != "false":
        raise SystemExit("endpoint scoring readiness policy must not execute scoring")

    rows = [
        {
            "component_id": "data_vector_structure",
            "component_status": "ready_source_side",
            "evidence_artifact": "data/derived/kids1000_cosebis_tomographic_mode_inventory_v1_summary.csv",
            "ready_for_scoring": "true",
            "blocking_status": "not_blocking",
            "readiness_note": f"{tomo['data_vector_rows']}_rows_{tomo['n_tomographic_pairs']}_pairs_{tomo['n_modes_per_pair']}_modes",
        },
        {
            "component_id": "covariance_matrix",
            "component_status": "ready_source_side",
            "evidence_artifact": "data/derived/kids1000_cosebis_covariance_readiness_v1_summary.csv",
            "ready_for_scoring": cov["positive_definite"],
            "blocking_status": "not_blocking" if cov["cholesky_ready"] == "true" else "blocking",
            "readiness_note": f"shape_{cov['covariance_shape']}_cholesky_{cov['cholesky_ready']}",
        },
        {
            "component_id": "covariance_solve_policy",
            "component_status": "ready_policy_only",
            "evidence_artifact": "data/derived/kids1000_cosebis_covariance_inversion_readiness_v1_summary.csv",
            "ready_for_scoring": "true" if inv["cholesky_ready"] == "true" else "false",
            "blocking_status": "not_blocking" if inv["cholesky_ready"] == "true" else "blocking",
            "readiness_note": inv["inversion_policy"],
        },
        {
            "component_id": "theory_vector",
            "component_status": theory["theory_vector_status"],
            "evidence_artifact": "data/derived/kids1000_cosebis_theory_vector_readiness_v1_summary.csv",
            "ready_for_scoring": "false",
            "blocking_status": "blocking",
            "readiness_note": "300_row_theory_vector_required_not_computed",
        },
        {
            "component_id": "web_path_mapping",
            "component_status": mapping["mapping_status"],
            "evidence_artifact": "data/derived/kids1000_cosebis_web_path_mapping_readiness_v1_summary.csv",
            "ready_for_scoring": "false",
            "blocking_status": "blocking",
            "readiness_note": "mapping_vector_required_not_computed",
        },
        {
            "component_id": "source_preflight",
            "component_status": preflight["status"],
            "evidence_artifact": "data/derived/kids1000_cosebis_path_mapping_source_preflight_v1_summary.csv",
            "ready_for_scoring": "false",
            "blocking_status": "blocking",
            "readiness_note": (
                f"available_{preflight['available_component_count']}_missing_{preflight['missing_component_count']}"
            ),
        },
        {
            "component_id": "blocker_resolution_order",
            "component_status": blockers["status"],
            "evidence_artifact": "data/derived/kids1000_cosebis_path_blocker_resolution_order_v1_summary.csv",
            "ready_for_scoring": "false",
            "blocking_status": "blocking",
            "readiness_note": f"first_blocker_{blockers['first_blocker']}",
        },
        {
            "component_id": "null_controls",
            "component_status": null_seeds["status"],
            "evidence_artifact": "data/derived/kids1000_cosebis_null_control_seed_inventory_v1_summary.csv",
            "ready_for_scoring": "false",
            "blocking_status": "blocking_until_mapping_exists",
            "readiness_note": f"declared_draws_{null_seeds['total_declared_control_draws']}_not_executed",
        },
    ]

    for row in rows:
        row.update(
            {
                "policy_id": policy["policy_id"],
                "selected_statistic": policy["selected_statistic"],
                "endpoint_scoring_allowed": "false",
                "scoring_executed": "false",
                "contains_predictions": "false",
                "contains_residuals": "false",
                "contains_fit_statistics": "false",
                "uses_kids_data_vector_values_for_source_selection": "false",
                "uses_posterior_chains": "false",
                "uses_posthoc_selection": "false",
                "claim_boundary": policy["claim_boundary"],
            }
        )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    blocking_rows = [row for row in rows if row["blocking_status"] != "not_blocking"]
    ready_rows = [row for row in rows if row["ready_for_scoring"] == "true"]
    summary = {
        "policy_id": policy["policy_id"],
        "status": "KIDS1000_COSEBIS_ENDPOINT_SCORING_READINESS_BUILT_NOT_SCORED",
        "component_count": str(len(rows)),
        "ready_component_count": str(len(ready_rows)),
        "blocking_component_count": str(len(blocking_rows)),
        "first_blocker": blockers["first_blocker"],
        "next_action": "resolve_F_overlap_then_D_path_E_web_before_theory_vector_mapping_and_scoring",
        "endpoint_scoring_allowed": "false",
        "scoring_executed": "false",
        "contains_predictions": "false",
        "contains_residuals": "false",
        "contains_fit_statistics": "false",
        "uses_kids_data_vector_values_for_source_selection": "false",
        "uses_posterior_chains": "false",
        "uses_posthoc_selection": "false",
        "claim_boundary": policy["claim_boundary"],
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_ENDPOINT_SCORING_READINESS_V1_BUILT "
        f"ready={len(ready_rows)} blockers={len(blocking_rows)} endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()
