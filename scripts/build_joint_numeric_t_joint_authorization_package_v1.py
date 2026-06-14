#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ZI_LEDGER = ROOT / "data/derived/joint_numeric_zi_distribution_ledger_v1_summary.csv"
ZI_LEDGER_ROWS = ROOT / "data/derived/joint_numeric_zi_distribution_ledger_v1.csv"
ZI_BLOCKER = ROOT / "data/derived/joint_numeric_zi_distribution_build_blocker_status_v1_summary.csv"
SHELL = ROOT / "data/derived/joint_single_statistic_protocol_shell_v1.csv"
COV = ROOT / "data/derived/joint_cross_probe_covariance_closure_review_response_v1_summary.csv"
POLICY = ROOT / "data/source_manifest/joint_numeric_t_joint_authorization_policy_v1.csv"
TEMPLATE = ROOT / "data/derived/joint_numeric_t_joint_authorization_response_template_v1.csv"
DOC = ROOT / "docs/joint_numeric_t_joint_authorization_package_v1.md"
INSTRUCTIONS = ROOT / "docs/joint_numeric_t_joint_authorization_reviewer_instructions_v1.md"
MANIFEST = ROOT / "data/derived/joint_numeric_t_joint_authorization_package_v1_manifest.csv"
SUMMARY = ROOT / "data/derived/joint_numeric_t_joint_authorization_package_v1_summary.csv"
PACKAGE = ROOT / "data/derived/joint_numeric_t_joint_authorization_package_v1.zip"
SHA = ROOT / "data/derived/joint_numeric_t_joint_authorization_package_v1.zip.sha256"
CLAIM_BOUNDARY = "joint_numeric_t_joint_authorization_not_endpoint_scoring_not_validation"
PACKAGE_ID = "JOINT_NUMERIC_T_JOINT_AUTHORIZATION_PACKAGE_V1"


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
        "contains_new_endpoint_scores": "false",
        "contains_new_fit_statistics": "false",
        "numeric_t_joint_allowed": "false",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def main() -> None:
    blocker = read_one(ZI_BLOCKER)
    ledger_rows = read_rows(ZI_LEDGER)
    shell_rows = read_rows(SHELL)
    cov = read_one(COV)
    aggregate = [row for row in ledger_rows if row["channel_id"] == "all_channels"]
    channel_rows = [row for row in ledger_rows if row["channel_id"] != "all_channels"]
    if blocker["current_blocker"] != "numeric_zi_distribution_ledger_built_numeric_t_joint_authorization_missing":
        raise SystemExit("numeric T_joint package requires z_i ledger built and T_joint authorization missing")
    if len(channel_rows) != 3 or len(shell_rows) != 3 or len(aggregate) != 1:
        raise SystemExit("expected three z_i channels and three shell channels")
    if any(row["numeric_z_i_defined"] != "true" for row in channel_rows):
        raise SystemExit("all channel z_i values must be defined")
    if any(row["computes_t_joint_now"] != "false" for row in ledger_rows):
        raise SystemExit("z_i ledger must not already compute T_joint")
    if cov.get("hard_blocker_remains_open") != "false" or cov.get("decision") != "JOINT_BLOCK_DIAGONAL_INDEPENDENCE_PRECONDITION_CAVEATED_CLOSED_NOT_SCORING":
        raise SystemExit("cross-probe covariance closure must be caveated-closed before T_joint authorization package")

    forbidden = (
        "endpoint_residuals;new_endpoint_scores;fit_improvements;posterior_chains;"
        "posthoc_channel_selection;posthoc_weight_tuning;posthoc_sign_changes;"
        "posthoc_center_scale_selection;posthoc_control_family_removal;"
        "cosmological_validation_claims;physical_validation_claims"
    )
    rows = [
        {
            "review_id": PACKAGE_ID,
            "question_id": "NTJ_Q1_SCOPE",
            "question": "May the precomputed channel-level z_i values be combined once using the frozen T_joint = sum_i q_i z_i shell?",
            "required_response": "authorize_numeric_t_joint_once_or_reject",
            "acceptance_condition": "Accept only one numeric T_joint ledger from frozen q_i and z_i; do not authorize endpoint scoring or validation.",
            "forbidden_inputs": forbidden,
            "numeric_t_joint_allowed": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "NTJ_Q2_FROZEN_INPUTS",
            "question": "Must q_i weights, signs, centers, scales, z_i values, and channel membership remain frozen exactly as packaged?",
            "required_response": "accept_frozen_numeric_inputs_or_reject",
            "acceptance_condition": "Accept only if no weights, signs, channels, centers, scales, or z_i values may be changed after seeing the numeric ledger.",
            "forbidden_inputs": forbidden,
            "numeric_t_joint_allowed": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "NTJ_Q3_CAVEATED_COVARIANCE",
            "question": "Must the existing caveated block-diagonal/cross-probe covariance status remain attached to the T_joint ledger?",
            "required_response": "accept_caveated_covariance_boundary_or_reject",
            "acceptance_condition": "Accept only if the T_joint output remains a caveated joint ledger and not a full-covariance validation result.",
            "forbidden_inputs": forbidden,
            "numeric_t_joint_allowed": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "NTJ_Q4_NO_VALIDATION",
            "question": "Must endpoint scoring, cosmological validation, and physical validation remain forbidden after T_joint is computed?",
            "required_response": "accept_numeric_t_joint_no_validation_or_reject",
            "acceptance_condition": "Accept only if a separate future authorization is required before any endpoint or validation claim.",
            "forbidden_inputs": forbidden,
            "numeric_t_joint_allowed": "false",
            "endpoint_scoring_allowed": "false",
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
                "# Joint numeric T_joint authorization package v1",
                "",
                "**Doc class:** external authorization handoff.",
                "**Status:** prepared, not completed.",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`.",
                "",
                "This package asks whether the existing channel-level numeric `z_i`",
                "ledger may be combined once under the already frozen symbolic shell:",
                "",
                "```text",
                "T_joint = sum_i q_i z_i",
                "```",
                "",
                "The package does not authorize new endpoint scores, new fitting,",
                "endpoint validation, cosmological validation, or physical validation.",
                "It only asks whether the already built `z_i` ledger and frozen `q_i`",
                "weights may be multiplied and summed into a numeric joint ledger.",
                "",
                "The existing KiDS endpoint-score-not-validation caveat, DESI small-N",
                "caveat, and caveated cross-probe covariance status remain attached.",
            ]
        )
        + "\n"
    )
    inputs = [POLICY, TEMPLATE, DOC, INSTRUCTIONS, ZI_LEDGER, ZI_LEDGER_ROWS, ZI_BLOCKER, SHELL, COV]
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
                "status": "JOINT_NUMERIC_T_JOINT_AUTHORIZATION_PACKAGE_READY_NOT_COMPLETED",
                "zip_path": rel(PACKAGE),
                "zip_sha256_path": rel(SHA),
                "zip_sha256": digest,
                "package_file_count": str(len(package_rows)),
                "review_completed": "false",
                "numeric_t_joint_allowed": "false",
                "endpoint_scoring_allowed": "false",
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "contains_new_endpoint_scores": "false",
                "contains_new_fit_statistics": "false",
                "verdict": "numeric_t_joint_authorization_package_ready_not_completed",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    print(f"JOINT_NUMERIC_T_JOINT_AUTHORIZATION_PACKAGE_V1_BUILT sha256={digest}")


if __name__ == "__main__":
    main()
