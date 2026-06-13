#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "weak_lensing" / "act_dr6_lensing"
TARBALL = RAW / "dr6_lensing_release.tar.gz"
OUT = ROOT / "data" / "source_manifest" / "act_dr6_lensing_product_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "act_dr6_lensing_product_v1_summary.csv"
DOC = ROOT / "docs" / "act_dr6_lensing_product_v1.md"
URL = "https://lambda.gsfc.nasa.gov/data/suborbital/ACT/ACT_dr6/dr6_lensing_release.tar.gz"
INFO_URL = "https://lambda.gsfc.nasa.gov/product/act/actadv_dr6_lensing_maps_info.html"
GET_URL = "https://lambda.gsfc.nasa.gov/product/act/actadv_dr6_lensing_maps_get.html"
EXPECTED_BYTES = 1371472486
CLAIM_BOUNDARY = "act_dr6_lensing_source_product_acquisition_not_endpoint_not_validation"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def head_metadata() -> dict[str, str]:
    req = Request(URL, method="HEAD", headers={"User-Agent": "tau-core-paper10-act-dr6-lensing-freeze/0.1"})
    with urlopen(req, timeout=120) as response:
        return {
            "status_code": str(getattr(response, "status", 200)),
            "content_length": response.headers.get("Content-Length", ""),
            "content_type": response.headers.get("Content-Type", ""),
            "last_modified": response.headers.get("Last-Modified", ""),
            "etag": response.headers.get("ETag", ""),
        }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    meta = head_metadata()
    exists = TARBALL.exists()
    byte_count = TARBALL.stat().st_size if exists else 0
    complete = exists and byte_count == EXPECTED_BYTES
    acquired_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    checksum = sha256_file(TARBALL) if complete else ""
    row = {
        "artifact_id": "ACT_DR6_LENSING_PRODUCT_V1",
        "provider": "NASA_LAMBDA_ACT_DR6",
        "product_name": "ACT_DR6_LENSING_RELEASE_TARBALL",
        "info_url": INFO_URL,
        "download_page_url": GET_URL,
        "product_url": URL,
        "local_path": str(TARBALL.relative_to(ROOT)),
        "head_status_code": meta["status_code"],
        "head_content_length": meta["content_length"],
        "head_content_type": meta["content_type"],
        "head_last_modified": meta["last_modified"],
        "head_etag": meta["etag"],
        "expected_byte_count": str(EXPECTED_BYTES),
        "local_file_exists": str(exists).lower(),
        "local_byte_count": str(byte_count),
        "download_complete": str(complete).lower(),
        "sha256": checksum,
        "acquired_or_checked_at_utc": acquired_at,
        "coordinate_frame_note": "ACT_DR6_lensing_maps_documented_as_equatorial_coordinates",
        "source_product_type": "cmb_lensing_convergence_alm_masks_filters_noise_release",
        "metric_lensing_numeric_product_available_for_source": str(complete).lower(),
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "contains_endpoint_scores": "false",
        "contains_distance_residuals": "false",
        "contains_fit_statistics": "false",
        "physical_lensing_path_weight_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(OUT, [row])
    summary = {
        "artifact_id": "ACT_DR6_LENSING_PRODUCT_V1",
        "status": "SOURCE_PRODUCT_COMPLETE" if complete else "SOURCE_PRODUCT_INCOMPLETE_OR_MISSING",
        "download_complete": str(complete).lower(),
        "expected_byte_count": str(EXPECTED_BYTES),
        "local_byte_count": str(byte_count),
        "metric_lensing_numeric_product_available_for_source": str(complete).lower(),
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_lensing_path_weight_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
        "verdict": "act_dr6_lensing_product_acquired_source_side_not_endpoint" if complete else "act_dr6_lensing_product_not_yet_complete",
    }
    write_csv(SUMMARY, [summary])
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# ACT DR6 lensing product acquisition v1",
                "",
                "**Doc class:** source product acquisition manifest",
                "**Status:** source-side only; not endpoint replay; not validation",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`",
                "",
                "This manifest freezes the public NASA LAMBDA ACT DR6 lensing release route.",
                "The LAMBDA product page describes ACT DR6 gravitational-lensing convergence maps in Equatorial coordinates, with maps, masks, filters, and noise products.",
                "",
                f"- info page: `{INFO_URL}`",
                f"- download page: `{GET_URL}`",
                f"- tarball URL: `{URL}`",
                f"- expected bytes: `{EXPECTED_BYTES}`",
                f"- local bytes: `{byte_count}`",
                f"- complete: `{str(complete).lower()}`",
                f"- verdict: `{summary['verdict']}`",
                "",
                "The artifact does not compute kappa/shear values at Pantheon rows, does not build a path integral, and does not authorize endpoint replay.",
                "",
            ]
        )
    )
    print(f"ACT_DR6_LENSING_PRODUCT_V1 status={summary['status']} bytes={byte_count} complete={complete}")


if __name__ == "__main__":
    main()
