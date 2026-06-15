#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ID = "JOINT_ROW_LEVEL_ALIGNED_CONTROL_VALUE_AUTHORIZATION_REVIEW_PACKAGE_V1"
CLAIM_BOUNDARY = "joint_row_level_aligned_control_value_authorization_not_values_not_scoring_not_validation"

ALIGN_RESPONSE = ROOT / "data/derived/joint_row_level_cross_channel_control_alignment_review_response_v1_summary.csv"
ALIGN_BLOCKER = ROOT / "data/derived/joint_row_level_cross_channel_control_alignment_blocker_status_v1_summary.csv"
ALIGN_DIAG = ROOT / "data/derived/joint_row_level_cross_channel_control_alignment_diagnostic_v1_summary.csv"
VALUES_SUMMARY = ROOT / "data/derived/joint_row_level_numeric_penalty_values_v1_summary.csv"
VALUES = ROOT / "data/derived/joint_row_level_numeric_penalty_values_v1.csv"
POLICY = ROOT / "data/source_manifest/joint_row_level_aligned_control_value_authorization_policy_v1.csv"
TEMPLATE = ROOT / "data/derived/joint_row_level_aligned_control_value_authorization_response_template_v1.csv"
PACKAGE = ROOT / "data/derived/joint_row_level_aligned_control_value_authorization_review_package_v1.zip"
SHA = ROOT / "data/derived/joint_row_level_aligned_control_value_authorization_review_package_v1.zip.sha256"
MANIFEST = ROOT / "data/derived/joint_row_level_aligned_control_value_authorization_review_package_v1_manifest.csv"
SUMMARY = ROOT / "data/derived/joint_row_level_aligned_control_value_authorization_review_package_v1_summary.csv"
DOC = ROOT / "docs/joint_row_level_aligned_control_value_authorization_review_package_v1.md"
AUTH_DIAG = ROOT / "data/derived/joint_row_level_aligned_control_value_authorization_diagnostic_v1.csv"
AUTH_DIAG_SUMMARY = ROOT / "data/derived/joint_row_level_aligned_control_value_authorization_diagnostic_v1_summary.csv"

