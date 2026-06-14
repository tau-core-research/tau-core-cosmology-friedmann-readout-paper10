#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/joint_row_level_numeric_penalty_authorization_review_policy_v1.csv"
TEMPLATE = ROOT / "data/derived/joint_row_level_numeric_penalty_authorization_review_response_template_v1.csv"
PACKAGE = ROOT / "data/derived/joint_row_level_numeric_penalty_authorization_review_package_v1.zip"
SHA = ROOT / "data/derived/joint_row_level_numeric_penalty_authorization_review_package_v1.zip.sha256"
MANIFEST = ROOT / "data/derived/joint_row_level_numeric_penalty_authorization_review_package_v1_manifest.csv"
SUMMARY = ROOT / "data/derived/joint_row_level_numeric_penalty_authorization_review_package_v1_summary.csv"
DOC = ROOT / "docs/joint_row_level_numeric_penalty_authorization_review_package_v1.md"
V4_SUMMARY = ROOT / "data/derived/joint_row_level_penalty_protocol_shell_v4_summary.csv"
FORMULA_SUMMARY = ROOT / "data/derived/joint_symbolic_row_level_penalty_formula_shell_v1_summary.csv"
PACKAGE_ID = "JOINT_ROW_LEVEL_NUMERIC_PENALTY_AUTHORIZATION_REVIEW_PACKAGE_V1"
CLAIM_BOUNDARY = "joint_row_level_numeric_penalty_authorization_review_not_scoring_not_validation"

