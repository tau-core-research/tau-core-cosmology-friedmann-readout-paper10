#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCAFFOLD = ROOT / "data/derived/joint_matched_control_suite_implementation_scaffold_v1.csv"
SCAFFOLD_SUMMARY = ROOT / "data/derived/joint_matched_control_suite_implementation_scaffold_v1_summary.csv"
RESOLUTION = ROOT / "data/derived/joint_matched_control_resolution_plan_v1.csv"
RESOLUTION_SUMMARY = ROOT / "data/derived/joint_matched_control_resolution_plan_v1_summary.csv"
BINDING_SUMMARY = ROOT / "data/derived/joint_single_statistic_binding_prerequisites_v1_summary.csv"
COV_SUMMARY = ROOT / "data/derived/joint_covariance_resolution_plan_v1_summary.csv"
OUT = ROOT / "data/derived/joint_matched_control_implementation_readiness_v1.csv"
SUMMARY = ROOT / "data/derived/joint_matched_control_implementation_readiness_v1_summary.csv"
DOC = ROOT / "docs/joint_matched_control_implementation_readiness_v1.md"
CLAIM_BOUNDARY = "joint_matched_control_implementation_readiness_not_scoring_not_validation"


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


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def main() -> None:
    scaffold_rows = read_rows(SCAFFOLD)
    scaffold_summary = read_one(SCAFFOLD_SUMMARY)
    resolution_rows = read_rows(RESOLUTION)
    resolution_summary = read_one(RESOLUTION_SUMMARY)
    binding = read_one(BINDING_SUMMARY)
    covariance = read_one(COV_SUMMARY)

    if scaffold_summary["implementation_ready"] != "false":
        raise SystemExit("readiness ledger is only valid while scaffold is not ready")
    if resolution_summary["implementation_ready_now"] != "false":
        raise SystemExit("resolution plan must remain not implementation-ready")
    if binding["ready_for_single_statistic_protocol"] != "false":
        raise SystemExit("single statistic protocol must remain blocked")
    if covariance["cross_probe_covariance_defined"] != "false":
        raise SystemExit("cross-probe covariance must remain open in this readiness ledger")

    resolution_by_family = {row["control_family"]: row for row in resolution_rows}
    rows: list[dict[str, str]] = []
    for idx, scaffold in enumerate(scaffold_rows, start=1):
        family = scaffold["control_family"]
        resolution = resolution_by_family[family]
        if scaffold["scaffold_status"] == "planned_not_implemented":
            readiness = "DESIGN_READY_PROTOCOL_BLOCKED"
            allowed_next_action = "write_source_frozen_builder_and_validator_after_single_statistic_binding_is_frozen"
        elif scaffold["scaffold_status"] == "blocked_by_upstream_gate":
            readiness = "UPSTREAM_BLOCKED"
            allowed_next_action = "do_not_build_until_binding_or_covariance_gate_closes"
        else:
            raise SystemExit(f"unexpected scaffold status for {family}: {scaffold['scaffold_status']}")
        rows.append(
            {
                "readiness_id": "JOINT_MATCHED_CONTROL_IMPLEMENTATION_READINESS_V1",
                "implementation_rank": str(idx),
                "control_family": family,
                "scaffold_status": scaffold["scaffold_status"],
                "readiness_status": readiness,
                "future_builder": scaffold["future_builder"],
                "future_validator": scaffold["future_validator"],
                "future_artifact": scaffold["future_artifact"],
                "upstream_blocker": scaffold["upstream_blocker"],
                "required_binding": resolution["required_binding"],
                "exit_condition": resolution["exit_condition"],
                "allowed_next_action": allowed_next_action,
                "same_statistic_required": scaffold["candidate_and_control_same_statistic_required"],
                "same_covariance_required": scaffold["candidate_and_control_same_covariance_required"],
                "allowed_to_score_now": "false",
                "endpoint_scoring_allowed": "false",
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    design_ready = sum(row["readiness_status"] == "DESIGN_READY_PROTOCOL_BLOCKED" for row in rows)
    upstream_blocked = sum(row["readiness_status"] == "UPSTREAM_BLOCKED" for row in rows)
    summary = {
        "readiness_id": "JOINT_MATCHED_CONTROL_IMPLEMENTATION_READINESS_V1",
        "control_families_total": str(len(rows)),
        "design_ready_protocol_blocked": str(design_ready),
        "upstream_blocked": str(upstream_blocked),
        "single_statistic_defined": binding["single_joint_statistic_defined"],
        "ready_for_single_statistic_protocol": binding["ready_for_single_statistic_protocol"],
        "cross_probe_covariance_defined": covariance["cross_probe_covariance_defined"],
        "fastest_covariance_route": covariance["fastest_route"],
        "implementation_ready_for_scoring": "false",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "next_required_action": "freeze_single_joint_statistic_binding_and_review_covariance_route_before_control_execution",
        "verdict": "MATCHED_CONTROL_IMPLEMENTATION_READINESS_HAS_DESIGNS_BUT_PROTOCOL_BINDING_BLOCKED",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(OUT, rows)
    write_csv(SUMMARY, [summary])

    DOC.write_text(
        "\n".join(
            [
                "# Joint matched-control implementation readiness v1",
                "",
                "**Doc class:** matched-control implementation readiness ledger",
                "**Status:** not scoring; not endpoint validation; not cosmological validation",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`",
                "",
                "This ledger separates two facts that should not be conflated:",
                "six control families have source-side design scaffolds, but no",
                "control family is executable for validation until the single joint",
                "statistic and covariance route are frozen for candidate and controls",
                "together.",
                "",
                "Summary:",
                "",
                f"- control families total: `{summary['control_families_total']}`",
                f"- design-ready but protocol-blocked families: `{summary['design_ready_protocol_blocked']}`",
                f"- upstream-blocked families: `{summary['upstream_blocked']}`",
                f"- single statistic defined: `{summary['single_statistic_defined']}`",
                f"- cross-probe covariance defined: `{summary['cross_probe_covariance_defined']}`",
                f"- fastest covariance route: `{summary['fastest_covariance_route']}`",
                f"- verdict: `{summary['verdict']}`",
                "",
                "Interpretation: the control route is becoming implementable, but this",
                "artifact intentionally does not run controls and does not authorize",
                "endpoint scoring.",
                "",
            ]
        )
    )
    print(
        "JOINT_MATCHED_CONTROL_IMPLEMENTATION_READINESS_V1_BUILT "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()
