#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ID = "JOINT_ROW_LEVEL_CROSS_CHANNEL_CONTROL_ALIGNMENT_REVIEW_PACKAGE_V1"
CLAIM_BOUNDARY = "joint_row_level_cross_channel_control_alignment_review_not_scoring_not_validation"

VALUES = ROOT / "data/derived/joint_row_level_numeric_penalty_values_v1.csv"
USE_AUTH = ROOT / "data/derived/joint_row_level_penalty_use_authorization_review_response_v1_summary.csv"
POLICY = ROOT / "data/source_manifest/joint_row_level_cross_channel_control_alignment_policy_v1.csv"
TEMPLATE = ROOT / "data/derived/joint_row_level_cross_channel_control_alignment_review_response_template_v1.csv"
PACKAGE = ROOT / "data/derived/joint_row_level_cross_channel_control_alignment_review_package_v1.zip"
SHA = ROOT / "data/derived/joint_row_level_cross_channel_control_alignment_review_package_v1.zip.sha256"
MANIFEST = ROOT / "data/derived/joint_row_level_cross_channel_control_alignment_review_package_v1_manifest.csv"
SUMMARY = ROOT / "data/derived/joint_row_level_cross_channel_control_alignment_review_package_v1_summary.csv"
DOC = ROOT / "docs/joint_row_level_cross_channel_control_alignment_review_package_v1.md"
DIAGNOSTIC = ROOT / "data/derived/joint_row_level_cross_channel_control_alignment_diagnostic_v1.csv"
DIAGNOSTIC_SUMMARY = ROOT / "data/derived/joint_row_level_cross_channel_control_alignment_diagnostic_v1_summary.csv"

