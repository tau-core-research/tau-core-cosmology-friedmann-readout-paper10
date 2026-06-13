#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/joint_block_diagonal_scoring_authorization_review_policy_v1.csv"
TEMPLATE = ROOT / "data/derived/joint_block_diagonal_scoring_authorization_review_response_template_v1.csv"
PACKAGE = ROOT / "data/derived/joint_block_diagonal_scoring_authorization_review_package_v1.zip"
SHA = ROOT / "data/derived/joint_block_diagonal_scoring_authorization_review_package_v1.zip.sha256"
MANIFEST = ROOT / "data/derived/joint_block_diagonal_scoring_authorization_review_package_v1_manifest.csv"
SUMMARY = ROOT / "data/derived/joint_block_diagonal_scoring_authorization_review_package_v1_summary.csv"
DOC = ROOT / "docs/joint_block_diagonal_scoring_authorization_review_package_v1.md"
CLOSURE_SUMMARY = ROOT / "data/derived/joint_cross_probe_covariance_closure_review_response_v1_summary.csv"
REQ_SUMMARY = ROOT / "data/derived/joint_cross_probe_covariance_source_requirements_v1_summary.csv"
BD_SUMMARY = ROOT / "data/derived/joint_block_diagonal_likelihood_surrogate_protocol_shell_v1_summary.csv"
CONTROL_SUMMARY = ROOT / "data/derived/joint_matched_control_suite_requirements_gate_v1_summary.csv"
STAT_SUMMARY = ROOT / "data/derived/joint_single_statistic_binding_prerequisites_v1_summary.csv"
PACKAGE_ID = "JOINT_BLOCK_DIAGONAL_SCORING_AUTHORIZATION_REVIEW_PACKAGE_V1"
CLAIM_BOUNDARY = "joint_block_diagonal_scoring_authorization_review_not_scoring_not_validation"

