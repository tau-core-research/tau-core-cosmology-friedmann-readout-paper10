#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_theory_vector_template_policy_v1.csv"
THEORY_POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_theory_vector_policy_v1.csv"
TOMO = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_mode_inventory_v1.csv"
TOMO_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_mode_inventory_v1_summary.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_theory_vector_template_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_theory_vector_template_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def main() -> None:
    policy = read_one(POLICY)
    theory_policy = read_one(THEORY_POLICY)
    tomo_summary = read_one(TOMO_SUMMARY)
    with TOMO.open(newline="") as f:
        pair_rows = list(csv.DictReader(f))

    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("theory-vector template policy must remain endpoint disabled")
    if policy["current_theory_values_computed"] != "false":
        raise SystemExit("theory-vector template policy must not compute theory values")
    if theory_policy["current_theory_vector_computed"] != "false":
        raise SystemExit("parent theory-vector policy must remain uncomputed")
    if policy["expected_rows"] != theory_policy["expected_theory_vector_rows"]:
        raise SystemExit("template expected rows must match parent theory-vector policy")
    if policy["expected_rows"] != tomo_summary["data_vector_rows"]:
        raise SystemExit("template expected rows must match COSEBIs row count")

    rows: list[dict[str, str]] = []
    row_index_zero_based = 0
    for pair in pair_rows:
        modes = [int(mode) for mode in pair["modes"].split(";")]
        if len(modes) != int(pair["n_modes"]):
            raise SystemExit(f"mode count mismatch for pair {pair['pair_id']}")
        for mode in modes:
            rows.append(
                {
                    "policy_id": policy["policy_id"],
                    "parent_policy": policy["parent_policy"],
                    "selected_statistic": policy["selected_statistic"],
                    "row_index_zero_based": str(row_index_zero_based),
                    "row_index_one_based": str(row_index_zero_based + 1),
                    "bin1": pair["bin1"],
                    "bin2": pair["bin2"],
                    "pair_id": pair["pair_id"],
                    "mode": str(mode),
                    "theory_value_status": "template_pending_source_frozen_mapping",
                    "theory_value": "",
                    "w_web_contribution": "",
                    "w_path_contribution": "",
                    "baseline_contribution": "",
                    "template_row_only": "true",
                    "contains_theory_value": "false",
                    "contains_prediction": "false",
                    "contains_residual": "false",
                    "contains_fit_statistic": "false",
                    "uses_kids_data_vector_values": "false",
                    "uses_posterior_chains": "false",
                    "endpoint_scoring_allowed": "false",
                    "claim_boundary": policy["claim_boundary"],
                }
            )
            row_index_zero_based += 1

    if len(rows) != int(policy["expected_rows"]):
        raise SystemExit("unexpected theory-vector template row count")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "policy_id": policy["policy_id"],
        "status": "KIDS1000_COSEBIS_THEORY_VECTOR_TEMPLATE_BUILT_NOT_COMPUTED",
        "selected_statistic": policy["selected_statistic"],
        "template_rows": str(len(rows)),
        "tomographic_pair_count": tomo_summary["n_tomographic_pairs"],
        "modes_per_pair": tomo_summary["n_modes_per_pair"],
        "theory_values_computed": "false",
        "contains_theory_vector": "false",
        "contains_predictions": "false",
        "contains_residuals": "false",
        "contains_fit_statistics": "false",
        "uses_kids_data_vector_values": "false",
        "uses_posterior_chains": "false",
        "endpoint_scoring_allowed": "false",
        "claim_boundary": policy["claim_boundary"],
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_THEORY_VECTOR_TEMPLATE_V1_BUILT "
        f"rows={len(rows)} theory_values=false endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()
