#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_f_overlap_full_route_cache_inventory_policy_v1.csv"
FULL_MASK_MANIFEST = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_full_mask_acquisition_manifest_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_full_route_cache_inventory_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_full_route_cache_inventory_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def main() -> None:
    policy = read_one(POLICY)
    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("cache inventory policy must keep endpoint scoring disabled")
    if policy["current_overlap_rule_computed"] != "false":
        raise SystemExit("cache inventory must not compute F_overlap")
    if policy["current_path_mapping_computed"] != "false":
        raise SystemExit("cache inventory must not compute path mapping")

    committed_subset_dir = ROOT / policy["committed_subset_dir"]
    local_cache_dir = ROOT / policy["local_full_route_cache_dir"]
    with FULL_MASK_MANIFEST.open(newline="") as f:
        manifest_rows = list(csv.DictReader(f))
    if len(manifest_rows) != 196:
        raise SystemExit("full route cache inventory expects 196 mask products")

    rows: list[dict[str, str]] = []
    for row in manifest_rows:
        filename = row["mask_product_url"].rsplit("/", 1)[-1]
        local_cache_path = local_cache_dir / filename
        committed_subset_path = committed_subset_dir / filename
        if local_cache_path.exists():
            present_path = local_cache_path
            source = "local_full_route_cache_v1"
        elif committed_subset_path.exists():
            present_path = committed_subset_path
            source = "committed_subset_v1"
        else:
            present_path = None
            source = "missing"
        present = present_path is not None
        byte_size = present_path.stat().st_size if present else 0
        rows.append(
            {
                "policy_id": policy["policy_id"],
                "tile_index_zero_based": row["tile_index_zero_based"],
                "mask_product_url": row["mask_product_url"],
                "filename": filename,
                "cache_source": source,
                "expected_local_full_route_cache_path": str(local_cache_path.relative_to(ROOT)),
                "committed_subset_path": str(committed_subset_path.relative_to(ROOT)),
                "local_or_committed_mask_present": bool_text(present),
                "byte_size": str(byte_size),
                "sha256": sha256_file(present_path) if present else "",
                "nonzero_file": bool_text(byte_size > 0),
                "accepted_for_source_cache_inventory": bool_text(present and byte_size > 0),
                "overlap_rule_computed": "false",
                "numeric_factor_computed": "false",
                "path_mapping_computed": "false",
                "contains_mapping_vector": "false",
                "contains_theory_vector": "false",
                "contains_predictions": "false",
                "contains_residuals": "false",
                "contains_fit_statistics": "false",
                "uses_kids_data_vector_values": "false",
                "uses_posterior_chains": "false",
                "uses_posthoc_tile_selection": "false",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": policy["claim_boundary"],
            }
        )

    present_rows = [row for row in rows if row["local_or_committed_mask_present"] == "true"]
    full_cache_rows = [row for row in rows if row["cache_source"] == "local_full_route_cache_v1"]
    subset_rows = [row for row in rows if row["cache_source"] == "committed_subset_v1"]
    missing_rows = [row for row in rows if row["cache_source"] == "missing"]
    nonzero_rows = [row for row in present_rows if row["nonzero_file"] == "true"]
    total_bytes = sum(int(row["byte_size"]) for row in present_rows)
    source_cache_complete = len(present_rows) == len(rows) and len(nonzero_rows) == len(rows)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "policy_id": policy["policy_id"],
        "status": "KIDS1000_COSEBIS_F_OVERLAP_FULL_ROUTE_CACHE_INVENTORY_BUILT_LOCAL_ONLY_NOT_SCORED",
        "expected_mask_count": str(len(rows)),
        "present_mask_count": str(len(present_rows)),
        "missing_mask_count": str(len(missing_rows)),
        "nonzero_file_count": str(len(nonzero_rows)),
        "local_full_route_cache_count": str(len(full_cache_rows)),
        "committed_subset_count": str(len(subset_rows)),
        "total_present_bytes": str(total_bytes),
        "source_cache_complete": bool_text(source_cache_complete),
        "local_cache_required_for_public_reproduce": policy["local_cache_required_for_public_reproduce"],
        "public_reproduce_uses_committed_inventory_only": "true",
        "overlap_rule_ready": "false",
        "overlap_rule_computed": "false",
        "numeric_factors_computed": "false",
        "path_mapping_computed": "false",
        "contains_mapping_vector": "false",
        "contains_theory_vector": "false",
        "contains_predictions": "false",
        "contains_residuals": "false",
        "contains_fit_statistics": "false",
        "uses_kids_data_vector_values": "false",
        "uses_posterior_chains": "false",
        "uses_posthoc_tile_selection": "false",
        "endpoint_scoring_allowed": "false",
        "claim_boundary": policy["claim_boundary"],
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_F_OVERLAP_FULL_ROUTE_CACHE_INVENTORY_V1_BUILT "
        f"present={summary['present_mask_count']} missing={summary['missing_mask_count']} "
        "endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()