PACKAGE_FILES = [
    "docs/joint_row_level_numeric_penalty_authorization_review_package_v1.md",
    "data/source_manifest/joint_row_level_numeric_penalty_authorization_review_policy_v1.csv",
    "data/derived/joint_row_level_numeric_penalty_authorization_review_response_template_v1.csv",
    "data/derived/joint_row_level_penalty_protocol_shell_v4.csv",
    "data/derived/joint_row_level_penalty_protocol_shell_v4_summary.csv",
    "docs/joint_row_level_penalty_protocol_shell_v4.md",
    "data/derived/joint_symbolic_row_level_penalty_formula_shell_v1.csv",
    "data/derived/joint_symbolic_row_level_penalty_formula_shell_v1_summary.csv",
    "docs/joint_symbolic_row_level_penalty_formula_shell_v1.md",
    "data/derived/joint_row_level_penalty_block_weight_binding_shell_v1.csv",
    "data/derived/joint_row_level_penalty_block_weight_binding_shell_v1_summary.csv",
    "docs/joint_row_level_penalty_block_weight_binding_shell_v1.md",
    "data/derived/joint_candidate_control_symmetric_normalized_feature_transform_v1_summary.csv",
    "docs/joint_candidate_control_symmetric_normalized_feature_transform_v1.md",
    "data/derived/joint_channel_local_source_normalization_rule_v1.csv",
    "data/derived/joint_channel_local_source_normalization_rule_v1_summary.csv",
    "docs/joint_channel_local_source_normalization_rule_v1.md",
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
        "contains_numeric_penalty_values": "false",
        "contains_lambda_row_numeric_value": "false",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def main() -> None:
    v4 = read_one(V4_SUMMARY)
    formula = read_one(FORMULA_SUMMARY)
    if v4["verdict"] != "SYMBOLIC_ROW_LEVEL_PENALTY_READY_NUMERIC_AUTHORIZATION_STILL_OPEN":
        raise SystemExit("v4 protocol shell is not at the expected numeric-authorization gate")
    if v4["requirements_satisfied"] != "5" or v4["requirements_open"] != "1":
        raise SystemExit("v4 protocol shell must have exactly one open numeric authorization gate")
    if formula["penalty_formula_defined"] != "true":
        raise SystemExit("symbolic formula must be defined")
    if formula["penalty_computed"] != "false":
        raise SystemExit("symbolic formula shell must not compute penalty")
    if formula["numeric_t_joint_rescoring_allowed"] != "false":
        raise SystemExit("symbolic formula shell must not allow rescoring")

    policy_rows = [
        {
            "review_id": PACKAGE_ID,
            "question_id": "RNP_Q1_FORMULA_SCOPE",
            "question": "Is the symbolic row-level penalty formula sufficiently specified to authorize a later numeric computation package?",
            "required_response": "accept_or_reject",
            "acceptance_condition": "Accept only if the reviewer agrees that the formula is source-only, candidate/control symmetric, and not residual-derived.",
            "forbidden_inputs": "endpoint_residuals;new_endpoint_scores;fit_improvements;posterior_chains;post_score_control_ranks",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "RNP_Q2_LAMBDA_POLICY",
            "question": "May a future numeric package compute source-feature penalty values while keeping lambda_row unset or externally predeclared?",
            "required_response": "accept_with_caveats_or_reject",
            "acceptance_condition": "Accept only if lambda_row remains symbolic, zero, or separately predeclared before any endpoint-score comparison.",
            "forbidden_inputs": "endpoint_residuals;new_endpoint_scores;fit_improvements;posterior_chains;post_score_control_ranks",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "RNP_Q3_NUMERIC_VALUES_BOUNDARY",
            "question": "Should the next package be limited to computing P_i(a) and P_row(a) values, without modifying T_joint?",
            "required_response": "accept_or_reject",
            "acceptance_condition": "Accept only for penalty-value computation; reject if the next step would directly rescore T_joint.",
            "forbidden_inputs": "endpoint_residuals;new_endpoint_scores;fit_improvements;posterior_chains;post_score_control_ranks",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "RNP_Q4_CONTROL_SYMMETRY",
            "question": "Are the candidate/control symmetry requirements strong enough for numeric penalty computation?",
            "required_response": "accept_or_reject",
            "acceptance_condition": "Accept only if every candidate and matched control uses the same transform, same block weights, same formula, and same covariance/caveat discipline.",
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
            "numeric_penalty_computation_authorized": "false",
            "lambda_row_numeric_value_authorized": "false",
            "t_joint_rescoring_authorized": "false",
            "separate_numeric_package_required": "true",
        }
        for row in policy_rows
    ]
    write_csv(TEMPLATE, template_rows)

    DOC.write_text(
        "\n".join(
            [
                "# Joint row-level numeric penalty authorization review package v1",
                "",
                "**Doc class:** external authorization handoff.",
                "**Status:** not scoring; not endpoint validation; not cosmological validation.",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`.",
                "",
                "This package asks whether the symbolic source-only row-level penalty",
                "formula may be promoted into a later numeric penalty-value computation",
                "package. It does not compute penalty values and does not modify",
                "`T_joint`.",
                "",
                "Upstream status:",
                "",
                f"- v4 protocol verdict: `{v4['verdict']}`",
                f"- symbolic formula verdict: `{formula['verdict']}`",
                f"- formula family: `{formula['formula_family']}`",
                f"- channel formula: `{formula['channel_penalty_formula']}`",
                f"- joint formula: `{formula['joint_penalty_formula']}`",
                "",
                "Allowed next action if accepted: build a separate package that computes",
                "`P_i(a)` and `P_row(a)` from the frozen normalized source features for",
                "candidates and matched controls under the same transform and block",
                "weights.  `lambda_row` must remain unset or separately predeclared, and",
                "`T_joint` rescoring remains forbidden unless a later authorization gate",
                "explicitly permits it.",
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
                "status": "JOINT_ROW_LEVEL_NUMERIC_PENALTY_AUTHORIZATION_REVIEW_PACKAGE_READY_NOT_COMPLETED",
                "zip_path": str(PACKAGE.relative_to(ROOT)),
                "zip_sha256_path": str(SHA.relative_to(ROOT)),
                "zip_sha256": digest,
                "package_file_count": str(len(package_rows)),
                "review_completed": "false",
                "numeric_penalty_computation_authorized": "false",
                "lambda_row_numeric_value_authorized": "false",
                "t_joint_rescoring_authorized": "false",
                "endpoint_scoring_allowed": "false",
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "contains_endpoint_residuals": "false",
                "contains_new_endpoint_scores": "false",
                "contains_fit_statistics": "false",
                "contains_numeric_penalty_values": "false",
                "contains_lambda_row_numeric_value": "false",
                "verdict": "numeric_penalty_authorization_review_package_ready_not_completed_not_scoring",
                "recommended_next_action": "send_zip_to_reviewer_before_any_numeric_penalty_values_or_rescoring",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    print(f"JOINT_ROW_LEVEL_NUMERIC_PENALTY_AUTHORIZATION_REVIEW_PACKAGE_V1_BUILT sha256={digest}")


if __name__ == "__main__":
    main()
