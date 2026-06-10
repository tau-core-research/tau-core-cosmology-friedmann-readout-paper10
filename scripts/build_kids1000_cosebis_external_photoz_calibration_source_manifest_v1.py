#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_external_photoz_calibration_source_manifest_policy_v1.csv"
ACQUISITION = ROOT / "data" / "derived" / "kids1000_cosebis_external_photoz_calibration_acquisition_plan_v1_summary.csv"
EVIDENCE = ROOT / "data" / "derived" / "kids1000_cosebis_photoz_tomographic_calibration_evidence_v1_summary.csv"
CACHE_DIR = ROOT / "data" / "source_manifest" / "source_page_cache" / "kids1000_photoz_calibration_v1"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_external_photoz_calibration_source_manifest_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_external_photoz_calibration_source_manifest_v1_summary.csv"


SOURCES = [
    {
        "source_id": "KIDS1000_PHOTOZ_CALIBRATION_AANDA",
        "route_ids": "R1_photoz_calibration_reference_manifest;R2_som_gold_or_nz_validation_manifest;R3_tomographic_bin_quality_manifest",
        "official_url": "https://www.aanda.org/articles/aa/full_html/2021/03/aa39018-20/aa39018-20.html",
        "cache_file": "KIDS1000_PHOTOZ_CALIBRATION_AANDA.html",
        "required_markers": [
            "KiDS-1000 catalogue: Redshift distributions and their calibration",
            "self-organising map",
            "five tomographic redshift bins",
            "gold",
            "Residual biases in the mean redshifts",
            "clustering redshift",
            "Table 3",
        ],
        "source_role": "published_photoz_redshift_distribution_calibration_and_tomographic_bin_quality_reference",
    },
    {
        "source_id": "KIDS1000_PHOTOZ_CALIBRATION_ARXIV",
        "route_ids": "R1_photoz_calibration_reference_manifest",
        "official_url": "https://arxiv.org/abs/2007.15635",
        "cache_file": "KIDS1000_PHOTOZ_CALIBRATION_ARXIV.html",
        "required_markers": [
            "KiDS-1000 catalogue: Redshift distributions and their calibration",
            "citation_doi",
            "citation_arxiv_id",
            "self-organising map",
            "five tomographic redshift bins",
        ],
        "source_role": "arxiv_metadata_mirror_for_photoz_calibration_reference",
    },
    {
        "source_id": "KIDS1000_SOM_GOLD_CATALOGUE",
        "route_ids": "R2_som_gold_or_nz_validation_manifest",
        "official_url": "https://kids.strw.leidenuniv.nl/DR4/KiDS-1000_shearcatalogue.php",
        "cache_file": "KIDS1000_SOM_GOLD_CATALOGUE.html",
        "required_markers": [
            "Weak lensing SOM-gold catalogue",
            "gold sample",
            "redshift measurements",
            "download an n(z) tarball",
            "5 tomographic",
            "Hildebrandt",
        ],
        "source_role": "official_kids_som_gold_catalogue_and_nz_product_route",
    },
]


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    policy = read_one(POLICY)
    acquisition = read_one(ACQUISITION)
    evidence = read_one(EVIDENCE)

    if policy["status"] != "EXTERNAL_PHOTOZ_CALIBRATION_SOURCE_MANIFEST_POLICY_FROZEN_PENDING_REVIEW":
        raise SystemExit("unexpected source-manifest policy status")
    if acquisition["verdict"] != "external_photoz_calibration_acquisition_plan_frozen_h1_still_open":
        raise SystemExit("expected acquisition plan to remain open")
    if evidence["h1_independent_evidence_complete"] != "false":
        raise SystemExit("source manifest expects H1 to remain incomplete before review")
    if policy["current_endpoint_replay_allowed"] != "false":
        raise SystemExit("source manifest must not authorize endpoint replay")

    rows = []
    for source in SOURCES:
        path = CACHE_DIR / source["cache_file"]
        if not path.exists():
            raise SystemExit(f"missing cached source file: {path}")
        text = path.read_text(errors="ignore")
        marker_status = {marker: (marker in text) for marker in source["required_markers"]}
        if not all(marker_status.values()):
            missing = [marker for marker, present in marker_status.items() if not present]
            raise SystemExit(f"{source['source_id']} missing markers: {missing}")
        rows.append(
            {
                "policy_id": policy["policy_id"],
                "source_id": source["source_id"],
                "route_ids": source["route_ids"],
                "official_url": source["official_url"],
                "cache_path": str(path.relative_to(ROOT)),
                "byte_count": str(path.stat().st_size),
                "sha256": sha256(path),
                "marker_count": str(len(source["required_markers"])),
                "all_required_markers_present": "true",
                "marker_summary": ";".join(marker.replace(";", ",") for marker in source["required_markers"]),
                "source_role": source["source_role"],
                "source_status": "CACHED_SOURCE_ATTACHED_PENDING_LEAKAGE_REVIEW",
                "forbidden_inputs_used": "false",
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "claim_boundary": policy["claim_boundary"],
            }
        )

    covered_routes = sorted({route for row in rows for route in row["route_ids"].split(";")})
    summary = [
        {
            "policy_id": policy["policy_id"],
            "status": "EXTERNAL_PHOTOZ_CALIBRATION_SOURCE_MANIFEST_BUILT_PENDING_REVIEW",
            "cached_source_count": str(len(rows)),
            "covered_routes": ";".join(covered_routes),
            "r1_to_r3_source_artifacts_attached": "true",
            "r4_leakage_review_complete": "false",
            "h1_independent_evidence_complete": "false",
            "computes_new_scores": "false",
            "uses_kids_data_vector_values_for_scoring": "false",
            "uses_kids_data_vector_values_for_source_selection": "false",
            "uses_residuals": "false",
            "uses_fit_statistics": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "verdict": "external_photoz_calibration_sources_attached_pending_leakage_review",
            "recommended_next_action": "complete_R4_leakage_review_before_marking_H1_complete_or_replaying_endpoint",
            "claim_boundary": policy["claim_boundary"],
        }
    ]
    write_csv(OUT, rows)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_EXTERNAL_PHOTOZ_CALIBRATION_SOURCE_MANIFEST_V1_BUILT "
        f"verdict={summary[0]['verdict']}"
    )


if __name__ == "__main__":
    main()
