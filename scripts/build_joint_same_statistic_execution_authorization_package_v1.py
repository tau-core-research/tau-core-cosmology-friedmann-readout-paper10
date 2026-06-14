#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PERM_SUMMARY = ROOT / "data/derived/joint_same_statistic_guarded_permission_replay_package_v1_summary.csv"
PERM_POLICY = ROOT / "data/source_manifest/joint_same_statistic_guarded_permission_replay_policy_v1.csv"
OLD_EXEC = ROOT / "data/derived/joint_guarded_replay_execution_authorization_response_v1_summary.csv"
RUNNER = ROOT / "scripts/run_joint_guarded_replay_permission_only_v1.py"
RUNNER_VALIDATOR = ROOT / "scripts/validate_joint_guarded_replay_permission_only_v1.py"
POLICY = ROOT / "data/source_manifest/joint_same_statistic_execution_authorization_policy_v1.csv"
TEMPLATE = ROOT / "data/derived/joint_same_statistic_execution_authorization_response_template_v1.csv"
DOC = ROOT / "docs/joint_same_statistic_execution_authorization_package_v1.md"
MANIFEST = ROOT / "data/derived/joint_same_statistic_execution_authorization_package_v1_manifest.csv"
SUMMARY = ROOT / "data/derived/joint_same_statistic_execution_authorization_package_v1_summary.csv"
PACKAGE = ROOT / "data/derived/joint_same_statistic_execution_authorization_package_v1.zip"
SHA = ROOT / "data/derived/joint_same_statistic_execution_authorization_package_v1.zip.sha256"
CLAIM_BOUNDARY = "joint_same_statistic_execution_authorization_not_validation"
PACKAGE_ID = "JOINT_SAME_STATISTIC_EXECUTION_AUTHORIZATION_PACKAGE_V1"


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
        "contains_endpoint_residuals": "false",
        "contains_new_endpoint_scores": "false",
        "contains_fit_statistics": "false",
        "permission_only_execution_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def main() -> None:
    perm = read_one(PERM_SUMMARY)
    old_exec = read_one(OLD_EXEC)
    if perm["status"] != "JOINT_SAME_STATISTIC_GUARDED_PERMISSION_REPLAY_PACKAGE_READY_NOT_EXECUTED":
        raise SystemExit("same-statistic permission package is not ready")
    if perm["same_statistic_bound"] != "true" or perm["matched_controls_bound"] != "true":
        raise SystemExit("same-statistic and matched-control bindings are required")
    if perm["direct_execution_allowed"] != "false" or perm["endpoint_scoring_allowed"] != "false":
        raise SystemExit("permission package must not allow direct execution/scoring")
    if old_exec["decision"] != "AUTHORIZE_JOINT_GUARDED_REPLAY_PERMISSION_ONLY_EXECUTION_NOT_VALIDATION":
        raise SystemExit("legacy execution authorization is not available as a narrow reference")
    for field in ["endpoint_validation_claimed", "cosmological_validation_claimed", "physical_validation_claimed"]:
        if old_exec[field] != "false":
            raise SystemExit(f"legacy execution authorization unsafe field: {field}")

    forbidden = "endpoint_residuals;new_endpoint_scores;fit_improvements;posterior_chains;post_score_control_ranks;posthoc_channel_selection;posthoc_block_weight_tuning;posthoc_covariance_reweighting;cosmological_validation_claims"
    rows = [
        {
            "review_id": PACKAGE_ID,
            "question_id": "JSSE_Q1_EXECUTION_SCOPE",
            "question": "May the same-statistic guarded package be executed once using the existing permission-only runner?",
            "required_response": "authorize_one_permission_only_execution_or_reject",
            "acceptance_condition": "Accept only one permission-only execution; no validation claim is allowed.",
            "forbidden_inputs": forbidden,
            "permission_only_execution_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "JSSE_Q2_SAME_STATISTIC_BINDING",
            "question": "Must the execution remain bound to the same symbolic statistic and matched controls frozen in the package?",
            "required_response": "accept_same_statistic_execution_binding_or_reject",
            "acceptance_condition": "Accept only if candidate and controls remain tied to the same T_joint shell, row scope, q_i weights, signs, and standardization rule.",
            "forbidden_inputs": forbidden,
            "permission_only_execution_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "JSSE_Q3_CAVEATS",
            "question": "Must caveated block-diagonal covariance and cross-probe caveats remain attached to the output?",
            "required_response": "accept_caveated_output_boundary_or_reject",
            "acceptance_condition": "Accept only if the output remains caveated and cannot be read as source-native covariance validation.",
            "forbidden_inputs": forbidden,
            "permission_only_execution_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "JSSE_Q4_NO_VALIDATION",
            "question": "Must the replay output remain non-validation even if numerically positive?",
            "required_response": "accept_permission_only_no_validation_or_reject",
            "acceptance_condition": "Accept only if the strongest allowed output is a permission-only diagnostic replay result.",
            "forbidden_inputs": forbidden,
            "permission_only_execution_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_rows(POLICY, rows)
    template = [
        {
            **row,
            "review_completed": "false",
            "reviewer_id_or_role": "",
            "reviewer_response": "",
            "reviewer_rationale": "",
            "forbidden_inputs_used": "false",
        }
        for row in rows
    ]
    write_rows(TEMPLATE, template)
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Joint same-statistic execution authorization package v1",
                "",
                "**Doc class:** external authorization handoff.",
                "**Status:** prepared, not completed.",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`.",
                "",
                "This package asks whether one permission-only execution may be run after",
                "the same-statistic guarded package. It is not itself execution and does",
                "not claim endpoint, cosmological, or physical validation.",
                "",
                "The execution, if authorized, must remain tied to the same symbolic",
                "statistic `T_joint = sum_i q_i z_i`, same matched-control boundary, and",
                "same caveated block-diagonal covariance route.",
                "",
                "The strongest allowed output is a permission-only diagnostic replay.",
            ]
        )
        + "\n"
    )
    inputs = [POLICY, TEMPLATE, DOC, PERM_SUMMARY, PERM_POLICY, OLD_EXEC, RUNNER, RUNNER_VALIDATOR]
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
                "status": "JOINT_SAME_STATISTIC_EXECUTION_AUTHORIZATION_PACKAGE_READY_NOT_COMPLETED",
                "zip_path": rel(PACKAGE),
                "zip_sha256_path": rel(SHA),
                "zip_sha256": digest,
                "package_file_count": str(len(package_rows)),
                "review_completed": "false",
                "permission_only_execution_allowed": "false",
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "contains_endpoint_residuals": "false",
                "contains_new_endpoint_scores": "false",
                "contains_fit_statistics": "false",
                "verdict": "same_statistic_execution_authorization_package_ready_not_completed_not_validation",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    print(f"JOINT_SAME_STATISTIC_EXECUTION_AUTHORIZATION_PACKAGE_V1_BUILT sha256={digest}")


if __name__ == "__main__":
    main()
