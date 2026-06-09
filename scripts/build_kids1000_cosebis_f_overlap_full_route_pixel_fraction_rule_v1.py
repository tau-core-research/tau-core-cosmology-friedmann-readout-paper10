#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path

import numpy as np
from astropy.io import fits


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_f_overlap_full_route_pixel_fraction_rule_policy_v1.csv"
CACHE_INVENTORY = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_full_route_cache_inventory_v1.csv"
CACHE_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_full_route_cache_inventory_v1_summary.csv"
DOMAIN = ROOT / "data" / "derived" / "kids1000_cosebis_path_mapping_domain_skeleton_v1.csv"
TILE_OUT = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_full_route_pixel_fraction_tile_rule_v1.csv"
DOMAIN_OUT = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_full_route_pixel_fraction_rule_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_full_route_pixel_fraction_rule_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def float_text(value: float) -> str:
    return f"{value:.12e}"


def mask_fraction(path: Path) -> dict[str, str | int | float]:
    with fits.open(path, memmap=False) as hdul:
        image = hdul[0].data
        header = hdul[0].header
        if image is None:
            raise SystemExit(f"missing image data in {path}")
        arr = np.asarray(image)
        finite = np.isfinite(arr)
        n_pixels = int(arr.size)
        n_finite = int(finite.sum())
        finite_values = arr[finite]
        nonzero_finite = int(np.count_nonzero(finite_values))
    return {
        "primary_shape": "x".join(str(value) for value in arr.shape),
        "bitpix": str(header.get("BITPIX", "")),
        "naxis": str(header.get("NAXIS", "")),
        "n_pixels": n_pixels,
        "n_finite_pixels": n_finite,
        "finite_fraction": (n_finite / n_pixels) if n_pixels else 0.0,
        "nonzero_finite_pixels": nonzero_finite,
        "nonzero_finite_fraction": (nonzero_finite / n_finite) if n_finite else 0.0,
    }


def cache_path(row: dict[str, str]) -> Path:
    if row["cache_source"] == "local_full_route_cache_v1":
        return ROOT / row["expected_local_full_route_cache_path"]
    if row["cache_source"] == "committed_subset_v1":
        return ROOT / row["committed_subset_path"]
    raise SystemExit(f"unusable cache source for full-route pixel fraction: {row['cache_source']}")


