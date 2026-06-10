#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_photoz_tomographic_calibration_evidence_policy_v1.csv"
HOLDOUT = ROOT / "data" / "derived" / "kids1000_cosebis_source_frozen_tomographic_holdout_manifest_v1_summary.csv"
SOURCE_CACHE = ROOT / "data" / "source_manifest" / "source_page_cache_manifest.csv"
PRODUCT = ROOT / "data" / "source_manifest" / "kids1000_lensing_products_v1.csv"
ZINV = ROOT / "data" / "derived" / "kids1000_cosebis_redshift_kernel_inventory_v1.csv"
ZSUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_redshift_kernel_inventory_v1_summary.csv"

OUT = ROOT / "data" / "derived" / "kids1000_cosebis_photoz_tomographic_calibration_evidence_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_photoz_tomographic_calibration_evidence_v1_summary.csv"


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


def cache_row(rows: list[dict[str, str]], source_id: str) -> dict[str, str]:
    for row in rows:
        if row["source_id"] == source_id:
            return row
    raise SystemExit(f"missing source cache row: {source_id}")


def main() -> None:
    policy = read_one(POLICY)
    holdout = read_one(HOLDOUT)
    product = read_one(PRODUCT)
    zsummary = read_one(ZSUMMARY)
    zrows = read_rows(ZINV)
    source_cache = cache_row(read_rows(SOURCE_CACHE), "WEAK_LENSING_PRODUCTS")

    if policy["status"] != "PHOTOZ_TOMOGRAPHIC_CALIBRATION_EVIDENCE_POLICY_FROZEN":
        raise SystemExit("unexpected photo-z evidence policy status")
    if policy["computes_new_scores"] != "false":
        raise SystemExit("evidence ledger must not compute scores")
    if policy["endpoint_replay_allowed"] != "false":
        raise SystemExit("evidence ledger must not authorize endpoint replay")
    if policy["endpoint_validation_claimed"] != "false":
        raise SystemExit("evidence ledger must not claim validation")
    if holdout["h2_holdout_partition_frozen"] != "true":
        raise SystemExit("holdout partition should be frozen before H1 evidence ledger")
    if product["status"] != "SOURCE_NATIVE_PRODUCT_FETCHED_FROZEN":
        raise SystemExit("KiDS source product must be fetched/frozen")
    if source_cache["status"] != "CACHED":
        raise SystemExit("KiDS landing page cache must be present")
    if len(zrows) != 5 or zsummary["n_source_bins"] != "5":
        raise SystemExit("expected five source redshift kernels")

    cache_text = (ROOT / source_cache["cache_path"]).read_text(errors="ignore")
    markers = {
        "weak_lensing_som_gold_catalogue": "Weak Lensing SOM-gold catalogue" in cache_text,
        "photometric_redshift_measurements": "photometric redshift measurements" in cache_text,
        "kuijken_2019_citation_marker": "Kuijken et al. 2019" in cache_text,
        "wright_2020_citation_marker": "Wright et al. 2020" in cache_text,
        "hildebrandt_2021_citation_marker": "Hildebrandt et al. 2021" in cache_text,
        "giblin_2021_citation_marker": "Giblin et al 2021" in cache_text,
    }
    if not all(markers.values()):
        raise SystemExit("cached KiDS page is missing expected photo-z/tomographic markers")

    selected_member = zrows[0]["selected_member"]
    rows = [
        {
            "policy_id": policy["policy_id"],
            "evidence_id": "E0_kids_lensing_product",
            "evidence_class": "source_native_product_checksum",
            "source_artifact": product["local_path"],
            "source_status": product["status"],
            "evidence_status": "ACCEPT_SOURCE_NATIVE_PRODUCT",
            "source_side_value": f"sha256={product['sha256']};bytes={product['byte_count']}",
            "h1_support_level": "supporting_source_product_only",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "evidence_id": "E1_kids_landing_page_photoz_markers",
            "evidence_class": "cached_public_documentation_marker",
            "source_artifact": source_cache["cache_path"],
            "source_status": source_cache["status"],
            "evidence_status": "ACCEPT_DOCUMENTATION_MARKERS",
            "source_side_value": ";".join(f"{key}={str(value).lower()}" for key, value in markers.items()),
            "h1_support_level": "supports_photoz_tomographic_context_not_external_calibration_closure",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "evidence_id": "E2_nz_source_inventory",
            "evidence_class": "source_native_redshift_kernel_inventory",
            "source_artifact": "data/derived/kids1000_cosebis_redshift_kernel_inventory_v1.csv",
            "source_status": zsummary["status"],
            "evidence_status": "ACCEPT_SOURCE_NATIVE_NZ",
            "source_side_value": (
                f"selected_member={selected_member};hdu={zsummary['selected_hdu_redshift_distribution']};"
                f"bins={zsummary['n_source_bins']};nz_rows={zsummary['nz_rows']};"
                f"mean_z_range={zsummary['min_mean_z']}..{zsummary['max_mean_z']}"
            ),
            "h1_support_level": "supports_source_native_tomographic_kernel_freeze",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "evidence_id": "E3_independent_external_calibration",
            "evidence_class": "independent_photoz_or_tomographic_calibration_closure",
            "source_artifact": "not_attached",
            "source_status": "MISSING",
            "evidence_status": "OPEN_REQUIRED_BEFORE_REPLAY",
            "source_side_value": "external_calibration_manifest_not_yet_frozen",
            "h1_support_level": "blocking_requirement_open",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": policy["claim_boundary"],
        },
    ]

    summary = [
        {
            "policy_id": policy["policy_id"],
            "status": "PHOTOZ_TOMOGRAPHIC_CALIBRATION_EVIDENCE_LEDGER_BUILT",
            "selected_statistic": policy["selected_statistic"],
            "evidence_rows": str(len(rows)),
            "source_native_product_frozen": "true",
            "cached_public_photoz_markers_present": "true",
            "source_native_nz_available": "true",
            "independent_external_photoz_calibration_attached": "false",
            "h1_independent_evidence_complete": "false",
            "h2_holdout_partition_frozen": holdout["h2_holdout_partition_frozen"],
            "computes_new_scores": "false",
            "uses_kids_data_vector_values_for_scoring": "false",
            "uses_kids_data_vector_values_for_source_selection": "false",
            "uses_residuals": "false",
            "uses_fit_statistics": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "verdict": "partial_photoz_tomographic_evidence_available_but_h1_external_calibration_open",
            "recommended_next_action": "attach_independent_external_photoz_or_tomographic_calibration_manifest_before_endpoint_replay",
            "claim_boundary": policy["claim_boundary"],
        }
    ]
    write_csv(OUT, rows)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_PHOTOZ_TOMOGRAPHIC_CALIBRATION_EVIDENCE_V1_BUILT "
        f"verdict={summary[0]['verdict']}"
    )


if __name__ == "__main__":
    main()
