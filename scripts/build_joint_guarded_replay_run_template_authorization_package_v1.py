#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/joint_guarded_replay_run_template_authorization_policy_v1.csv"
TEMPLATE = ROOT / "data/derived/joint_guarded_replay_run_template_authorization_response_template_v1.csv"
SUMMARY = ROOT / "data/derived/joint_guarded_replay_run_template_authorization_package_v1_summary.csv"
MANIFEST = ROOT / "data/derived/joint_guarded_replay_run_template_authorization_package_v1_manifest.csv"
PACKAGE = ROOT / "data/derived/joint_guarded_replay_run_template_authorization_package_v1.zip"
SHA = ROOT / "data/derived/joint_guarded_replay_run_template_authorization_package_v1.zip.sha256"
DOC = ROOT / "docs/joint_guarded_replay_run_template_authorization_package_v1.md"
RUN_TEMPLATE = ROOT / "data/source_manifest/joint_guarded_replay_run_template_v1.csv"
RUN_TEMPLATE_SUMMARY = ROOT / "data/derived/joint_guarded_replay_run_template_v1_summary.csv"
RUN_TEMPLATE_DOC = ROOT / "docs/joint_guarded_replay_run_template_v1.md"
PERMISSION_RESPONSE = ROOT / "data/derived/joint_guarded_permission_replay_authorization_response_v1_summary.csv"
SCORING_AUTH_RESPONSE = ROOT / "data/derived/joint_block_diagonal_scoring_authorization_review_response_v1_summary.csv"
CLAIM_BOUNDARY = "joint_guarded_replay_run_template_authorization_not_execution_not_scoring_not_validation"
PACKAGE_ID = "JOINT_GUARDED_REPLAY_RUN_TEMPLATE_AUTHORIZATION_PACKAGE_V1"


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


