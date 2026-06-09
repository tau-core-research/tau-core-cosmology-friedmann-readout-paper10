#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path

import numpy as np
from astropy.io import fits


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_d_path_full_route_mask_load_rule_policy_v1.csv"
CACHE_INVENTORY = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_full_route_cache_inventory_v1.csv"
CACHE_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_full_route_cache_inventory_v1_summary.csv"
DOMAIN = ROOT / "data" / "derived" / "kids1000_cosebis_path_mapping_domain_skeleton_v1.csv"
F_OVERLAP_TILE = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_full_route_pixel_fraction_tile_rule_v1.csv"
TILE_OUT = ROOT / "data" / "derived" / "kids1000_cosebis_d_path_full_route_mask_load_tile_rule_v1.csv"
DOMAIN_OUT = ROOT / "data" / "derived" / "kids1000_cosebis_d_path_full_route_mask_load_rule_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_d_path_full_route_mask_load_rule_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def float_text(value: float) -> str:
    return f"{value:.12e}"


def cache_path(row: dict[str, str]) -> Path:
    if row["cache_source"] == "local_full_route_cache_v1":
        return ROOT / row["expected_local_full_route_cache_path"]
    if row["cache_source"] == "committed_subset_v1":
        return ROOT / row["committed_subset_path"]
    raise SystemExit(f"unusable cache source for D_path mask-load rule: {row['cache_source']}")


def mask_load(path: Path) -> dict[str, str | int | float]:
    with fits.open(path, memmap=False) as hdul:
        image = hdul[0].data
        header = hdul[0].header
        if image is None:
            raise SystemExit(f"missing image data in {path}")
        arr = np.asarray(image, dtype=np.float64)
        finite = np.isfinite(arr)
        n_pixels = int(arr.size)
        n_finite = int(finite.sum())
        finite_values = arr[finite]
        nonzero = finite_values[finite_values != 0]
        n_nonzero = int(nonzero.size)
        mean_nonzero = float(nonzero.mean()) if n_nonzero else 0.0
        std_nonzero = float(nonzero.std()) if n_nonzero else 0.0
        median_nonzero = float(np.median(nonzero)) if n_nonzero else 0.0
    return {
        "primary_shape": "x".join(str(value) for value in arr.shape),
        "bitpix": str(header.get("BITPIX", "")),
        "naxis": str(header.get("NAXIS", "")),
        "n_pixels": n_pixels,
        "n_finite_pixels": n_finite,
        "nonzero_finite_pixels": n_nonzero,
        "mean_nonzero_mask_value": mean_nonzero,
        "std_nonzero_mask_value": std_nonzero,
        "median_nonzero_mask_value": median_nonzero,
    }


