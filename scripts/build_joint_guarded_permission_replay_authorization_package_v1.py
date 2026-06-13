#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/joint_guarded_permission_replay_authorization_policy_v1.csv"
TEMPLATE = ROOT / "data/derived/joint_guarded_permission_replay_authorization_response_template_v1.csv"
SUMMARY = ROOT / "data/derived/joint_guarded_permission_replay_authorization_package_v1_summary.csv"
MANIFEST = ROOT / "data/derived/joint_guarded_permission_replay_authorization_package_v1_manifest.csv"
PACKAGE = ROOT / "data/derived/joint_guarded_permission_replay_authorization_package_v1.zip"
SHA = ROOT / "data/derived/joint_guarded_permission_replay_authorization_package_v1.zip.sha256"
DOC = ROOT / "docs/joint_guarded_permission_replay_authorization_package_v1.md"
RESPONSE_SUMMARY = ROOT / "data/derived/joint_block_diagonal_scoring_authorization_review_response_v1_summary.csv"
SOURCE_REQ = ROOT / "data/derived/joint_cross_probe_covariance_source_requirements_v1_summary.csv"
SINGLE_STAT = ROOT / "data/derived/joint_single_statistic_binding_prerequisites_v1_summary.csv"
CONTROLS = ROOT / "data/derived/joint_matched_control_suite_requirements_gate_v1_summary.csv"
PROTOCOL = ROOT / "data/derived/joint_block_diagonal_likelihood_surrogate_protocol_shell_v1_summary.csv"
CLAIM_BOUNDARY = "joint_guarded_permission_replay_authorization_not_scoring_not_validation"
PACKAGE_ID = "JOINT_GUARDED_PERMISSION_REPLAY_AUTHORIZATION_PACKAGE_V1"


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
    response = read_one(RESPONSE_SUMMARY)
    source_req = read_one(SOURCE_REQ)
    single_stat = read_one(SINGLE_STAT)
    controls = read_one(CONTROLS)
    protocol = read_one(PROTOCOL)

    if response["decision"] != "AUTHORIZE_SEPARATE_GUARDED_JOINT_PERMISSION_REPLAY_PACKAGE_NOT_SCORING_NOT_VALIDATION":
        raise SystemExit("guarded replay package requires completed scoring-authorization review")
    if response["same_statistic_controls_required"] != "true":
        raise SystemExit("same-statistic controls must be required")
    if response["direct_scoring_allowed"] != "false":
        raise SystemExit("direct scoring must remain forbidden")
    if source_req["verdict"] != "JOINT_CROSS_PROBE_CAVEATED_INDEPENDENCE_PRECONDITION_CLOSED_SCORING_AUTH_REQUIRED":
        raise SystemExit("cross-probe source requirements are not in the expected caveated-closed state")
    if controls["verdict"] != "JOINT_MATCHED_CONTROL_SUITE_REQUIREMENTS_FROZEN_IMPLEMENTATION_BLOCKED":
        raise SystemExit("matched-control requirements must remain frozen before replay")
    if single_stat["verdict"] != "JOINT_SINGLE_STATISTIC_BINDING_PREREQUISITES_FROZEN_PROTOCOL_BLOCKED":
        raise SystemExit("single-statistic binding must remain frozen before replay")
    if protocol["verdict"] != "JOINT_BLOCK_DIAGONAL_PROTOCOL_SHELL_FROZEN_COVARIANCE_STILL_OPEN_NOT_SCORING":
        raise SystemExit("block-diagonal protocol shell must remain frozen and not scoring")

    policy_rows = [
        {
            "review_id": PACKAGE_ID,
            "question_id": "JGPR_Q1_PERMISSION_SCOPE",
            "question": "May a guarded permission-only joint replay package be built under the completed caveated block-diagonal authorization?",
            "required_response": "authorize_guarded_replay_package_or_reject",
            "acceptance_condition": "Authorize only package preparation; direct scoring remains forbidden until a separate run artifact is built and validated.",
            "forbidden_inputs": "endpoint_residuals;new_endpoint_scores;fit_improvements;posterior_chains;post_score_control_ranks",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "JGPR_Q2_SAME_STATISTIC",
            "question": "Are candidate and controls required to use the same frozen block-diagonal statistic and block weights?",
            "required_response": "accept_same_statistic_binding_or_reject",
            "acceptance_condition": "Accept only if candidate, wrong-channel, shuffled, sign-flip, block-drop, null/readout, leakage, and shared-statistic controls remain bound to the same statistic.",
            "forbidden_inputs": "endpoint_residuals;new_endpoint_scores;fit_improvements;posterior_chains;post_score_control_ranks",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "JGPR_Q3_CAVEATS",
            "question": "Must the block-diagonal caveats remain attached to any permission-only replay result?",
            "required_response": "accept_caveats_or_reject",
            "acceptance_condition": "Accept only if missing cross-probe covariance, shared sky/mask, redshift-kernel overlap, and shared nuisance/cosmology caveats remain attached.",
            "forbidden_inputs": "endpoint_residuals;new_endpoint_scores;fit_improvements;posterior_chains;post_score_control_ranks",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "JGPR_Q4_NEXT_ACTION",
            "question": "Is the next allowed artifact a guarded replay run template rather than direct execution?",
            "required_response": "accept_run_template_first_or_reject",
            "acceptance_condition": "Accept keeps this as authorization only; a separate run-template validator must pass before any executable replay script is run.",
            "forbidden_inputs": "endpoint_residuals;new_endpoint_scores;fit_improvements;posterior_chains;post_score_control_ranks",
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
                "guarded_replay_package_authorized": "false",
                "direct_execution_allowed": "false",
                "separate_run_template_required": "true",
            }
        )
    write_rows(TEMPLATE, template_rows)

    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Joint guarded permission replay authorization package v1",
                "",
                "**Doc class:** reviewer handoff package.",
                "**Status:** prepared, not completed.",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`.",
                "",
                "This package asks whether a guarded permission-only joint replay package may be prepared.",
                "It is not scoring, not endpoint validation, and not cosmological validation.",
                "",
                "The upstream scoring-authorization review allows only a separate guarded package.",
                "Candidate and controls must use the same block-diagonal statistic and covariance blocks.",
                "",
                "Mandatory caveats carried forward:",
                "- no source-native cross-probe covariance product is available;",
                "- block-diagonal independence is caveated;",
                "- shared sky/mask, redshift-kernel, cosmology/nuisance, calibration, and population covariance caveats remain active;",
                "- direct execution remains forbidden until a separate run-template gate is built and validated.",
            ]
        )
        + "\n"
    )

    package_inputs = [
        POLICY,
        TEMPLATE,
        DOC,
        RESPONSE_SUMMARY,
        SOURCE_REQ,
        SINGLE_STAT,
        CONTROLS,
        PROTOCOL,
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
                "endpoint_scoring_allowed": "false",
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_rows(MANIFEST, manifest_rows)

    with zipfile.ZipFile(PACKAGE, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in package_inputs + [MANIFEST]:
            zf.write(path, rel(path))
    zip_hash = sha256(PACKAGE)
    SHA.write_text(f"{zip_hash}  {PACKAGE.name}\n")

    summary = {
        "run_id": "JOINT_GUARDED_PERMISSION_REPLAY_AUTHORIZATION_PACKAGE_V1",
        "status": "JOINT_GUARDED_PERMISSION_REPLAY_AUTHORIZATION_PACKAGE_READY_NOT_COMPLETED",
        "package_path": rel(PACKAGE),
        "zip_sha256": zip_hash,
        "package_file_count": str(len(package_inputs) + 1),
        "review_completed": "false",
        "guarded_replay_package_authorized": "false",
        "direct_execution_allowed": "false",
        "separate_run_template_required": "true",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "contains_endpoint_residuals": "false",
        "contains_new_endpoint_scores": "false",
        "contains_fit_statistics": "false",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_one(SUMMARY, summary)
    print(
        "JOINT_GUARDED_PERMISSION_REPLAY_AUTHORIZATION_PACKAGE_V1_BUILT "
        f"sha256={zip_hash}"
    )


if __name__ == "__main__":
    main()