def write_rows(path: Path, rows: list[dict[str, str]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
    if fieldnames is None:
        fieldnames = list(rows[0])
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_one(path: Path, row: dict[str, str]) -> None:
    write_rows(path, [row], list(row))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def require_false(row: dict[str, str], fields: list[str], label: str) -> None:
    for field in fields:
        if row.get(field) != "false":
            raise SystemExit(f"{label} {field} must be false")


def main() -> None:
    run_template = read_one(RUN_TEMPLATE)
    run_summary = read_one(RUN_TEMPLATE_SUMMARY)
    permission = read_one(PERMISSION_RESPONSE)
    scoring_auth = read_one(SCORING_AUTH_RESPONSE)

    if run_summary["status"] != "JOINT_GUARDED_REPLAY_RUN_TEMPLATE_READY_NOT_EXECUTED":
        raise SystemExit("run template must be ready-not-executed")
    if run_template["run_template_only"] != "true":
        raise SystemExit("run template must remain template-only")
    require_false(
        run_template,
        [
            "direct_execution_allowed",
            "endpoint_scoring_allowed",
            "endpoint_validation_claimed",
            "cosmological_validation_claimed",
        ],
        "run_template",
    )
    if permission["decision"] != "AUTHORIZE_GUARDED_PERMISSION_REPLAY_PACKAGE_PREPARATION_ONLY_NOT_EXECUTION_NOT_SCORING_NOT_VALIDATION":
        raise SystemExit("permission response is not in preparation-only state")
    if scoring_auth["decision"] != "AUTHORIZE_SEPARATE_GUARDED_JOINT_PERMISSION_REPLAY_PACKAGE_NOT_SCORING_NOT_VALIDATION":
        raise SystemExit("scoring authorization response is not in permission-only state")

    forbidden = "endpoint_residuals;new_endpoint_scores;fit_improvements;posterior_chains;post_score_control_ranks;posthoc_channel_selection;posthoc_block_weight_tuning;posthoc_covariance_reweighting;cosmological_validation_claims"
    policy_rows = [
        {
            "review_id": PACKAGE_ID,
            "question_id": "JGRT_Q1_TEMPLATE_SCOPE",
            "question": "May this frozen joint guarded replay run-template be promoted to an executable permission-only replay plan?",
            "required_response": "authorize_template_for_separate_permission_only_replay_or_reject",
            "acceptance_condition": "Authorize only if execution remains a separate downstream act and the current package itself is not treated as scoring or validation.",
            "forbidden_inputs": forbidden,
            "direct_execution_allowed_by_this_package": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "JGRT_Q2_IDENTICAL_STATISTIC",
            "question": "Are candidate and all controls bound to the same frozen block-diagonal statistic and block weights?",
            "required_response": "accept_identical_statistic_and_weights_or_reject",
            "acceptance_condition": "Accept only if candidate, shuffled-channel, wrong-channel, sign-flip, block-drop, null/readout, leakage, shared-statistic, and covariance-binding controls use the same statistic and weights.",
            "forbidden_inputs": forbidden,
            "direct_execution_allowed_by_this_package": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "JGRT_Q3_COVARIANCE_CAVEATS",
            "question": "Do all cross-probe covariance and block-diagonal caveats remain attached to any later permission-only replay?",
            "required_response": "accept_caveated_block_diagonal_conditions_or_reject",
            "acceptance_condition": "Accept only if missing source-native cross-probe covariance, block-diagonal independence, sky/mask overlap, redshift-kernel overlap, shared cosmology/nuisance, calibration, and population caveats remain attached.",
            "forbidden_inputs": forbidden,
            "direct_execution_allowed_by_this_package": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "JGRT_Q4_NO_VALIDATION_CLAIM",
            "question": "Is any future replay under this template limited to permission-only diagnostic status unless a later validation gate is separately passed?",
            "required_response": "accept_permission_only_no_validation_or_reject",
            "acceptance_condition": "Accept only if this package cannot be cited as endpoint validation, cosmological validation, or physical proof.",
            "forbidden_inputs": forbidden,
            "direct_execution_allowed_by_this_package": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_rows(POLICY, policy_rows)

    template_rows = []
    for row in policy_rows:
        template_rows.append(
            {
                **row,
                "review_completed": "false",
                "reviewer_id_or_role": "",
                "reviewer_response": "",
                "reviewer_rationale": "",
                "forbidden_inputs_used": "false",
                "template_authorized_for_later_permission_replay": "false",
                "direct_execution_allowed": "false",
                "separate_execution_step_required": "true",
            }
        )
    write_rows(TEMPLATE, template_rows)

    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Joint guarded replay run-template authorization package v1",
                "",
                "**Doc class:** external reviewer handoff package.",
                "**Status:** prepared, not completed.",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`.",
                "",
                "This package asks whether the frozen joint guarded replay run-template",
                "may be used as the basis for a later executable permission-only replay.",
                "It is not itself execution, endpoint scoring, endpoint validation, or",
                "cosmological validation.",
                "",
                "The reviewed template keeps candidate and controls under identical",
                "block-diagonal statistic, block-weight, covariance/caveat, and",
                "matched-control conditions.",
                "",
                "Mandatory controls carried by the template:",
                "",
                *[f"- `{item}`" for item in run_template["required_controls"].split(";")],
                "",
                "Mandatory caveats carried by the template:",
                "",
                *[f"- `{item}`" for item in run_template["required_caveats"].split(";")],
                "",
                "The reviewer should reject this package if any direct execution,",
                "endpoint scoring, endpoint validation, or cosmological validation",
                "claim is inferred from the template itself.",
                "",
            ]
        )
    )

    package_inputs = [
        POLICY,
        TEMPLATE,
        DOC,
        RUN_TEMPLATE,
        RUN_TEMPLATE_SUMMARY,
        RUN_TEMPLATE_DOC,
        PERMISSION_RESPONSE,
        SCORING_AUTH_RESPONSE,
    ]
    manifest_rows = []
    for path in package_inputs:
        manifest_rows.append(
            {
                "package_path": rel(path),
                "sha256": sha256(path),
                "contains_endpoint_residuals": "false",
                "contains_new_endpoint_scores": "false",
                "contains_fit_statistics": "false",
                "direct_execution_allowed": "false",
                "endpoint_scoring_allowed": "false",
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_rows(MANIFEST, manifest_rows)

    with zipfile.ZipFile(PACKAGE, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in package_inputs + [MANIFEST]:
            info = zipfile.ZipInfo(rel(path))
            info.date_time = (2026, 1, 1, 0, 0, 0)
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, path.read_bytes())
    zip_hash = sha256(PACKAGE)
    SHA.write_text(f"{zip_hash}  {PACKAGE.name}\n")

    summary = {
        "run_id": PACKAGE_ID,
        "status": "JOINT_GUARDED_REPLAY_RUN_TEMPLATE_AUTHORIZATION_PACKAGE_READY_NOT_COMPLETED",
        "package_path": rel(PACKAGE),
        "zip_sha256": zip_hash,
        "package_file_count": str(len(package_inputs) + 1),
        "review_completed": "false",
        "template_authorized_for_later_permission_replay": "false",
        "direct_execution_allowed": "false",
        "separate_execution_step_required": "true",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "contains_endpoint_residuals": "false",
        "contains_new_endpoint_scores": "false",
        "contains_fit_statistics": "false",
        "verdict": "joint_guarded_replay_run_template_authorization_package_ready_not_completed",
        "recommended_next_action": "send_zip_to_reviewer_and_validate_completed_response_before_any_execution",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_one(SUMMARY, summary)
    print(
        "JOINT_GUARDED_REPLAY_RUN_TEMPLATE_AUTHORIZATION_PACKAGE_V1_BUILT "
        f"sha256={zip_hash}"
    )


if __name__ == "__main__":
    main()
