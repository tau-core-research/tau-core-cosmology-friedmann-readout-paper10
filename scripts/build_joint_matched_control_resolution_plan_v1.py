#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQ = ROOT / "data/derived/joint_matched_control_suite_requirements_gate_v1.csv"
REQ_SUMMARY = ROOT / "data/derived/joint_matched_control_suite_requirements_gate_v1_summary.csv"
SCAFFOLD = ROOT / "data/derived/joint_matched_control_suite_implementation_scaffold_v1.csv"
BINDING = ROOT / "data/derived/joint_single_statistic_binding_prerequisites_v1.csv"
COV_PLAN_SUMMARY = ROOT / "data/derived/joint_covariance_resolution_plan_v1_summary.csv"
OUT = ROOT / "data/derived/joint_matched_control_resolution_plan_v1.csv"
SUMMARY = ROOT / "data/derived/joint_matched_control_resolution_plan_v1_summary.csv"
DOC = ROOT / "docs/joint_matched_control_resolution_plan_v1.md"
CLAIM_BOUNDARY = "joint_matched_control_resolution_plan_not_scoring_not_validation"


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
    req_summary = read_one(REQ_SUMMARY)
    req_rows = read_rows(REQ)
    scaffold_rows = read_rows(SCAFFOLD)
    binding_rows = read_rows(BINDING)
    cov_plan = read_one(COV_PLAN_SUMMARY)

    if req_summary["control_suite_defined"] != "true":
        raise SystemExit("control suite must be defined before resolution planning")
    if req_summary["control_suite_implemented_under_joint_statistic"] != "false":
        raise SystemExit("this plan is only valid while controls are not yet implemented")
    if cov_plan["fastest_route"] != "caveated_block_diagonal_surrogate_plus_same_statistic_controls":
        raise SystemExit("unexpected covariance fastest route")
    if len(binding_rows) != 3:
        raise SystemExit("expected three active channel binding rows")

    req_by_id = {row["control_id"]: row for row in req_rows}
    rows: list[dict[str, str]] = []
    for index, scaffold in enumerate(scaffold_rows, start=1):
        req = req_by_id[scaffold["source_requirement_id"]]
        if scaffold["candidate_and_control_same_statistic_required"] != "true":
            raise SystemExit(f"same-statistic binding missing: {scaffold['control_family']}")
        if scaffold["candidate_and_control_same_covariance_required"] != "true":
            raise SystemExit(f"same-covariance binding missing: {scaffold['control_family']}")
        rows.append(
            {
                "plan_id": "JOINT_MATCHED_CONTROL_RESOLUTION_PLAN_V1",
                "implementation_rank": str(index),
                "source_requirement_id": scaffold["source_requirement_id"],
                "control_family": scaffold["control_family"],
                "future_builder": scaffold["future_builder"],
                "future_validator": scaffold["future_validator"],
                "future_artifact": scaffold["future_artifact"],
                "minimum_control_count_rule": scaffold["minimum_control_count_rule"],
                "required_freeze_input": scaffold["required_freeze_input"],
                "current_status": scaffold["scaffold_status"],
                "current_blocker": scaffold["upstream_blocker"],
                "required_binding": req["required_binding"],
                "exit_condition": "future_artifact_exists_and_validator_passes_under_same_statistic_same_covariance",
                "allowed_to_score_now": "false",
                "endpoint_scoring_allowed": "false",
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    write_csv(OUT, rows)
    blocked_upstream = sum(1 for row in rows if row["current_status"] == "blocked_by_upstream_gate")
    planned = sum(1 for row in rows if row["current_status"] == "planned_not_implemented")
    summary = {
        "plan_id": "JOINT_MATCHED_CONTROL_RESOLUTION_PLAN_V1",
        "active_channel_order": req_summary["active_channel_order"],
        "control_families_total": str(len(rows)),
        "planned_not_implemented": str(planned),
        "blocked_by_upstream_gate": str(blocked_upstream),
        "single_statistic_binding_rows": str(len(binding_rows)),
        "same_statistic_required_for_all_controls": "true",
        "same_covariance_required_for_all_controls": "true",
        "fastest_covariance_route": cov_plan["fastest_route"],
        "implementation_ready_now": "false",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "next_required_action": "instantiate_single_joint_statistic_and_covariance_binding_then_build_all_control_artifacts",
        "verdict": "MATCHED_CONTROL_RESOLUTION_PLAN_FROZEN_IMPLEMENTATION_BLOCKED_NOT_SCORING",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(SUMMARY, [summary])
    DOC.write_text(
        "\n".join(
            [
                "# Joint matched-control resolution plan v1",
                "",
                "**Doc class:** post-replay control-suite blocker-resolution plan",
                "**Status:** not scoring; not endpoint validation; not cosmological validation",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`",
                "",
                "This plan freezes how the third promotion blocker should be resolved.",
                "It does not run the controls. It only binds every future control family",
                "to the same joint statistic and same covariance route as the candidate.",
                "",
                "Required control families:",
                "",
                "1. `shuffled_channel_labels`",
                "2. `wrong_channel_or_wrong_family_controls`",
                "3. `sign_flip_controls`",
                "4. `leave_one_probe_or_block_drop`",
                "5. `null_readout_controls`",
                "6. `scope_and_forbidden_input_controls`",
                "7. `single_statistic_binding`",
                "8. `covariance_binding`",
                "",
                "Summary:",
                "",
                f"- active channel order: `{summary['active_channel_order']}`",
                f"- control families total: `{summary['control_families_total']}`",
                f"- planned not implemented: `{summary['planned_not_implemented']}`",
                f"- blocked by upstream gate: `{summary['blocked_by_upstream_gate']}`",
                f"- fastest covariance route: `{summary['fastest_covariance_route']}`",
                f"- verdict: `{summary['verdict']}`",
                "",
                "Interpretation: the control-suite route is now fully specified as a",
                "future implementation plan, but it remains blocked until the single joint",
                "statistic and covariance binding are instantiated and reviewed.",
                "",
            ]
        )
    )
    print(
        "JOINT_MATCHED_CONTROL_RESOLUTION_PLAN_V1_BUILT "
        f"controls={summary['control_families_total']} verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()
