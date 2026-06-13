#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/low_z_pantheon_time_readout_source_audit_policy_v1.csv"
AUDIT = ROOT / "data/derived/low_z_pantheon_time_readout_source_audit_v1.csv"
SUMMARY = ROOT / "data/derived/low_z_pantheon_time_readout_source_audit_v1_summary.csv"
CLAIM_BOUNDARY = "time_readout_source_audit_source_side_not_scoring_not_validation"


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
    policy = read_one(POLICY)
    rows = read_rows(AUDIT)
    summary = read_one(SUMMARY)
    require(policy["status"] == "TIME_READOUT_SOURCE_AUDIT_SOURCE_SIDE_NOT_SCORING", "bad policy")
    require(policy["endpoint_replay_allowed"] == "false", "policy must not authorize replay")
    require(summary["status"] == "TIME_READOUT_SOURCE_AUDIT_BUILT_SOURCE_SIDE_NOT_SCORING", "bad summary")
    require(summary["rows"] == str(len(rows)), "row count mismatch")
    require(summary["rows"] == "424", "expected 424 low-z rows")
    require(summary["cc_hz_row_count"] == "32", "expected 32 CC H(z) rows")
    require(summary["partial_path_scope_rows"] == "12", "expected 12 partial path-scope rows")
    require(summary["cc_hz_product_fetched_frozen"] == "true", "CC product should be fetched/frozen")
    require(summary["sdss_bao_rsd_products_fetched_frozen"] == "true", "SDSS products should be fetched/frozen")
    require(summary["cmb_route_cache_available"] == "true", "CMB route cache should be available")
    require(summary["delta_clock_scale_frozen"] == "false", "Delta_clock scale must remain missing")
    require(summary["time_readout_numeric_rule_available"] == "false", "numeric rule must remain missing")
    require(summary["endpoint_replay_allowed"] == "false", "summary must not authorize replay")
    require(summary["endpoint_validation_claimed"] == "false", "summary must not claim validation")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    require(
        summary["verdict"] == "time_readout_sources_partially_available_but_delta_clock_rule_missing",
        "bad verdict",
    )
    for row in rows:
        require(row["cc_hz_product_fetched_frozen"] == "true", "row CC product mismatch")
        require(row["sdss_bao_rsd_products_fetched_frozen"] == "true", "row SDSS product mismatch")
        require(row["cmb_route_cache_available"] == "true", "row CMB route mismatch")
        require(row["delta_clock_scale_frozen"] == "false", "row Delta_clock scale must be missing")
        require(row["time_readout_numeric_rule_available"] == "false", "row numeric rule must be missing")
        require(
            row["W_time_value_status"] == "BLOCKED_DELTA_CLOCK_SCALE_AND_NUMERIC_RULE_MISSING",
            "bad W_time status",
        )
        require(row["W_time_source_value"] == "NA", "W_time source value must remain NA")
        require(row["endpoint_replay_allowed"] == "false", "row must not authorize replay")
        require(row["endpoint_validation_claimed"] == "false", "row must not claim validation")
        require(row["contains_distance_residuals"] == "false", "row must not contain residuals")
        require(row["contains_late_time_fit_parameters"] == "false", "row must not contain late-time fits")
        require(row["contains_fit_statistics"] == "false", "row must not contain fit statistics")
        require(row["uses_posthoc_hz_smoothing"] == "false", "row must not use posthoc smoothing")
        require(row["uses_posthoc_clock_anomaly_labels"] == "false", "row must not use clock labels")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
        float(row["nearest_cc_hz_delta_z"])
        float(row["nearest_sdss_bao_rsd_delta_z"])
    print(
        "PAPER10_TIME_READOUT_SOURCE_AUDIT_VALIDATED "
        f"rows={summary['rows']} cc_near={summary['low_z_rows_with_cc_hz_support_delta_z_le_0p05']} "
        "w_time=false"
    )


if __name__ == "__main__":
    main()