PACKAGE_FILES = [
    "docs/joint_block_diagonal_scoring_authorization_review_package_v1.md",
    "data/source_manifest/joint_block_diagonal_scoring_authorization_review_policy_v1.csv",
    "data/derived/joint_block_diagonal_scoring_authorization_review_response_template_v1.csv",
    "data/derived/joint_cross_probe_covariance_closure_review_response_v1.csv",
    "data/derived/joint_cross_probe_covariance_closure_review_response_v1_summary.csv",
    "data/derived/joint_cross_probe_covariance_source_requirements_v1.csv",
    "data/derived/joint_cross_probe_covariance_source_requirements_v1_summary.csv",
    "docs/joint_cross_probe_covariance_source_requirements_v1.md",
    "data/derived/joint_block_diagonal_likelihood_surrogate_protocol_shell_v1.csv",
    "data/derived/joint_block_diagonal_likelihood_surrogate_protocol_shell_v1_summary.csv",
    "docs/joint_block_diagonal_likelihood_surrogate_protocol_shell_v1.md",
    "data/derived/joint_matched_control_suite_requirements_gate_v1.csv",
    "data/derived/joint_matched_control_suite_requirements_gate_v1_summary.csv",
    "docs/joint_matched_control_suite_requirements_gate_v1.md",
    "data/derived/joint_single_statistic_binding_prerequisites_v1.csv",
    "data/derived/joint_single_statistic_binding_prerequisites_v1_summary.csv",
    "docs/joint_single_statistic_binding_prerequisites_v1.md",
]


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path.relative_to(ROOT)}")
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
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def manifest_row(rel: str) -> dict[str, str]:
    path = ROOT / rel
    if not path.exists():
        raise SystemExit(f"missing package file: {rel}")
    return {
        "package_id": PACKAGE_ID,
        "package_path": rel,
        "byte_count": str(path.stat().st_size),
        "sha256": sha256(path),
        "contains_endpoint_residuals": "false",
        "contains_new_endpoint_scores": "false",
        "contains_fit_statistics": "false",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def main() -> None:
    closure = read_one(CLOSURE_SUMMARY)
    req = read_one(REQ_SUMMARY)
    bd = read_one(BD_SUMMARY)
    controls = read_one(CONTROL_SUMMARY)
    stat = read_one(STAT_SUMMARY)
    if closure["decision"] != "JOINT_BLOCK_DIAGONAL_INDEPENDENCE_PRECONDITION_CAVEATED_CLOSED_NOT_SCORING":
        raise SystemExit("caveated independence precondition is not closed")
    if req["independence_rationale_route_ready"] != "true":
        raise SystemExit("source requirements gate does not mark independence route ready")
    if bd["single_joint_surrogate_form_declared"] != "true":
        raise SystemExit("block-diagonal surrogate form is not declared")
    if controls["verdict"] != "JOINT_MATCHED_CONTROL_SUITE_REQUIREMENTS_FROZEN_IMPLEMENTATION_BLOCKED":
        raise SystemExit("matched-control requirements are not frozen")
    if stat["verdict"] != "JOINT_SINGLE_STATISTIC_BINDING_PREREQUISITES_FROZEN_PROTOCOL_BLOCKED":
        raise SystemExit("single-statistic prerequisites are not frozen")

    policy_rows = [
        {
            "review_id": PACKAGE_ID,
            "question_id": "BDSA_Q1_CAVEATED_PRECONDITION",
            "question": "Does the completed cross-probe closure review allow a caveated block-diagonal independence precondition for a later permission-only joint replay?",
            "required_response": "accept_or_reject",
            "acceptance_condition": "Accept only if the reviewer agrees this is a scoring-authorization review, not scoring itself.",
            "forbidden_inputs": "endpoint_residuals;new_endpoint_scores;fit_improvements;posterior_chains;post_score_control_ranks",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "BDSA_Q2_CAVEATS",
            "question": "Are the required block-diagonal caveats explicit enough to carry into a permission-only replay?",
            "required_response": "accept_with_caveats_or_reject",
            "acceptance_condition": "Accept only if shared sky/mask, redshift-kernel, cosmology/nuisance, calibration, and missing population covariance caveats are carried forward.",
            "forbidden_inputs": "endpoint_residuals;new_endpoint_scores;fit_improvements;posterior_chains;post_score_control_ranks",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "BDSA_Q3_SAME_STATISTIC_CONTROLS",
            "question": "May the next artifact bind candidate and controls to the same block-diagonal statistic and covariance blocks?",
            "required_response": "accept_protocol_authorization_or_reject",
            "acceptance_condition": "Accept only for a future permission-only replay package with matched controls; reject if controls/statistic are not sufficiently specified.",
            "forbidden_inputs": "endpoint_residuals;new_endpoint_scores;fit_improvements;posterior_chains;post_score_control_ranks",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "BDSA_Q4_NEXT_ACTION",
            "question": "Is the next allowed action a separate guarded scoring/replay package rather than direct scoring?",
            "required_response": "accept_or_reject",
            "acceptance_condition": "Accept keeps this as authorization only; direct scoring remains forbidden until a separate replay package is built and validated.",
            "forbidden_inputs": "endpoint_residuals;new_endpoint_scores;fit_improvements;posterior_chains;post_score_control_ranks",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(POLICY, policy_rows)
    template_rows = [
        {
            **row,
            "review_completed": "false",
            "reviewer_id_or_role": "",
            "reviewer_response": "",
            "reviewer_rationale": "",
            "forbidden_inputs_used": "false",
            "permission_only_replay_authorization_allowed": "false",
            "separate_replay_package_required": "true",
        }
        for row in policy_rows
    ]
    write_csv(TEMPLATE, template_rows)
    DOC.write_text(
        "\n".join(
            [
                "# Joint block-diagonal scoring authorization review package v1",
                "",
                "**Doc class:** external authorization handoff",
                "**Status:** not scoring; not endpoint validation; not cosmological validation",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`",
                "",
                "This package asks whether the caveated block-diagonal independence",
                "precondition may be promoted into a later permission-only joint replay",
                "authorization package. It does not run the replay and does not compute",
                "scores.",
                "",
                "Upstream status:",
                "",
                f"- closure decision: `{closure['decision']}`",
                f"- source requirements verdict: `{req['verdict']}`",
                f"- block-diagonal shell verdict: `{bd['verdict']}`",
                f"- matched-control requirements verdict: `{controls['verdict']}`",
                f"- statistic prerequisites verdict: `{stat['verdict']}`",
                "",
                "The required caveats are shared sky/mask overlap, redshift-kernel overlap,",
                "shared cosmology/nuisance/calibration correlations, and missing",
                "population-level cross-probe covariance.",
                "",
            ]
        )
    )
    manifest_rows = [manifest_row(rel) for rel in PACKAGE_FILES]
    write_csv(MANIFEST, manifest_rows)
    package_rows = manifest_rows + [manifest_row(str(MANIFEST.relative_to(ROOT)))]
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
                "status": "JOINT_BLOCK_DIAGONAL_SCORING_AUTHORIZATION_REVIEW_PACKAGE_READY_NOT_COMPLETED",
                "zip_path": str(PACKAGE.relative_to(ROOT)),
                "zip_sha256_path": str(SHA.relative_to(ROOT)),
                "zip_sha256": digest,
                "package_file_count": str(len(package_rows)),
                "review_completed": "false",
                "permission_only_replay_authorization_allowed": "false",
                "endpoint_scoring_allowed": "false",
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "contains_endpoint_residuals": "false",
                "contains_new_endpoint_scores": "false",
                "contains_fit_statistics": "false",
                "verdict": "block_diagonal_scoring_authorization_review_package_ready_not_completed_not_scoring",
                "recommended_next_action": "send_zip_to_reviewer_before_any_guarded_replay_package",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    print(f"JOINT_BLOCK_DIAGONAL_SCORING_AUTHORIZATION_REVIEW_PACKAGE_V1_BUILT sha256={digest}")


if __name__ == "__main__":
    main()
