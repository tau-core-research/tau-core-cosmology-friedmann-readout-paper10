#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMMON_EXPORT = ROOT / "data/derived/joint_common_source_feature_export_v5_summary.csv"
NORMALIZATION = ROOT / "data/derived/joint_channel_local_source_normalization_rule_v1_summary.csv"
TRANSFORM = ROOT / "data/derived/joint_candidate_control_symmetric_normalized_feature_transform_v1_summary.csv"
OUT = ROOT / "data/derived/joint_row_level_penalty_protocol_shell_v2.csv"
SUMMARY = ROOT / "data/derived/joint_row_level_penalty_protocol_shell_v2_summary.csv"
DOC = ROOT / "docs/joint_row_level_penalty_protocol_shell_v2.md"
CLAIM_BOUNDARY = "joint_row_level_penalty_protocol_shell_v2_not_scoring_not_validation"


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
    if common["source_feature_export_complete_for_penalty"] != "true":
        raise SystemExit("common source-feature export is not complete for penalty design")
    if common["numeric_t_joint_rescoring_allowed"] != "false":
        raise SystemExit("common source-feature export must not authorize rescoring")
    if common["endpoint_validation_claimed"] != "false":
        raise SystemExit("common source-feature export must not claim validation")
    if normalization["source_only_normalization_frozen"] != "true":
        raise SystemExit("source-only normalization must be frozen")
    if normalization["normalization_applied_to_scoring"] != "false":
        raise SystemExit("normalization must not be applied to scoring")
    if transform["candidate_control_symmetric_transform_built"] != "true":
        raise SystemExit("candidate/control symmetric transform must be built")
    if transform["penalty_computed"] != "false":
        raise SystemExit("transform must not compute penalty")

    rows = [
        {
            "protocol_id": "JOINT_ROW_LEVEL_PENALTY_PROTOCOL_SHELL_V2",
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
            "protocol_id": "JOINT_ROW_LEVEL_PENALTY_PROTOCOL_SHELL_V2",
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
            "protocol_id": "JOINT_ROW_LEVEL_PENALTY_PROTOCOL_SHELL_V2",
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
            "protocol_id": "JOINT_ROW_LEVEL_PENALTY_PROTOCOL_SHELL_V2",
            "requirement_id": "RLP_R4_COVARIANCE_OR_BLOCK_WEIGHT_BINDING",
            "status": "OPEN_REQUIRED",
            "evidence": "row-level feature penalty has not been bound to the block-diagonal/cross-probe covariance shell",
            "future_penalty_rule": "bind_penalty_to_predeclared_joint_likelihood_surrogate_before_any_score_change",
            "forbidden_action": "do_not_modify_T_joint_without_separate_scoring_authorization",
            "numeric_t_joint_rescoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    satisfied = sum(row["status"] == "SATISFIED" for row in rows)
    open_count = len(rows) - satisfied
    summary = {
        "protocol_id": "JOINT_ROW_LEVEL_PENALTY_PROTOCOL_SHELL_V2",
        "requirements_total": str(len(rows)),
        "requirements_satisfied": str(satisfied),
        "requirements_open": str(open_count),
        "source_feature_inputs_complete": "true",
        "channel_local_normalization_frozen": "true",
        "candidate_control_symmetric_transform_built": "true",
        "penalty_formula_defined": "false",
        "penalty_computed": "false",
        "numeric_t_joint_rescoring_allowed": "false",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "verdict": "NORMALIZED_SYMMETRIC_TRANSFORM_READY_COVARIANCE_BINDING_STILL_OPEN",
        "next_required_action": "bind_transform_to_covariance_or_block_weight_shell_before_any_penalty_formula",
        "claim_boundary": CLAIM_BOUNDARY,
    }

    write_csv(OUT, rows)
    write_csv(SUMMARY, [summary])
    DOC.write_text(
        "\n".join(
            [
                "# Joint row-level penalty protocol shell v2",
                "",
                "**Doc class:** protocol shell.",
                "**Status:** normalized symmetric transform ready; penalty not defined; not scoring; not validation.",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`.",
                "",
                "This shell updates v1 after freezing the channel-local source-only",
                "normalization rule and the candidate/control symmetric normalized",
                "feature transform.",
                "",
                "The shell does not define a penalty formula, does not compute a penalty,",
                "does not authorize endpoint replay, and does not permit `T_joint`",
                "rescoring. Before any score can change, the normalized transform must",
                "be bound to a covariance or block-weight shell in a separate reviewed",
                "gate.",
                "",
                f"Verdict: `{summary['verdict']}`.",
                f"Next action: `{summary['next_required_action']}`.",
                "",
            ]
        )
    )
    print(
        "JOINT_ROW_LEVEL_PENALTY_PROTOCOL_SHELL_V2_BUILT "
        f"open={summary['requirements_open']}"
    )


if __name__ == "__main__":
    main()
