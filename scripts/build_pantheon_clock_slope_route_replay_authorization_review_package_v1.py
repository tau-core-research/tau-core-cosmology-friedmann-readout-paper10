#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_SUMMARY = ROOT / "data/derived/pantheon_clock_slope_route_replay_authorization_review_template_v1_summary.csv"
OUT_ZIP = ROOT / "data/derived/pantheon_clock_slope_route_replay_authorization_review_package_v1.zip"
OUT_ZIP_SHA256 = ROOT / "data/derived/pantheon_clock_slope_route_replay_authorization_review_package_v1.zip.sha256"
MANIFEST = ROOT / "data/derived/pantheon_clock_slope_route_replay_authorization_review_package_v1_manifest.csv"
SUMMARY = ROOT / "data/derived/pantheon_clock_slope_route_replay_authorization_review_package_v1_summary.csv"
PACKAGE_ID = "PANTHEON_CLOCK_SLOPE_ROUTE_REPLAY_AUTHORIZATION_REVIEW_PACKAGE_V1"
CLAIM_BOUNDARY = "clock_slope_route_replay_authorization_review_not_validation"

PACKAGE_FILES = [
    "docs/pantheon_clock_slope_route_replay_authorization_review_v1.md",
    "data/source_manifest/pantheon_clock_slope_route_replay_authorization_review_policy_v1.csv",
    "data/derived/pantheon_clock_slope_route_replay_authorization_review_response_template_v1.csv",
    "data/derived/pantheon_clock_slope_route_replay_authorization_review_template_v1_summary.csv",
    "docs/pantheon_clock_slope_route_gate_v1.md",
    "data/source_manifest/pantheon_clock_slope_route_gate_policy_v1.csv",
    "data/derived/pantheon_clock_slope_route_gate_v1.csv",
    "docs/pantheon_time_readout_clock_rate_phase_cc_support_candidate_v1.md",
    "data/source_manifest/pantheon_time_readout_clock_rate_phase_cc_support_candidate_policy_v1.csv",
    "data/derived/pantheon_time_readout_clock_rate_phase_cc_support_candidate_v1_summary.csv",
    "docs/pantheon_clock_rate_phase_cc_support_fast_screen_v1.md",
    "data/source_manifest/pantheon_clock_rate_phase_cc_support_fast_screen_v1.csv",
    "data/derived/pantheon_clock_rate_phase_cc_support_fast_screen_v1_summary.csv",
    "data/derived/pantheon_clock_rate_phase_cc_support_fast_screen_v1_family_summary.csv",
    "scripts/validate_pantheon_clock_slope_route_replay_authorization_review_template_v1.py",
]


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain one row")
    return rows[0]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def manifest_row(rel: str) -> dict[str, str]:
    path = ROOT / rel
    if not path.exists():
        raise SystemExit(f"missing clock_slope authorization package file: {rel}")
    return {
        "package_id": PACKAGE_ID,
        "package_path": rel,
        "byte_count": str(path.stat().st_size),
        "sha256": sha256(path),
        "contains_endpoint_residuals": "false",
        "contains_endpoint_scores": "false",
        "contains_fit_statistics": "false",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def main() -> None:
    template_summary = read_one(TEMPLATE_SUMMARY)
    if template_summary["status"] != "CLOCK_SLOPE_ROUTE_REPLAY_AUTHORIZATION_TEMPLATE_READY_NOT_COMPLETED":
        raise SystemExit("authorization package requires a blank clock_slope template")
    if template_summary["endpoint_replay_allowed"] != "false":
        raise SystemExit("authorization package must not pre-authorize replay")
    if template_summary["endpoint_validation_claimed"] != "false":
        raise SystemExit("authorization package must not claim validation")
    if template_summary["physical_validation_claimed"] != "false":
        raise SystemExit("authorization package must not claim physical validation")

    rows = [manifest_row(rel) for rel in PACKAGE_FILES]
    write_csv(MANIFEST, rows)
    package_rows = rows + [manifest_row(str(MANIFEST.relative_to(ROOT)))]
    OUT_ZIP.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(OUT_ZIP, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for row in package_rows:
            path = ROOT / row["package_path"]
            info = zipfile.ZipInfo(row["package_path"])
            info.date_time = (2026, 1, 1, 0, 0, 0)
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, path.read_bytes())
    zip_sha256 = sha256(OUT_ZIP)
    OUT_ZIP_SHA256.write_text(f"{zip_sha256}  {OUT_ZIP.name}\n")
    summary = [
        {
            "package_id": PACKAGE_ID,
            "status": "CLOCK_SLOPE_ROUTE_REPLAY_AUTHORIZATION_PACKAGE_BUILT_NOT_COMPLETED",
            "zip_path": str(OUT_ZIP.relative_to(ROOT)),
            "zip_sha256_path": str(OUT_ZIP_SHA256.relative_to(ROOT)),
            "zip_sha256": zip_sha256,
            "package_file_count": str(len(package_rows)),
            "review_completed": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "contains_endpoint_residuals": "false",
            "contains_endpoint_scores": "false",
            "contains_fit_statistics": "false",
            "physical_validation_claimed": "false",
            "verdict": "clock_slope_route_replay_authorization_package_ready_not_completed",
            "recommended_next_action": "send_zip_to_reviewer_and_validate_completed_authorization_response",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_CLOCK_SLOPE_ROUTE_REPLAY_AUTHORIZATION_PACKAGE_BUILT "
        f"verdict={summary[0]['verdict']}"
    )


if __name__ == "__main__":
    main()
