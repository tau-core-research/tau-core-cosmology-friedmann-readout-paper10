#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROMOTION = ROOT / "data/derived/joint_numeric_t_joint_promotion_gate_v1_summary.csv"
PROMOTION_ROWS = ROOT / "data/derived/joint_numeric_t_joint_promotion_gate_v1.csv"
TJOINT_LEDGER = ROOT / "data/derived/joint_numeric_t_joint_ledger_v1_summary.csv"
ZI_LEDGER = ROOT / "data/derived/joint_numeric_zi_distribution_ledger_v1_summary.csv"
CONTROL_COVERAGE = ROOT / "data/derived/joint_same_statistic_control_coverage_status_v1_summary.csv"
COVARIANCE = ROOT / "data/derived/joint_covariance_resolution_plan_v1_summary.csv"
BLOCKER = ROOT / "data/derived/joint_numeric_t_joint_blocker_status_v1_summary.csv"
POLICY = ROOT / "data/source_manifest/joint_numeric_t_joint_control_suite_authorization_policy_v1.csv"
TEMPLATE = ROOT / "data/derived/joint_numeric_t_joint_control_suite_authorization_response_template_v1.csv"
SUMMARY = ROOT / "data/derived/joint_numeric_t_joint_control_suite_authorization_package_v1_summary.csv"
MANIFEST = ROOT / "data/derived/joint_numeric_t_joint_control_suite_authorization_package_v1_manifest.csv"
PACKAGE = ROOT / "data/derived/joint_numeric_t_joint_control_suite_authorization_package_v1.zip"
SHA = ROOT / "data/derived/joint_numeric_t_joint_control_suite_authorization_package_v1.zip.sha256"
DOC = ROOT / "docs/joint_numeric_t_joint_control_suite_authorization_package_v1.md"
INSTRUCTIONS = ROOT / "docs/joint_numeric_t_joint_control_suite_authorization_reviewer_instructions_v1.md"
EXTERNAL_MESSAGE = ROOT / "docs/joint_numeric_t_joint_control_suite_authorization_external_reviewer_message_v1.md"
PACKAGE_ID = "JOINT_NUMERIC_T_JOINT_CONTROL_SUITE_AUTHORIZATION_PACKAGE_V1"
CLAIM_BOUNDARY = "joint_numeric_t_joint_control_suite_authorization_not_scoring_not_validation"


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
        "control_suite_authorization_allowed": "false",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def main() -> None:
    promotion = read_one(PROMOTION)
    tjoint = read_one(TJOINT_LEDGER)
    coverage = read_one(CONTROL_COVERAGE)
    covariance = read_one(COVARIANCE)
    blocker = read_one(BLOCKER)

    if promotion["verdict"] != "NUMERIC_T_JOINT_LEDGER_BUILT_PROMOTION_STILL_BLOCKED_FOR_ENDPOINT_SCORING":
        raise SystemExit("numeric T_joint promotion gate is not in the expected post-ledger blocked state")
    if promotion["numeric_t_joint_ledger_built"] != "true":
        raise SystemExit("numeric T_joint ledger must be built before control-suite authorization")
    if tjoint["computes_endpoint_score_now"] != "false":
        raise SystemExit("T_joint ledger must not already compute endpoint score")
    if coverage["numeric_executable_binding_passed"] != "false":
        raise SystemExit("control-suite authorization package expects numeric controls to remain unbuilt")
    if covariance["cross_probe_covariance_defined"] != "false":
        raise SystemExit("this package preserves the caveated/open cross-probe covariance boundary")
    if blocker["current_blocker"] != "numeric_t_joint_ledger_built_endpoint_scoring_authorization_missing":
        raise SystemExit("unexpected numeric T_joint blocker state")

    forbidden = (
        "endpoint_residuals;new_endpoint_scores;fit_improvements;posterior_chains;"
        "posthoc_channel_selection;posthoc_weight_tuning;posthoc_sign_changes;"
        "posthoc_center_scale_selection;posthoc_control_family_removal;"
        "posthoc_covariance_reweighting;cosmological_validation_claims;"
        "physical_validation_claims"
    )
    rows = [
        {
            "review_id": PACKAGE_ID,
            "question_id": "CS_Q1_SCOPE",
            "question": "May a numeric same-T_joint matched-control suite be prepared from the frozen ledgers without endpoint scoring?",
            "required_response": "authorize_control_suite_build_only_or_reject",
            "acceptance_condition": "Accept only if the output is a control-suite build authorization, not endpoint scoring or validation.",
            "forbidden_inputs": forbidden,
            "control_suite_authorization_allowed": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "CS_Q2_SAME_STATISTIC",
            "question": "Must every control use the same numeric T_joint statistic, q_i weights, signs, z_i standardization, and row scope?",
            "required_response": "accept_same_numeric_t_joint_binding_or_reject",
            "acceptance_condition": "Accept only if no control may change the statistic, weights, signs, centers, scales, or channel membership.",
            "forbidden_inputs": forbidden,
            "control_suite_authorization_allowed": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "CS_Q3_REQUIRED_CONTROLS",
            "question": "Must sign-flip, block-drop, shuffled-channel, wrong-channel/family, scope/forbidden-input, and null-readout controls be represented before endpoint claims?",
            "required_response": "accept_required_control_families_or_reject",
            "acceptance_condition": "Accept only if missing numeric control families remain blockers for endpoint validation claims.",
            "forbidden_inputs": forbidden,
            "control_suite_authorization_allowed": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "CS_Q4_COVARIANCE_BOUNDARY",
            "question": "Must the caveated block-diagonal/cross-probe covariance boundary remain attached to the control-suite result?",
            "required_response": "accept_caveated_covariance_boundary_or_reject",
            "acceptance_condition": "Accept only if the control suite remains a prevalidation ledger until a separate covariance/endpoint authorization is completed.",
            "forbidden_inputs": forbidden,
            "control_suite_authorization_allowed": "false",
            "endpoint_scoring_allowed": "false",
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
                "# Joint numeric T_joint control-suite authorization package v1",
                "",
                "**Doc class:** external authorization handoff.",
                "**Status:** prepared, not completed.",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`.",
                "",
                "This package asks whether the next artifact may build a numeric",
                "same-statistic matched-control suite around the already frozen",
                "`T_joint = sum_i q_i z_i` ledger.",
                "",
                f"Frozen numeric `T_joint`: `{tjoint['numeric_t_joint']}`.",
                "",
                "It does not authorize endpoint scoring, cosmological validation,",
                "or physical validation. The caveated cross-probe covariance boundary",
                "and all forbidden-input rules remain attached.",
                "",
            ]
        )
    )
    INSTRUCTIONS.write_text(
        "\n".join(
            [
                "# Joint Numeric T_joint Control-Suite Authorization Reviewer Instructions v1",
                "",
                "You do not need repository access. Review only the files in the zip.",
                "",
                "If accepted, use these exact decisions in the response CSV:",
                "",
                "- `AUTHORIZE_CONTROL_SUITE_BUILD_ONLY_NOT_ENDPOINT_SCORING`",
                "- `ACCEPT_SAME_NUMERIC_TJOINT_BINDING_NO_RETUNING`",
                "- `ACCEPT_REQUIRED_CONTROL_FAMILIES_AS_ENDPOINT_BLOCKERS`",
                "- `ACCEPT_CAVEATED_COVARIANCE_BOUNDARY`",
                "",
                "Keep `endpoint_scoring_allowed=false`,",
                "`endpoint_validation_claimed=false`,",
                "`cosmological_validation_claimed=false`, and",
                "`physical_validation_claimed=false` unless rejecting the package.",
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
                "The request is narrow: may the authors build a numeric control suite",
                "using the already frozen `T_joint` statistic? This is not endpoint",
                "scoring and not evidence for cosmological or physical validation.",
                "",
                "Please reject if any row appears to use endpoint residuals, new",
                "scores, post-hoc channel selection, weight tuning, sign tuning,",
                "center/scale reselection, covariance reweighting, or validation",
                "claims.",
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
        PROMOTION,
        PROMOTION_ROWS,
        TJOINT_LEDGER,
        ZI_LEDGER,
        CONTROL_COVERAGE,
        COVARIANCE,
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
                "status": "JOINT_NUMERIC_T_JOINT_CONTROL_SUITE_AUTHORIZATION_PACKAGE_READY_NOT_COMPLETED",
                "zip_path": rel(PACKAGE),
                "zip_sha256_path": rel(SHA),
                "zip_sha256": digest,
                "package_file_count": str(len(package_rows)),
                "frozen_numeric_t_joint": tjoint["numeric_t_joint"],
                "review_completed": "false",
                "control_suite_authorization_allowed": "false",
                "endpoint_scoring_allowed": "false",
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "contains_endpoint_scores": "false",
                "contains_fit_statistics": "false",
                "next_required_action": "send_zip_to_reviewer_then_validate_completed_response_before_control_suite_build",
                "verdict": "control_suite_authorization_package_ready_not_completed",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    print(f"JOINT_NUMERIC_T_JOINT_CONTROL_SUITE_AUTHORIZATION_PACKAGE_V1_BUILT sha256={digest}")


if __name__ == "__main__":
    main()
