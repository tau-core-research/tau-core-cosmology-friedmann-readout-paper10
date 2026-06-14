#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ID = "JOINT_ROW_LEVEL_PENALTY_USE_AUTHORIZATION_REVIEW_PACKAGE_V1"
CLAIM_BOUNDARY = "joint_row_level_penalty_use_authorization_review_not_scoring_not_validation"

POLICY = ROOT / "data/source_manifest/joint_row_level_penalty_use_authorization_review_policy_v1.csv"
TEMPLATE = ROOT / "data/derived/joint_row_level_penalty_use_authorization_review_response_template_v1.csv"
PACKAGE = ROOT / "data/derived/joint_row_level_penalty_use_authorization_review_package_v1.zip"
SHA = ROOT / "data/derived/joint_row_level_penalty_use_authorization_review_package_v1.zip.sha256"
MANIFEST = ROOT / "data/derived/joint_row_level_penalty_use_authorization_review_package_v1_manifest.csv"
SUMMARY = ROOT / "data/derived/joint_row_level_penalty_use_authorization_review_package_v1_summary.csv"
DOC = ROOT / "docs/joint_row_level_penalty_use_authorization_review_package_v1.md"
VALUES_SUMMARY = ROOT / "data/derived/joint_row_level_numeric_penalty_values_v1_summary.csv"
VALUE_REVIEW_SUMMARY = ROOT / "data/derived/joint_row_level_numeric_penalty_value_review_response_v1_summary.csv"
VALUE_BLOCKER_SUMMARY = ROOT / "data/derived/joint_row_level_numeric_penalty_value_review_blocker_status_v1_summary.csv"

