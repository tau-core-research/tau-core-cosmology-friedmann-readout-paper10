#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ID = "JOINT_ROW_LEVEL_T_JOINT_RESCORING_AUTHORIZATION_REVIEW_PACKAGE_V1"
CLAIM_BOUNDARY = "joint_row_level_t_joint_rescoring_authorization_not_endpoint_scoring_not_validation"

READINESS = ROOT / "data/derived/joint_row_level_scoring_readiness_v1_summary.csv"
ALIGNED = ROOT / "data/derived/joint_row_level_aligned_control_values_v1_summary.csv"
LAMBDA = ROOT / "data/derived/joint_row_level_numeric_lambda_blocker_status_v1_summary.csv"
LAMBDA_RESPONSE = ROOT / "data/derived/joint_row_level_numeric_lambda_review_response_v1_summary.csv"
FORMULA = ROOT / "data/derived/joint_symbolic_row_level_penalty_formula_shell_v1_summary.csv"
POLICY = ROOT / "data/source_manifest/joint_row_level_t_joint_rescoring_authorization_policy_v1.csv"
TEMPLATE = ROOT / "data/derived/joint_row_level_t_joint_rescoring_authorization_response_template_v1.csv"
PACKAGE = ROOT / "data/derived/joint_row_level_t_joint_rescoring_authorization_review_package_v1.zip"
SHA = ROOT / "data/derived/joint_row_level_t_joint_rescoring_authorization_review_package_v1.zip.sha256"
MANIFEST = ROOT / "data/derived/joint_row_level_t_joint_rescoring_authorization_review_package_v1_manifest.csv"
SUMMARY = ROOT / "data/derived/joint_row_level_t_joint_rescoring_authorization_review_package_v1_summary.csv"
DOC = ROOT / "docs/joint_row_level_t_joint_rescoring_authorization_review_package_v1.md"

