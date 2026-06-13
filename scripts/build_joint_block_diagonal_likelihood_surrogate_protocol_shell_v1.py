#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BDI_SUMMARY = ROOT / "data/derived/joint_block_diagonal_independence_review_response_v1_summary.csv"
BINDING = ROOT / "data/derived/joint_single_statistic_binding_prerequisites_v1.csv"
BINDING_SUMMARY = ROOT / "data/derived/joint_single_statistic_binding_prerequisites_v1_summary.csv"
OUT = ROOT / "data/derived/joint_block_diagonal_likelihood_surrogate_protocol_shell_v1.csv"
SUMMARY = ROOT / "data/derived/joint_block_diagonal_likelihood_surrogate_protocol_shell_v1_summary.csv"
DOC = ROOT / "docs/joint_block_diagonal_likelihood_surrogate_protocol_shell_v1.md"
CLAIM_BOUNDARY = "joint_block_diagonal_likelihood_surrogate_protocol_shell_not_scoring_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path.relative_to(ROOT)}")
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
    bdi = read_one(BDI_SUMMARY)
    binding = read_rows(BINDING)
    binding_summary = read_one(BINDING_SUMMARY)
    if binding_summary["verdict"] != "JOINT_SINGLE_STATISTIC_BINDING_PREREQUISITES_FROZEN_PROTOCOL_BLOCKED":
        raise SystemExit("single-statistic binding prerequisites must remain protocol-blocked")
    if binding_summary["endpoint_scoring_allowed"] != "false":
        raise SystemExit("binding prerequisites unexpectedly allow endpoint scoring")
    if bdi["endpoint_scoring_allowed"] != "false":
        raise SystemExit("block-diagonal review unexpectedly allows endpoint scoring")

    review_completed = bdi["response_status"] != "not_completed"
    shell_allowed = bdi["future_protocol_shell_allowed"] == "true"
    covariance_closed = bdi["cross_probe_covariance_defined"] == "true"
    independence_closed = bdi["cross_probe_independence_status"] in {
        "manual_followup_completed",
        "source_independence_closed",
    }
    protocol_executable = review_completed and shell_allowed and (covariance_closed or independence_closed)

    rows: list[dict[str, str]] = []
    for row in binding:
        rows.append(
            {
                "protocol_id": "JOINT_BLOCK_DIAGONAL_LIKELIHOOD_SURROGATE_PROTOCOL_SHELL_V1",
                "channel_id": row["channel_id"],
                "channel_order": row["channel_order"],
                "row_scope_artifact": row["row_scope_artifact"],
                "score_source_artifact": row["score_source_artifact"],
                "covariance_block_rule": row["covariance_artifact"],
                "nuisance_or_amplitude_rule": row["nuisance_or_amplitude_rule"],
                "candidate_residual_symbol": f"r_{row['channel_order']}",
                "candidate_covariance_symbol": f"C_{row['channel_order']}",
                "block_statistic_form": "r_i^T C_i^{-1} r_i",
                "joint_surrogate_form": "sum_i r_i^T C_i^{-1} r_i",
                "candidate_control_same_statistic_required": "true",
                "candidate_control_same_covariance_required": "true",
                "review_response_status": bdi["response_status"],
                "future_protocol_shell_allowed_by_review": str(shell_allowed).lower(),
                "cross_probe_covariance_defined": str(covariance_closed).lower(),
                "cross_probe_independence_closed": str(independence_closed).lower(),
                "protocol_executable": str(protocol_executable).lower(),
                "contains_endpoint_residuals": "false",
                "contains_new_endpoint_scores": "false",
                "contains_fit_statistics": "false",
                "endpoint_scoring_allowed": "false",
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(OUT, rows)

    if not review_completed:
        verdict = "JOINT_BLOCK_DIAGONAL_PROTOCOL_SHELL_DRAFT_WAITING_FOR_REVIEW_NOT_SCORING"
        next_action = "complete_block_diagonal_independence_review_response"
    elif shell_allowed and not protocol_executable:
        verdict = "JOINT_BLOCK_DIAGONAL_PROTOCOL_SHELL_FROZEN_COVARIANCE_STILL_OPEN_NOT_SCORING"
        next_action = "close_cross_probe_covariance_or_independence_before_any_scoring"
    elif protocol_executable:
        verdict = "JOINT_BLOCK_DIAGONAL_PROTOCOL_SHELL_REVIEWED_BUT_SCORING_STILL_REQUIRES_SEPARATE_AUTHORIZATION"
        next_action = "prepare_separate_single_statistic_scoring_authorization_package"
    else:
        verdict = "JOINT_BLOCK_DIAGONAL_PROTOCOL_SHELL_REJECTED_NOT_SCORING"
        next_action = "revise_covariance_route_or_seek_source_native_cross_probe_covariance"

    summary = {
        "protocol_id": "JOINT_BLOCK_DIAGONAL_LIKELIHOOD_SURROGATE_PROTOCOL_SHELL_V1",
        "active_channel_count": str(len(rows)),
        "active_channel_order": ";".join(row["channel_id"] for row in rows),
        "review_response_status": bdi["response_status"],
        "review_decision": bdi["decision"],
        "future_protocol_shell_allowed_by_review": str(shell_allowed).lower(),
        "cross_probe_covariance_defined": str(covariance_closed).lower(),
        "cross_probe_independence_closed": str(independence_closed).lower(),
        "single_joint_surrogate_form_declared": "true",
        "candidate_control_same_statistic_required": "true",
        "candidate_control_same_covariance_required": "true",
        "protocol_executable": str(protocol_executable).lower(),
        "contains_endpoint_residuals": "false",
        "contains_new_endpoint_scores": "false",
        "contains_fit_statistics": "false",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "next_required_action": next_action,
        "verdict": verdict,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(SUMMARY, [summary])

    DOC.write_text(
        "\n".join(
            [
                "# Joint block-diagonal likelihood-surrogate protocol shell v1",
                "",
                "**Doc class:** protocol shell draft",
                "**Status:** not scoring; not endpoint validation; not cosmological validation",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`",
                "",
                "This artifact freezes the algebraic shape of a possible future",
                "block-diagonal likelihood-surrogate for the three active Paper10",
                "channels. It is a shell only: it does not read endpoint residuals,",
                "does not invert new covariance matrices, does not compute a score,",
                "and does not authorize a replay.",
                "",
                "The predeclared shell is:",
                "",
                "\\[",
                "  Q_{\\rm joint}^{\\rm BD} = \\sum_i r_i^T C_i^{-1} r_i,",
                "\\]",
                "",
                "where each block must use the same row scope, score-source artifact,",
                "covariance block, nuisance rule, and statistic for the candidate and",
                "all matched controls.",
                "",
                "Current machine state:",
                "",
                f"- active channels: `{summary['active_channel_order']}`",
                f"- block-diagonal review status: `{summary['review_response_status']}`",
                f"- protocol shell allowed by review: `{summary['future_protocol_shell_allowed_by_review']}`",
                f"- cross-probe covariance defined: `{summary['cross_probe_covariance_defined']}`",
                f"- cross-probe independence closed: `{summary['cross_probe_independence_closed']}`",
                f"- executable now: `{summary['protocol_executable']}`",
                f"- endpoint scoring allowed: `{summary['endpoint_scoring_allowed']}`",
                f"- verdict: `{summary['verdict']}`",
                "",
            ]
        )
    )
    print(
        "JOINT_BLOCK_DIAGONAL_LIKELIHOOD_SURROGATE_PROTOCOL_SHELL_V1_BUILT "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()
