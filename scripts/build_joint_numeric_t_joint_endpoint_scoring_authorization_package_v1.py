#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REVIEW_RESPONSE = ROOT / "data/derived/joint_numeric_t_joint_control_suite_review_response_v1_summary.csv"
CONTROL_SUITE = ROOT / "data/derived/joint_numeric_t_joint_control_suite_v1_summary.csv"
CONTROL_SUITE_ROWS = ROOT / "data/derived/joint_numeric_t_joint_control_suite_v1.csv"
TJOINT_LEDGER = ROOT / "data/derived/joint_numeric_t_joint_ledger_v1_summary.csv"
BLOCKER = ROOT / "data/derived/joint_numeric_t_joint_control_suite_blocker_status_v1_summary.csv"
POLICY = ROOT / "data/source_manifest/joint_numeric_t_joint_endpoint_scoring_authorization_policy_v1.csv"
TEMPLATE = ROOT / "data/derived/joint_numeric_t_joint_endpoint_scoring_authorization_response_template_v1.csv"
SUMMARY = ROOT / "data/derived/joint_numeric_t_joint_endpoint_scoring_authorization_package_v1_summary.csv"
MANIFEST = ROOT / "data/derived/joint_numeric_t_joint_endpoint_scoring_authorization_package_v1_manifest.csv"
PACKAGE = ROOT / "data/derived/joint_numeric_t_joint_endpoint_scoring_authorization_package_v1.zip"
SHA = ROOT / "data/derived/joint_numeric_t_joint_endpoint_scoring_authorization_package_v1.zip.sha256"
DOC = ROOT / "docs/joint_numeric_t_joint_endpoint_scoring_authorization_package_v1.md"
INSTRUCTIONS = ROOT / "docs/joint_numeric_t_joint_endpoint_scoring_authorization_reviewer_instructions_v1.md"
EXTERNAL_MESSAGE = ROOT / "docs/joint_numeric_t_joint_endpoint_scoring_authorization_external_reviewer_message_v1.md"
PACKAGE_ID = "JOINT_NUMERIC_T_JOINT_ENDPOINT_SCORING_AUTHORIZATION_PACKAGE_V1"
CLAIM_BOUNDARY = "joint_numeric_t_joint_endpoint_scoring_authorization_not_validation"


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
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def main() -> None:
    review = read_one(REVIEW_RESPONSE)
    control = read_one(CONTROL_SUITE)
    tjoint = read_one(TJOINT_LEDGER)
    blocker = read_one(BLOCKER)

    if review["decision"] != "AUTHORIZE_PREPARE_ENDPOINT_SCORING_AUTHORIZATION_PACKAGE_NOT_SCORING":
        raise SystemExit("control-suite review has not authorized preparing endpoint-scoring authorization package")
    if review["endpoint_scoring_allowed"] != "false":
        raise SystemExit("control-suite review response must not authorize scoring directly")
    if review["endpoint_scoring_authorization_package_preparation_allowed"] != "true":
        raise SystemExit("control-suite review response must allow only authorization-package preparation")
    if control["verdict"] != "NUMERIC_T_JOINT_CONTROL_SUITE_BUILT_PREVALIDATION_NOT_ENDPOINT_SCORING":
        raise SystemExit("control suite must be the prevalidation non-scoring suite")
    if control["controls_beating_or_equal_candidate"] != "0":
        raise SystemExit("endpoint authorization package requires 0 controls beating/equal candidate")
    if tjoint["computes_endpoint_score_now"] != "false":
        raise SystemExit("T_joint ledger must remain non-scoring")
    if blocker["current_blocker"] != "control_suite_built_endpoint_scoring_authorization_missing":
        raise SystemExit("unexpected control-suite blocker state")

    forbidden = (
        "posthoc_channel_selection;posthoc_weight_tuning;posthoc_sign_changes;"
        "posthoc_center_scale_selection;posthoc_control_family_removal;"
        "posthoc_covariance_reweighting;new_endpoint_residuals;fit_improvement_hunting;"
        "posterior_chains;cosmological_validation_claims;physical_validation_claims"
    )
    rows = [
        {
            "review_id": PACKAGE_ID,
            "question_id": "ES_Q1_SCOPE",
            "question": "May one narrow permission-only endpoint-scoring replay be prepared from the frozen numeric T_joint and its 26 same-statistic controls?",
            "required_response": "authorize_permission_only_endpoint_scoring_or_reject",
            "acceptance_condition": "Authorize only one frozen permission-only scoring replay; no validation claim is allowed.",
            "forbidden_inputs": forbidden,
            "permission_only_endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "ES_Q2_BINDING",
            "question": "Must the endpoint scoring use the exact frozen T_joint statistic, q_i weights, signs, z_i standardization, row scope, and control suite?",
            "required_response": "accept_exact_frozen_tjoint_and_controls_or_reject",
            "acceptance_condition": "Accept only if candidate and all controls remain tied to the same frozen statistic and scope.",
            "forbidden_inputs": forbidden,
            "permission_only_endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "ES_Q3_CONTROL_RESULT",
            "question": "Is the 0/26 control-suite result sufficient only as a precondition for a permission-only replay, not as validation?",
            "required_response": "accept_precondition_only_or_reject",
            "acceptance_condition": "Accept only if 0/26 remains prevalidation evidence and cannot be reported as cosmological validation.",
            "forbidden_inputs": forbidden,
            "permission_only_endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "ES_Q4_CAVEATS",
            "question": "Must block-diagonal/cross-probe covariance caveats and non-validation language remain attached to the endpoint-scoring output?",
            "required_response": "accept_caveat_binding_or_reject",
            "acceptance_condition": "Accept only if the output remains permission-only and caveated even if the numeric score is positive.",
            "forbidden_inputs": forbidden,
            "permission_only_endpoint_scoring_allowed": "false",
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
                "# Joint numeric T_joint endpoint-scoring authorization package v1",
                "",
                "**Doc class:** external authorization handoff.",
                "**Status:** prepared, not completed.",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`.",
                "",
                "This package asks whether one narrow permission-only endpoint-scoring",
                "replay may be run from the already frozen numeric `T_joint` and its",
                "same-statistic control suite.",
                "",
                f"Frozen numeric `T_joint`: `{control['candidate_numeric_t_joint']}`.",
                f"Controls beating/equal candidate: `{control['controls_beating_or_equal_candidate']}/{control['numeric_control_count']}`.",
                "",
                "The package does not run scoring and does not authorize validation,",
                "cosmological discovery, or physical proof claims.",
                "",
            ]
        )
    )
    INSTRUCTIONS.write_text(
        "\n".join(
            [
                "# Joint Numeric T_joint Endpoint-Scoring Authorization Reviewer Instructions v1",
                "",
                "You do not need repository access. Review only the files in the zip.",
                "",
                "If accepted, use these exact decisions in the response CSV:",
                "",
                "- `AUTHORIZE_PERMISSION_ONLY_ENDPOINT_SCORING_NOT_VALIDATION`",
                "- `ACCEPT_EXACT_FROZEN_TJOINT_AND_CONTROLS_NO_RETUNING`",
                "- `ACCEPT_CONTROL_RESULT_AS_PRECONDITION_ONLY_NOT_VALIDATION`",
                "- `ACCEPT_CAVEAT_BINDING_NO_VALIDATION`",
                "",
                "Keep `endpoint_validation_claimed=false`,",
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
                "and complete the response CSV only from the packaged files.",
                "",
                "The request is narrow: may the authors run one permission-only endpoint",
                "scoring replay using the frozen numeric T_joint and the frozen 26-control",
                "same-statistic suite? This is not a validation or discovery claim.",
                "",
                "Please reject if any row appears to permit post-hoc tuning, control",
                "removal, covariance reweighting, validation language, or physical claims.",
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
        REVIEW_RESPONSE,
        CONTROL_SUITE,
        CONTROL_SUITE_ROWS,
        TJOINT_LEDGER,
        BLOCKER,
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
                "status": "JOINT_NUMERIC_T_JOINT_ENDPOINT_SCORING_AUTHORIZATION_PACKAGE_READY_NOT_COMPLETED",
                "zip_path": rel(PACKAGE),
                "zip_sha256_path": rel(SHA),
                "zip_sha256": digest,
                "package_file_count": str(len(package_rows)),
                "candidate_numeric_t_joint": control["candidate_numeric_t_joint"],
                "numeric_control_count": control["numeric_control_count"],
                "controls_beating_or_equal_candidate": control["controls_beating_or_equal_candidate"],
                "review_completed": "false",
                "permission_only_endpoint_scoring_allowed": "false",
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "contains_endpoint_scores": "false",
                "contains_fit_statistics": "false",
                "next_required_action": "send_zip_to_reviewer_then_import_completed_response_before_running_permission_only_scoring",
                "verdict": "endpoint_scoring_authorization_package_ready_not_completed",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    print(f"JOINT_NUMERIC_T_JOINT_ENDPOINT_SCORING_AUTHORIZATION_PACKAGE_V1_BUILT sha256={digest}")


if __name__ == "__main__":
    main()
