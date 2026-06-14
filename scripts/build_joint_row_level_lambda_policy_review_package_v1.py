#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ID = "JOINT_ROW_LEVEL_LAMBDA_POLICY_REVIEW_PACKAGE_V1"
CLAIM_BOUNDARY = "joint_row_level_lambda_policy_review_not_numeric_not_scoring_not_validation"

VALUES_SUMMARY = ROOT / "data/derived/joint_row_level_numeric_penalty_values_v1_summary.csv"
USE_AUTH = ROOT / "data/derived/joint_row_level_penalty_use_authorization_review_response_v1_summary.csv"
FORMULA = ROOT / "data/derived/joint_symbolic_row_level_penalty_formula_shell_v1_summary.csv"
POLICY = ROOT / "data/source_manifest/joint_row_level_lambda_policy_v1.csv"
TEMPLATE = ROOT / "data/derived/joint_row_level_lambda_policy_review_response_template_v1.csv"
PACKAGE = ROOT / "data/derived/joint_row_level_lambda_policy_review_package_v1.zip"
SHA = ROOT / "data/derived/joint_row_level_lambda_policy_review_package_v1.zip.sha256"
MANIFEST = ROOT / "data/derived/joint_row_level_lambda_policy_review_package_v1_manifest.csv"
SUMMARY = ROOT / "data/derived/joint_row_level_lambda_policy_review_package_v1_summary.csv"
DOC = ROOT / "docs/joint_row_level_lambda_policy_review_package_v1.md"
DIAGNOSTIC = ROOT / "data/derived/joint_row_level_lambda_policy_diagnostic_v1.csv"
DIAGNOSTIC_SUMMARY = ROOT / "data/derived/joint_row_level_lambda_policy_diagnostic_v1_summary.csv"

