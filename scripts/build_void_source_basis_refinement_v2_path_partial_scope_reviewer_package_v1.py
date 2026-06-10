#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = (
    ROOT
    / "data"
    / "source_manifest"
    / "void_source_basis_refinement_v2_path_partial_scope_reviewer_package_policy_v1.csv"
)
VALUES_SUMMARY = (
    ROOT
    / "data"
    / "derived"
    / "void_source_basis_refinement_v2_path_partial_scope_values_summary.csv"
)
OUT_ZIP = (
    ROOT
    / "data"
    / "derived"
    / "void_source_basis_refinement_v2_path_partial_scope_reviewer_package_v1.zip"
)
OUT_ZIP_SHA256 = (
    ROOT
    / "data"
    / "derived"
    / "void_source_basis_refinement_v2_path_partial_scope_reviewer_package_v1.zip.sha256"
)
MANIFEST = (
    ROOT
    / "data"
    / "derived"
    / "void_source_basis_refinement_v2_path_partial_scope_reviewer_package_v1_manifest.csv"
)
SUMMARY = (
    ROOT
    / "data"
    / "derived"
    / "void_source_basis_refinement_v2_path_partial_scope_reviewer_package_v1_summary.csv"
)

PACKAGE_ID = "VOID_SOURCE_BASIS_REFINEMENT_V2_PATH_PARTIAL_SCOPE_REVIEWER_PACKAGE_V1"
CLAIM_BOUNDARY = "v2_path_partial_scope_reviewer_package_not_validation"

PACKAGE_FILES = [
    "docs/void_source_basis_refinement_v2_path_partial_scope_reviewer_package_v1.md",
    "docs/void_source_basis_refinement_v2_projection_morphology_gate_v1.md",
    "data/source_manifest/void_source_basis_refinement_v2_path_partial_scope_reviewer_package_policy_v1.csv",
    "data/derived/void_source_basis_refinement_v2_path_partial_scope_reviewer_response_template_v1.csv",
    "data/derived/void_source_basis_refinement_v2_path_projection_crossmap_audit_summary.csv",
    "data/derived/void_source_basis_refinement_v2_path_projection_crossmap_audit.csv",
    "data/derived/void_source_basis_refinement_v2_path_partial_scope_policy_summary.csv",
    "data/derived/void_source_basis_refinement_v2_path_partial_scope_policy.csv",
    "data/derived/void_source_basis_refinement_v2_path_partial_scope_values_summary.csv",
    "data/derived/void_source_basis_refinement_v2_path_partial_scope_values.csv",
    "data/derived/void_source_basis_refinement_v2_path_projection_route_ledger_summary.csv",
    "data/derived/void_source_basis_refinement_v2_multichannel_coupling_ledger_summary.csv",
    "scripts/build_void_source_basis_refinement_v2_path_partial_scope_reviewer_package_v1.py",
    "scripts/validate_void_source_basis_refinement_v2_path_partial_scope_reviewer_package_v1.py",
    "scripts/validate_void_source_basis_refinement_v2_path_projection_crossmap_audit_v1.py",
    "scripts/validate_void_source_basis_refinement_v2_path_partial_scope_policy_v1.py",
    "scripts/validate_void_source_basis_refinement_v2_path_partial_scope_values_v1.py",
]


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def manifest_row(rel: str, policy: dict[str, str]) -> dict[str, str]:
    path = ROOT / rel
    if not path.exists():
        raise SystemExit(f"missing V2 partial path reviewer package file: {rel}")
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
        "claim_boundary": policy["claim_boundary"],
    }


def main() -> None:
    policy = read_one(POLICY)
    values_summary = read_one(VALUES_SUMMARY)
    if policy["status"] != "V2_PATH_PARTIAL_SCOPE_REVIEWER_PACKAGE_POLICY_FROZEN":
        raise SystemExit("unexpected V2 partial path reviewer package policy status")
    if policy["review_completed"] != "false":
        raise SystemExit("reviewer package must not include a completed review")
    if policy["current_endpoint_replay_allowed"] != "false":
        raise SystemExit("reviewer package must not authorize endpoint replay")
    if policy["endpoint_validation_claimed"] != "false":
        raise SystemExit("reviewer package must not claim endpoint validation")
    if policy["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("unexpected claim boundary")
    if values_summary["verdict"] != "partial_scope_W_path_values_available_only_as_source_side_control":
        raise SystemExit("reviewer package requires the frozen partial-scope values summary")
    if values_summary["endpoint_replay_allowed"] != "false":
        raise SystemExit("partial-scope values must not authorize endpoint replay")
    if values_summary["endpoint_validation_claimed"] != "false":
        raise SystemExit("partial-scope values must not claim validation")

    rows = [manifest_row(rel, policy) for rel in PACKAGE_FILES]
    write_csv(MANIFEST, rows)
    package_rows = rows + [manifest_row(str(MANIFEST.relative_to(ROOT)), policy)]

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
            "status": "V2_PATH_PARTIAL_SCOPE_REVIEWER_PACKAGE_BUILT_NOT_COMPLETED",
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
            "verdict": "partial_path_scope_reviewer_package_ready_not_completed",
            "recommended_next_action": "send_zip_to_reviewer_and_validate_completed_response",
            "claim_boundary": policy["claim_boundary"],
        }
    ]
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_V2_PATH_PARTIAL_SCOPE_REVIEWER_PACKAGE_V1_BUILT "
        f"verdict={summary[0]['verdict']}"
    )


if __name__ == "__main__":
    main()
