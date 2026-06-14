#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BINDING = ROOT / "data/derived/joint_row_level_penalty_block_weight_binding_shell_v1.csv"
BINDING_SUMMARY = ROOT / "data/derived/joint_row_level_penalty_block_weight_binding_shell_v1_summary.csv"
OUT = ROOT / "data/derived/joint_symbolic_row_level_penalty_formula_shell_v1.csv"
SUMMARY = ROOT / "data/derived/joint_symbolic_row_level_penalty_formula_shell_v1_summary.csv"
DOC = ROOT / "docs/joint_symbolic_row_level_penalty_formula_shell_v1.md"
CLAIM_BOUNDARY = "joint_symbolic_row_level_penalty_formula_shell_not_scoring_not_validation"


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


def main() -> None:
    binding_rows = read_rows(BINDING)
    binding_summary = read_one(BINDING_SUMMARY)
    if binding_summary["binding_frozen_for_future_penalty_design"] != "true":
        raise SystemExit("block-weight binding shell must be frozen")
    if binding_summary["penalty_computed"] != "false":
        raise SystemExit("binding shell must not compute a penalty")
    if binding_summary["numeric_t_joint_rescoring_allowed"] != "false":
        raise SystemExit("binding shell must not allow rescoring")

    rows: list[dict[str, str]] = []
    for row in binding_rows:
        channel = row["channel_id"]
        rows.append(
            {
                "formula_id": "JOINT_SYMBOLIC_ROW_LEVEL_PENALTY_FORMULA_SHELL_V1",
                "channel_id": channel,
                "channel_order": row["channel_order"],
                "input_transform_artifact": row["normalized_transform_artifact"],
                "normalized_feature_symbol": "z_{i,a,r,f}",
                "candidate_or_control_symbol": "a",
                "row_symbol": "r",
                "feature_symbol": "f",
                "channel_weight_symbol": row["future_row_penalty_block_weight_symbol"],
                "channel_weight_policy": row["future_row_penalty_block_weight_policy"],
                "channel_weight_value": row["future_row_penalty_block_weight_value"],
                "channel_penalty_symbol": "P_i(a)",
                "channel_penalty_formula": "P_i(a)=omega_i*mean_{r,f}(z_{i,a,r,f}^2)",
                "joint_penalty_symbol": "P_row(a)",
                "joint_penalty_formula": "P_row(a)=sum_i P_i(a)",
                "future_score_shell": "T_joint_penalized(a)=T_joint(a)+lambda_row*P_row(a)",
                "lambda_status": "symbolic_only_not_numeric_not_fit",
                "candidate_control_same_formula_required": "true",
                "candidate_control_same_transform_required": row["candidate_control_same_transform_required"],
                "candidate_control_same_block_weight_required": row["candidate_control_same_block_weight_required"],
                "candidate_control_same_covariance_required": row["candidate_control_same_covariance_required"],
                "uses_endpoint_scores_or_residuals": "false",
                "penalty_formula_defined": "true",
                "penalty_computed": "false",
                "numeric_penalty_values_written": "false",
                "numeric_t_joint_rescoring_allowed": "false",
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    write_csv(OUT, rows)

    summary = {
        "formula_id": "JOINT_SYMBOLIC_ROW_LEVEL_PENALTY_FORMULA_SHELL_V1",
        "active_channel_count": binding_summary["active_channel_count"],
        "active_channels": binding_summary["active_channels"],
        "input_transform_artifact": "data/derived/joint_candidate_control_symmetric_normalized_feature_transform_v1.csv.gz",
        "formula_family": "source_only_normalized_quadratic_feature_energy",
        "channel_penalty_formula": "P_i(a)=omega_i*mean_{r,f}(z_{i,a,r,f}^2)",
        "joint_penalty_formula": "P_row(a)=sum_i P_i(a)",
        "future_score_shell": "T_joint_penalized(a)=T_joint(a)+lambda_row*P_row(a)",
        "lambda_status": "symbolic_only_not_numeric_not_fit",
        "candidate_control_same_formula_required": "true",
        "candidate_control_same_transform_required": "true",
        "candidate_control_same_block_weight_required": "true",
        "candidate_control_same_covariance_required": "true",
        "uses_endpoint_scores_or_residuals": "false",
        "penalty_formula_defined": "true",
        "penalty_computed": "false",
        "numeric_penalty_values_written": "false",
        "numeric_t_joint_rescoring_allowed": "false",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "verdict": "SYMBOLIC_ROW_LEVEL_PENALTY_FORMULA_FROZEN_NOT_COMPUTED_NOT_SCORING",
        "next_required_action": "prepare_numeric_penalty_computation_authorization_review_package_before_any_values_or_rescoring",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(SUMMARY, [summary])

    DOC.write_text(
        "\n".join(
            [
                "# Joint symbolic row-level penalty formula shell v1",
                "",
                "**Doc class:** symbolic formula shell.",
                "**Status:** formula defined symbolically; no numeric penalty; not scoring; not validation.",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`.",
                "",
                "This artifact freezes only the symbolic shape of a possible future",
                "row-level source-feature penalty. It does not read endpoint residuals,",
                "does not compute penalty values, does not choose a numeric",
                "`lambda_row`, and does not modify `T_joint`.",
                "",
                "For candidate or control alternative \\(a\\), channel \\(i\\), row",
                "\\(r\\), and source feature \\(f\\), let \\(z_{i,a,r,f}\\) denote the",
                "already frozen normalized source feature.  The frozen symbolic shell is:",
                "",
                "\\[",
                "  P_i(a) = \\omega_i\\,\\mathrm{mean}_{r,f}\\, z_{i,a,r,f}^2,",
                "\\]",
                "",
                "\\[",
                "  P_{\\rm row}(a) = \\sum_i P_i(a),",
                "\\]",
                "",
                "with the already frozen equal-channel preweight shell \\(\\omega_i=1/3\\)",
                "for the three active channels.  A possible future score shell would be",
                "",
                "\\[",
                "  T_{\\rm joint}^{\\rm penalized}(a)",
                "  = T_{\\rm joint}(a) + \\lambda_{\\rm row} P_{\\rm row}(a),",
                "\\]",
                "",
                "but \\(\\lambda_{\\rm row}\\) is symbolic only here. No numeric value is",
                "chosen, fitted, inferred, or applied.",
                "",
                "The formula is candidate/control symmetric: every candidate and every",
                "matched control must use the same normalized transform, same block",
                "weights, same covariance/caveat discipline, and same formula.",
                "",
                f"Verdict: `{summary['verdict']}`.",
                f"Next action: `{summary['next_required_action']}`.",
                "",
            ]
        )
    )
    print(
        "JOINT_SYMBOLIC_ROW_LEVEL_PENALTY_FORMULA_SHELL_V1_BUILT "
        f"channels={summary['active_channel_count']}"
    )


if __name__ == "__main__":
    main()
