#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/joint_cross_probe_covariance_closure_review_policy_v1.csv"
TEMPLATE = ROOT / "data/derived/joint_cross_probe_covariance_closure_review_response_template_v1.csv"
PACKAGE = ROOT / "data/derived/joint_cross_probe_covariance_closure_review_package_v1.zip"
SHA = ROOT / "data/derived/joint_cross_probe_covariance_closure_review_package_v1.zip.sha256"
MANIFEST = ROOT / "data/derived/joint_cross_probe_covariance_closure_review_package_v1_manifest.csv"
SUMMARY = ROOT / "data/derived/joint_cross_probe_covariance_closure_review_package_v1_summary.csv"
DOC = ROOT / "docs/joint_cross_probe_covariance_closure_review_package_v1.md"
PACKAGE_ID = "JOINT_CROSS_PROBE_COVARIANCE_CLOSURE_REVIEW_PACKAGE_V1"
CLAIM_BOUNDARY = "joint_cross_probe_covariance_closure_review_not_scoring_not_validation"

PACKAGE_FILES = [
    "docs/joint_cross_probe_covariance_closure_review_package_v1.md",
    "data/source_manifest/joint_cross_probe_covariance_closure_review_policy_v1.csv",
    "data/derived/joint_cross_probe_covariance_closure_review_response_template_v1.csv",
    "data/source_manifest/joint_covariance_model_policy_v1.csv",
    "data/derived/joint_covariance_model_requirements_gate_v1.csv",
    "data/derived/joint_covariance_model_requirements_gate_v1_summary.csv",
    "docs/joint_covariance_model_requirements_gate_v1.md",
    "data/derived/joint_block_diagonal_independence_review_response_v1.csv",
    "data/derived/joint_block_diagonal_independence_review_response_v1_summary.csv",
    "docs/joint_block_diagonal_independence_review_package_v1.md",
    "data/derived/joint_block_diagonal_likelihood_surrogate_protocol_shell_v1.csv",
    "data/derived/joint_block_diagonal_likelihood_surrogate_protocol_shell_v1_summary.csv",
    "docs/joint_block_diagonal_likelihood_surrogate_protocol_shell_v1.md",
    "data/source_manifest/joint_matched_control_suite_requirements_policy_v1.csv",
    "data/derived/joint_matched_control_suite_requirements_gate_v1.csv",
    "data/derived/joint_matched_control_suite_requirements_gate_v1_summary.csv",
    "docs/joint_matched_control_suite_requirements_gate_v1.md",
]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required input: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def manifest_row(rel: str) -> dict[str, str]:
    path = ROOT / rel
    if not path.exists():
        raise SystemExit(f"missing review package member: {rel}")
    return {
        "package_id": PACKAGE_ID,
        "package_path": rel,
        "byte_count": str(path.stat().st_size),
        "sha256": sha256(path),
        "contains_endpoint_residuals": "false",
        "contains_new_endpoint_scores": "false",
        "contains_fit_statistics": "false",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def main() -> None:
    cov_summary = read_one(ROOT / "data/derived/joint_covariance_model_requirements_gate_v1_summary.csv")
    bdi_summary = read_one(ROOT / "data/derived/joint_block_diagonal_independence_review_response_v1_summary.csv")
    bd_shell = read_one(ROOT / "data/derived/joint_block_diagonal_likelihood_surrogate_protocol_shell_v1_summary.csv")

    if cov_summary["cross_probe_covariance_defined"] != "false":
        raise SystemExit("cross-probe covariance is already defined; closure review package is not needed")
    if cov_summary["endpoint_scoring_allowed"] != "false":
        raise SystemExit("covariance gate unexpectedly allows scoring")
    if bdi_summary["cross_probe_independence_status"] != "kept_open":
        raise SystemExit("block-diagonal independence response is not in the expected open state")
    if bd_shell["protocol_executable"] != "false":
        raise SystemExit("block-diagonal shell unexpectedly executable")

    policy_rows = [
        {
            "review_id": PACKAGE_ID,
            "question_id": "CPC_Q1_SCOPE",
            "question": "Does this package correctly identify the unresolved joint blocker as cross-probe covariance or independence across KiDS/COSEBIs, observer/path low-z, and DESI shape/readout blocks?",
            "required_response": "accept_or_caveated_accept_or_reject",
            "acceptance_condition": "Accept only if the reviewer agrees this is a source-side covariance/independence gate, not a scoring gate.",
            "forbidden_inputs": "endpoint_residuals;new_endpoint_scores;fit_improvements;posterior_chains;post_score_control_ranks",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "CPC_Q2_COVARIANCE_ROUTE",
            "question": "Is there a source-native or source-frozen cross-probe covariance product available now that can close the joint covariance blocker?",
            "required_response": "available_now_or_not_available_or_caveated_candidate",
            "acceptance_condition": "Available-now requires a named source product, dimensional scope, and no endpoint-score dependence; otherwise the blocker remains open.",
            "forbidden_inputs": "endpoint_residuals;new_endpoint_scores;fit_improvements;posterior_chains;post_score_control_ranks",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "CPC_Q3_INDEPENDENCE_ROUTE",
            "question": "If no cross-probe covariance product is available, is a block-diagonal independence approximation source-side justified for a future scoring protocol?",
            "required_response": "accept_future_scoring_precondition_or_keep_open",
            "acceptance_condition": "Accept only with source-side rationale that the active probes are sufficiently independent for the stated limited protocol; otherwise keep open.",
            "forbidden_inputs": "endpoint_residuals;new_endpoint_scores;fit_improvements;posterior_chains;post_score_control_ranks",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "CPC_Q4_LIMITS",
            "question": "What limitations must be carried forward if a future block-diagonal surrogate is used?",
            "required_response": "list_required_caveats_or_reject",
            "acceptance_condition": "The response must name caveats such as shared sky, shared cosmological parameters, overlapping redshift sensitivity, calibration/nuisance correlations, and non-population covariance gaps where relevant.",
            "forbidden_inputs": "endpoint_residuals;new_endpoint_scores;fit_improvements;posterior_chains;post_score_control_ranks",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "CPC_Q5_NEXT_ACTION",
            "question": "What is the next allowed action after this review: keep blocker open, acquire covariance product, or freeze caveated block-diagonal scoring preconditions?",
            "required_response": "choose_one_with_rationale",
            "acceptance_condition": "The next action cannot be endpoint scoring unless Q2 or Q3 supplies an accepted source-side closure route and a separate scoring authorization is later created.",
            "forbidden_inputs": "endpoint_residuals;new_endpoint_scores;fit_improvements;posterior_chains;post_score_control_ranks",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(POLICY, policy_rows)

    template_rows = []
    for row in policy_rows:
        template_rows.append(
            {
                **row,
                "review_completed": "false",
                "reviewer_id_or_role": "",
                "reviewer_response": "",
                "reviewer_rationale": "",
                "source_reference_or_url": "",
                "forbidden_inputs_used": "false",
                "cross_probe_covariance_product_available": "false",
                "block_diagonal_independence_source_justified": "false",
                "future_scoring_precondition_closure_allowed": "false",
                "separate_scoring_authorization_required": "true",
                "hard_blocker_remains_open": "true",
            }
        )
    write_csv(TEMPLATE, template_rows)

    DOC.write_text(
        "\n".join(
            [
                "# Joint cross-probe covariance closure review package v1",
                "",
                "**Doc class:** external source-side review handoff",
                "**Status:** not scoring; not endpoint validation; not cosmological validation",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`",
                "",
                "This package addresses the blocker left open by the block-diagonal",
                "independence review. It asks whether the joint Paper10 route can close",
                "the cross-probe covariance/independence condition without using endpoint",
                "residuals, endpoint scores, fit improvements, posterior chains, or",
                "post-score control ranks.",
                "",
                "Current machine state:",
                "",
                f"- active channels: `{cov_summary['active_channel_order']}`",
                f"- covariance gate verdict: `{cov_summary['verdict']}`",
                f"- block-diagonal review decision: `{bdi_summary['decision']}`",
                f"- block-diagonal shell verdict: `{bd_shell['verdict']}`",
                f"- cross-probe covariance defined: `{cov_summary['cross_probe_covariance_defined']}`",
                f"- block-diagonal shell executable: `{bd_shell['protocol_executable']}`",
                f"- endpoint scoring allowed: `{bd_shell['endpoint_scoring_allowed']}`",
                "",
                "Allowed closure routes:",
                "",
                "1. **Covariance-product route:** identify a source-native or source-frozen",
                "   cross-probe covariance product with dimensional scope and provenance.",
                "2. **Independence-rationale route:** justify a caveated block-diagonal",
                "   approximation from source-side probe design, redshift/sky/nuisance",
                "   separation, and known calibration overlap limits.",
                "",
                "Neither route authorizes scoring by itself. A separate scoring/replay",
                "authorization must be created after source-side closure, if closure is accepted.",
                "",
                "Reviewer instruction:",
                "",
                "- Fill `data/derived/joint_cross_probe_covariance_closure_review_response_template_v1.csv`.",
                "- Do not use endpoint residuals, new endpoint scores, fit improvements,",
                "  posterior chains, or post-score control ranks.",
                "- If keeping the blocker open, state the missing source-side evidence.",
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
                "status": "JOINT_CROSS_PROBE_COVARIANCE_CLOSURE_REVIEW_PACKAGE_READY_NOT_COMPLETED",
                "zip_path": str(PACKAGE.relative_to(ROOT)),
                "zip_sha256_path": str(SHA.relative_to(ROOT)),
                "zip_sha256": digest,
                "package_file_count": str(len(package_rows)),
                "review_completed": "false",
                "active_channel_order": cov_summary["active_channel_order"],
                "cross_probe_covariance_defined": cov_summary["cross_probe_covariance_defined"],
                "block_diagonal_shell_executable": bd_shell["protocol_executable"],
                "endpoint_scoring_allowed": "false",
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "contains_endpoint_residuals": "false",
                "contains_new_endpoint_scores": "false",
                "contains_fit_statistics": "false",
                "hard_blocker_remains_open": "true",
                "verdict": "cross_probe_covariance_closure_review_package_ready_not_completed_not_scoring",
                "recommended_next_action": "send_zip_to_reviewer_to_close_or_keep_open_cross_probe_covariance_independence",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    print(f"JOINT_CROSS_PROBE_COVARIANCE_CLOSURE_REVIEW_PACKAGE_V1_BUILT sha256={digest}")


if __name__ == "__main__":
    main()
