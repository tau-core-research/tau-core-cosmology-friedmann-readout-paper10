#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BINDING = ROOT / "data/derived/joint_symbolic_statistic_binding_status_v1_summary.csv"
SIGN = ROOT / "data/derived/joint_control_sign_flip_symbolic_v1_summary.csv"
DROP = ROOT / "data/derived/joint_control_block_drop_symbolic_v1_summary.csv"
OUT = ROOT / "data/derived/joint_same_statistic_control_coverage_status_v1.csv"
SUMMARY = ROOT / "data/derived/joint_same_statistic_control_coverage_status_v1_summary.csv"
DOC = ROOT / "docs/joint_same_statistic_control_coverage_status_v1.md"
CLAIM_BOUNDARY = "joint_same_statistic_control_coverage_status_not_scoring_not_validation"


def read_one(path: Path) -> dict[str, str]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def status_row(
    family: str,
    artifact: str,
    coverage_status: str,
    controls_count: str,
    remaining_blocker: str,
) -> dict[str, str]:
    return {
        "coverage_id": "JOINT_SAME_STATISTIC_CONTROL_COVERAGE_STATUS_V1",
        "control_family": family,
        "artifact": artifact,
        "coverage_status": coverage_status,
        "controls_count": controls_count,
        "same_symbolic_statistic_required": "true",
        "numeric_executable_statistic_required": "true",
        "cross_probe_covariance_required": "true",
        "remaining_blocker": remaining_blocker,
        "computes_numeric_statistic_now": "false",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def main() -> None:
    binding = read_one(BINDING)
    sign = read_one(SIGN)
    drop = read_one(DROP)
    if binding["symbolic_binding_passed"] != "true":
        raise SystemExit("symbolic binding must pass before coverage status")
    if binding["numeric_executable_binding_passed"] != "false":
        raise SystemExit("coverage status expects numeric executable binding to remain blocked")
    if sign["verdict"] != "SIGN_FLIP_CONTROLS_SYMBOLICALLY_COMPLETE_NOT_SCORING":
        raise SystemExit("sign-flip symbolic controls are not complete")
    if drop["verdict"] != "BLOCK_DROP_CONTROLS_SYMBOLICALLY_COMPLETE_NOT_SCORING":
        raise SystemExit("block-drop symbolic controls are not complete")

    rows = [
        status_row(
            "sign_flip_controls",
            "data/derived/joint_control_sign_flip_symbolic_v1.csv",
            "SYMBOLIC_COMPLETE_NUMERIC_BLOCKED",
            sign["control_count"],
            "numeric_T_joint_and_covariance_binding",
        ),
        status_row(
            "leave_one_probe_or_block_drop",
            "data/derived/joint_control_block_drop_symbolic_v1.csv",
            "SYMBOLIC_COMPLETE_NUMERIC_BLOCKED",
            drop["control_count"],
            "numeric_T_joint_and_covariance_binding",
        ),
        status_row(
            "shuffled_channel_labels",
            "not_yet_built",
            "DESIGN_READY_NUMERIC_BLOCKED",
            "0",
            "numeric_T_joint_same_rows_and_shuffle_seed_policy",
        ),
        status_row(
            "wrong_channel_or_wrong_family_controls",
            "not_yet_built",
            "DESIGN_READY_NUMERIC_BLOCKED",
            "0",
            "numeric_T_joint_same_rows_and_wrong_family_mapping",
        ),
        status_row(
            "scope_and_forbidden_input_controls",
            "not_yet_built",
            "DESIGN_READY_NUMERIC_BLOCKED",
            "0",
            "numeric_T_joint_same_rows_and_forbidden_field_manifest",
        ),
        status_row(
            "null_readout_controls",
            "partly_covered_by_all_drop_null_symbolic_control",
            "SYMBOLIC_PARTIAL_NUMERIC_BLOCKED",
            "1",
            "numeric_T_joint_and_covariance_binding",
        ),
    ]
    symbolic_complete = sum("SYMBOLIC_COMPLETE" in row["coverage_status"] for row in rows)
    design_ready = sum(row["coverage_status"] == "DESIGN_READY_NUMERIC_BLOCKED" for row in rows)
    partial = sum("PARTIAL" in row["coverage_status"] for row in rows)
    summary = {
        "coverage_id": "JOINT_SAME_STATISTIC_CONTROL_COVERAGE_STATUS_V1",
        "tracked_control_families": str(len(rows)),
        "symbolic_complete_families": str(symbolic_complete),
        "symbolic_partial_families": str(partial),
        "design_ready_numeric_blocked_families": str(design_ready),
        "symbolic_binding_passed": binding["symbolic_binding_passed"],
        "numeric_executable_binding_passed": binding["numeric_executable_binding_passed"],
        "cross_probe_covariance_closed": binding["cross_probe_covariance_closed"],
        "computes_numeric_statistic_now": "false",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "next_required_action": "bind_numeric_T_joint_and_covariance_before_promoting_symbolic_controls_to_scoring_controls",
        "verdict": "SAME_STATISTIC_CONTROL_COVERAGE_SYMBOLIC_PROGRESS_NUMERIC_BLOCKED",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(OUT, rows)
    write_csv(SUMMARY, [summary])
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Joint same-statistic control coverage status v1",
                "",
                "**Doc class:** matched-control coverage ledger",
                "**Status:** symbolic progress only; not scoring; not validation",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`",
                "",
                "This artifact records which same-statistic matched-control families",
                "have been built symbolically and which remain design-ready but",
                "numeric-blocked. It does not compute a numeric joint statistic and",
                "does not authorize endpoint scoring.",
                "",
                "Current coverage:",
                "",
                f"- symbolic complete families: `{summary['symbolic_complete_families']}`",
                f"- symbolic partial families: `{summary['symbolic_partial_families']}`",
                f"- design-ready but numeric-blocked families: `{summary['design_ready_numeric_blocked_families']}`",
                f"- numeric executable binding passed: `{summary['numeric_executable_binding_passed']}`",
                f"- cross-probe covariance closed: `{summary['cross_probe_covariance_closed']}`",
                f"- verdict: `{summary['verdict']}`",
                "",
            ]
        )
    )
    print(
        "JOINT_SAME_STATISTIC_CONTROL_COVERAGE_STATUS_V1_BUILT "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()
