#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/void_source_basis_refinement_v2_observer_basis_candidate_review_policy_v1.csv"
SCREEN_SUMMARY = ROOT / "data/derived/void_source_basis_refinement_v2_observer_basis_fast_screen_v1_summary.csv"
FAMILY_SUMMARY = ROOT / "data/derived/void_source_basis_refinement_v2_observer_basis_fast_screen_v1_family_summary.csv"
DOC = ROOT / "docs/void_source_basis_refinement_v2_observer_basis_candidate_review_v1.md"
TEMPLATE = ROOT / "data/derived/void_source_basis_refinement_v2_observer_basis_candidate_review_response_template_v1.csv"
PACKAGE = ROOT / "data/derived/void_source_basis_refinement_v2_observer_basis_candidate_review_package_v1.zip"
MANIFEST = ROOT / "data/derived/void_source_basis_refinement_v2_observer_basis_candidate_review_package_v1_manifest.csv"
SUMMARY = ROOT / "data/derived/void_source_basis_refinement_v2_observer_basis_candidate_review_package_v1_summary.csv"
SHA = ROOT / "data/derived/void_source_basis_refinement_v2_observer_basis_candidate_review_package_v1.zip.sha256"
CLAIM_BOUNDARY = "v2_observer_basis_candidate_review_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
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
    screen = read_one(SCREEN_SUMMARY)
    if policy["candidate_family"] != "W_path_x_sky_x_x_zcenter":
        raise SystemExit("candidate mismatch")
    if screen["best_candidate_family"] != policy["candidate_family"]:
        raise SystemExit("screen best candidate mismatch")
    if screen["endpoint_replay_allowed"] != "false" or screen["endpoint_validation_claimed"] != "false":
        raise SystemExit("screen must not be replay/validation")
    family = next(row for row in read_rows(FAMILY_SUMMARY) if row["family_id"] == policy["candidate_family"])
    if family["survives_family_controls"] != "true":
        raise SystemExit("candidate must survive local controls before review package")
    questions = [
        (
            "Q1_candidate_predeclared",
            "Was W_path_x_sky_x_x_zcenter present in the predeclared fast-screen basis before this review?",
        ),
        (
            "Q2_source_side_inputs",
            "Are the candidate inputs restricted to source-side W_path, sky_x, and centered zHD, without endpoint residuals?",
        ),
        (
            "Q3_control_result",
            "Does the candidate improve baseline and survive its local controls in the diagnostic screen?",
        ),
        (
            "Q4_next_action",
            "May this candidate proceed only to a separate permission-only replay authorization package, with no validation claim?",
        ),
    ]
    template_rows = [
        {
            "question_id": qid,
            "question": question,
            "candidate_family": policy["candidate_family"],
            "reviewer_response": "",
            "reviewer_rationale": "",
            "review_completed": "false",
            "forbidden_inputs_used": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_lensing_path_weight_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for qid, question in questions
    ]
    write_csv(TEMPLATE, template_rows)
    package_files = [POLICY, SCREEN_SUMMARY, FAMILY_SUMMARY, DOC, TEMPLATE]
    with zipfile.ZipFile(PACKAGE, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in package_files:
            arcname = path.relative_to(ROOT).as_posix()
            info = zipfile.ZipInfo(arcname)
            info.date_time = (2026, 1, 1, 0, 0, 0)
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, path.read_bytes())
    digest = sha256(PACKAGE)
    SHA.write_text(f"{digest}  {PACKAGE.name}\n")
    write_csv(
        MANIFEST,
        [
            {
                "path": path.relative_to(ROOT).as_posix(),
                "sha256": sha256(path),
                "claim_boundary": CLAIM_BOUNDARY,
            }
            for path in package_files
        ],
    )
    write_csv(
        SUMMARY,
        [
            {
                "policy_id": policy["policy_id"],
                "status": "V2_OBSERVER_BASIS_CANDIDATE_REVIEW_PACKAGE_BUILT_NOT_COMPLETED",
                "candidate_family": policy["candidate_family"],
                "screen_verdict": screen["verdict"],
                "delta_chi2_candidate_minus_baseline": family["delta_chi2_candidate_minus_baseline"],
                "delta_chi2_candidate_minus_best_control": family["delta_chi2_candidate_minus_best_control"],
                "zip_path": PACKAGE.relative_to(ROOT).as_posix(),
                "zip_sha256": digest,
                "review_completed": "false",
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "physical_lensing_path_weight_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
                "verdict": "observer_basis_candidate_review_package_ready_not_completed",
            }
        ],
    )
    print(
        "PAPER10_OBSERVER_BASIS_CANDIDATE_REVIEW_PACKAGE_BUILT "
        f"candidate={policy['candidate_family']} sha256={digest}"
    )


if __name__ == "__main__":
    main()
