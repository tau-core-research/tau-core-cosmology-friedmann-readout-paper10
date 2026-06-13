#!/usr/bin/env python3
from __future__ import annotations

import csv
import tarfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARBALL = ROOT / "data" / "raw" / "weak_lensing" / "act_dr6_lensing" / "dr6_lensing_release.tar.gz"
OUT = ROOT / "data" / "derived" / "act_dr6_lensing_inventory_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "act_dr6_lensing_inventory_v1_summary.csv"
CLAIM_BOUNDARY = "act_dr6_lensing_inventory_source_side_not_endpoint_not_validation"

VARIANT_ROLE = {
    "baseline": "recommended_science_variant",
    "diff_f150_f090": "null_control_variant",
    "diff_f150_f090_tonly": "null_control_variant",
    "curl": "null_control_variant",
}


def product_type(name: str) -> str:
    base = Path(name).name
    if base.startswith("kappa_alm_data_"):
        return "kappa_alm_modes"
    if base.startswith("mask_"):
        return "healpix_mask"
    if base.startswith("kappa_filter_"):
        return "multipole_filter"
    if base.startswith("N_L_kk_"):
        return "noise_per_mode"
    if base == "README":
        return "release_readme"
    return "other"


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    if not TARBALL.exists():
        raise SystemExit("ACT DR6 lensing tarball is missing")
    rows: list[dict[str, str]] = []
    with tarfile.open(TARBALL, "r:gz") as tf:
        for member in tf.getmembers():
            if not member.isfile():
                continue
            name = member.name.lstrip("./")
            parts = Path(name).parts
            variant = ""
            if len(parts) >= 3 and parts[0] == "maps":
                variant = parts[1]
            ptype = product_type(name)
            rows.append(
                {
                    "artifact_id": "ACT_DR6_LENSING_INVENTORY_V1",
                    "tar_member": name,
                    "variant": variant,
                    "product_type": ptype,
                    "byte_count": str(member.size),
                    "variant_role": VARIANT_ROLE.get(variant, "diagnostic_or_alternative_variant" if variant else "metadata"),
                    "endpoint_replay_allowed": "false",
                    "endpoint_validation_claimed": "false",
                    "physical_lensing_path_weight_claimed": "false",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    write_csv(OUT, rows)
    variants = sorted({row["variant"] for row in rows if row["variant"]})
    summary = {
        "artifact_id": "ACT_DR6_LENSING_INVENTORY_V1",
        "status": "SOURCE_INVENTORY_BUILT_NOT_ENDPOINT",
        "rows": str(len(rows)),
        "variant_count": str(len(variants)),
        "variants": ";".join(variants),
        "kappa_alm_products": str(sum(row["product_type"] == "kappa_alm_modes" for row in rows)),
        "mask_products": str(sum(row["product_type"] == "healpix_mask" for row in rows)),
        "noise_products": str(sum(row["product_type"] == "noise_per_mode" for row in rows)),
        "filter_products": str(sum(row["product_type"] == "multipole_filter" for row in rows)),
        "recommended_science_variant_available": str(any(row["variant"] == "baseline" for row in rows)).lower(),
        "null_control_variants_available": str(
            all(variant in variants for variant in ("diff_f150_f090", "diff_f150_f090_tonly", "curl"))
        ).lower(),
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_lensing_path_weight_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
        "verdict": "act_dr6_inventory_ready_for_source_side_sampling_gate_not_endpoint",
    }
    write_csv(SUMMARY, [summary])
    print(
        "ACT_DR6_LENSING_INVENTORY_V1_BUILT "
        f"rows={summary['rows']} variants={summary['variant_count']} endpoint=false"
    )


if __name__ == "__main__":
    main()
