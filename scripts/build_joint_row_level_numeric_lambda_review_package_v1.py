#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ID = "JOINT_ROW_LEVEL_NUMERIC_LAMBDA_REVIEW_PACKAGE_V1"
CLAIM_BOUNDARY = "joint_row_level_numeric_lambda_review_not_rescoring_not_validation"

LAMBDA_POLICY_RESPONSE = ROOT / "data/derived/joint_row_level_lambda_policy_review_response_v1_summary.csv"
LAMBDA_BLOCKER = ROOT / "data/derived/joint_row_level_lambda_policy_blocker_status_v1_summary.csv"
FORMULA = ROOT / "data/derived/joint_symbolic_row_level_penalty_formula_shell_v1_summary.csv"
VALUES_SUMMARY = ROOT / "data/derived/joint_row_level_numeric_penalty_values_v1_summary.csv"
POLICY = ROOT / "data/source_manifest/joint_row_level_numeric_lambda_review_policy_v1.csv"
TEMPLATE = ROOT / "data/derived/joint_row_level_numeric_lambda_review_response_template_v1.csv"
PACKAGE = ROOT / "data/derived/joint_row_level_numeric_lambda_review_package_v1.zip"
SHA = ROOT / "data/derived/joint_row_level_numeric_lambda_review_package_v1.zip.sha256"
MANIFEST = ROOT / "data/derived/joint_row_level_numeric_lambda_review_package_v1_manifest.csv"
SUMMARY = ROOT / "data/derived/joint_row_level_numeric_lambda_review_package_v1_summary.csv"
DOC = ROOT / "docs/joint_row_level_numeric_lambda_review_package_v1.md"
DIAG = ROOT / "data/derived/joint_row_level_numeric_lambda_candidate_v1.csv"
DIAG_SUMMARY = ROOT / "data/derived/joint_row_level_numeric_lambda_candidate_v1_summary.csv"

