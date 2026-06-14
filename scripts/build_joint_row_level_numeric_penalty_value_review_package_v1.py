#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ID = "JOINT_ROW_LEVEL_NUMERIC_PENALTY_VALUE_REVIEW_PACKAGE_V1"
CLAIM_BOUNDARY = "joint_row_level_numeric_penalty_value_review_not_rescoring_not_validation"

POLICY = ROOT / "data/source_manifest/joint_row_level_numeric_penalty_value_review_policy_v1.csv"
TEMPLATE = ROOT / "data/derived/joint_row_level_numeric_penalty_value_review_response_template_v1.csv"
PACKAGE = ROOT / "data/derived/joint_row_level_numeric_penalty_value_review_package_v1.zip"
SHA = ROOT / "data/derived/joint_row_level_numeric_penalty_value_review_package_v1.zip.sha256"
MANIFEST = ROOT / "data/derived/joint_row_level_numeric_penalty_value_review_package_v1_manifest.csv"
SUMMARY = ROOT / "data/derived/joint_row_level_numeric_penalty_value_review_package_v1_summary.csv"
DOC = ROOT / "docs/joint_row_level_numeric_penalty_value_review_package_v1.md"
VALUE_SUMMARY = ROOT / "data/derived/joint_row_level_numeric_penalty_values_v1_summary.csv"

PACKAGE_FILES = [
    "docs/joint_row_level_numeric_penalty_value_review_package_v1.md",
    "data/source_manifest/joint_row_level_numeric_penalty_value_review_policy_v1.csv",
    "data/derived/joint_row_level_numeric_penalty_value_review_response_template_v1.csv",
    "data/derived/joint_row_level_numeric_penalty_values_v1.csv",
    "data/derived/joint_row_level_numeric_penalty_values_joint_v1.csv",
    "data/derived/joint_row_level_numeric_penalty_values_v1_summary.csv",
    "docs/joint_row_level_numeric_penalty_values_v1.md",
    "scripts/build_joint_row_level_numeric_penalty_values_v1.py",
    "scripts/validate_joint_row_level_numeric_penalty_values_v1.py",
    "data/derived/joint_candidate_control_symmetric_normalized_feature_transform_v1_summary.csv",
    "data/derived/joint_row_level_penalty_block_weight_binding_shell_v1.csv",
    "data/derived/joint_row_level_numeric_penalty_authorization_review_response_v1_summary.csv",
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
        "contains_numeric_penalty_values": "true" if "numeric_penalty_values" in rel else "false",
        "contains_lambda_row_numeric_value": "false",
        "t_joint_rescoring_allowed": "false",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def main() -> None:
    values = read_one(VALUE_SUMMARY)
    if values["verdict"] != "NUMERIC_PENALTY_VALUES_COMPUTED_NOT_RESCORING":
        raise SystemExit("numeric penalty values are not at review-ready status")
    for key in [
        "lambda_row_numeric_value_defined",
        "t_joint_rescoring_allowed",
        "endpoint_scoring_allowed",
        "endpoint_validation_claimed",
    ]:
        if values[key] != "false":
            raise SystemExit(f"{key} must remain false")

    policy_rows = [
        {
            "review_id": PACKAGE_ID,
            "question_id": "NPV_Q1_REPRODUCIBILITY",
            "question": "Do the included scripts and artifacts reproduce the reported P_i and candidate P_row values?",
            "required_response": "accept_or_reject",
            "acceptance_condition": "Accept only if the reviewer can reproduce the values without endpoint residuals, endpoint scores, or fit statistics.",
            "forbidden_inputs": "endpoint_residuals;endpoint_scores;fit_improvements;posterior_chains;post_score_control_ranks",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "NPV_Q2_CONTROL_SCOPE",
            "question": "Is the control handling correctly limited to channel-local penalty values in this package?",
            "required_response": "accept_or_reject",
            "acceptance_condition": "Accept only if the reviewer agrees that no cross-channel control alignment is introduced here.",
            "forbidden_inputs": "endpoint_residuals;endpoint_scores;fit_improvements;posterior_chains;post_score_control_ranks",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "NPV_Q3_BOUNDARY",
            "question": "Does the package keep lambda_row, T_joint rescoring, endpoint scoring, and validation claims forbidden?",
            "required_response": "accept_or_reject",
            "acceptance_condition": "Accept only if all boundary flags remain false and the package is treated as a diagnostic value package.",
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
                "numeric_penalty_values_accepted": "false",
                "cross_channel_control_alignment_authorized": "false",
                "lambda_row_numeric_value_authorized": "false",
                "t_joint_rescoring_authorized": "false",
            }
            for row in policy_rows
        ],
    )

    DOC.write_text(
        "\n".join(
            [
                "# Joint row-level numeric penalty value review package v1",
                "",
                "**Doc class:** external value-audit handoff.",
                "**Status:** numeric penalty values only; not `lambda_row`; not `T_joint` rescoring; not endpoint validation.",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`.",
                "",
                "This package asks a reviewer to audit the already computed numeric",
                "row-level penalty values. It does not ask for permission to use a",
                "numeric `lambda_row`, modify `T_joint`, replay an endpoint, or make a",
                "validation claim.",
                "",
                "Current value summary:",
                "",
                f"- feature rows read: `{values['feature_rows_read']}`",
                f"- channel penalty rows: `{values['channel_penalty_rows']}`",
                f"- candidate channel penalty rows: `{values['candidate_channel_penalty_rows']}`",
                f"- control channel penalty rows: `{values['control_channel_penalty_rows']}`",
                f"- complete joint penalty rows: `{values['complete_joint_penalty_rows']}`",
                f"- candidate `P_row`: `{values['P_row_candidate']}`",
                "",
                "Review focus:",
                "",
                "1. Reproduce the values from the included scripts and artifacts.",
                "2. Confirm that controls remain channel-local in this package.",
                "3. Confirm that no endpoint residuals, endpoint scores, or fit",
                "   statistics enter the value computation.",
                "4. Confirm that all rescoring and validation flags remain false.",
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
                "status": "JOINT_ROW_LEVEL_NUMERIC_PENALTY_VALUE_REVIEW_PACKAGE_READY_NOT_COMPLETED",
                "zip_path": str(PACKAGE.relative_to(ROOT)),
                "zip_sha256_path": str(SHA.relative_to(ROOT)),
                "zip_sha256": digest,
                "package_file_count": str(len(package_rows)),
                "review_completed": "false",
                "numeric_penalty_values_accepted": "false",
                "cross_channel_control_alignment_authorized": "false",
                "lambda_row_numeric_value_authorized": "false",
                "t_joint_rescoring_authorized": "false",
                "endpoint_scoring_allowed": "false",
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "contains_endpoint_residuals": "false",
                "contains_new_endpoint_scores": "false",
                "contains_fit_statistics": "false",
                "contains_numeric_penalty_values": "true",
                "contains_lambda_row_numeric_value": "false",
                "verdict": "numeric_penalty_value_review_package_ready_not_completed_not_scoring",
                "recommended_next_action": "send_zip_to_reviewer_before_any_lambda_or_rescoring",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    print(f"JOINT_ROW_LEVEL_NUMERIC_PENALTY_VALUE_REVIEW_PACKAGE_V1_BUILT sha256={digest}")


if __name__ == "__main__":
    main()
