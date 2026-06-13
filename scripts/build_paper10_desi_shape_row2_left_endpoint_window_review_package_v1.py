#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_shape_row2_left_endpoint_window_review_policy_v1.csv"
TEMPLATE = ROOT / "data/derived/paper10_desi_shape_row2_left_endpoint_window_review_response_template_v1.csv"
PACKAGE = ROOT / "data/derived/paper10_desi_shape_row2_left_endpoint_window_review_package_v1.zip"
SHA = ROOT / "data/derived/paper10_desi_shape_row2_left_endpoint_window_review_package_v1.zip.sha256"
MANIFEST = ROOT / "data/derived/paper10_desi_shape_row2_left_endpoint_window_review_package_v1_manifest.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_shape_row2_left_endpoint_window_review_package_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_shape_row2_left_endpoint_window_review_not_validation"
PACKAGE_ID = "PAPER10_DESI_SHAPE_ROW2_LEFT_ENDPOINT_WINDOW_REVIEW_PACKAGE_V1"

PACKAGE_FILES = [
    "docs/paper10_desi_shape_row2_left_endpoint_window_review_v1.md",
    "data/source_manifest/paper10_desi_shape_row2_left_endpoint_window_review_policy_v1.csv",
    "data/derived/paper10_desi_shape_row2_left_endpoint_window_review_response_template_v1.csv",
    "docs/paper10_desi_shape_row2_endpoint_pair_independence_scout_v1.md",
    "data/source_manifest/paper10_desi_shape_row2_endpoint_pair_independence_scout_policy_v1.csv",
    "data/derived/paper10_desi_shape_row2_endpoint_pair_independence_scout_v1.csv",
    "data/derived/paper10_desi_shape_row2_endpoint_pair_independence_scout_v1_summary.csv",
    "docs/paper10_desi_shape_row2_left_endpoint_nearmiss_freeze_v1.md",
    "data/source_manifest/paper10_desi_shape_row2_left_endpoint_nearmiss_freeze_policy_v1.csv",
    "data/derived/paper10_desi_shape_row2_left_endpoint_nearmiss_freeze_v1.csv",
    "data/derived/paper10_desi_shape_row2_left_endpoint_nearmiss_freeze_v1_summary.csv",
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


def manifest_row(rel: str) -> dict[str, str]:
    path = ROOT / rel
    if not path.exists():
        raise SystemExit(f"missing package member: {rel}")
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
    policy_rows = read_rows(POLICY)
    if len(policy_rows) != 3:
        raise SystemExit("row2 left endpoint window review policy must contain three rows")
    if {row["claim_boundary"] for row in policy_rows} != {CLAIM_BOUNDARY}:
        raise SystemExit("bad row2 left endpoint window review claim boundary")
    for row in policy_rows:
        for field in ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"]:
            if row[field] != "false":
                raise SystemExit(f"policy {field} must remain false")

    near = read_one(ROOT / "data/derived/paper10_desi_shape_row2_left_endpoint_nearmiss_freeze_v1_summary.csv")
    if near["status"] != "DESI_SHAPE_ROW2_LEFT_ENDPOINT_NEARMISS_CONTEXT_FROZEN_NOT_REPLAY_NOT_VALIDATION":
        raise SystemExit("window review expects a frozen left endpoint near-miss parent")
    if near["left_endpoint_release_allowed"] != "false":
        raise SystemExit("window review must start with left endpoint unreleased")

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
                "source_reference_or_url": "",
                "forbidden_inputs_used": "false",
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(TEMPLATE, template_rows)

    rows = [manifest_row(rel) for rel in PACKAGE_FILES]
    write_csv(MANIFEST, rows)
    package_rows = rows + [manifest_row(str(MANIFEST.relative_to(ROOT)))]
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
                "status": "DESI_SHAPE_ROW2_LEFT_ENDPOINT_WINDOW_REVIEW_PACKAGE_BUILT_NOT_COMPLETED",
                "zip_path": str(PACKAGE.relative_to(ROOT)),
                "zip_sha256_path": str(SHA.relative_to(ROOT)),
                "zip_sha256": digest,
                "package_file_count": str(len(package_rows)),
                "review_completed": "false",
                "left_endpoint_release_allowed": "false",
                "row2_promotion_ready": "false",
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "contains_endpoint_residuals": "false",
                "contains_endpoint_scores": "false",
                "contains_fit_statistics": "false",
                "verdict": "row2_left_endpoint_window_review_package_ready_not_completed_not_replay",
                "recommended_next_action": "send_zip_to_reviewer_before_any_window_change_or_promotion_request",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    print(f"paper10_desi_shape_row2_left_endpoint_window_review_package_v1: built sha256={digest}")


if __name__ == "__main__":
    main()