def main() -> None:
    policy = read_one(POLICY)
    cache_summary = read_one(CACHE_SUMMARY)
    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("D_path mask-load policy must keep endpoint scoring disabled")
    if policy["current_path_mapping_computed"] != "false":
        raise SystemExit("D_path mask-load rule must not compute path mapping")
    if policy["current_theory_vector_computed"] != "false":
        raise SystemExit("D_path mask-load rule must not compute theory vectors")
    if cache_summary["source_cache_complete"] != "true":
        raise SystemExit("D_path mask-load rule requires complete source cache")

    with CACHE_INVENTORY.open(newline="") as f:
        cache_rows = list(csv.DictReader(f))
    with F_OVERLAP_TILE.open(newline="") as f:
        f_overlap_rows = list(csv.DictReader(f))
    f_by_tile = {row["tile_index_zero_based"]: row for row in f_overlap_rows}
    if len(cache_rows) != int(policy["expected_tile_count"]):
        raise SystemExit("D_path mask-load rule expects 196 cache rows")

    tile_rows: list[dict[str, str]] = []
    means: list[float] = []
    for row in cache_rows:
        if row["accepted_for_source_cache_inventory"] != "true":
            raise SystemExit("all cache rows must be accepted before D_path derivation")
        path = cache_path(row)
        if not path.exists():
            raise SystemExit(f"missing cached mask product: {path.relative_to(ROOT)}")
        stats = mask_load(path)
        mean = float(stats["mean_nonzero_mask_value"])
        means.append(mean)
        f_overlap = f_by_tile[row["tile_index_zero_based"]]
        tile_rows.append(
            {
                "policy_id": policy["policy_id"],
                "tile_index_zero_based": row["tile_index_zero_based"],
                "filename": row["filename"],
                "cache_source": row["cache_source"],
                "sha256": row["sha256"],
                "source_scope": policy["source_scope"],
                "d_path_rule": policy["d_path_rule"],
                "primary_shape": str(stats["primary_shape"]),
                "bitpix": str(stats["bitpix"]),
                "naxis": str(stats["naxis"]),
                "n_pixels": str(stats["n_pixels"]),
                "n_finite_pixels": str(stats["n_finite_pixels"]),
                "nonzero_finite_pixels": str(stats["nonzero_finite_pixels"]),
                "mean_nonzero_mask_value": float_text(mean),
                "std_nonzero_mask_value": float_text(float(stats["std_nonzero_mask_value"])),
                "median_nonzero_mask_value": float_text(float(stats["median_nonzero_mask_value"])),
                "f_overlap_value_for_nonidentity_check": f_overlap["f_overlap_full_route_pixel_fraction_value"],
                "d_path_mask_load_computed": "true",
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

    max_mean = max(means)
    min_mean = min(means)
    mean_mean = sum(means) / len(means)
    if max_mean <= 0.0:
        raise SystemExit("D_path mask-load means must contain positive support")
    for row in tile_rows:
        value = float(row["mean_nonzero_mask_value"]) / max_mean
        row["d_path_full_route_mask_load_value"] = float_text(value)
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
                    "d_path_value": tile["d_path_full_route_mask_load_value"],
                    "d_path_rule_component": "full_route_mean_nonzero_mask_value_normalized_by_max_tile_mean",
                    "mean_nonzero_mask_value": tile["mean_nonzero_mask_value"],
                    "d_path_mask_load_computed": "true",
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
        raise SystemExit("D_path mask-load domain rule must contain 58,800 rows")

    with TILE_OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(tile_rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(tile_rows)
    with DOMAIN_OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(domain_rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(domain_rows)

    values = [float(row["d_path_full_route_mask_load_value"]) for row in tile_rows]
    f_values = [float(row["f_overlap_value_for_nonidentity_check"]) for row in tile_rows]
    unique_values = len({round(value, 12) for value in values})
    non_degenerate = unique_values > 1 and (max(values) - min(values)) > 1e-6
    max_abs_delta_from_f_overlap = max(abs(a - b) for a, b in zip(values, f_values))
    summary = {
        "policy_id": policy["policy_id"],
        "status": "KIDS1000_COSEBIS_D_PATH_FULL_ROUTE_MASK_LOAD_RULE_BUILT_SOURCE_ONLY_NOT_MAPPED",
        "tile_count": str(len(tile_rows)),
        "target_rows": "300",
        "domain_rows": str(len(domain_rows)),
        "source_scope": policy["source_scope"],
        "d_path_rule": policy["d_path_rule"],
        "min_mean_nonzero_mask_value": float_text(min_mean),
        "max_mean_nonzero_mask_value": float_text(max_mean),
        "mean_mean_nonzero_mask_value": float_text(mean_mean),
        "min_d_path_value": float_text(min(values)),
        "max_d_path_value": float_text(max(values)),
        "mean_d_path_value": float_text(sum(values) / len(values)),
        "unique_d_path_value_count_rounded_1e_minus_12": str(unique_values),
        "max_abs_delta_from_f_overlap": float_text(max_abs_delta_from_f_overlap),
        "d_path_full_route_mask_load_non_degenerate": "true" if non_degenerate else "false",
        "d_path_source_route_support": "true" if non_degenerate else "false",
        "d_path_not_identical_to_f_overlap": "true" if max_abs_delta_from_f_overlap > 1e-6 else "false",
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
        "PAPER10_KIDS1000_COSEBIS_D_PATH_FULL_ROUTE_MASK_LOAD_RULE_V1_BUILT "
        f"domain_rows={len(domain_rows)} non_degenerate={summary['d_path_full_route_mask_load_non_degenerate']} "
        "endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()
