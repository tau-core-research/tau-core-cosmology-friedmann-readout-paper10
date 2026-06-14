#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COV_GATE = ROOT / "data/derived/joint_covariance_model_requirements_gate_v1.csv"
COV_SUMMARY = ROOT / "data/derived/joint_covariance_model_requirements_gate_v1_summary.csv"
SOURCE_REQ = ROOT / "data/derived/joint_cross_probe_covariance_source_requirements_v1.csv"
SOURCE_REQ_SUMMARY = ROOT / "data/derived/joint_cross_probe_covariance_source_requirements_v1_summary.csv"
PROTOCOL_SHELL = ROOT / "data/derived/joint_block_diagonal_likelihood_surrogate_protocol_shell_v1_summary.csv"
OUT = ROOT / "data/derived/joint_covariance_resolution_plan_v1.csv"
SUMMARY = ROOT / "data/derived/joint_covariance_resolution_plan_v1_summary.csv"
DOC = ROOT / "docs/joint_covariance_resolution_plan_v1.md"
CLAIM_BOUNDARY = "joint_covariance_resolution_plan_not_scoring_not_validation"


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
    cov_rows = read_rows(COV_GATE)
    cov_summary = read_one(COV_SUMMARY)
    req_rows = read_rows(SOURCE_REQ)
    req_summary = read_one(SOURCE_REQ_SUMMARY)
    protocol = read_one(PROTOCOL_SHELL)

    if cov_summary["cross_probe_covariance_defined"] != "false":
        raise SystemExit("this plan is only valid while cross-probe covariance is not defined")
    if req_summary["independence_rationale_route_ready"] != "true":
        raise SystemExit("expected caveated independence route to be ready")
    if protocol["protocol_executable"] != "false":
        raise SystemExit("protocol shell must remain non-executable")

    req_by_id = {row["requirement_id"]: row for row in req_rows}
    rows = [
        {
            "plan_id": "JOINT_COVARIANCE_RESOLUTION_PLAN_V1",
            "resolution_route": "source_native_cross_probe_covariance_product",
            "resolution_rank": "1",
            "required_artifact": "published_joint_covariance_or_official_mock_covariance_or_source_frozen_analytic_cross_covariance",
            "current_status": req_by_id["CPC_SRC_02_CROSS_COV_PRODUCT"]["current_status"],
            "current_evidence": req_by_id["CPC_SRC_02_CROSS_COV_PRODUCT"]["current_evidence"],
            "exit_condition": "cross_probe_covariance_defined=true_and_candidate_controls_bound_to_same_covariance",
            "allowed_to_score_now": "false",
            "why_preferred": "would remove the strongest covariance blocker without relying on block-diagonal independence",
        },
        {
            "plan_id": "JOINT_COVARIANCE_RESOLUTION_PLAN_V1",
            "resolution_route": "caveated_block_diagonal_surrogate",
            "resolution_rank": "2",
            "required_artifact": "reviewed_block_diagonal_surrogate_with_shared_sky_redshift_kernel_nuisance_and_population_caveats",
            "current_status": req_by_id["CPC_SRC_06_BLOCK_DIAGONAL_LIMITS"]["current_status"],
            "current_evidence": req_by_id["CPC_SRC_06_BLOCK_DIAGONAL_LIMITS"]["current_evidence"],
            "exit_condition": "block_diagonal_surrogate_allowed_for_scoring_under_separate_authorization_and_same_statistic_controls",
            "allowed_to_score_now": "false",
            "why_preferred": "is the fastest documented path but remains caveated and cannot become validation by itself",
        },
        {
            "plan_id": "JOINT_COVARIANCE_RESOLUTION_PLAN_V1",
            "resolution_route": "same_statistic_control_binding",
            "resolution_rank": "3",
            "required_artifact": "candidate_and_all_controls_use_same_block_covariance_same_rows_same_statistic_same_caveats",
            "current_status": req_by_id["CPC_SRC_07_SAME_STATISTIC_AND_CONTROLS"]["current_status"],
            "current_evidence": req_by_id["CPC_SRC_07_SAME_STATISTIC_AND_CONTROLS"]["current_evidence"],
            "exit_condition": "same_statistic_matched_control_suite_implemented_and_validates_without_endpoint_leakage",
            "allowed_to_score_now": "false",
            "why_preferred": "prevents the block-diagonal route from becoming a candidate-only convenience statistic",
        },
    ]
    for row in rows:
        row.update(
            {
                "endpoint_scoring_allowed": "false",
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(OUT, rows)

    hard_blocks = [row for row in cov_rows if row["hard_blocker"] == "true"]
    summary = {
        "plan_id": "JOINT_COVARIANCE_RESOLUTION_PLAN_V1",
        "active_channel_order": cov_summary["active_channel_order"],
        "block_covariance_blocks_available": cov_summary["channel_covariance_blocks_available"],
        "block_covariance_blocks_total": cov_summary["channel_covariance_blocks_total"],
        "cross_probe_covariance_defined": cov_summary["cross_probe_covariance_defined"],
        "independence_rationale_route_ready": req_summary["independence_rationale_route_ready"],
        "block_diagonal_protocol_shell_declared": protocol["single_joint_surrogate_form_declared"],
        "hard_covariance_blockers_current": str(len(hard_blocks)),
        "resolution_routes_frozen": str(len(rows)),
        "fastest_route": "caveated_block_diagonal_surrogate_plus_same_statistic_controls",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "verdict": "COVARIANCE_RESOLUTION_ROUTES_FROZEN_CROSS_PROBE_STILL_OPEN_NOT_SCORING",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(SUMMARY, [summary])
    DOC.write_text(
        "\n".join(
            [
                "# Joint covariance resolution plan v1",
                "",
                "**Doc class:** post-replay covariance blocker-resolution plan",
                "**Status:** not scoring; not endpoint validation; not cosmological validation",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`",
                "",
                "This plan freezes the allowed routes for resolving the second promotion",
                "blocker in the joint guarded replay. It does not run a joint score and",
                "does not promote the block-diagonal surrogate to validation.",
                "",
                "Allowed routes:",
                "",
                "1. source-native or source-frozen cross-probe covariance product;",
                "2. caveated block-diagonal surrogate with explicit shared-sky, redshift,",
                "   nuisance, calibration, and population-covariance caveats;",
                "3. same-statistic matched-control binding under the chosen covariance route.",
                "",
                "Summary:",
                "",
                f"- active channel order: `{summary['active_channel_order']}`",
                f"- block covariance blocks available: `{summary['block_covariance_blocks_available']}/{summary['block_covariance_blocks_total']}`",
                f"- cross-probe covariance defined: `{summary['cross_probe_covariance_defined']}`",
                f"- independence rationale route ready: `{summary['independence_rationale_route_ready']}`",
                f"- fastest route: `{summary['fastest_route']}`",
                f"- verdict: `{summary['verdict']}`",
                "",
                "Interpretation: the fastest viable next route is a caveated block-diagonal",
                "surrogate plus same-statistic matched controls, but this remains a",
                "prevalidation surrogate until a stronger covariance product or validation",
                "protocol is reviewed separately.",
                "",
            ]
        )
    )
    print(
        "JOINT_COVARIANCE_RESOLUTION_PLAN_V1_BUILT "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()