PACKAGE_FILES = [
    "docs/joint_row_level_penalty_use_authorization_review_package_v1.md",
    "data/source_manifest/joint_row_level_penalty_use_authorization_review_policy_v1.csv",
    "data/derived/joint_row_level_penalty_use_authorization_review_response_template_v1.csv",
    "data/derived/joint_row_level_numeric_penalty_values_v1_summary.csv",
    "data/derived/joint_row_level_numeric_penalty_values_joint_v1.csv",
    "data/derived/joint_row_level_numeric_penalty_value_review_response_v1_summary.csv",
    "data/derived/joint_row_level_numeric_penalty_value_review_blocker_status_v1_summary.csv",
    "docs/joint_row_level_numeric_penalty_value_review_blocker_status_v1.md",
    "data/derived/joint_symbolic_row_level_penalty_formula_shell_v1_summary.csv",
    "data/derived/joint_row_level_penalty_protocol_shell_v4_summary.csv",
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
        "contains_t_joint_rescoring": "false",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def main() -> None:
    values = read_one(VALUES_SUMMARY)
    review = read_one(VALUE_REVIEW_SUMMARY)
    blocker = read_one(VALUE_BLOCKER_SUMMARY)
    if values["verdict"] != "NUMERIC_PENALTY_VALUES_COMPUTED_NOT_RESCORING":
        raise SystemExit("numeric values are not in expected computed-not-rescoring state")
    if review["decision"] != "ACCEPT_NUMERIC_PENALTY_VALUES_NOT_LAMBDA_NOT_T_JOINT_RESCORING_NOT_VALIDATION":
        raise SystemExit("numeric values have not been accepted by review")
    if blocker["verdict"] != "NUMERIC_PENALTY_VALUES_ACCEPTED_FOR_RECORD_ONLY_NEXT_USE_BLOCKED":
        raise SystemExit("next use is not properly blocked")
    for key in [
        "cross_channel_control_alignment_authorized",
        "lambda_row_numeric_value_authorized",
        "t_joint_rescoring_authorized",
        "endpoint_validation_claimed",
    ]:
        if blocker[key] != "false":
            raise SystemExit(f"unsafe blocker field: {key}")

    policy_rows = [
        {
            "review_id": PACKAGE_ID,
            "question_id": "PUA_Q1_VALUES_AS_PRECONDITION",
            "question": "May the accepted numeric penalty values be treated as a precondition for a later use-policy review, without being used for scoring here?",
            "required_response": "accept_or_reject",
            "acceptance_condition": "Accept only if the values remain record-only in this package and no score is changed.",
            "forbidden_inputs": "endpoint_residuals;endpoint_scores;fit_improvements;posterior_chains;post_score_control_ranks",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "PUA_Q2_CROSS_CHANNEL_CONTROL_BLOCKER",
            "question": "Must cross-channel control alignment remain a required blocker before any penalized joint score can be used?",
            "required_response": "accept_or_reject",
            "acceptance_condition": "Accept only if the reviewer agrees that channel-local controls are insufficient for a penalized joint score.",
            "forbidden_inputs": "endpoint_residuals;endpoint_scores;fit_improvements;posterior_chains;post_score_control_ranks",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "PUA_Q3_LAMBDA_POLICY_ROUTE",
            "question": "May a future package propose a residual-blind lambda_row policy, while this package keeps lambda_row unset?",
            "required_response": "accept_with_caveats_or_reject",
            "acceptance_condition": "Accept only if lambda_row remains unset here and any future value must be predeclared without endpoint-score feedback.",
            "forbidden_inputs": "endpoint_residuals;endpoint_scores;fit_improvements;posterior_chains;post_score_control_ranks",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "PUA_Q4_RESCORING_ROUTE",
            "question": "Should T_joint rescoring remain forbidden until both lambda_row policy and cross-channel controls are separately accepted?",
            "required_response": "accept_or_reject",
            "acceptance_condition": "Accept only if this package does not authorize rescoring and keeps endpoint replay blocked.",
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
                "values_as_precondition_accepted": "false",
                "cross_channel_control_alignment_required": "false",
                "future_lambda_policy_package_allowed": "false",
                "lambda_row_numeric_value_authorized": "false",
                "t_joint_rescoring_authorized": "false",
                "endpoint_replay_allowed": "false",
            }
            for row in policy_rows
        ],
    )

    DOC.write_text(
        "\n".join(
            [
                "# Joint row-level penalty use authorization review package v1",
                "",
                "**Doc class:** external authorization handoff.",
                "**Status:** use-policy review only; not `lambda_row`; not `T_joint` rescoring; not endpoint validation.",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`.",
                "",
                "The numeric row-level penalty values have been computed and accepted",
                "for the record. The current blocker remains: they cannot be used in a",
                "penalized joint statistic until a separate policy binds both a",
                "residual-blind `lambda_row` route and a cross-channel control",
                "alignment route.",
                "",
                "Current accepted value state:",
                "",
                f"- candidate `P_row`: `{values['P_row_candidate']}`",
                f"- channel penalty rows: `{values['channel_penalty_rows']}`",
                f"- control channel rows: `{values['control_channel_penalty_rows']}`",
                f"- value review decision: `{review['decision']}`",
                f"- blocker verdict: `{blocker['verdict']}`",
                "",
                "This package asks whether the next route may be planned. It does not",
                "choose `lambda_row`, does not align controls, does not rescore",
                "`T_joint`, and does not authorize endpoint replay.",
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
                "status": "JOINT_ROW_LEVEL_PENALTY_USE_AUTHORIZATION_REVIEW_PACKAGE_READY_NOT_COMPLETED",
                "zip_path": str(PACKAGE.relative_to(ROOT)),
                "zip_sha256_path": str(SHA.relative_to(ROOT)),
                "zip_sha256": digest,
                "package_file_count": str(len(package_rows)),
                "review_completed": "false",
                "values_as_precondition_accepted": "false",
                "cross_channel_control_alignment_required": "false",
                "future_lambda_policy_package_allowed": "false",
                "lambda_row_numeric_value_authorized": "false",
                "t_joint_rescoring_authorized": "false",
                "endpoint_replay_allowed": "false",
                "endpoint_scoring_allowed": "false",
                "endpoint_validation_claimed": "false",
                "contains_endpoint_residuals": "false",
                "contains_new_endpoint_scores": "false",
                "contains_fit_statistics": "false",
                "contains_numeric_penalty_values": "true",
                "contains_lambda_row_numeric_value": "false",
                "contains_t_joint_rescoring": "false",
                "verdict": "penalty_use_authorization_review_package_ready_not_completed_not_scoring",
                "recommended_next_action": "send_zip_to_reviewer_before_any_lambda_or_rescoring_policy",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    print(f"JOINT_ROW_LEVEL_PENALTY_USE_AUTHORIZATION_REVIEW_PACKAGE_V1_BUILT sha256={digest}")


if __name__ == "__main__":
    main()