PACKAGE_FILES = [
    "docs/joint_row_level_cross_channel_control_alignment_review_package_v1.md",
    "data/source_manifest/joint_row_level_cross_channel_control_alignment_policy_v1.csv",
    "data/derived/joint_row_level_cross_channel_control_alignment_review_response_template_v1.csv",
    "data/derived/joint_row_level_cross_channel_control_alignment_diagnostic_v1.csv",
    "data/derived/joint_row_level_cross_channel_control_alignment_diagnostic_v1_summary.csv",
    "data/derived/joint_row_level_numeric_penalty_values_v1_summary.csv",
    "data/derived/joint_row_level_penalty_use_authorization_review_response_v1_summary.csv",
    "data/derived/joint_row_level_penalty_use_authorization_blocker_status_v1_summary.csv",
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
    return {
        "package_id": PACKAGE_ID,
        "package_path": rel,
        "byte_count": str(path.stat().st_size),
        "sha256": sha256(path),
        "contains_endpoint_residuals": "false",
        "contains_new_endpoint_scores": "false",
        "contains_fit_statistics": "false",
        "contains_aligned_joint_control_values": "false",
        "contains_lambda_row_numeric_value": "false",
        "contains_t_joint_rescoring": "false",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def main() -> None:
    use_auth = read_one(USE_AUTH)
    if use_auth["decision"] != "AUTHORIZE_PENALTY_USE_POLICY_ROUTE_PLANNING_ONLY_NOT_LAMBDA_NOT_RESCORING_NOT_VALIDATION":
        raise SystemExit("penalty use route planning is not authorized")
    rows = read_rows(VALUES)
    controls = [row for row in rows if row["row_type"] != "candidate"]
    by_channel: dict[str, list[dict[str, str]]] = defaultdict(list)
    family_counts: dict[str, Counter[str]] = defaultdict(Counter)
    for row in controls:
        by_channel[row["channel_id"]].append(row)
        family_counts[row["channel_id"]][row["control_family"]] += 1
    channels = sorted(by_channel)
    if len(channels) != 3:
        raise SystemExit(f"expected three active channels with controls, got {channels}")
    for ch in channels:
        by_channel[ch].sort(key=lambda r: (r["control_family"], r["control_id"]))

    min_count = min(len(by_channel[ch]) for ch in channels)
    diagnostic_rows = []
    for ch in channels:
        diagnostic_rows.append(
            {
                "diagnostic_id": "JRLC_ALIGN_DIAGNOSTIC_V1",
                "channel_id": ch,
                "control_count": str(len(by_channel[ch])),
                "control_family_counts": ";".join(f"{k}:{family_counts[ch][k]}" for k in sorted(family_counts[ch])),
                "deterministic_sort_key": "control_family,control_id",
                "min_index_aligned_count_if_accepted": str(min_count),
                "alignment_values_computed": "false",
                "endpoint_scoring_allowed": "false",
                "endpoint_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(DIAGNOSTIC, diagnostic_rows)
    diag_summary = {
        "diagnostic_id": "JRLC_ALIGN_DIAGNOSTIC_V1",
        "active_channels": "|".join(channels),
        "control_counts_by_channel": ";".join(f"{ch}:{len(by_channel[ch])}" for ch in channels),
        "min_index_aligned_count_if_accepted": str(min_count),
        "proposed_alignment_rule": "deterministic_min_count_index_alignment_after_sort_by_control_family_then_control_id",
        "alignment_values_computed": "false",
        "lambda_row_numeric_value_authorized": "false",
        "t_joint_rescoring_authorized": "false",
        "endpoint_validation_claimed": "false",
        "verdict": "CROSS_CHANNEL_CONTROL_ALIGNMENT_DESIGN_READY_FOR_REVIEW_NOT_COMPUTED",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(DIAGNOSTIC_SUMMARY, [diag_summary])

    policy_rows = [
        {
            "review_id": PACKAGE_ID,
            "question_id": "CCA_Q1_NEED",
            "question": "Is a residual-blind cross-channel control alignment required before any penalized joint score can be used?",
            "required_response": "accept_or_reject",
            "acceptance_condition": "Accept only if channel-local controls are insufficient for penalized joint-control comparison.",
            "forbidden_inputs": "endpoint_residuals;endpoint_scores;fit_improvements;posterior_chains;post_score_control_ranks",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "CCA_Q2_RULE",
            "question": "Is the proposed deterministic min-count index alignment rule acceptable as a design to test next?",
            "required_response": "accept_with_caveats_or_reject",
            "acceptance_condition": "Accept only as a design-review step; no aligned values are computed in this package.",
            "forbidden_inputs": "endpoint_residuals;endpoint_scores;fit_improvements;posterior_chains;post_score_control_ranks",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "CCA_Q3_BOUNDARY",
            "question": "Should aligned joint control values, lambda_row, and T_joint rescoring remain forbidden until separate authorization?",
            "required_response": "accept_or_reject",
            "acceptance_condition": "Accept only if this package remains a non-computing alignment design package.",
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
                "cross_channel_control_alignment_required": "false",
                "alignment_design_accepted": "false",
                "aligned_joint_control_values_authorized": "false",
                "lambda_row_numeric_value_authorized": "false",
                "t_joint_rescoring_authorized": "false",
            }
            for row in policy_rows
        ],
    )

    DOC.write_text(
        "\n".join(
            [
                "# Joint row-level cross-channel control alignment review package v1",
                "",
                "**Doc class:** external design-review handoff.",
                "**Status:** alignment design only; no aligned values; not `lambda_row`; not `T_joint` rescoring; not endpoint validation.",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`.",
                "",
                "The current numeric penalty values are channel-local for controls.",
                "Before any penalized joint-control comparison, a residual-blind",
                "cross-channel alignment rule must be accepted. This package proposes",
                "only a deterministic design for review:",
                "",
                "`sort controls by (control_family, control_id) within each channel,",
                "then align the first min_count controls by index across channels.`",
                "",
                "No aligned joint control values are computed here.",
                "",
                f"- active channels: `{diag_summary['active_channels']}`",
                f"- control counts: `{diag_summary['control_counts_by_channel']}`",
                f"- min aligned count if accepted: `{diag_summary['min_index_aligned_count_if_accepted']}`",
                "",
                "The severe count imbalance is explicit and remains a caveat. The",
                "reviewer may reject this design or accept it only as a cautious",
                "next-step alignment test.",
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
                "status": "JOINT_ROW_LEVEL_CROSS_CHANNEL_CONTROL_ALIGNMENT_REVIEW_PACKAGE_READY_NOT_COMPLETED",
                "zip_path": str(PACKAGE.relative_to(ROOT)),
                "zip_sha256_path": str(SHA.relative_to(ROOT)),
                "zip_sha256": digest,
                "package_file_count": str(len(package_rows)),
                "review_completed": "false",
                "cross_channel_control_alignment_required": "false",
                "alignment_design_accepted": "false",
                "aligned_joint_control_values_authorized": "false",
                "lambda_row_numeric_value_authorized": "false",
                "t_joint_rescoring_authorized": "false",
                "endpoint_scoring_allowed": "false",
                "endpoint_validation_claimed": "false",
                "contains_endpoint_residuals": "false",
                "contains_new_endpoint_scores": "false",
                "contains_fit_statistics": "false",
                "contains_aligned_joint_control_values": "false",
                "contains_lambda_row_numeric_value": "false",
                "contains_t_joint_rescoring": "false",
                "verdict": "cross_channel_control_alignment_design_review_package_ready_not_completed_not_scoring",
                "recommended_next_action": "send_zip_to_reviewer_before_any_aligned_control_values_or_lambda_or_rescoring",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    print(f"JOINT_ROW_LEVEL_CROSS_CHANNEL_CONTROL_ALIGNMENT_REVIEW_PACKAGE_V1_BUILT sha256={digest}")


if __name__ == "__main__":
    main()
