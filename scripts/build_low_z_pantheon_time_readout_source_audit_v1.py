#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/low_z_pantheon_time_readout_source_audit_policy_v1.csv"
LOW_Z_MASK = ROOT / "data/derived/low_z_pantheon_void_scope_candidate_v1_row_mask.csv"
CC_HZ = ROOT / "data/raw/hz_compilation/cosmic_chronometers_hz/data_CC.dat"
PILOT_PRODUCTS = ROOT / "data/source_manifest/pilot_frozen_product_manifest.csv"
SDSS_PRODUCTS = ROOT / "data/source_manifest/sdss_multitracer_bao_rsd_products_v1.csv"
CMB_ROUTE_CACHE = ROOT / "data/source_manifest/source_page_cache/PLANCK_LAMBDA_CMB.html"
OUT = ROOT / "data/derived/low_z_pantheon_time_readout_source_audit_v1.csv"
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


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def load_cc_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with CC_HZ.open() as f:
        for line in f:
            if not line.strip() or line.startswith("#"):
                continue
            z, hz, err, reference = line.strip().split(",", 3)
            rows.append({"z": z, "Hz": hz, "errHz": err, "reference": reference})
    if not rows:
        raise SystemExit("CC H(z) table is empty")
    return rows


def nearest_z_distance(z: float, candidates: list[float]) -> float:
    if not candidates:
        return math.nan
    return min(abs(z - candidate) for candidate in candidates)


def main() -> None:
    policy = read_one(POLICY)
    if policy["status"] != "TIME_READOUT_SOURCE_AUDIT_SOURCE_SIDE_NOT_SCORING":
        raise SystemExit("policy status mismatch")
    if policy["endpoint_replay_allowed"] != "false" or policy["endpoint_validation_claimed"] != "false":
        raise SystemExit("time source audit policy must not authorize replay or validation")
    if not CMB_ROUTE_CACHE.exists():
        raise SystemExit("cached Planck/LAMBDA route page is missing")
    low_z_rows = [row for row in read_rows(LOW_Z_MASK) if row["included"] == "true"]
    cc_rows = load_cc_rows()
    pilot_products = read_rows(PILOT_PRODUCTS)
    sdss_products = read_rows(SDSS_PRODUCTS)
    cc_product = next((row for row in pilot_products if row["product_id"] == "CC_HZ_TABLE"), None)
    if cc_product is None or cc_product["status"] != "PILOT_PRODUCT_FETCHED_FROZEN":
        raise SystemExit("CC H(z) product is not fetched/frozen")
    sdss_frozen = [row for row in sdss_products if row["status"] == "SOURCE_NATIVE_PRODUCT_FETCHED_FROZEN"]
    if len(sdss_frozen) < 2:
        raise SystemExit("expected both SDSS BAO/RSD products to be fetched/frozen")
    cc_z = [float(row["z"]) for row in cc_rows]
    sdss_z = sorted({0.70, 0.77, 0.845})
    rows: list[dict[str, str]] = []
    for row in low_z_rows:
        z = float(row["zHD"])
        cc_nearest = nearest_z_distance(z, cc_z)
        sdss_nearest = nearest_z_distance(z, sdss_z)
        rows.append(
            {
                "artifact_id": "LOW_Z_PANTHEON_TIME_READOUT_SOURCE_AUDIT_V1",
                "CID": row["CID"],
                "source_row_index": row["source_row_index"],
                "zHD": row["zHD"],
                "cc_hz_product_fetched_frozen": "true",
                "cc_hz_row_count": str(len(cc_rows)),
                "nearest_cc_hz_delta_z": f"{cc_nearest:.12g}",
                "cc_hz_support_near_low_z": str(cc_nearest <= 0.05).lower(),
                "sdss_bao_rsd_products_fetched_frozen": "true",
                "nearest_sdss_bao_rsd_delta_z": f"{sdss_nearest:.12g}",
                "cmb_route_cache_available": "true",
                "delta_clock_scale_frozen": "false",
                "time_readout_numeric_rule_available": "false",
                "W_time_value_status": "BLOCKED_DELTA_CLOCK_SCALE_AND_NUMERIC_RULE_MISSING",
                "W_time_source_value": "NA",
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "contains_endpoint_scores": "false",
                "contains_distance_residuals": "false",
                "contains_late_time_fit_parameters": "false",
                "contains_fit_statistics": "false",
                "uses_posthoc_hz_smoothing": "false",
                "uses_posthoc_clock_anomaly_labels": "false",
                "physical_lensing_path_weight_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    cc_near = sum(row["cc_hz_support_near_low_z"] == "true" for row in rows)
    partial_scope = {"344", "350", "374", "375", "384", "448", "554", "595", "603", "606", "635", "701"}
    partial_rows = [row for row in rows if row["source_row_index"] in partial_scope]
    summary = [
        {
            "artifact_id": "LOW_Z_PANTHEON_TIME_READOUT_SOURCE_AUDIT_V1",
            "status": "TIME_READOUT_SOURCE_AUDIT_BUILT_SOURCE_SIDE_NOT_SCORING",
            "rows": str(len(rows)),
            "cc_hz_row_count": str(len(cc_rows)),
            "cc_hz_min_z": f"{min(cc_z):.12g}",
            "cc_hz_max_z": f"{max(cc_z):.12g}",
            "low_z_rows_with_cc_hz_support_delta_z_le_0p05": str(cc_near),
            "sdss_bao_rsd_redshift_nodes": ";".join(f"{value:.12g}" for value in sdss_z),
            "partial_path_scope_rows": str(len(partial_rows)),
            "partial_path_scope_cc_hz_support_delta_z_le_0p05": str(
                sum(row["cc_hz_support_near_low_z"] == "true" for row in partial_rows)
            ),
            "cc_hz_product_fetched_frozen": "true",
            "sdss_bao_rsd_products_fetched_frozen": "true",
            "cmb_route_cache_available": "true",
            "delta_clock_scale_frozen": "false",
            "time_readout_numeric_rule_available": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_lensing_path_weight_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
            "verdict": "time_readout_sources_partially_available_but_delta_clock_rule_missing",
        }
    ]
    write_csv(OUT, rows)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_TIME_READOUT_SOURCE_AUDIT_BUILT "
        f"rows={summary[0]['rows']} cc_near={summary[0]['low_z_rows_with_cc_hz_support_delta_z_le_0p05']} "
        "w_time=false"
    )


if __name__ == "__main__":
    main()