PACKAGE_FILES = [
    "docs/joint_row_level_lambda_policy_review_package_v1.md",
    "data/source_manifest/joint_row_level_lambda_policy_v1.csv",
    "data/derived/joint_row_level_lambda_policy_review_response_template_v1.csv",
    "data/derived/joint_row_level_lambda_policy_diagnostic_v1.csv",
    "data/derived/joint_row_level_lambda_policy_diagnostic_v1_summary.csv",
    "data/derived/joint_row_level_numeric_penalty_values_v1_summary.csv",
    "data/derived/joint_row_level_penalty_use_authorization_review_response_v1_summary.csv",
    "data/derived/joint_symbolic_row_level_penalty_formula_shell_v1_summary.csv",
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
    return {
        "package_id": PACKAGE_ID,
        "package_path": rel,
        "byte_count": str(path.stat().st_size),
        "sha256": sha256(path),
        "contains_endpoint_residuals": "false",
        "contains_new_endpoint_scores": "false",
        "contains_fit_statistics": "false",
        "contains_lambda_row_numeric_value": "false",
        "contains_t_joint_rescoring": "false",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def main() -> None:
    values = read_one(VALUES_SUMMARY)
    use_auth = read_one(USE_AUTH)
    formula = read_one(FORMULA)
    if values["verdict"] != "NUMERIC_PENALTY_VALUES_COMPUTED_NOT_RESCORING":
        raise SystemExit("numeric penalty values are not available")
    if use_auth["future_lambda_policy_package_allowed"] != "true":
        raise SystemExit("future lambda policy package is not authorized for planning")
    if formula["future_score_shell"] != "T_joint_penalized(a)=T_joint(a)+lambda_row*P_row(a)":
        raise SystemExit("unexpected future score shell")

    diagnostic_rows = [
        {
            "diagnostic_id": "JRLP_LAMBDA_POLICY_DIAGNOSTIC_V1",
            "quantity": "T_joint",
            "dimension_status": "dimensionless_standardized_joint_statistic",
            "source": "joint_numeric_t_joint_symbolic_shell",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "diagnostic_id": "JRLP_LAMBDA_POLICY_DIAGNOSTIC_V1",
            "quantity": "P_row",
            "dimension_status": "dimensionless_quadratic_normalized_feature_energy",
            "source": str(VALUES_SUMMARY.relative_to(ROOT)),
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "diagnostic_id": "JRLP_LAMBDA_POLICY_DIAGNOSTIC_V1",
            "quantity": "lambda_row",
            "dimension_status": "dimensionless_required_if_later_numeric_value_is_authorized",
            "source": "policy_only_no_numeric_value_in_this_package",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(DIAGNOSTIC, diagnostic_rows)
    diag_summary = {
        "diagnostic_id": "JRLP_LAMBDA_POLICY_DIAGNOSTIC_V1",
        "future_score_shell": formula["future_score_shell"],
        "candidate_P_row": values["P_row_candidate"],
        "lambda_row_dimension": "dimensionless",
        "lambda_row_numeric_value_defined": "false",
        "lambda_row_numeric_value_authorized": "false",
        "t_joint_rescoring_authorized": "false",
        "endpoint_validation_claimed": "false",
        "verdict": "LAMBDA_POLICY_DESIGN_READY_FOR_REVIEW_NO_NUMERIC_VALUE",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(DIAGNOSTIC_SUMMARY, [diag_summary])

    policy_rows = [
        {
            "review_id": PACKAGE_ID,
            "question_id": "LP_Q1_DIMENSIONAL_BOUNDARY",
            "question": "Is lambda_row required to be dimensionless in the symbolic shell T_joint + lambda_row P_row?",
            "required_response": "accept_or_reject",
            "acceptance_condition": "Accept only if the reviewer agrees that T_joint and P_row are dimensionless and any future lambda_row must be dimensionless.",
            "forbidden_inputs": "endpoint_residuals;endpoint_scores;fit_improvements;posterior_chains;post_score_control_ranks",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "LP_Q2_RESIDUAL_BLIND_REQUIREMENT",
            "question": "Must any future numeric lambda_row value be predeclared without endpoint-score feedback?",
            "required_response": "accept_or_reject",
            "acceptance_condition": "Accept only if no endpoint residuals, endpoint scores, fit improvements, or post-score ranks may set lambda_row.",
            "forbidden_inputs": "endpoint_residuals;endpoint_scores;fit_improvements;posterior_chains;post_score_control_ranks",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "LP_Q3_POLICY_ONLY",
            "question": "Should this package remain policy-only with no numeric lambda_row and no T_joint rescoring?",
            "required_response": "accept_or_reject",
            "acceptance_condition": "Accept only if this package is not treated as a numeric lambda or rescoring authorization.",
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
                "lambda_row_policy_accepted": "false",
                "lambda_row_dimensionless_required": "false",
                "future_numeric_lambda_package_allowed": "false",
                "lambda_row_numeric_value_authorized": "false",
                "t_joint_rescoring_authorized": "false",
            }
            for row in policy_rows
        ],
    )

    DOC.write_text(
        "\n".join(
            [
                "# Joint row-level lambda policy review package v1",
                "",
                "**Doc class:** external design-review handoff.",
                "**Status:** lambda policy only; no numeric lambda; not `T_joint` rescoring; not endpoint validation.",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`.",
                "",
                "This package freezes the only safe policy boundary for a possible",
                "future `lambda_row` route. It does not choose a numeric value.",
                "",
                "Symbolic shell:",
                "",
                "`T_joint_penalized(a)=T_joint(a)+lambda_row*P_row(a)`",
                "",
                "Dimensional audit:",
                "",
                "- `T_joint` is dimensionless as a standardized joint statistic.",
                "- `P_row` is dimensionless as a quadratic normalized feature energy.",
                "- therefore any later `lambda_row` must be dimensionless.",
                "",
                "Boundary:",
                "",
                "- no endpoint residuals",
                "- no endpoint scores",
                "- no fit-improvement feedback",
                "- no posterior chains",
                "- no post-score control ranks",
                "- no numeric `lambda_row` in this package",
                "- no `T_joint` rescoring in this package",
                "",
                f"Candidate `P_row` currently on record: `{values['P_row_candidate']}`.",
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
                "status": "JOINT_ROW_LEVEL_LAMBDA_POLICY_REVIEW_PACKAGE_READY_NOT_COMPLETED",
                "zip_path": str(PACKAGE.relative_to(ROOT)),
                "zip_sha256_path": str(SHA.relative_to(ROOT)),
                "zip_sha256": digest,
                "package_file_count": str(len(package_rows)),
                "review_completed": "false",
                "lambda_row_policy_accepted": "false",
                "lambda_row_dimensionless_required": "false",
                "future_numeric_lambda_package_allowed": "false",
                "lambda_row_numeric_value_authorized": "false",
                "t_joint_rescoring_authorized": "false",
                "endpoint_scoring_allowed": "false",
                "endpoint_validation_claimed": "false",
                "contains_endpoint_residuals": "false",
                "contains_new_endpoint_scores": "false",
                "contains_fit_statistics": "false",
                "contains_lambda_row_numeric_value": "false",
                "contains_t_joint_rescoring": "false",
                "verdict": "lambda_policy_review_package_ready_not_completed_not_scoring",
                "recommended_next_action": "send_zip_to_reviewer_before_any_numeric_lambda_or_rescoring",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    print(f"JOINT_ROW_LEVEL_LAMBDA_POLICY_REVIEW_PACKAGE_V1_BUILT sha256={digest}")


if __name__ == "__main__":
    main()
