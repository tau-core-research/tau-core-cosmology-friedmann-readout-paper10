#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRANSFORM = ROOT / "data/derived/joint_candidate_control_symmetric_normalized_feature_transform_v1_summary.csv"
BD_SHELL = ROOT / "data/derived/joint_block_diagonal_likelihood_surrogate_protocol_shell_v1.csv"
BD_SUMMARY = ROOT / "data/derived/joint_block_diagonal_likelihood_surrogate_protocol_shell_v1_summary.csv"
CLOSURE_SUMMARY = ROOT / "data/derived/joint_cross_probe_covariance_closure_review_response_v1_summary.csv"
OUT = ROOT / "data/derived/joint_row_level_penalty_block_weight_binding_shell_v1.csv"
SUMMARY = ROOT / "data/derived/joint_row_level_penalty_block_weight_binding_shell_v1_summary.csv"
DOC = ROOT / "docs/joint_row_level_penalty_block_weight_binding_shell_v1.md"
CLAIM_BOUNDARY = "joint_row_level_penalty_block_weight_binding_shell_not_scoring_not_validation"


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


def parse_counts(counts: str) -> dict[tuple[str, str], int]:
    parsed: dict[tuple[str, str], int] = {}
    for part in counts.split(";"):
        if not part:
            continue
        left, value = part.split("=", 1)
        channel, row_type = left.split(":", 1)
        parsed[(channel, row_type)] = int(value)
    return parsed


def main() -> None:
    transform = read_one(TRANSFORM)
    bd_rows = read_rows(BD_SHELL)
    bd_summary = read_one(BD_SUMMARY)
    closure = read_one(CLOSURE_SUMMARY)

    if transform["candidate_control_symmetric_transform_built"] != "true":
        raise SystemExit("candidate/control symmetric transform must be built first")
    if transform["penalty_formula_defined"] != "false" or transform["penalty_computed"] != "false":
        raise SystemExit("transform must not define or compute a penalty")
    if bd_summary["endpoint_scoring_allowed"] != "false":
        raise SystemExit("block-diagonal shell must not allow endpoint scoring")
    if closure["endpoint_scoring_allowed"] != "false":
        raise SystemExit("covariance closure response must not allow endpoint scoring")
    if closure["future_scoring_precondition_closure_allowed"] != "true":
        raise SystemExit("covariance closure must allow only future precondition closure")

    counts = parse_counts(transform["row_type_counts"])
    active_channels = [row["channel_id"] for row in bd_rows]
    if sorted(active_channels) != sorted(transform["channels"].split(";")):
        raise SystemExit("transform channels and block-diagonal shell channels differ")

    channel_count = len(active_channels)
    equal_weight_expr = f"1/{channel_count}"
    rows: list[dict[str, str]] = []
    for row in bd_rows:
        channel = row["channel_id"]
        rows.append(
            {
                "binding_id": "JOINT_ROW_LEVEL_PENALTY_BLOCK_WEIGHT_BINDING_SHELL_V1",
                "channel_id": channel,
                "channel_order": row["channel_order"],
                "normalized_transform_artifact": "data/derived/joint_candidate_control_symmetric_normalized_feature_transform_v1.csv.gz",
                "candidate_rows_in_transform": str(counts.get((channel, "candidate"), 0)),
                "matched_control_rows_in_transform": str(counts.get((channel, "matched_control"), 0)),
                "covariance_block_rule": row["covariance_block_rule"],
                "likelihood_block_symbol": row["candidate_covariance_symbol"],
                "block_statistic_form": row["block_statistic_form"],
                "future_row_penalty_block_weight_symbol": f"omega_{row['channel_order']}",
                "future_row_penalty_block_weight_policy": "equal_channel_preweight_shell_only",
                "future_row_penalty_block_weight_value": equal_weight_expr,
                "candidate_control_same_transform_required": "true",
                "candidate_control_same_block_weight_required": "true",
                "candidate_control_same_covariance_required": row["candidate_control_same_covariance_required"],
                "cross_probe_covariance_product_available": closure["cross_probe_covariance_product_available"],
                "block_diagonal_independence_source_justified": closure["block_diagonal_independence_source_justified"],
                "binding_frozen_for_future_penalty_design": "true",
                "penalty_formula_defined": "false",
                "penalty_computed": "false",
                "numeric_t_joint_rescoring_allowed": "false",
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    write_csv(OUT, rows)

    summary = {
        "binding_id": "JOINT_ROW_LEVEL_PENALTY_BLOCK_WEIGHT_BINDING_SHELL_V1",
        "active_channel_count": str(channel_count),
        "active_channels": ";".join(active_channels),
        "normalized_feature_rows": transform["normalized_feature_rows"],
        "candidate_control_symmetric_transform_built": "true",
        "covariance_binding_route": "caveated_block_diagonal_independence",
        "cross_probe_covariance_product_available": closure["cross_probe_covariance_product_available"],
        "block_diagonal_independence_source_justified": closure["block_diagonal_independence_source_justified"],
        "block_weight_policy": "equal_channel_preweight_shell_only",
        "block_weight_value_per_channel": equal_weight_expr,
        "binding_frozen_for_future_penalty_design": "true",
        "penalty_formula_defined": "false",
        "penalty_computed": "false",
        "numeric_t_joint_rescoring_allowed": "false",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "verdict": "BLOCK_WEIGHT_BINDING_SHELL_FROZEN_NOT_SCORING",
        "next_required_action": "define_symbolic_row_level_penalty_formula_in_separate_non_scoring_gate",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(SUMMARY, [summary])

    DOC.write_text(
        "\n".join(
            [
                "# Joint row-level penalty block-weight binding shell v1",
                "",
                "**Doc class:** covariance/block-weight binding shell.",
                "**Status:** binding frozen for future penalty design; penalty not defined; not scoring; not validation.",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`.",
                "",
                "This shell binds the candidate/control-symmetric normalized feature",
                "transform to the existing caveated block-diagonal joint route.  It",
                "does not introduce a row-level penalty formula and does not modify",
                "`T_joint`.",
                "",
                "The only frozen block-weight policy is an equal-channel preweight",
                "shell, used solely as a future design constraint:",
                "",
                "\\[",
                f"  \\omega_i = {equal_weight_expr}, \\qquad i=1,\\ldots,{channel_count}.",
                "\\]",
                "",
                "A later penalty formula must apply the same normalized transform,",
                "the same channel weights, and the same covariance/caveat discipline",
                "to candidates and matched controls.  Any numeric rescoring still",
                "requires a separate authorization gate.",
                "",
                "Current machine state:",
                "",
                f"- active channels: `{summary['active_channels']}`",
                f"- normalized feature rows: `{summary['normalized_feature_rows']}`",
                f"- covariance binding route: `{summary['covariance_binding_route']}`",
                f"- cross-probe covariance product available: `{summary['cross_probe_covariance_product_available']}`",
                f"- block-diagonal independence source-justified: `{summary['block_diagonal_independence_source_justified']}`",
                f"- block-weight policy: `{summary['block_weight_policy']}`",
                f"- penalty formula defined: `{summary['penalty_formula_defined']}`",
                f"- numeric `T_joint` rescoring allowed: `{summary['numeric_t_joint_rescoring_allowed']}`",
                f"- verdict: `{summary['verdict']}`",
                "",
            ]
        )
    )
    print(
        "JOINT_ROW_LEVEL_PENALTY_BLOCK_WEIGHT_BINDING_SHELL_V1_BUILT "
        f"channels={channel_count}"
    )


if __name__ == "__main__":
    main()
