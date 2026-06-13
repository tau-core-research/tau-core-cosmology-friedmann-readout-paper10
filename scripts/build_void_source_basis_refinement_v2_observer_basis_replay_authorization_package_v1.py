#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/void_source_basis_refinement_v2_observer_basis_replay_authorization_policy_v1.csv"
CANDIDATE_REVIEW = ROOT / "data/derived/void_source_basis_refinement_v2_observer_basis_candidate_review_response_v1_summary.csv"
SCREEN_SUMMARY = ROOT / "data/derived/void_source_basis_refinement_v2_observer_basis_fast_screen_v1_summary.csv"
FAMILY_SUMMARY = ROOT / "data/derived/void_source_basis_refinement_v2_observer_basis_fast_screen_v1_family_summary.csv"
DOC = ROOT / "docs/void_source_basis_refinement_v2_observer_basis_replay_authorization_v1.md"
TEMPLATE = ROOT / "data/derived/void_source_basis_refinement_v2_observer_basis_replay_authorization_response_template_v1.csv"
PACKAGE = ROOT / "data/derived/void_source_basis_refinement_v2_observer_basis_replay_authorization_package_v1.zip"
MANIFEST = ROOT / "data/derived/void_source_basis_refinement_v2_observer_basis_replay_authorization_package_v1_manifest.csv"
SUMMARY = ROOT / "data/derived/void_source_basis_refinement_v2_observer_basis_replay_authorization_package_v1_summary.csv"
SHA = ROOT / "data/derived/void_source_basis_refinement_v2_observer_basis_replay_authorization_package_v1.zip.sha256"
CLAIM_BOUNDARY = "v2_observer_basis_replay_authorization_not_validation"


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
    review = read_one(CANDIDATE_REVIEW)
    screen = read_one(SCREEN_SUMMARY)
    if policy["candidate_family"] != "W_path_x_sky_x_x_zcenter":
        raise SystemExit("candidate mismatch")
    if review["candidate_family"] != policy["candidate_family"]:
        raise SystemExit("review candidate mismatch")
    if review["status"] != "V2_OBSERVER_BASIS_CANDIDATE_REVIEW_ACCEPTED_FOR_SEPARATE_AUTHORIZATION_PACKAGE_NOT_REPLAY":
        raise SystemExit("candidate review did not accept package preparation")
    if review["endpoint_replay_allowed"] != "false" or review["endpoint_validation_claimed"] != "false":
        raise SystemExit("candidate review must not itself authorize replay")
    if screen["best_candidate_family"] != policy["candidate_family"]:
        raise SystemExit("screen best candidate mismatch")
    family = next(row for row in read_rows(FAMILY_SUMMARY) if row["family_id"] == policy["candidate_family"])
    questions = [
        (
            "Q1_replay_scope",
            "May W_path_x_sky_x_x_zcenter be replayed once on the frozen 12-row partial path scope?",
        ),
        (
            "Q2_family_freeze",
            "Is the source family frozen from W_path, sky_x, and centered zHD, with no endpoint residual input?",
        ),
        (
            "Q3_controls",
            "Are the required controls off, wrong_sign, deterministic_shuffle, and rank_reverse sufficient for this permission-only replay?",
        ),
        (
            "Q4_authorization",
            "If all caveats are preserved, is the decision GO_OBSERVER_BASIS_REPLAY_PERMISSION_ONLY?",
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
            "authorization_scope": "single_permission_only_12_row_W_path_x_sky_x_x_zcenter_replay_not_validation",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for qid, question in questions
    ]
    write_csv(TEMPLATE, template_rows)
    package_files = [POLICY, CANDIDATE_REVIEW, SCREEN_SUMMARY, FAMILY_SUMMARY, DOC, TEMPLATE]
    with zipfile.ZipFile(PACKAGE, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in package_files:
            zf.write(path, path.relative_to(ROOT).as_posix())
    digest = sha256(PACKAGE)
    SHA.write_text(f"{digest}  {PACKAGE.name}\n")
    write_csv(
        MANIFEST,
        [
            {"path": path.relative_to(ROOT).as_posix(), "sha256": sha256(path), "claim_boundary": CLAIM_BOUNDARY}
            for path in package_files
        ],
    )
    write_csv(
        SUMMARY,
        [
            {
                "policy_id": policy["policy_id"],
                "status": "V2_OBSERVER_BASIS_REPLAY_AUTHORIZATION_PACKAGE_BUILT_NOT_COMPLETED",
                "candidate_family": policy["candidate_family"],
                "candidate_review_decision": review["decision"],
                "delta_chi2_candidate_minus_baseline": family["delta_chi2_candidate_minus_baseline"],
                "delta_chi2_candidate_minus_best_control": family["delta_chi2_candidate_minus_best_control"],
                "zip_path": PACKAGE.relative_to(ROOT).as_posix(),
                "zip_sha256": digest,
                "review_completed": "false",
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "physical_lensing_path_weight_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
                "verdict": "observer_basis_replay_authorization_package_ready_not_completed",
            }
        ],
    )
    print(
        "PAPER10_OBSERVER_BASIS_REPLAY_AUTHORIZATION_PACKAGE_BUILT "
        f"candidate={policy['candidate_family']} sha256={digest}"
    )


if __name__ == "__main__":
    main()