PACKAGE_FILES = [
    "docs/joint_row_level_t_joint_rescoring_authorization_review_package_v1.md",
    "data/source_manifest/joint_row_level_t_joint_rescoring_authorization_policy_v1.csv",
    "data/derived/joint_row_level_t_joint_rescoring_authorization_response_template_v1.csv",
    "data/derived/joint_row_level_scoring_readiness_v1_summary.csv",
    "data/derived/joint_row_level_scoring_readiness_v1.csv",
    "data/derived/joint_row_level_aligned_control_values_v1_summary.csv",
    "data/derived/joint_row_level_aligned_control_values_v1.csv",
    "data/derived/joint_row_level_numeric_lambda_blocker_status_v1_summary.csv",
    "data/derived/joint_row_level_numeric_lambda_review_response_v1_summary.csv",
    "data/derived/joint_symbolic_row_level_penalty_formula_shell_v1_summary.csv",
    "scripts/build_joint_row_level_t_joint_rescoring_authorization_review_package_v1.py",
    "scripts/validate_joint_row_level_t_joint_rescoring_authorization_review_package_v1.py",
]


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def one(path: Path) -> dict[str, str]:
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
        "contains_t_joint_penalized_values": "false",
        "contains_rescoring_authorization": "false",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def main() -> None:
    readiness = one(READINESS)
    aligned = one(ALIGNED)
    lambda_blocker = one(LAMBDA)
    lambda_response = one(LAMBDA_RESPONSE)
    formula = one(FORMULA)

    if readiness["verdict"] != "ROW_LEVEL_SCORING_NOT_READY_T_JOINT_RESCORING_AUTHORIZATION_MISSING":
        raise SystemExit("readiness ledger is not at rescoring-authorization-missing state")
    if aligned["verdict"] != "ALIGNED_CONTROL_VALUES_COMPUTED_NOT_RESCORING":
        raise SystemExit("aligned-control values are not ready")
    if lambda_blocker["verdict"] != "NUMERIC_LAMBDA_RECORDED_RESCORING_STILL_BLOCKED":
        raise SystemExit("numeric lambda is not recorded with rescoring blocked")
    if lambda_response["decision"] != "AUTHORIZE_NUMERIC_LAMBDA_RECORD_ONLY_NOT_RESCORING_NOT_VALIDATION":
        raise SystemExit("numeric lambda response is not accepted")
    if formula["future_score_shell"] != "T_joint_penalized(a)=T_joint(a)+lambda_row*P_row(a)":
        raise SystemExit("unexpected symbolic score shell")

    policy_rows = [
        {
            "review_id": PACKAGE_ID,
            "question_id": "RJRS_Q1_UPSTREAM_GATES",
            "question": "Are the aligned-control values and numeric lambda record-only gates complete enough to consider a separate rescoring authorization package?",
            "required_response": "accept_or_reject",
            "acceptance_condition": "Accept only if aligned controls are computed and lambda_row=1.0 is recorded, while endpoint scoring remains forbidden.",
            "forbidden_inputs": "endpoint_residuals;endpoint_scores;fit_improvements;posterior_chains;post_score_control_ranks",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "RJRS_Q2_RESCORING_PERMISSION",
            "question": "May a later guarded artifact compute record-only T_joint_penalized values from the frozen shell T_joint + lambda_row*P_row?",
            "required_response": "AUTHORIZE_RESCORING_LEDGER_ONLY_or_NO_GO",
            "acceptance_condition": "GO authorizes only a record-only penalized T_joint ledger; it does not authorize endpoint scoring or validation.",
            "forbidden_inputs": "endpoint_residuals;endpoint_scores;fit_improvements;posterior_chains;post_score_control_ranks",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "RJRS_Q3_BOUNDARY",
            "question": "Should endpoint scoring, endpoint validation, cosmological validation, and physical validation remain forbidden after this package?",
            "required_response": "accept_or_reject",
            "acceptance_condition": "Accept only if the package is treated as rescoring-ledger authorization, not endpoint scoring.",
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
                "upstream_gates_accepted": "false",
                "t_joint_rescoring_ledger_authorized": "false",
                "endpoint_scoring_authorized": "false",
                "endpoint_validation_claimed_by_reviewer": "false",
            }
            for row in policy_rows
        ],
    )

    DOC.write_text(
        "\n".join(
            [
                "# Joint row-level T_joint rescoring authorization review package v1",
                "",
                "**Doc class:** external rescoring-authorization handoff.",
                "**Status:** asks only for a future record-only penalized `T_joint` ledger; not endpoint scoring; not validation.",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`.",
                "",
                "Upstream gates now satisfy the prerequisites for asking a separate",
                "rescoring question:",
                "",
                f"- aligned controls: `{aligned['aligned_control_rows']}` rows, mean `P_row_control={aligned['P_row_control_mean']}`",
                f"- numeric lambda: `lambda_row={lambda_blocker['lambda_row_numeric_value']}`",
                f"- symbolic shell: `{formula['future_score_shell']}`",
                "",
                "This package does not compute `T_joint_penalized`, does not run endpoint",
                "scoring, and does not claim validation. A positive response would only",
                "permit a later guarded record-only penalized-statistic ledger.",
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
                "status": "JOINT_ROW_LEVEL_T_JOINT_RESCORING_AUTHORIZATION_REVIEW_PACKAGE_READY_NOT_COMPLETED",
                "zip_path": str(PACKAGE.relative_to(ROOT)),
                "zip_sha256_path": str(SHA.relative_to(ROOT)),
                "zip_sha256": digest,
                "package_file_count": str(len(package_rows)),
                "review_completed": "false",
                "aligned_control_values_ready": readiness["aligned_control_values_ready"],
                "numeric_lambda_ready": readiness["numeric_lambda_ready"],
                "lambda_row_numeric_value": readiness["lambda_row_numeric_value"],
                "t_joint_rescoring_ledger_authorized": "false",
                "endpoint_scoring_allowed": "false",
                "endpoint_validation_claimed": "false",
                "contains_endpoint_residuals": "false",
                "contains_new_endpoint_scores": "false",
                "contains_fit_statistics": "false",
                "contains_t_joint_penalized_values": "false",
                "verdict": "rescoring_authorization_package_ready_not_completed_not_endpoint_scoring",
                "recommended_next_action": "send_zip_to_reviewer_before_any_T_joint_penalized_computation",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    print(f"{PACKAGE_ID}_BUILT sha256={digest}")


if __name__ == "__main__":
    main()
