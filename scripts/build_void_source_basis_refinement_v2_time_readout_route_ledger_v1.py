#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOW_Z_MASK = ROOT / "data" / "derived" / "low_z_pantheon_void_scope_candidate_v1_row_mask.csv"
PRODUCT_PLAN = ROOT / "data" / "source_manifest" / "paper10_product_freeze_plan.csv"
PARAM_PLAN = ROOT / "data" / "source_manifest" / "cosmology_activation_parameter_freeze_plan_v1.csv"
CHANNELS = ROOT / "data" / "source_manifest" / "cosmology_channel_manifest_v1.csv"
RULES = ROOT / "data" / "source_manifest" / "cosmology_activation_rule_manifest_v1.csv"
OUT = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_time_readout_route_ledger.csv"
SUMMARY = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_time_readout_route_ledger_summary.csv"

COMPONENT_ID = "V2_TIME_READOUT_PROJECTION"
CLAIM_BOUNDARY = "v2_time_readout_route_ledger_not_scoring_not_validation"
REQUIRED_PRODUCTS = {"CC_HZ_TABLE", "DESI_BAO_DISTANCE_VECTOR", "PLANCK_CMB_PRIORS"}


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


def main() -> None:
    low_z_rows = [row for row in read_rows(LOW_Z_MASK) if row["included"] == "true"]
    product_rows = read_rows(PRODUCT_PLAN)
    param_rows = read_rows(PARAM_PLAN)
    channel_rows = read_rows(CHANNELS)
    rule_rows = read_rows(RULES)
    if not low_z_rows:
        raise SystemExit("no included low-z rows found")
    products = {row["product_id"]: row for row in product_rows}
    missing_products = sorted(REQUIRED_PRODUCTS - set(products))
    if missing_products:
        raise SystemExit(f"missing required time products in freeze plan: {missing_products}")
    time_products = [products[item] for item in sorted(REQUIRED_PRODUCTS)]
    fetched = [row for row in time_products if row["freeze_status"] != "PRODUCT_SELECTED_NOT_FETCHED"]
    channel = next(row for row in channel_rows if row["channel_id"] == "W_TIME_READOUT")
    rule = next(row for row in rule_rows if row["channel_id"] == "W_TIME_READOUT")
    params = [row for row in param_rows if row["channel_id"] == "W_TIME_READOUT"]
    if channel["endpoint_scoring_allowed"] != "false" or rule["endpoint_scoring_allowed"] != "false":
        raise SystemExit("time channel/rule must remain endpoint disabled")
    if any(row["endpoint_scoring_allowed"] != "false" for row in params):
        raise SystemExit("time parameter freeze routes must remain endpoint disabled")

    product_status_blob = ";".join(f"{row['product_id']}={row['freeze_status']}" for row in time_products)
    parameter_status_blob = ";".join(f"{row['parameter_id']}={row['freeze_status']}" for row in params)
    time_route_declared = channel["freeze_status"] == "CHANNEL_DECLARED_NOT_ENDPOINT" and rule["rule_status"].endswith("NOT_NUMERIC")
    time_values_computable = bool(fetched) and len(fetched) == len(time_products)

    rows: list[dict[str, str]] = []
    for row in low_z_rows:
        rows.append(
            {
                "component_id": COMPONENT_ID,
                "channel_id": "W_TIME_READOUT",
                "source_scope": "LOW_Z_PANTHEON_VOID_SCOPE_CANDIDATE_POLICY_V1_INCLUDED_ROWS",
                "CID": row["CID"],
                "source_row_index": row["source_row_index"],
                "zHD": row["zHD"],
                "time_route_declared": str(time_route_declared).lower(),
                "required_products": ";".join(sorted(REQUIRED_PRODUCTS)),
                "required_product_status": product_status_blob,
                "parameter_freeze_status": parameter_status_blob,
                "time_values_computable": str(time_values_computable).lower(),
                "W_time_value_status": "BLOCKED_TIME_PRODUCTS_NOT_FETCHED_OR_NOT_NUMERIC",
                "W_time_source_value": "NA",
                "time_off_control": "0",
                "wrong_clock_proxy_available": "false",
                "shuffled_redshift_bin_control_available": "false",
                "missing_next_artifact": "data/derived/void_source_basis_refinement_v2_time_readout_values.csv",
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "contains_endpoint_scores": "false",
                "contains_distance_residuals": "false",
                "contains_late_time_fit_parameters": "false",
                "contains_fit_statistics": "false",
                "uses_posthoc_hz_smoothing": "false",
                "uses_posthoc_clock_anomaly_labels": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    summary = [
        {
            "component_id": COMPONENT_ID,
            "status": "V2_TIME_READOUT_ROUTE_LEDGER_FROZEN_VALUES_BLOCKED",
            "low_z_scope_artifact": str(LOW_Z_MASK.relative_to(ROOT)),
            "product_freeze_plan_artifact": str(PRODUCT_PLAN.relative_to(ROOT)),
            "parameter_freeze_plan_artifact": str(PARAM_PLAN.relative_to(ROOT)),
            "output_artifact": str(OUT.relative_to(ROOT)),
            "n_rows": str(len(rows)),
            "time_route_declared": str(time_route_declared).lower(),
            "required_products": ";".join(sorted(REQUIRED_PRODUCTS)),
            "required_product_status": product_status_blob,
            "parameter_freeze_status": parameter_status_blob,
            "time_values_computable": str(time_values_computable).lower(),
            "time_values_computed": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "contains_endpoint_scores": "false",
            "contains_distance_residuals": "false",
            "contains_late_time_fit_parameters": "false",
            "contains_fit_statistics": "false",
            "verdict": "time_route_declared_but_products_not_fetched_or_numeric_rule_missing",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(OUT, rows)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_V2_TIME_READOUT_ROUTE_LEDGER_BUILT "
        f"rows={len(rows)} time_values_computable={str(time_values_computable).lower()} "
        "time_values_computed=false"
    )


if __name__ == "__main__":
    main()