PACKAGE_FILES = [
    "docs/joint_row_level_aligned_control_value_authorization_review_package_v1.md",
    "data/source_manifest/joint_row_level_aligned_control_value_authorization_policy_v1.csv",
    "data/derived/joint_row_level_aligned_control_value_authorization_response_template_v1.csv",
    "data/derived/joint_row_level_aligned_control_value_authorization_diagnostic_v1.csv",
    "data/derived/joint_row_level_aligned_control_value_authorization_diagnostic_v1_summary.csv",
    "data/derived/joint_row_level_cross_channel_control_alignment_review_response_v1_summary.csv",
    "data/derived/joint_row_level_cross_channel_control_alignment_blocker_status_v1_summary.csv",
    "data/derived/joint_row_level_cross_channel_control_alignment_diagnostic_v1_summary.csv",
    "data/derived/joint_row_level_numeric_penalty_values_v1_summary.csv",
    "data/derived/joint_row_level_numeric_penalty_values_v1.csv",
    "scripts/build_joint_row_level_aligned_control_value_authorization_review_package_v1.py",
    "scripts/validate_joint_row_level_aligned_control_value_authorization_review_package_v1.py",
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
    is_values = rel.endswith("joint_row_level_numeric_penalty_values_v1.csv")
    return {
        "package_id": PACKAGE_ID,
        "package_path": rel,
        "byte_count": str(path.stat().st_size),
        "sha256": sha256(path),
        "contains_endpoint_residuals": "false",
        "contains_new_endpoint_scores": "false",
        "contains_fit_statistics": "false",
        "contains_channel_local_penalty_values": "true" if is_values else "false",
        "contains_aligned_joint_control_values": "false",
        "contains_lambda_row_numeric_value": "false",
        "contains_t_joint_rescoring": "false",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def main() -> None:
    align_response = read_one(ALIGN_RESPONSE)
    align_blocker = read_one(ALIGN_BLOCKER)
    align_diag = read_one(ALIGN_DIAG)
    values = read_one(VALUES_SUMMARY)

    if align_response["decision"] != "ACCEPT_CROSS_CHANNEL_CONTROL_ALIGNMENT_DESIGN_NOT_VALUES_NOT_RESCORING_NOT_VALIDATION":
        raise SystemExit("cross-channel alignment design review is not accepted")
    if align_blocker["verdict"] != "CROSS_CHANNEL_ALIGNMENT_DESIGN_ACCEPTED_VALUES_STILL_BLOCKED":
        raise SystemExit("cross-channel blocker is not at values-still-blocked state")
    if align_diag["alignment_values_computed"] != "false":
        raise SystemExit("alignment diagnostic must not already contain aligned values")
    if values["verdict"] != "NUMERIC_PENALTY_VALUES_COMPUTED_NOT_RESCORING":
        raise SystemExit("channel-local numeric penalty values are not available")

    value_rows = read_rows(VALUES)
    control_rows = [row for row in value_rows if row.get("row_type") != "candidate"]
    candidate_rows = [row for row in value_rows if row.get("row_type") == "candidate"]
    active_channels = align_diag["active_channels"].split("|")
    min_count = int(align_diag["min_index_aligned_count_if_accepted"])

    auth_diag_rows = [
        {
            "diagnostic_id": "JRL_ALIGNED_CONTROL_VALUE_AUTHORIZATION_DIAGNOSTIC_V1",
            "quantity": "alignment_rule",
            "value": align_diag["proposed_alignment_rule"],
            "source": str(ALIGN_DIAG.relative_to(ROOT)),
            "aligned_values_computed": "false",
            "lambda_row_numeric_value_authorized": "false",
            "t_joint_rescoring_authorized": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "diagnostic_id": "JRL_ALIGNED_CONTROL_VALUE_AUTHORIZATION_DIAGNOSTIC_V1",
            "quantity": "active_channels",
            "value": "|".join(active_channels),
            "source": str(ALIGN_DIAG.relative_to(ROOT)),
            "aligned_values_computed": "false",
            "lambda_row_numeric_value_authorized": "false",
            "t_joint_rescoring_authorized": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "diagnostic_id": "JRL_ALIGNED_CONTROL_VALUE_AUTHORIZATION_DIAGNOSTIC_V1",
            "quantity": "min_aligned_control_count_if_later_authorized",
            "value": str(min_count),
            "source": str(ALIGN_DIAG.relative_to(ROOT)),
            "aligned_values_computed": "false",
            "lambda_row_numeric_value_authorized": "false",
            "t_joint_rescoring_authorized": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(AUTH_DIAG, auth_diag_rows)
    write_csv(
        AUTH_DIAG_SUMMARY,
        [
            {
                "diagnostic_id": "JRL_ALIGNED_CONTROL_VALUE_AUTHORIZATION_DIAGNOSTIC_V1",
                "alignment_design_decision": align_response["decision"],
                "blocker_verdict": align_blocker["verdict"],
                "active_channels": "|".join(active_channels),
                "control_rows_available": str(len(control_rows)),
                "candidate_rows_available": str(len(candidate_rows)),
                "min_aligned_control_count_if_later_authorized": str(min_count),
                "alignment_values_computed": "false",
                "aligned_joint_control_values_authorized": "false",
                "lambda_row_numeric_value_authorized": "false",
                "t_joint_rescoring_authorized": "false",
                "endpoint_validation_claimed": "false",
                "verdict": "ALIGNED_CONTROL_VALUE_AUTHORIZATION_PACKAGE_READY_NOT_COMPLETED_NOT_VALUES",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )

    policy_rows = [
        {
            "review_id": PACKAGE_ID,
            "question_id": "ACV_Q1_UPSTREAM_DESIGN",
            "question": "Does the completed design review permit preparing a separate residual-blind aligned-control value authorization package?",
            "required_response": "accept_or_reject",
            "acceptance_condition": "Accept only if the reviewer agrees this package is downstream of the accepted design review and still contains no aligned values.",
            "forbidden_inputs": "endpoint_residuals;endpoint_scores;fit_improvements;posterior_chains;post_score_control_ranks",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "ACV_Q2_VALUE_COMPUTATION_PERMISSION",
            "question": "May a later script compute aligned joint-control values using only the deterministic min-count index alignment rule and channel-local penalty values?",
            "required_response": "AUTHORIZE_ALIGNED_CONTROL_VALUE_COMPUTATION_ONLY_or_NO_GO",
            "acceptance_condition": "GO authorizes only a later aligned-control value computation; it does not authorize lambda_row, T_joint rescoring, endpoint scoring, or validation.",
            "forbidden_inputs": "endpoint_residuals;endpoint_scores;fit_improvements;posterior_chains;post_score_control_ranks",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "ACV_Q3_CONTROL_COUNT_CAVEAT",
            "question": "Is the min-count alignment caveat acceptable for a value-computation-only package?",
            "required_response": "accept_with_caveats_or_reject",
            "acceptance_condition": "Accept only if the reviewer records the control-count caveat and agrees it is not an endpoint-validating statistic.",
            "forbidden_inputs": "endpoint_residuals;endpoint_scores;fit_improvements;posterior_chains;post_score_control_ranks",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "ACV_Q4_BOUNDARY",
            "question": "Should lambda_row, T_joint rescoring, endpoint scoring, and validation remain forbidden after this package?",
            "required_response": "accept_or_reject",
            "acceptance_condition": "Accept only if all rescoring and validation flags remain false.",
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
                "upstream_design_accepted": "false",
                "aligned_control_value_computation_authorized": "false",
                "aligned_joint_control_values_authorized": "false",
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
                "# Joint row-level aligned-control value authorization review package v1",
                "",
                "**Doc class:** external authorization handoff.",
                "**Status:** authorization to compute aligned control values only; no aligned values yet; not `lambda_row`; not `T_joint` rescoring; not endpoint validation.",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`.",
                "",
                "The previous cross-channel alignment design review has been completed.",
                "It accepted the deterministic design but kept aligned values blocked.",
                "This package is the next narrow gate: it asks whether a later script may",
                "compute aligned joint-control values from source-frozen channel-local",
                "penalty values using that deterministic rule.",
                "",
                "It does not contain aligned joint-control values.",
                "It does not choose a numeric `lambda_row`.",
                "It does not rescore `T_joint`.",
                "It does not authorize endpoint scoring or validation.",
                "",
                "Frozen proposed rule:",
                "",
                f"`{align_diag['proposed_alignment_rule']}`",
                "",
                "Current diagnostic state:",
                "",
                f"- alignment design decision: `{align_response['decision']}`",
                f"- blocker verdict: `{align_blocker['verdict']}`",
                f"- active channels: `{ '|'.join(active_channels) }`",
                f"- control rows available: `{len(control_rows)}`",
                f"- candidate rows available: `{len(candidate_rows)}`",
                f"- min aligned control count if later authorized: `{min_count}`",
                "",
                "A positive response may only authorize the later value-computation",
                "artifact. A separate numeric-lambda gate and a separate rescoring gate",
                "would still be required before any penalized `T_joint` result.",
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
                "status": "JOINT_ROW_LEVEL_ALIGNED_CONTROL_VALUE_AUTHORIZATION_REVIEW_PACKAGE_READY_NOT_COMPLETED",
                "zip_path": str(PACKAGE.relative_to(ROOT)),
                "zip_sha256_path": str(SHA.relative_to(ROOT)),
                "zip_sha256": digest,
                "package_file_count": str(len(package_rows)),
                "review_completed": "false",
                "upstream_design_accepted": "true",
                "aligned_control_value_computation_authorized": "false",
                "aligned_joint_control_values_authorized": "false",
                "lambda_row_numeric_value_authorized": "false",
                "t_joint_rescoring_authorized": "false",
                "endpoint_scoring_allowed": "false",
                "endpoint_validation_claimed": "false",
                "contains_endpoint_residuals": "false",
                "contains_new_endpoint_scores": "false",
                "contains_fit_statistics": "false",
                "contains_channel_local_penalty_values": "true",
                "contains_aligned_joint_control_values": "false",
                "contains_lambda_row_numeric_value": "false",
                "contains_t_joint_rescoring": "false",
                "verdict": "aligned_control_value_authorization_package_ready_not_completed_not_values_not_scoring",
                "recommended_next_action": "send_zip_to_reviewer_before_any_aligned_control_value_computation",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    print(f"{PACKAGE_ID}_BUILT sha256={digest}")


if __name__ == "__main__":
    main()
