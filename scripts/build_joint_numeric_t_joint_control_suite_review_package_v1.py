#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUITE = ROOT / "data/derived/joint_numeric_t_joint_control_suite_v1.csv"
SUITE_SUMMARY = ROOT / "data/derived/joint_numeric_t_joint_control_suite_v1_summary.csv"
BLOCKER = ROOT / "data/derived/joint_numeric_t_joint_control_suite_blocker_status_v1_summary.csv"
TJOINT = ROOT / "data/derived/joint_numeric_t_joint_ledger_v1_summary.csv"
POLICY = ROOT / "data/source_manifest/joint_numeric_t_joint_control_suite_review_policy_v1.csv"
TEMPLATE = ROOT / "data/derived/joint_numeric_t_joint_control_suite_review_response_template_v1.csv"
SUMMARY = ROOT / "data/derived/joint_numeric_t_joint_control_suite_review_package_v1_summary.csv"
MANIFEST = ROOT / "data/derived/joint_numeric_t_joint_control_suite_review_package_v1_manifest.csv"
PACKAGE = ROOT / "data/derived/joint_numeric_t_joint_control_suite_review_package_v1.zip"
SHA = ROOT / "data/derived/joint_numeric_t_joint_control_suite_review_package_v1.zip.sha256"
DOC = ROOT / "docs/joint_numeric_t_joint_control_suite_review_package_v1.md"
INSTRUCTIONS = ROOT / "docs/joint_numeric_t_joint_control_suite_review_instructions_v1.md"
EXTERNAL_MESSAGE = ROOT / "docs/joint_numeric_t_joint_control_suite_review_external_message_v1.md"
PACKAGE_ID = "JOINT_NUMERIC_T_JOINT_CONTROL_SUITE_REVIEW_PACKAGE_V1"
CLAIM_BOUNDARY = "joint_numeric_t_joint_control_suite_review_not_endpoint_scoring_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def manifest_row(path: Path) -> dict[str, str]:
    return {
        "package_id": PACKAGE_ID,
        "package_path": rel(path),
        "sha256": sha256(path),
        "contains_endpoint_scores": "false",
        "contains_fit_statistics": "false",
        "endpoint_scoring_authorization_package_preparation_allowed": "false",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def main() -> None:
    suite = read_one(SUITE_SUMMARY)
    blocker = read_one(BLOCKER)
    tjoint = read_one(TJOINT)
    if suite["verdict"] != "NUMERIC_T_JOINT_CONTROL_SUITE_BUILT_PREVALIDATION_NOT_ENDPOINT_SCORING":
        raise SystemExit("control suite must be built before review package")
    if suite["controls_beating_or_equal_candidate"] != "0":
        raise SystemExit("this review package expects zero controls beating/equal candidate")
    if blocker["current_blocker"] != "control_suite_built_endpoint_scoring_authorization_missing":
        raise SystemExit("control-suite blocker must point to endpoint authorization missing")
    if tjoint["endpoint_scoring_allowed"] != "false":
        raise SystemExit("T_joint ledger must not authorize endpoint scoring")

    forbidden = (
        "new_endpoint_scores;new_endpoint_residuals;fit_improvements;"
        "posterior_chains;posthoc_channel_selection;posthoc_weight_tuning;"
        "posthoc_sign_changes;posthoc_control_family_removal;"
        "posthoc_covariance_reweighting;cosmological_validation_claims;"
        "physical_validation_claims"
    )
    rows = [
        {
            "review_id": PACKAGE_ID,
            "question_id": "CSR_Q1_SCOPE",
            "question": "Is this package limited to reviewing the prevalidation control-suite ledger, without authorizing endpoint scoring?",
            "required_response": "accept_review_scope_or_reject",
            "acceptance_condition": "Accept only if the reviewer treats this as control-suite review, not endpoint scoring or validation.",
            "forbidden_inputs": forbidden,
            "endpoint_scoring_authorization_package_preparation_allowed": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "CSR_Q2_SAME_STATISTIC_CONTROLS",
            "question": "Do the listed controls preserve the same frozen T_joint statistic, q_i weights, signs, z_i standardization, and row-scope boundary?",
            "required_response": "accept_same_statistic_controls_or_reject",
            "acceptance_condition": "Accept only if no retuning or post-hoc family removal is allowed.",
            "forbidden_inputs": forbidden,
            "endpoint_scoring_authorization_package_preparation_allowed": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "CSR_Q3_CONTROL_RESULT",
            "question": "Is the reported 0/26 controls beating or equaling the candidate suitable as a precondition for preparing a separate endpoint-scoring authorization package?",
            "required_response": "accept_prepare_endpoint_authorization_package_or_reject",
            "acceptance_condition": "Accept only as permission to prepare a separate endpoint-scoring authorization package; do not authorize scoring directly.",
            "forbidden_inputs": forbidden,
            "endpoint_scoring_authorization_package_preparation_allowed": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "CSR_Q4_CAVEATS",
            "question": "Must the caveated covariance, KiDS endpoint-score-not-validation, DESI small-N, and observer/path permission-only caveats remain attached?",
            "required_response": "accept_caveat_preservation_or_reject",
            "acceptance_condition": "Accept only if caveats remain attached to any future endpoint-authorization package.",
            "forbidden_inputs": forbidden,
            "endpoint_scoring_authorization_package_preparation_allowed": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_rows(POLICY, rows)
    write_rows(
        TEMPLATE,
        [
            {
                **row,
                "review_completed": "false",
                "reviewer_id_or_role": "",
                "reviewer_response": "",
                "reviewer_rationale": "",
                "forbidden_inputs_used": "false",
            }
            for row in rows
        ],
    )
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Joint numeric T_joint control-suite review package v1",
                "",
                "**Doc class:** external review handoff.",
                "**Status:** prepared, not completed.",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`.",
                "",
                "This package reviews the already built numeric same-statistic",
                "control-suite ledger. It asks whether the authors may prepare a",
                "separate endpoint-scoring authorization package. It does not",
                "authorize endpoint scoring directly.",
                "",
                f"Candidate `T_joint`: `{suite['candidate_numeric_t_joint']}`.",
                f"Numeric controls: `{suite['numeric_control_count']}`.",
                f"Controls beating/equal candidate: `{suite['controls_beating_or_equal_candidate']}`.",
                "",
            ]
        )
    )
    INSTRUCTIONS.write_text(
        "\n".join(
            [
                "# Joint Numeric T_joint Control-Suite Review Instructions v1",
                "",
                "You do not need repository access. Review only the zip contents.",
                "",
                "If accepted, use these exact response tokens:",
                "",
                "- `ACCEPT_CONTROL_SUITE_REVIEW_SCOPE_NOT_ENDPOINT_SCORING`",
                "- `ACCEPT_SAME_STATISTIC_CONTROLS_NO_RETUNING`",
                "- `ACCEPT_PREPARE_SEPARATE_ENDPOINT_AUTHORIZATION_PACKAGE`",
                "- `ACCEPT_CAVEAT_PRESERVATION`",
                "",
                "If and only if all four rows are accepted, set",
                "`endpoint_scoring_authorization_package_preparation_allowed=true`",
                "on every row. This authorizes preparation of a later package only.",
                "",
                "Keep all direct scoring and validation fields false:",
                "`endpoint_scoring_allowed=false`,",
                "`endpoint_validation_claimed=false`,",
                "`cosmological_validation_claimed=false`, and",
                "`physical_validation_claimed=false`.",
                "",
            ]
        )
    )
    EXTERNAL_MESSAGE.write_text(
        "\n".join(
            [
                "# Message to External Reviewer",
                "",
                "You do not need repository access. Please inspect the attached zip",
                "and complete the response CSV from the packaged files only.",
                "",
                "The narrow question: may the authors prepare a separate endpoint-scoring",
                "authorization package after a prevalidation same-T_joint control suite",
                "where 0/26 numeric controls beat or equal the candidate?",
                "",
                "This is not itself endpoint scoring, a p-value, a likelihood ratio,",
                "or cosmological/physical validation.",
                "",
                "If accepted, please set",
                "`endpoint_scoring_authorization_package_preparation_allowed=true`",
                "on all rows, while keeping direct scoring and all validation fields false.",
                "",
            ]
        )
    )
    inputs = [
        POLICY,
        TEMPLATE,
        DOC,
        INSTRUCTIONS,
        EXTERNAL_MESSAGE,
        SUITE,
        SUITE_SUMMARY,
        BLOCKER,
        TJOINT,
        ROOT / "docs/joint_numeric_t_joint_control_suite_v1.md",
        ROOT / "scripts/build_joint_numeric_t_joint_control_suite_v1.py",
        ROOT / "scripts/validate_joint_numeric_t_joint_control_suite_v1.py",
    ]
    manifest = [manifest_row(path) for path in inputs]
    write_rows(MANIFEST, manifest)
    package_rows = manifest + [manifest_row(MANIFEST)]
    with zipfile.ZipFile(PACKAGE, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for row in package_rows:
            path = ROOT / row["package_path"]
            info = zipfile.ZipInfo(row["package_path"])
            info.date_time = (2026, 1, 1, 0, 0, 0)
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, path.read_bytes())
    digest = sha256(PACKAGE)
    SHA.write_text(f"{digest}  {PACKAGE.name}\n")
    write_rows(
        SUMMARY,
        [
            {
                "package_id": PACKAGE_ID,
                "status": "JOINT_NUMERIC_T_JOINT_CONTROL_SUITE_REVIEW_PACKAGE_READY_NOT_COMPLETED",
                "zip_path": rel(PACKAGE),
                "zip_sha256_path": rel(SHA),
                "zip_sha256": digest,
                "package_file_count": str(len(package_rows)),
                "candidate_numeric_t_joint": suite["candidate_numeric_t_joint"],
                "numeric_control_count": suite["numeric_control_count"],
                "controls_beating_or_equal_candidate": suite["controls_beating_or_equal_candidate"],
                "review_completed": "false",
                "endpoint_scoring_authorization_package_preparation_allowed": "false",
                "endpoint_scoring_allowed": "false",
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "contains_endpoint_scores": "false",
                "contains_fit_statistics": "false",
                "next_required_action": "send_zip_to_reviewer_then_validate_completed_response",
                "verdict": "control_suite_review_package_ready_not_completed",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    print(f"JOINT_NUMERIC_T_JOINT_CONTROL_SUITE_REVIEW_PACKAGE_V1_BUILT sha256={digest}")


if __name__ == "__main__":
    main()
