#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/joint_block_diagonal_independence_review_policy_v1.csv"
TEMPLATE = ROOT / "data/derived/joint_block_diagonal_independence_review_response_template_v1.csv"
PACKAGE = ROOT / "data/derived/joint_block_diagonal_independence_review_package_v1.zip"
SHA = ROOT / "data/derived/joint_block_diagonal_independence_review_package_v1.zip.sha256"
MANIFEST = ROOT / "data/derived/joint_block_diagonal_independence_review_package_v1_manifest.csv"
SUMMARY = ROOT / "data/derived/joint_block_diagonal_independence_review_package_v1_summary.csv"
DOC = ROOT / "docs/joint_block_diagonal_independence_review_package_v1.md"
PACKAGE_ID = "JOINT_BLOCK_DIAGONAL_INDEPENDENCE_REVIEW_PACKAGE_V1"
CLAIM_BOUNDARY = "joint_block_diagonal_independence_review_not_scoring_not_validation"

PACKAGE_FILES = [
    "docs/joint_block_diagonal_independence_review_package_v1.md",
    "data/source_manifest/joint_block_diagonal_independence_review_policy_v1.csv",
    "data/derived/joint_block_diagonal_independence_review_response_template_v1.csv",
    "data/source_manifest/joint_covariance_model_policy_v1.csv",
    "data/derived/joint_covariance_model_requirements_gate_v1.csv",
    "data/derived/joint_covariance_model_requirements_gate_v1_summary.csv",
    "docs/joint_covariance_model_requirements_gate_v1.md",
    "data/source_manifest/joint_likelihood_surrogate_requirements_policy_v1.csv",
    "data/derived/joint_likelihood_surrogate_requirements_gate_v1.csv",
    "data/derived/joint_likelihood_surrogate_requirements_gate_v1_summary.csv",
    "docs/joint_likelihood_surrogate_requirements_gate_v1.md",
    "data/source_manifest/joint_best_justified_kernel_manifest_v1.csv",
    "data/derived/joint_best_justified_qi_review_response_v1.csv",
    "data/derived/joint_best_justified_qi_review_response_v1_summary.csv",
    "docs/joint_best_justified_qi_review_notes_v1.md",
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
    likelihood_summary = read_one(ROOT / "data/derived/joint_likelihood_surrogate_requirements_gate_v1_summary.csv")
    qi_summary = read_one(ROOT / "data/derived/joint_best_justified_qi_review_response_v1_summary.csv")

    if cov_summary["verdict"] != "JOINT_COVARIANCE_MODEL_REQUIREMENTS_PARTIAL_BLOCKS_READY_CROSS_PROBE_BLOCKED":
        raise SystemExit("covariance model gate is not in the expected blocked state")
    if likelihood_summary["verdict"] != "JOINT_LIKELIHOOD_SURROGATE_REQUIREMENTS_FROZEN_SCORING_BLOCKED":
        raise SystemExit("likelihood surrogate gate is not in the expected blocked state")
    if qi_summary["decision"] != "QI_REVIEW_ACCEPTED_OR_CAVEATED_SOURCE_SIDE_NOT_VALIDATION":
        raise SystemExit("Q_i review response is not accepted/caveated")

    policy_rows = [
        {
            "review_id": PACKAGE_ID,
            "question_id": "BDI_Q1_BLOCK_SCOPE",
            "question": "Are the three active blocks correctly identified as KiDS/COSEBIs, observer/path low-z, and DESI shape/readout?",
            "required_response": "accept_or_caveated_accept_or_reject",
            "acceptance_condition": "Accept or caveated accept preserves the active-block scope; reject must name the incorrect block.",
            "forbidden_inputs": "endpoint_residuals;new_endpoint_scores;fit_improvements;posterior_chains;post_score_control_ranks",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "BDI_Q2_BLOCK_DIAGONAL_SURROGATE",
            "question": "May a block-diagonal covariance surrogate be prepared for future review as a caveated approximation, without scoring permission?",
            "required_response": "accept_as_future_review_only_or_reject",
            "acceptance_condition": "Accept only if the reviewer agrees this is not endpoint scoring and requires explicit caveats.",
            "forbidden_inputs": "endpoint_residuals;new_endpoint_scores;fit_improvements;posterior_chains;post_score_control_ranks",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "BDI_Q3_CROSS_PROBE_INDEPENDENCE",
            "question": "Is cross-probe independence sufficiently supported now, or must it remain an open blocker?",
            "required_response": "must_keep_open_or_provide_source_rationale",
            "acceptance_condition": "Default accepted answer keeps cross-probe independence open; closing it requires source-side rationale independent of endpoint scores.",
            "forbidden_inputs": "endpoint_residuals;new_endpoint_scores;fit_improvements;posterior_chains;post_score_control_ranks",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "BDI_Q4_NEXT_GATE",
            "question": "Should the next artifact be a block-diagonal likelihood-surrogate protocol shell, not a scoring run?",
            "required_response": "accept_or_reject",
            "acceptance_condition": "Accept keeps the next step as protocol shell; reject must specify a safer next gate.",
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
                "forbidden_inputs_used": "false",
                "block_diagonal_surrogate_allowed_for_future_review": cov_summary["block_diagonal_surrogate_allowed_for_future_review"],
                "block_diagonal_surrogate_allowed_for_scoring_now": cov_summary["block_diagonal_surrogate_allowed_for_scoring_now"],
                "cross_probe_covariance_defined": cov_summary["cross_probe_covariance_defined"],
                "hard_blockers_open": cov_summary["hard_blockers_open"],
            }
        )
    write_csv(TEMPLATE, template_rows)

    DOC.write_text(
        "\n".join(
            [
                "# Joint block-diagonal independence review package v1",
                "",
                "**Doc class:** external review handoff",
                "**Status:** not scoring; not endpoint validation; not cosmological validation",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`",
                "",
                "This package asks a reviewer whether a block-diagonal covariance",
                "surrogate may be prepared as a future protocol shell for the three",
                "active Paper10 channels. It does not authorize scoring. The current",
                "cross-probe covariance/independence condition remains open unless a",
                "reviewer supplies source-side rationale independent of endpoint scores.",
                "",
                "Current machine state:",
                "",
                f"- covariance gate: `{cov_summary['verdict']}`",
                f"- active channels: `{cov_summary['active_channel_order']}`",
                f"- block-diagonal future review allowed: `{cov_summary['block_diagonal_surrogate_allowed_for_future_review']}`",
                f"- scoring now allowed: `{cov_summary['block_diagonal_surrogate_allowed_for_scoring_now']}`",
                f"- cross-probe covariance defined: `{cov_summary['cross_probe_covariance_defined']}`",
                f"- hard blockers open: `{cov_summary['hard_blockers_open']}`",
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
                "status": "JOINT_BLOCK_DIAGONAL_INDEPENDENCE_REVIEW_PACKAGE_READY_NOT_COMPLETED",
                "zip_path": str(PACKAGE.relative_to(ROOT)),
                "zip_sha256_path": str(SHA.relative_to(ROOT)),
                "zip_sha256": digest,
                "package_file_count": str(len(package_rows)),
                "review_completed": "false",
                "block_diagonal_surrogate_allowed_for_future_review": cov_summary["block_diagonal_surrogate_allowed_for_future_review"],
                "block_diagonal_surrogate_allowed_for_scoring_now": cov_summary["block_diagonal_surrogate_allowed_for_scoring_now"],
                "cross_probe_covariance_defined": cov_summary["cross_probe_covariance_defined"],
                "hard_blockers_open": cov_summary["hard_blockers_open"],
                "endpoint_scoring_allowed": "false",
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "contains_endpoint_residuals": "false",
                "contains_new_endpoint_scores": "false",
                "contains_fit_statistics": "false",
                "verdict": "block_diagonal_independence_review_package_ready_not_completed_not_scoring",
                "recommended_next_action": "send_zip_to_reviewer_before_building_block_diagonal_likelihood_surrogate_protocol",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    print(f"JOINT_BLOCK_DIAGONAL_INDEPENDENCE_REVIEW_PACKAGE_V1_BUILT sha256={digest}")


if __name__ == "__main__":
    main()
