#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BINDING = ROOT / "data/derived/joint_single_statistic_binding_prerequisites_v1.csv"
BINDING_SUMMARY = ROOT / "data/derived/joint_single_statistic_binding_prerequisites_v1_summary.csv"
CONTROL_READY = ROOT / "data/derived/joint_matched_control_implementation_readiness_v1_summary.csv"
COV_PLAN = ROOT / "data/derived/joint_covariance_resolution_plan_v1_summary.csv"
OUT = ROOT / "data/derived/joint_single_statistic_protocol_shell_v1.csv"
SUMMARY = ROOT / "data/derived/joint_single_statistic_protocol_shell_v1_summary.csv"
DOC = ROOT / "docs/joint_single_statistic_protocol_shell_v1.md"
CLAIM_BOUNDARY = "joint_single_statistic_protocol_shell_not_scoring_not_validation"


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
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    binding_rows = read_rows(BINDING)
    binding_summary = read_one(BINDING_SUMMARY)
    control_ready = read_one(CONTROL_READY)
    cov_plan = read_one(COV_PLAN)

    if binding_summary["single_joint_statistic_defined"] != "false":
        raise SystemExit("protocol shell expects no executable single statistic yet")
    if binding_summary["ready_for_single_statistic_protocol"] != "false":
        raise SystemExit("binding prerequisites must remain protocol-blocked")
    if control_ready["implementation_ready_for_scoring"] != "false":
        raise SystemExit("matched controls must remain not scoring-ready")
    if cov_plan["cross_probe_covariance_defined"] != "false":
        raise SystemExit("cross-probe covariance must remain open for this shell")

    rows: list[dict[str, str]] = []
    for binding in binding_rows:
        rows.append(
            {
                "protocol_id": "JOINT_SINGLE_STATISTIC_PROTOCOL_SHELL_V1",
                "channel_order": binding["channel_order"],
                "channel_id": binding["channel_id"],
                "kernel_role": binding["kernel_role"],
                "q_i": binding["q_i"],
                "row_scope_artifact": binding["row_scope_artifact"],
                "score_source_artifact": binding["score_source_artifact"],
                "covariance_artifact": binding["covariance_artifact"],
                "symbolic_channel_statistic": "z_i = signed_standardized_channel_response(candidate_or_control_i)",
                "symbolic_joint_statistic": "T_joint = sum_i q_i z_i",
                "same_formula_for_candidate_and_controls": "true",
                "same_rows_for_candidate_and_controls": "true",
                "same_covariance_for_candidate_and_controls": "true",
                "uses_observed_endpoint_values": "false",
                "computes_numeric_statistic_now": "false",
                "protocol_executable": "false",
                "endpoint_scoring_allowed": "false",
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(OUT, rows)

    summary = {
        "protocol_id": "JOINT_SINGLE_STATISTIC_PROTOCOL_SHELL_V1",
        "active_channel_count": str(len(rows)),
        "active_channel_order": ";".join(row["channel_id"] for row in rows),
        "symbolic_joint_statistic": "T_joint = sum_i q_i z_i",
        "candidate_control_same_formula_required": "true",
        "candidate_control_same_rows_required": "true",
        "candidate_control_same_covariance_required": "true",
        "single_joint_statistic_defined": "false",
        "protocol_executable": "false",
        "cross_probe_covariance_defined": cov_plan["cross_probe_covariance_defined"],
        "matched_controls_ready_for_scoring": control_ready["implementation_ready_for_scoring"],
        "contains_endpoint_residuals": "false",
        "contains_new_endpoint_scores": "false",
        "contains_fit_statistics": "false",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "next_required_action": "freeze_covariance_route_and_build_same_statistic_controls_before_numeric_T_joint",
        "verdict": "JOINT_SINGLE_STATISTIC_PROTOCOL_SHELL_FROZEN_SYMBOLIC_NOT_EXECUTABLE",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(SUMMARY, [summary])

    DOC.write_text(
        "\n".join(
            [
                "# Joint single-statistic protocol shell v1",
                "",
                "**Doc class:** symbolic protocol shell",
                "**Status:** not executable; not scoring; not endpoint validation; not cosmological validation",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`",
                "",
                "This shell states the future joint statistic form that candidate and",
                "matched controls must share. It does not compute the statistic.",
                "",
                "Symbolic form:",
                "",
                "```text",
                "z_i = signed_standardized_channel_response(candidate_or_control_i)",
                "T_joint = sum_i q_i z_i",
                "```",
                "",
                "The formula is only admissible for scoring after the covariance route,",
                "row scope, channel standardization, and matched-control suite are frozen",
                "for candidate and controls together.",
                "",
                "Summary:",
                "",
                f"- active channels: `{summary['active_channel_order']}`",
                f"- symbolic joint statistic: `{summary['symbolic_joint_statistic']}`",
                f"- single joint statistic defined: `{summary['single_joint_statistic_defined']}`",
                f"- protocol executable: `{summary['protocol_executable']}`",
                f"- cross-probe covariance defined: `{summary['cross_probe_covariance_defined']}`",
                f"- matched controls ready for scoring: `{summary['matched_controls_ready_for_scoring']}`",
                f"- verdict: `{summary['verdict']}`",
                "",
            ]
        )
    )
    print(
        "JOINT_SINGLE_STATISTIC_PROTOCOL_SHELL_V1_BUILT "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()
