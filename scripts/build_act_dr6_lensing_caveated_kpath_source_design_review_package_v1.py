#!/usr/bin/env python3
"""Build a standalone review package for the caveated ACT K_path design."""

from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data" / "derived"
SOURCE = ROOT / "data" / "source_manifest"
PACKAGE = DERIVED / "act_dr6_lensing_caveated_kpath_source_design_review_package_v1.zip"
MANIFEST = DERIVED / "act_dr6_lensing_caveated_kpath_source_design_review_package_v1_manifest.csv"
SUMMARY = DERIVED / "act_dr6_lensing_caveated_kpath_source_design_review_package_v1_summary.csv"
TEMPLATE = DERIVED / "act_dr6_lensing_caveated_kpath_source_design_review_response_template_v1.csv"


FILES = [
    SOURCE / "act_dr6_lensing_caveated_kpath_source_design_v1.csv",
    DERIVED / "act_dr6_lensing_caveated_kpath_source_design_v1_summary.csv",
    SOURCE / "act_dr6_lensing_next_source_basis_design_scaffold_v1.csv",
    DERIVED / "act_dr6_lensing_next_source_basis_design_scaffold_v1_summary.csv",
    DERIVED / "act_dr6_lensing_reopen_closure_ledger_v1.csv",
    DERIVED / "act_dr6_lensing_reopen_closure_ledger_v1_summary.csv",
    DERIVED / "act_dr6_lensing_path_weight_candidate_v1_summary.csv",
    DERIVED / "act_dr6_lensing_path_weight_authorized_replay_v1_summary.csv",
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in FILES if not path.exists()]
    if missing:
        raise SystemExit(f"missing package inputs: {missing}")

    instructions = DERIVED / "act_dr6_lensing_caveated_kpath_source_design_review_instructions_v1.md"
    instructions.write_text(
        "\n".join(
            [
                "# ACT DR6 caveated K_path source-design review package v1",
                "",
                "The reviewer does not need repository access.",
                "",
                "Review task:",
                "",
                "1. Check whether the ACT baseline kappa source object may be carried only as a",
                "   caveated, dimensionless K_path shape proxy.",
                "2. Check that curl and frequency-difference products remain K_null controls.",
                "3. Check that the partial ACT mask coverage is explicitly reported.",
                "4. Check that no endpoint scores, distance residuals, fit statistics, fitted",
                "   amplitudes, or post-hoc branch choices are used to define the source design.",
                "5. Decide whether this package is acceptable as a source-side design for a",
                "   future permission-only replay review.",
                "",
                "Allowed verdicts:",
                "",
                "- ACCEPT_CAVEATED_KPATH_SOURCE_DESIGN_FOR_REVIEW_ONLY",
                "- ACCEPT_AS_DIAGNOSTIC_ONLY_NO_REPLAY",
                "- REJECT_SOURCE_DESIGN_LEAKAGE_OR_UNSUPPORTED_MAPPING",
                "",
                "Important boundary: this review cannot authorize validation, physical K_path",
                "promotion, dark-sector inference, or endpoint replay by itself.",
                "",
            ]
        )
    )

    response_rows = [
        {
            "review_item": "source_product_status",
            "question": "Is the ACT baseline kappa source product acceptable as a caveated path-proxy source object?",
            "response": "",
            "notes": "",
        },
        {
            "review_item": "proxy_mapping_status",
            "question": "Is the median/MAD shape mapping acceptable only as dimensionless proxy shape, not physical amplitude?",
            "response": "",
            "notes": "",
        },
        {
            "review_item": "null_control_status",
            "question": "Are curl and frequency-difference products retained as K_null controls?",
            "response": "",
            "notes": "",
        },
        {
            "review_item": "leakage_status",
            "question": "Were endpoint scores, residuals, fit statistics, fitted amplitudes, or winner labels used?",
            "response": "",
            "notes": "",
        },
        {
            "review_item": "overall_verdict",
            "question": "Choose one allowed verdict from the instruction file.",
            "response": "",
            "notes": "",
        },
    ]
    write_csv(TEMPLATE, response_rows)

    package_files = FILES + [instructions, TEMPLATE]
    with zipfile.ZipFile(PACKAGE, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in package_files:
            arcname = path.relative_to(ROOT).as_posix()
            info = zipfile.ZipInfo(arcname)
            info.date_time = (2026, 1, 1, 0, 0, 0)
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, path.read_bytes())

    manifest_rows = [
        {
            "package_id": "ACT_DR6_LENSING_CAVEATED_KPATH_SOURCE_DESIGN_REVIEW_PACKAGE_V1",
            "path": path.relative_to(ROOT).as_posix(),
            "sha256": sha256(path),
            "bytes": str(path.stat().st_size),
        }
        for path in package_files
    ]
    write_csv(MANIFEST, manifest_rows)
    (PACKAGE.with_suffix(PACKAGE.suffix + ".sha256")).write_text(sha256(PACKAGE) + "\n")
    write_csv(
        SUMMARY,
        [
            {
                "package_id": "ACT_DR6_LENSING_CAVEATED_KPATH_SOURCE_DESIGN_REVIEW_PACKAGE_V1",
                "zip_path": PACKAGE.relative_to(ROOT).as_posix(),
                "file_count": str(len(package_files)),
                "response_template": TEMPLATE.relative_to(ROOT).as_posix(),
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "physical_lensing_path_weight_claimed": "false",
                "claim_boundary": "review_package_for_source_design_only_not_replay_authorization",
                "verdict": "ACT_CAVEATED_KPATH_SOURCE_DESIGN_REVIEW_PACKAGE_READY",
            }
        ],
    )


if __name__ == "__main__":
    main()
