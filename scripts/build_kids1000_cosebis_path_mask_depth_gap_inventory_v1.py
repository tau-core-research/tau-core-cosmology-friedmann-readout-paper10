#!/usr/bin/env python3
from __future__ import annotations

import csv
import tarfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_path_mask_depth_gap_policy_v1.csv"
PRODUCTS = ROOT / "data" / "source_manifest" / "kids1000_lensing_products_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_path_mask_depth_gap_inventory_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_path_mask_depth_gap_inventory_v1_summary.csv"


KEYWORDS = ("mask", "depth", "footprint", "random", "healpix", "mangle")


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def classify_member(name: str) -> tuple[str, str]:
    lower = name.lower()
    if "data_fits/" in lower and lower.endswith(".fits"):
        return "not_path_product", "statistic_fits_filename_token_not_survey_path_map"
    if "chains_and_config_files/" in lower:
        return "not_path_product", "chain_or_config_product_not_survey_path_map"
    if lower.endswith("read.me"):
        return "documentation", "release_readme"
    if any(token in lower for token in KEYWORDS):
        return "candidate_requires_external_review", "keyword_match_not_accepted_as_path_map"
    return "not_path_product", "no_path_keyword"


def main() -> None:
    policy = read_one(POLICY)
    product = read_one(PRODUCTS)
    if policy["endpoint_scoring_allowed"].lower() != "false":
        raise SystemExit("path mask/depth gap policy must remain endpoint disabled")
    if policy["current_path_mapping_computed"].lower() != "false":
        raise SystemExit("path mapping must not be computed in the gap audit")
    if product["endpoint_allowed"].lower() != "false":
        raise SystemExit("KiDS source product must remain endpoint disabled")

    rows: list[dict[str, str]] = []
    with tarfile.open(ROOT / product["local_path"], "r:gz") as tf:
        for member in tf.getmembers():
            name = member.name
            lower = name.lower()
            if any(token in lower for token in KEYWORDS) or lower.endswith("read.me"):
                role, reason = classify_member(name)
                rows.append(
                    {
                        "policy_id": policy["policy_id"],
                        "parent_policy": policy["parent_policy"],
                        "member_name": name,
                        "member_size_bytes": str(member.size),
                        "keyword_hits": ";".join(token for token in KEYWORDS if token in lower),
                        "path_product_role": role,
                        "classification_reason": reason,
                        "accepted_as_path_mask_depth_product": "false",
                        "current_path_mapping_computed": "false",
                        "contains_mapping_vector": "false",
                        "contains_theory_vector": "false",
                        "contains_predictions": "false",
                        "contains_residuals": "false",
                        "contains_fit_statistics": "false",
                        "uses_kids_data_vector_values": "false",
                        "uses_posterior_chains": "false",
                        "uses_posthoc_path_selection": "false",
                        "endpoint_scoring_allowed": "false",
                        "claim_boundary": "kids1000_cosebis_path_mask_depth_gap_not_validation",
                    }
                )

    if not rows:
        rows.append(
            {
                "policy_id": policy["policy_id"],
                "parent_policy": policy["parent_policy"],
                "member_name": "NO_KEYWORD_MATCHING_MEMBER",
                "member_size_bytes": "0",
                "keyword_hits": "",
                "path_product_role": "not_available",
                "classification_reason": "no_mask_depth_footprint_random_healpix_or_mangle_member_found",
                "accepted_as_path_mask_depth_product": "false",
                "current_path_mapping_computed": "false",
                "contains_mapping_vector": "false",
                "contains_theory_vector": "false",
                "contains_predictions": "false",
                "contains_residuals": "false",
                "contains_fit_statistics": "false",
                "uses_kids_data_vector_values": "false",
                "uses_posterior_chains": "false",
                "uses_posthoc_path_selection": "false",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "kids1000_cosebis_path_mask_depth_gap_not_validation",
            }
        )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    accepted_count = sum(row["accepted_as_path_mask_depth_product"] == "true" for row in rows)
    summary = {
        "policy_id": policy["policy_id"],
        "status": "KIDS1000_COSEBIS_PATH_MASK_DEPTH_GAP_BUILT_EXTERNAL_PRODUCT_REQUIRED",
        "searched_product": product["local_path"],
        "candidate_rows": str(len(rows)),
        "accepted_path_mask_depth_products": str(accepted_count),
        "path_mask_depth_product_available": "true" if accepted_count else "false",
        "current_path_mapping_computed": "false",
        "contains_mapping_vector": "false",
        "contains_theory_vector": "false",
        "contains_predictions": "false",
        "contains_residuals": "false",
        "contains_fit_statistics": "false",
        "uses_kids_data_vector_values": "false",
        "uses_posterior_chains": "false",
        "uses_posthoc_path_selection": "false",
        "endpoint_scoring_allowed": "false",
        "blocker": "external_source_frozen_lensing_path_mask_or_depth_map_required",
        "claim_boundary": "kids1000_cosebis_path_mask_depth_gap_not_validation",
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_PATH_MASK_DEPTH_GAP_V1_BUILT "
        f"accepted_path_products={accepted_count} endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()
