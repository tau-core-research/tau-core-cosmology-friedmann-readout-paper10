#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_shape_row2_moresco2012_source_attachment_review_policy_v1.csv"
ATTACHMENT = ROOT / "data/derived/paper10_desi_shape_row2_moresco2012_source_attachment_v1.csv"
ATTACHMENT_SUMMARY = ROOT / "data/derived/paper10_desi_shape_row2_moresco2012_source_attachment_v1_summary.csv"
ATTACHMENT_DOC = ROOT / "docs/paper10_desi_shape_row2_moresco2012_source_attachment_v1.md"
SUPPORT_SCAN = ROOT / "data/derived/paper10_desi_shape_core_source_support_scan_v1.csv"
SUPPORT_SUMMARY = ROOT / "data/derived/paper10_desi_shape_core_source_support_scan_v1_summary.csv"
REVIEW_DOC = ROOT / "docs/paper10_desi_shape_row2_moresco2012_source_attachment_review_v1.md"
REFS = ROOT / "paper10_submission_source/refs.bib"
TEMPLATE = ROOT / "data/derived/paper10_desi_shape_row2_moresco2012_source_attachment_review_response_template_v1.csv"
PACKAGE = ROOT / "data/derived/paper10_desi_shape_row2_moresco2012_source_attachment_review_package_v1.zip"
SHA = ROOT / "data/derived/paper10_desi_shape_row2_moresco2012_source_attachment_review_package_v1.zip.sha256"
MANIFEST = ROOT / "data/derived/paper10_desi_shape_row2_moresco2012_source_attachment_review_package_v1_manifest.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_shape_row2_moresco2012_source_attachment_review_package_v1_summary.csv"
PACKAGE_ID = "PAPER10_DESI_SHAPE_ROW2_MORESCO2012_SOURCE_ATTACHMENT_REVIEW_PACKAGE_V1"
CLAIM_BOUNDARY = "paper10_desi_shape_row2_moresco2012_source_attachment_review_not_validation"

PACKAGE_FILES = [
    POLICY,
    REVIEW_DOC,
    TEMPLATE,
    ATTACHMENT,
    ATTACHMENT_SUMMARY,
    ATTACHMENT_DOC,
    SUPPORT_SCAN,
    SUPPORT_SUMMARY,
    REFS,
]


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required input: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def manifest_row(path: Path) -> dict[str, str]:
    if not path.exists():
        raise SystemExit(f"missing review package member: {path.relative_to(ROOT)}")
    return {
        "package_id": PACKAGE_ID,
        "package_path": path.relative_to(ROOT).as_posix(),
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
    policy_rows = read_rows(POLICY)
    if len(policy_rows) != 4:
        raise SystemExit("row2 attachment review policy must contain four questions")
    if {row["claim_boundary"] for row in policy_rows} != {CLAIM_BOUNDARY}:
        raise SystemExit("bad row2 attachment review policy claim boundary")
    if any(row["endpoint_replay_allowed"] != "false" for row in policy_rows):
        raise SystemExit("policy must not authorize replay")

    attachment = read_one(ATTACHMENT)
    attachment_summary = read_one(ATTACHMENT_SUMMARY)
    support_summary = read_one(SUPPORT_SUMMARY)
    if attachment["source_key"] != "Moresco2012ExpansionRate":
        raise SystemExit("review package expects Moresco2012 attachment")
    if attachment["row2_endpoint_ready"] != "false":
        raise SystemExit("row2 must not be endpoint-ready before review")
    if attachment["endpoint_pair_replacement"] != "false":
        raise SystemExit("attachment must not be endpoint-pair replacement")
    if attachment_summary["verdict"] != "row2_moresco2012_in_interval_support_attached_partial_not_endpoint_ready":
        raise SystemExit("bad attachment summary verdict")
    if support_summary["row2_moresco2012_support_found"] != "true":
        raise SystemExit("support scan must find row2 Moresco2012 support")

    template_rows = []
    for row in policy_rows:
        template_rows.append(
            {
                "policy_id": row["policy_id"],
                "question_id": row["question_id"],
                "question_text": row["question_text"],
                "required_response": row["required_response"],
                "acceptance_condition": row["acceptance_condition"],
                "review_completed": "false",
                "reviewer_id_or_role": "",
                "reviewer_response": "",
                "reviewer_rationale": "",
                "forbidden_inputs_used": "false",
                "attached_source_key": attachment["source_key"],
                "attached_source_reference": attachment["source_reference"],
                "attached_z": attachment["z"],
                "endpoint_pair_replacement": attachment["endpoint_pair_replacement"],
                "row2_source_caveat_reduced": attachment["row2_source_caveat_reduced"],
                "row2_endpoint_ready": attachment["row2_endpoint_ready"],
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(TEMPLATE, template_rows)

    rows = [manifest_row(path) for path in PACKAGE_FILES]
    write_csv(MANIFEST, rows)
    package_rows = rows + [manifest_row(MANIFEST)]
    with zipfile.ZipFile(PACKAGE, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for row in package_rows:
            path = ROOT / row["package_path"]
            info = zipfile.ZipInfo(row["package_path"])
            info.date_time = (2026, 1, 1, 0, 0, 0)
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, path.read_bytes())
    digest = sha256(PACKAGE)
    SHA.write_text(f"{digest}  {PACKAGE.name}\n")
    write_csv(
        SUMMARY,
        [
            {
                "package_id": PACKAGE_ID,
                "status": "DESI_SHAPE_ROW2_MORESCO2012_SOURCE_ATTACHMENT_REVIEW_PACKAGE_BUILT_NOT_COMPLETED",
                "zip_path": PACKAGE.relative_to(ROOT).as_posix(),
                "zip_sha256_path": SHA.relative_to(ROOT).as_posix(),
                "zip_sha256": digest,
                "package_file_count": str(len(package_rows)),
                "review_completed": "false",
                "attached_source_key": attachment["source_key"],
                "attached_source_reference": attachment["source_reference"],
                "attached_z": attachment["z"],
                "endpoint_pair_replacement": attachment["endpoint_pair_replacement"],
                "row2_source_caveat_reduced": attachment["row2_source_caveat_reduced"],
                "row2_endpoint_ready": attachment["row2_endpoint_ready"],
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "contains_endpoint_residuals": "false",
                "contains_endpoint_scores": "false",
                "contains_fit_statistics": "false",
                "claim_boundary": CLAIM_BOUNDARY,
                "verdict": "row2_moresco2012_source_attachment_review_package_ready_not_completed",
                "recommended_next_action": "send_zip_to_reviewer_and_validate_completed_source_side_response",
            }
        ],
    )
    print(f"paper10_desi_shape_row2_moresco2012_source_attachment_review_package_v1: built sha256={digest}")


if __name__ == "__main__":
    main()
