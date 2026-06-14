#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
V3 = ROOT / "data/derived/joint_row_level_penalty_protocol_shell_v3_summary.csv"
FORMULA = ROOT / "data/derived/joint_symbolic_row_level_penalty_formula_shell_v1_summary.csv"
OUT = ROOT / "data/derived/joint_row_level_penalty_protocol_shell_v4.csv"
SUMMARY = ROOT / "data/derived/joint_row_level_penalty_protocol_shell_v4_summary.csv"
DOC = ROOT / "docs/joint_row_level_penalty_protocol_shell_v4.md"
CLAIM_BOUNDARY = "joint_row_level_penalty_protocol_shell_v4_not_scoring_not_validation"


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
    v3 = read_one(V3)
    formula = read_one(FORMULA)
    if v3["requirements_satisfied"] != "4" or v3["requirements_open"] != "1":
        raise SystemExit("v3 protocol shell must have exactly the symbolic formula gate open")
    if formula["penalty_formula_defined"] != "true":
        raise SystemExit("symbolic penalty formula must be defined")
    if formula["penalty_computed"] != "false":
        raise SystemExit("symbolic formula shell must not compute penalty")
    if formula["numeric_t_joint_rescoring_allowed"] != "false":
        raise SystemExit("symbolic formula shell must not allow rescoring")
    if formula["uses_endpoint_scores_or_residuals"] != "false":
        raise SystemExit("symbolic formula must not use endpoint scores/residuals")

    rows = [
        {
            "protocol_id": "JOINT_ROW_LEVEL_PENALTY_PROTOCOL_SHELL_V4",
            "requirement_id": "RLP_R1_SOURCE_FEATURE_INPUTS",
            "status": "SATISFIED",
            "evidence": "joint_common_source_feature_export_v5",
            "future_penalty_rule": "may_use_only_residual_blind_source_feature_artifacts",
            "forbidden_action": "do_not_read_endpoint_scores_residuals_or_fit_statistics",
            "numeric_t_joint_rescoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "protocol_id": "JOINT_ROW_LEVEL_PENALTY_PROTOCOL_SHELL_V4",
            "requirement_id": "RLP_R2_CHANNEL_LOCAL_NORMALIZATION",
            "status": "SATISFIED",
            "evidence": "joint_channel_local_source_normalization_rule_v1",
            "future_penalty_rule": "use_frozen_channel_local_source_only_normalization",
            "forbidden_action": "do_not_normalize_by_candidate_margin_AIC_chi2_or_T_joint_rank",
            "numeric_t_joint_rescoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "protocol_id": "JOINT_ROW_LEVEL_PENALTY_PROTOCOL_SHELL_V4",
            "requirement_id": "RLP_R3_CONTROL_SYMMETRY",
            "status": "SATISFIED",
            "evidence": "joint_candidate_control_symmetric_normalized_feature_transform_v1",
            "future_penalty_rule": "candidate_and_controls_share_identical_source_feature_transform_and_null_family_scope",
            "forbidden_action": "do_not_apply_penalty_only_to_losing_controls_or_after_seeing_endpoint_order",
            "numeric_t_joint_rescoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "protocol_id": "JOINT_ROW_LEVEL_PENALTY_PROTOCOL_SHELL_V4",
            "requirement_id": "RLP_R4_COVARIANCE_OR_BLOCK_WEIGHT_BINDING",
            "status": "SATISFIED",
            "evidence": "joint_row_level_penalty_block_weight_binding_shell_v1",
            "future_penalty_rule": "same_block_weight_and_covariance_caveat_discipline_for_candidate_and_controls",
            "forbidden_action": "do_not_modify_T_joint_without_separate_scoring_authorization",
            "numeric_t_joint_rescoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "protocol_id": "JOINT_ROW_LEVEL_PENALTY_PROTOCOL_SHELL_V4",
            "requirement_id": "RLP_R5_SYMBOLIC_PENALTY_FORMULA",
            "status": "SATISFIED",
            "evidence": "joint_symbolic_row_level_penalty_formula_shell_v1",
            "future_penalty_rule": formula["future_score_shell"],
            "forbidden_action": "do_not_choose_lambda_row_or_compute_numeric_penalty_in_this_shell",
            "numeric_t_joint_rescoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "protocol_id": "JOINT_ROW_LEVEL_PENALTY_PROTOCOL_SHELL_V4",
            "requirement_id": "RLP_R6_NUMERIC_PENALTY_COMPUTATION_AUTHORIZATION",
            "status": "OPEN_REQUIRED",
            "evidence": "no numeric penalty computation or lambda_row authorization has been reviewed",
            "future_penalty_rule": "numeric_penalty_values_and_lambda_row_require_separate_authorization_before_any_rescoring",
            "forbidden_action": "do_not_compute_numeric_penalty_values_or_rescore_T_joint",
            "numeric_t_joint_rescoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    satisfied = sum(row["status"] == "SATISFIED" for row in rows)
    open_count = len(rows) - satisfied
    summary = {
        "protocol_id": "JOINT_ROW_LEVEL_PENALTY_PROTOCOL_SHELL_V4",
        "requirements_total": str(len(rows)),
        "requirements_satisfied": str(satisfied),
        "requirements_open": str(open_count),
        "source_feature_inputs_complete": "true",
        "channel_local_normalization_frozen": "true",
        "candidate_control_symmetric_transform_built": "true",
        "covariance_or_block_weight_binding_frozen": "true",
        "symbolic_penalty_formula_defined": "true",
        "penalty_formula_defined": "true",
        "penalty_computed": "false",
        "lambda_row_numeric_value_defined": "false",
        "numeric_penalty_values_written": "false",
        "numeric_t_joint_rescoring_allowed": "false",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "verdict": "SYMBOLIC_ROW_LEVEL_PENALTY_READY_NUMERIC_AUTHORIZATION_STILL_OPEN",
        "next_required_action": "prepare_numeric_penalty_computation_authorization_review_package_before_any_values_or_rescoring",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(OUT, rows)
    write_csv(SUMMARY, [summary])
    DOC.write_text(
        "\n".join(
            [
                "# Joint row-level penalty protocol shell v4",
                "",
                "**Doc class:** protocol shell.",
                "**Status:** symbolic row-level penalty ready; numeric computation authorization open; not scoring; not validation.",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`.",
                "",
                "This shell supersedes v3 by closing the symbolic formula gate through",
                "the non-scoring symbolic formula shell. It still does not compute",
                "numeric penalty values, choose `lambda_row`, authorize endpoint",
                "replay, or permit `T_joint` rescoring.",
                "",
                "Frozen symbolic score shell:",
                "",
                f"`{formula['future_score_shell']}`",
                "",
                "Open gate:",
                "",
                "- numeric penalty computation and `lambda_row` authorization, in a",
                "  separate review package.",
                "",
                f"Verdict: `{summary['verdict']}`.",
                f"Next action: `{summary['next_required_action']}`.",
                "",
            ]
        )
    )
    print(
        "JOINT_ROW_LEVEL_PENALTY_PROTOCOL_SHELL_V4_BUILT "
        f"open={summary['requirements_open']}"
    )


if __name__ == "__main__":
    main()