PACKAGE_FILES = [
    "docs/joint_row_level_numeric_lambda_review_package_v1.md",
    "data/source_manifest/joint_row_level_numeric_lambda_review_policy_v1.csv",
    "data/derived/joint_row_level_numeric_lambda_review_response_template_v1.csv",
    "data/derived/joint_row_level_numeric_lambda_candidate_v1.csv",
    "data/derived/joint_row_level_numeric_lambda_candidate_v1_summary.csv",
    "data/derived/joint_row_level_lambda_policy_review_response_v1_summary.csv",
    "data/derived/joint_row_level_lambda_policy_blocker_status_v1_summary.csv",
    "data/derived/joint_symbolic_row_level_penalty_formula_shell_v1_summary.csv",
    "data/derived/joint_row_level_numeric_penalty_values_v1_summary.csv",
    "scripts/build_joint_row_level_numeric_lambda_review_package_v1.py",
    "scripts/validate_joint_row_level_numeric_lambda_review_package_v1.py",
]


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


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
    path.parent.mkdir(parents=True, exist_ok=True)
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
    is_lambda = rel.endswith("joint_row_level_numeric_lambda_candidate_v1.csv") or rel.endswith(
        "joint_row_level_numeric_lambda_candidate_v1_summary.csv"
    )
    return {
        "package_id": PACKAGE_ID,
        "package_path": rel,
        "byte_count": str(path.stat().st_size),
        "sha256": sha256(path),
        "contains_endpoint_residuals": "false",
        "contains_new_endpoint_scores": "false",
        "contains_fit_statistics": "false",
        "contains_lambda_row_numeric_value": "true" if is_lambda else "false",
        "contains_t_joint_rescoring": "false",
        "contains_endpoint_scoring": "false",
        "endpoint_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def main() -> None:
    lambda_policy = read_one(LAMBDA_POLICY_RESPONSE)
    lambda_blocker = read_one(LAMBDA_BLOCKER)
    formula = read_one(FORMULA)
    values = read_one(VALUES_SUMMARY)

    if lambda_policy["decision"] != "ACCEPT_LAMBDA_POLICY_BOUNDARY_NOT_NUMERIC_NOT_RESCORING_NOT_VALIDATION":
        raise SystemExit("lambda policy review is not accepted")
    if lambda_blocker["verdict"] != "LAMBDA_POLICY_ACCEPTED_NUMERIC_VALUE_STILL_BLOCKED":
        raise SystemExit("lambda blocker is not at numeric-value-still-blocked state")
    if formula["future_score_shell"] != "T_joint_penalized(a)=T_joint(a)+lambda_row*P_row(a)":
        raise SystemExit("unexpected symbolic score shell")
    if values["verdict"] != "NUMERIC_PENALTY_VALUES_COMPUTED_NOT_RESCORING":
        raise SystemExit("numeric penalty values are not available")

    lambda_value = "1.0"
    lambda_rule = "dimensionless_unit_weight_prior"
    write_csv(
        DIAG,
        [
            {
                "candidate_id": "JOINT_ROW_LEVEL_NUMERIC_LAMBDA_CANDIDATE_V1",
                "lambda_row_numeric_value": lambda_value,
                "lambda_row_dimension": "dimensionless",
                "lambda_rule": lambda_rule,
                "rationale": "unit coefficient because T_joint and P_row are both dimensionless; no endpoint residuals or scores used",
                "uses_endpoint_residuals": "false",
                "uses_endpoint_scores": "false",
                "uses_fit_improvement_feedback": "false",
                "uses_posterior_chains": "false",
                "uses_post_score_control_ranks": "false",
                "t_joint_rescoring_authorized": "false",
                "endpoint_scoring_allowed": "false",
                "endpoint_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    write_csv(
        DIAG_SUMMARY,
        [
            {
                "candidate_id": "JOINT_ROW_LEVEL_NUMERIC_LAMBDA_CANDIDATE_V1",
                "lambda_row_numeric_value": lambda_value,
                "lambda_row_dimension": "dimensionless",
                "lambda_rule": lambda_rule,
                "lambda_source_status": "residual_blind_unit_prior_candidate_for_review",
                "policy_decision": lambda_policy["decision"],
                "blocker_verdict": lambda_blocker["verdict"],
                "candidate_P_row_context": values["P_row_candidate"],
                "lambda_row_numeric_value_authorized": "false",
                "t_joint_rescoring_authorized": "false",
                "endpoint_scoring_allowed": "false",
                "endpoint_validation_claimed": "false",
                "verdict": "NUMERIC_LAMBDA_CANDIDATE_PACKAGED_FOR_REVIEW_NOT_AUTHORIZED_NOT_RESCORING",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )

    policy_rows = [
        {
            "review_id": PACKAGE_ID,
            "question_id": "NL_Q1_POLICY_COMPATIBILITY",
            "question": "Is the proposed numeric lambda_row value compatible with the accepted dimensionless residual-blind lambda policy?",
            "required_response": "accept_or_reject",
            "acceptance_condition": "Accept only if lambda_row=1 is treated as a dimensionless unit-weight prior, not as endpoint tuning.",
            "forbidden_inputs": "endpoint_residuals;endpoint_scores;fit_improvements;posterior_chains;post_score_control_ranks",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "NL_Q2_NUMERIC_VALUE_AUTHORIZATION",
            "question": "Authorize or reject recording lambda_row=1 as the frozen numeric lambda candidate for a later rescoring-authorization package.",
            "required_response": "AUTHORIZE_NUMERIC_LAMBDA_RECORD_ONLY_or_NO_GO",
            "acceptance_condition": "GO authorizes recording the numeric lambda only; it does not authorize applying it to T_joint.",
            "forbidden_inputs": "endpoint_residuals;endpoint_scores;fit_improvements;posterior_chains;post_score_control_ranks",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "NL_Q3_BOUNDARY",
            "question": "Should T_joint rescoring, endpoint scoring, and validation remain forbidden after this package?",
            "required_response": "accept_or_reject",
            "acceptance_condition": "Accept only if this package is numeric-lambda record-only and all scoring flags remain false.",
            "forbidden_inputs": "endpoint_residuals;endpoint_scores;fit_improvements;posterior_chains;post_score_control_ranks",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(POLICY, policy_rows)
    write_csv(
        TEMPLATE,
        [
            {
                **row,
                "review_completed": "false",
                "reviewer_id_or_role": "",
                "reviewer_response": "",
                "reviewer_rationale": "",
                "forbidden_inputs_used": "false",
                "lambda_policy_compatible": "false",
                "lambda_row_numeric_value_authorized": "false",
                "t_joint_rescoring_authorized": "false",
                "endpoint_scoring_authorized": "false",
            }
            for row in policy_rows
        ],
    )

    DOC.write_text(
        "\n".join(
            [
                "# Joint row-level numeric lambda review package v1",
                "",
                "**Doc class:** external numeric-lambda review handoff.",
                "**Status:** numeric `lambda_row` candidate only; not `T_joint` rescoring; not endpoint scoring; not validation.",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`.",
                "",
                "The previous lambda-policy review accepted only the dimensional and",
                "residual-blind boundary. This package proposes the narrowest possible",
                "numeric candidate under that boundary:",
                "",
                "`lambda_row = 1`",
                "",
                "Rationale: both `T_joint` and `P_row` are dimensionless.  The unit",
                "coefficient is therefore a source-blind, endpoint-blind unit-weight",
                "prior on the already frozen row-level penalty. It is not fitted from",
                "endpoint residuals, endpoint scores, fit improvements, posterior",
                "chains, or post-score control ranks.",
                "",
                "This package does not apply the value. It only asks whether the value",
                "may be recorded as a frozen numeric candidate for a later, separate",
                "rescoring-authorization package.",
                "",
                "Current context:",
                "",
                f"- symbolic shell: `{formula['future_score_shell']}`",
                f"- lambda policy decision: `{lambda_policy['decision']}`",
                f"- blocker verdict: `{lambda_blocker['verdict']}`",
                f"- candidate `P_row` context: `{values['P_row_candidate']}`",
                "",
                "A positive response would still not authorize `T_joint` rescoring,",
                "endpoint scoring, or validation.",
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
                "status": "JOINT_ROW_LEVEL_NUMERIC_LAMBDA_REVIEW_PACKAGE_READY_NOT_COMPLETED",
                "zip_path": str(PACKAGE.relative_to(ROOT)),
                "zip_sha256_path": str(SHA.relative_to(ROOT)),
                "zip_sha256": digest,
                "package_file_count": str(len(package_rows)),
                "review_completed": "false",
                "lambda_row_numeric_value": lambda_value,
                "lambda_row_dimension": "dimensionless",
                "lambda_rule": lambda_rule,
                "lambda_row_numeric_value_authorized": "false",
                "t_joint_rescoring_authorized": "false",
                "endpoint_scoring_allowed": "false",
                "endpoint_validation_claimed": "false",
                "contains_endpoint_residuals": "false",
                "contains_new_endpoint_scores": "false",
                "contains_fit_statistics": "false",
                "contains_lambda_row_numeric_value": "true",
                "contains_t_joint_rescoring": "false",
                "verdict": "numeric_lambda_review_package_ready_not_completed_not_rescoring",
                "recommended_next_action": "send_zip_to_reviewer_before_any_T_joint_rescoring",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    print(f"{PACKAGE_ID}_BUILT sha256={digest}")


if __name__ == "__main__":
    main()
