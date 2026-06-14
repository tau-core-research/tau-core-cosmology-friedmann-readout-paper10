#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMMON_EXPORT = ROOT / "data/derived/joint_common_source_feature_export_v5_summary.csv"
NORMALIZATION = ROOT / "data/derived/joint_channel_local_source_normalization_rule_v1_summary.csv"
TRANSFORM = ROOT / "data/derived/joint_candidate_control_symmetric_normalized_feature_transform_v1_summary.csv"
BINDING = ROOT / "data/derived/joint_row_level_penalty_block_weight_binding_shell_v1_summary.csv"
OUT = ROOT / "data/derived/joint_row_level_penalty_protocol_shell_v3.csv"
SUMMARY = ROOT / "data/derived/joint_row_level_penalty_protocol_shell_v3_summary.csv"
DOC = ROOT / "docs/joint_row_level_penalty_protocol_shell_v3.md"
CLAIM_BOUNDARY = "joint_row_level_penalty_protocol_shell_v3_not_scoring_not_validation"


def read_one(path: Path) -> dict[str, str]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
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


def main() -> None:
    common = read_one(COMMON_EXPORT)
    normalization = read_one(NORMALIZATION)
    transform = read_one(TRANSFORM)
    binding = read_one(BINDING)

    if common["source_feature_export_complete_for_penalty"] != "true":
        raise SystemExit("common source-feature export must be complete")
    if normalization["source_only_normalization_frozen"] != "true":
        raise SystemExit("source-only normalization must be frozen")
    if transform["candidate_control_symmetric_transform_built"] != "true":
        raise SystemExit("candidate/control symmetric transform must be built")
    if binding["binding_frozen_for_future_penalty_design"] != "true":
        raise SystemExit("block-weight binding shell must be frozen")
    for artifact_name, row in [
        ("common", common),
        ("normalization", normalization),
        ("transform", transform),
        ("binding", binding),
    ]:
        if row["numeric_t_joint_rescoring_allowed"] != "false":
            raise SystemExit(f"{artifact_name} artifact unexpectedly allows rescoring")
        if row["endpoint_validation_claimed"] != "false":
            raise SystemExit(f"{artifact_name} artifact unexpectedly claims validation")

    rows = [
        {
            "protocol_id": "JOINT_ROW_LEVEL_PENALTY_PROTOCOL_SHELL_V3",
            "requirement_id": "RLP_R1_SOURCE_FEATURE_INPUTS",
            "status": "SATISFIED",
            "evidence": (
                "joint_common_source_feature_export_v5;"
                f"channels={common['complete_or_caveated_feature_channels']};"
                f"rows={common['total_feature_rows']};"
                f"kids_row_controls={common['kids_row_level_controls_exported']}"
            ),
            "future_penalty_rule": "may_use_only_residual_blind_source_feature_artifacts",
            "forbidden_action": "do_not_read_endpoint_scores_residuals_or_fit_statistics",
            "numeric_t_joint_rescoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "protocol_id": "JOINT_ROW_LEVEL_PENALTY_PROTOCOL_SHELL_V3",
            "requirement_id": "RLP_R2_CHANNEL_LOCAL_NORMALIZATION",
            "status": "SATISFIED",
            "evidence": (
                "joint_channel_local_source_normalization_rule_v1;"
                f"channels={normalization['channels']};"
                f"rule={normalization['normalization_rule']}"
            ),
            "future_penalty_rule": "freeze per-channel source-only normalization before comparing rows or controls",
            "forbidden_action": "do_not_normalize_by_candidate_margin_AIC_chi2_or_T_joint_rank",
            "numeric_t_joint_rescoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "protocol_id": "JOINT_ROW_LEVEL_PENALTY_PROTOCOL_SHELL_V3",
            "requirement_id": "RLP_R3_CONTROL_SYMMETRY",
            "status": "SATISFIED",
            "evidence": (
                "joint_candidate_control_symmetric_normalized_feature_transform_v1;"
                f"rows={transform['normalized_feature_rows']};"
                f"row_type_counts={transform['row_type_counts']}"
            ),
            "future_penalty_rule": "candidate_and_controls_share_identical_source_feature_transform_and_null_family_scope",
            "forbidden_action": "do_not_apply_penalty_only_to_losing_controls_or_after_seeing_endpoint_order",
            "numeric_t_joint_rescoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "protocol_id": "JOINT_ROW_LEVEL_PENALTY_PROTOCOL_SHELL_V3",
            "requirement_id": "RLP_R4_COVARIANCE_OR_BLOCK_WEIGHT_BINDING",
            "status": "SATISFIED",
            "evidence": (
                "joint_row_level_penalty_block_weight_binding_shell_v1;"
                f"route={binding['covariance_binding_route']};"
                f"block_weight_policy={binding['block_weight_policy']};"
                f"channels={binding['active_channels']}"
            ),
            "future_penalty_rule": "future_penalty_must_use_same_block_weight_and_covariance_caveat_discipline_for_candidate_and_controls",
            "forbidden_action": "do_not_modify_T_joint_without_separate_scoring_authorization",
            "numeric_t_joint_rescoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "protocol_id": "JOINT_ROW_LEVEL_PENALTY_PROTOCOL_SHELL_V3",
            "requirement_id": "RLP_R5_SYMBOLIC_PENALTY_FORMULA",
            "status": "OPEN_REQUIRED",
            "evidence": "no symbolic row-level penalty formula has been defined or reviewed",
            "future_penalty_rule": "define_symbolic_formula_without_endpoint_scores_before_any_numeric_penalty_or_rescoring",
            "forbidden_action": "do_not_compute_numeric_penalty_or_rescore_T_joint_in_this_shell",
            "numeric_t_joint_rescoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    satisfied = sum(row["status"] == "SATISFIED" for row in rows)
    open_count = len(rows) - satisfied
    summary = {
        "protocol_id": "JOINT_ROW_LEVEL_PENALTY_PROTOCOL_SHELL_V3",
        "requirements_total": str(len(rows)),
        "requirements_satisfied": str(satisfied),
        "requirements_open": str(open_count),
        "source_feature_inputs_complete": "true",
        "channel_local_normalization_frozen": "true",
        "candidate_control_symmetric_transform_built": "true",
        "covariance_or_block_weight_binding_frozen": "true",
        "penalty_formula_defined": "false",
        "penalty_computed": "false",
        "numeric_t_joint_rescoring_allowed": "false",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "verdict": "ROW_LEVEL_PENALTY_INPUTS_AND_BINDING_READY_SYMBOLIC_FORMULA_STILL_OPEN",
        "next_required_action": "define_symbolic_row_level_penalty_formula_in_separate_non_scoring_gate",
        "claim_boundary": CLAIM_BOUNDARY,
    }

    write_csv(OUT, rows)
    write_csv(SUMMARY, [summary])
    DOC.write_text(
        "\n".join(
            [
                "# Joint row-level penalty protocol shell v3",
                "",
                "**Doc class:** protocol shell.",
                "**Status:** inputs and block-weight binding ready; symbolic penalty formula still open; not scoring; not validation.",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`.",
                "",
                "This shell supersedes v2 by closing the covariance/block-weight",
                "binding requirement through the non-scoring block-weight binding",
                "shell.  It still does not define a penalty formula, compute a",
                "penalty, authorize endpoint replay, or permit `T_joint` rescoring.",
                "",
                "Closed gates:",
                "",
                "- source-feature inputs;",
                "- channel-local source-only normalization;",
                "- candidate/control symmetric normalized transform;",
                "- covariance/block-weight binding shell.",
                "",
                "Open gate:",
                "",
                "- symbolic row-level penalty formula, in a separate non-scoring",
                "  review gate.",
                "",
                f"Verdict: `{summary['verdict']}`.",
                f"Next action: `{summary['next_required_action']}`.",
                "",
            ]
        )
    )
    print(
        "JOINT_ROW_LEVEL_PENALTY_PROTOCOL_SHELL_V3_BUILT "
        f"open={summary['requirements_open']}"
    )


if __name__ == "__main__":
    main()