def main() -> None:
    policy = read_one(POLICY)
    cache_summary = read_one(CACHE_SUMMARY)
    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("full-route pixel-fraction policy must keep endpoint scoring disabled")
    if policy["current_path_mapping_computed"] != "false":
        raise SystemExit("full-route pixel-fraction rule must not compute path mapping")
    if policy["current_theory_vector_computed"] != "false":
        raise SystemExit("full-route pixel-fraction rule must not compute theory vectors")
    if cache_summary["source_cache_complete"] != "true":
        raise SystemExit("full-route pixel-fraction rule requires complete source cache")

    with CACHE_INVENTORY.open(newline="") as f:
        cache_rows = list(csv.DictReader(f))
    if len(cache_rows) != int(policy["expected_tile_count"]):
        raise SystemExit("full-route pixel-fraction rule expects 196 cache rows")

    tile_rows: list[dict[str, str]] = []
    raw_fractions: list[float] = []
    for row in cache_rows:
        if row["accepted_for_source_cache_inventory"] != "true":
            raise SystemExit("all cache rows must be accepted before pixel-fraction derivation")
        path = cache_path(row)
        if not path.exists():
            raise SystemExit(f"missing cached mask product: {path.relative_to(ROOT)}")
        stats = mask_fraction(path)
        fraction = float(stats["nonzero_finite_fraction"])
        raw_fractions.append(fraction)
        tile_rows.append(
            {
                "policy_id": policy["policy_id"],
                "tile_index_zero_based": row["tile_index_zero_based"],
                "filename": row["filename"],
                "cache_source": row["cache_source"],
                "sha256": row["sha256"],
                "source_scope": policy["source_scope"],
                "pixel_rule": policy["pixel_rule"],
                "primary_shape": str(stats["primary_shape"]),
                "bitpix": str(stats["bitpix"]),
                "naxis": str(stats["naxis"]),
                "n_pixels": str(stats["n_pixels"]),
                "n_finite_pixels": str(stats["n_finite_pixels"]),
                "finite_fraction": float_text(float(stats["finite_fraction"])),
                "nonzero_finite_pixels": str(stats["nonzero_finite_pixels"]),
                "nonzero_finite_fraction": float_text(fraction),
                "full_route_pixel_fraction_computed": "true",
                "path_mapping_computed": "false",
                "contains_mapping_vector": "false",
                "contains_theory_vector": "false",
                "contains_predictions": "false",
                "contains_residuals": "false",
                "contains_fit_statistics": "false",
                "uses_kids_data_vector_values": "false",
                "uses_posterior_chains": "false",
                "uses_posthoc_tile_selection": "false",
                "uses_posthoc_path_projection_labels": "false",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": policy["claim_boundary"],
            }
        )

    max_fraction = max(raw_fractions)
    min_fraction = min(raw_fractions)
    mean_fraction = sum(raw_fractions) / len(raw_fractions)
    if max_fraction <= 0.0:
        raise SystemExit("full-route pixel fractions must contain positive support")
    for row in tile_rows:
        fraction = float(row["nonzero_finite_fraction"])
        row["f_overlap_full_route_pixel_fraction_value"] = float_text(fraction / max_fraction)
        row["normalization_rule"] = policy["normalization_rule"]

    tile_by_index = {row["tile_index_zero_based"]: row for row in tile_rows}
    domain_rows: list[dict[str, str]] = []
    with DOMAIN.open(newline="") as f:
        for domain in csv.DictReader(f):
            tile = tile_by_index[domain["tile_index_zero_based"]]
            domain_rows.append(
                {
                    "policy_id": policy["policy_id"],
                    "domain_row_index_zero_based": domain["domain_row_index_zero_based"],
                    "target_row_index_zero_based": domain["target_row_index_zero_based"],
                    "tile_index_zero_based": domain["tile_index_zero_based"],
                    "pair_id": domain["pair_id"],
                    "bin1": domain["bin1"],
                    "bin2": domain["bin2"],
                    "mode": domain["mode"],
                    "tile_ra_deg_filename_proxy": domain["tile_ra_deg_filename_proxy"],
                    "tile_dec_deg_filename_proxy": domain["tile_dec_deg_filename_proxy"],
                    "f_overlap_value": tile["f_overlap_full_route_pixel_fraction_value"],
                    "f_overlap_rule_component": "full_route_finite_nonzero_pixel_fraction_normalized_by_max_tile_fraction",
                    "nonzero_finite_fraction": tile["nonzero_finite_fraction"],
                    "full_route_pixel_fraction_computed": "true",
                    "path_mapping_computed": "false",
                    "contains_mapping_vector": "false",
                    "contains_theory_vector": "false",
                    "contains_predictions": "false",
                    "contains_residuals": "false",
                    "contains_fit_statistics": "false",
                    "uses_kids_data_vector_values": "false",
                    "uses_posterior_chains": "false",
                    "uses_posthoc_tile_selection": "false",
                    "uses_posthoc_path_projection_labels": "false",
                    "endpoint_scoring_allowed": "false",
                    "claim_boundary": policy["claim_boundary"],
                }
            )
    if len(domain_rows) != int(policy["expected_domain_rows"]):
        raise SystemExit("full-route pixel-fraction domain rule must contain 58,800 rows")

    TILE_OUT.parent.mkdir(parents=True, exist_ok=True)
    with TILE_OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(tile_rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(tile_rows)
    with DOMAIN_OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(domain_rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(domain_rows)

    values = [float(row["f_overlap_full_route_pixel_fraction_value"]) for row in tile_rows]
    unique_values = len({round(value, 12) for value in values})
    non_degenerate = unique_values > 1 and (max(values) - min(values)) > 1e-6
    summary = {
        "policy_id": policy["policy_id"],
        "status": "KIDS1000_COSEBIS_F_OVERLAP_FULL_ROUTE_PIXEL_FRACTION_RULE_BUILT_SOURCE_ONLY_NOT_MAPPED",
        "tile_count": str(len(tile_rows)),
        "target_rows": "300",
        "domain_rows": str(len(domain_rows)),
        "source_scope": policy["source_scope"],
        "pixel_rule": policy["pixel_rule"],
        "min_nonzero_finite_fraction": float_text(min_fraction),
        "max_nonzero_finite_fraction": float_text(max_fraction),
        "mean_nonzero_finite_fraction": float_text(mean_fraction),
        "min_f_overlap_value": float_text(min(values)),
        "max_f_overlap_value": float_text(max(values)),
        "mean_f_overlap_value": float_text(sum(values) / len(values)),
        "unique_f_overlap_value_count_rounded_1e_minus_12": str(unique_values),
        "full_route_pixel_fraction_non_degenerate": "true" if non_degenerate else "false",
        "f_overlap_endpoint_route_support": "true" if non_degenerate else "false",
        "path_mapping_computed": "false",
        "contains_mapping_vector": "false",
        "contains_theory_vector": "false",
        "contains_predictions": "false",
        "contains_residuals": "false",
        "contains_fit_statistics": "false",
        "uses_kids_data_vector_values": "false",
        "uses_posterior_chains": "false",
        "uses_posthoc_tile_selection": "false",
        "uses_posthoc_path_projection_labels": "false",
        "endpoint_scoring_allowed": "false",
        "claim_boundary": policy["claim_boundary"],
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_F_OVERLAP_FULL_ROUTE_PIXEL_FRACTION_RULE_V1_BUILT "
        f"domain_rows={len(domain_rows)} non_degenerate={summary['full_route_pixel_fraction_non_degenerate']} "
        "endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()
