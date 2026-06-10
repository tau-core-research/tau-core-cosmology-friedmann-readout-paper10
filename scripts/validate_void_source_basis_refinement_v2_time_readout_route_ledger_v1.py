#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_time_readout_route_ledger.csv"
SUMMARY = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_time_readout_route_ledger_summary.csv"

COMPONENT_ID = "V2_TIME_READOUT_PROJECTION"
CLAIM_BOUNDARY = "v2_time_readout_route_ledger_not_scoring_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    rows = read_rows(LEDGER)
    summary = read_one(SUMMARY)
    require(rows, "time route ledger is empty")
    require(summary["component_id"] == COMPONENT_ID, "summary component mismatch")
    require(summary["status"] == "V2_TIME_READOUT_ROUTE_LEDGER_FROZEN_VALUES_BLOCKED", "bad summary status")
    require(summary["n_rows"] == str(len(rows)), "row count mismatch")
    require(summary["time_route_declared"] == "true", "time route should be declared")
    require(summary["time_values_computable"] == "false", "time values must not yet be computable")
    require(summary["time_values_computed"] == "false", "time values must not be computed")
    for product_id in ["CC_HZ_TABLE", "DESI_BAO_DISTANCE_VECTOR", "PLANCK_CMB_PRIORS"]:
        require(
            f"{product_id}=PRODUCT_SELECTED_NOT_FETCHED" in summary["required_product_status"],
            f"{product_id} should remain selected but not fetched",
        )
    require(summary["endpoint_replay_allowed"] == "false", "summary must not allow endpoint replay")
    require(summary["endpoint_validation_claimed"] == "false", "summary must not claim endpoint validation")
    require(summary["contains_endpoint_scores"] == "false", "summary must not contain endpoint scores")
    require(summary["contains_distance_residuals"] == "false", "summary must not contain distance residuals")
    require(summary["contains_late_time_fit_parameters"] == "false", "summary must not contain late-time fits")
    require(summary["contains_fit_statistics"] == "false", "summary must not contain fit statistics")
    require(
        summary["verdict"] == "time_route_declared_but_products_not_fetched_or_numeric_rule_missing",
        "unexpected time route verdict",
    )
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")

    for row in rows:
        require(row["component_id"] == COMPONENT_ID, "row component mismatch")
        require(row["channel_id"] == "W_TIME_READOUT", "row channel mismatch")
        require(row["time_route_declared"] == "true", "row time route mismatch")
        require(row["time_values_computable"] == "false", "row must not compute time values")
        require(
            row["W_time_value_status"] == "BLOCKED_TIME_PRODUCTS_NOT_FETCHED_OR_NOT_NUMERIC",
            "time value status mismatch",
        )
        require(row["W_time_source_value"] == "NA", "W_time source value must remain NA")
        require(row["time_off_control"] == "0", "time off control must be zero")
        require(row["wrong_clock_proxy_available"] == "false", "wrong clock proxy must not be available yet")
        require(row["shuffled_redshift_bin_control_available"] == "false", "redshift shuffle must not be available yet")
        require(row["endpoint_replay_allowed"] == "false", "rows must not allow endpoint replay")
        require(row["endpoint_validation_claimed"] == "false", "rows must not claim endpoint validation")
        require(row["contains_endpoint_scores"] == "false", "rows must not contain endpoint scores")
        require(row["contains_distance_residuals"] == "false", "rows must not contain distance residuals")
        require(row["contains_late_time_fit_parameters"] == "false", "rows must not contain late-time fits")
        require(row["contains_fit_statistics"] == "false", "rows must not contain fit statistics")
        require(row["uses_posthoc_hz_smoothing"] == "false", "rows must not use posthoc H(z) smoothing")
        require(row["uses_posthoc_clock_anomaly_labels"] == "false", "rows must not use clock anomaly labels")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
    print(
        "PAPER10_V2_TIME_READOUT_ROUTE_LEDGER_VALIDATED "
        f"rows={len(rows)} time_values_computed=false"
    )


if __name__ == "__main__":
    main()
