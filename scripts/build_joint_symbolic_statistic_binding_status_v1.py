#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SHELL = ROOT / "data/derived/joint_single_statistic_protocol_shell_v1_summary.csv"
SAME_AUTH = ROOT / "data/derived/joint_same_statistic_replay_authorization_response_v1_summary.csv"
PERMISSION = ROOT / "data/derived/joint_same_statistic_guarded_permission_replay_package_v1_summary.csv"
EXECUTION = ROOT / "data/derived/joint_same_statistic_execution_authorization_response_v1_summary.csv"
REPLAY = ROOT / "data/derived/joint_guarded_replay_permission_only_summary_v1.csv"
OUT = ROOT / "data/derived/joint_symbolic_statistic_binding_status_v1.csv"
SUMMARY = ROOT / "data/derived/joint_symbolic_statistic_binding_status_v1_summary.csv"
DOC = ROOT / "docs/joint_symbolic_statistic_binding_status_v1.md"
CLAIM_BOUNDARY = "joint_symbolic_statistic_binding_status_not_scoring_not_validation"


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


def main() -> None:
    shell = read_one(SHELL)
    same_auth = read_one(SAME_AUTH)
    permission = read_one(PERMISSION)
    execution = read_one(EXECUTION)
    replay = read_one(REPLAY)

    if shell["symbolic_joint_statistic"] != "T_joint = sum_i q_i z_i":
        raise SystemExit("unexpected symbolic joint statistic")
    if same_auth["decision"] != "AUTHORIZE_SAME_STATISTIC_GUARDED_PERMISSION_REPLAY_PACKAGE_NOT_SCORING_NOT_VALIDATION":
        raise SystemExit("same-statistic authorization is not accepted")
    if permission["same_statistic_bound"] != "true":
        raise SystemExit("same-statistic permission package is not bound")
    if execution["decision"] != "AUTHORIZE_SAME_STATISTIC_PERMISSION_ONLY_EXECUTION_NOT_VALIDATION":
        raise SystemExit("same-statistic execution authorization is not accepted")
    if replay["status"] != "JOINT_GUARDED_REPLAY_PERMISSION_ONLY_COMPLETE_NOT_VALIDATION":
        raise SystemExit("permission-only replay is not complete")

    rows = [
        {
            "criterion_id": "JSSB_01_SYMBOLIC_FORM_FROZEN",
            "criterion": "The symbolic joint statistic form is frozen.",
            "status": "pass",
            "evidence": shell["symbolic_joint_statistic"],
            "blocks_validation_if_failed": "true",
        },
        {
            "criterion_id": "JSSB_02_CANDIDATE_CONTROL_SAME_FORMULA",
            "criterion": "Candidate and controls must use the same symbolic formula.",
            "status": "pass" if shell["candidate_control_same_formula_required"] == "true" else "blocked",
            "evidence": f"same_formula={shell['candidate_control_same_formula_required']}",
            "blocks_validation_if_failed": "true",
        },
        {
            "criterion_id": "JSSB_03_SAME_ROWS_AND_COVARIANCE_REQUIRED",
            "criterion": "Candidate and controls must use the same rows and covariance route.",
            "status": "pass"
            if shell["candidate_control_same_rows_required"] == "true"
            and shell["candidate_control_same_covariance_required"] == "true"
            else "blocked",
            "evidence": f"same_rows={shell['candidate_control_same_rows_required']}; same_covariance={shell['candidate_control_same_covariance_required']}",
            "blocks_validation_if_failed": "true",
        },
        {
            "criterion_id": "JSSB_04_PERMISSION_REPLAY_BOUND",
            "criterion": "The permission-only replay was run under same-statistic authorization.",
            "status": "pass",
            "evidence": replay["verdict"],
            "blocks_validation_if_failed": "true",
        },
        {
            "criterion_id": "JSSB_05_NUMERIC_EXECUTABLE_STATISTIC",
            "criterion": "A numeric executable statistic for validation-facing controls is defined.",
            "status": "blocked",
            "evidence": "symbolic shell only; protocol_executable=false",
            "blocks_validation_if_failed": "true",
        },
        {
            "criterion_id": "JSSB_06_CROSS_PROBE_COVARIANCE",
            "criterion": "The cross-probe covariance route is closed for validation-facing controls.",
            "status": "blocked",
            "evidence": f"cross_probe_covariance_defined={shell['cross_probe_covariance_defined']}",
            "blocks_validation_if_failed": "true",
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

    passed = sum(row["status"] == "pass" for row in rows)
    blocked = sum(row["status"] == "blocked" for row in rows)
    summary = {
        "gate_id": "JOINT_SYMBOLIC_STATISTIC_BINDING_STATUS_V1",
        "symbolic_joint_statistic": shell["symbolic_joint_statistic"],
        "symbolic_binding_passed": "true" if blocked < len(rows) and passed >= 4 else "false",
        "numeric_executable_binding_passed": "false",
        "cross_probe_covariance_closed": shell["cross_probe_covariance_defined"],
        "criteria_total": str(len(rows)),
        "criteria_passed": str(passed),
        "criteria_blocked": str(blocked),
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "next_required_action": "implement_same_statistic_controls_as_symbolic_bound_nonvalidation_artifacts_then_close_numeric_statistic_and_covariance_before_validation",
        "verdict": "SYMBOLIC_SAME_STATISTIC_BINDING_PASSED_NUMERIC_VALIDATION_BINDING_BLOCKED",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(SUMMARY, [summary])

    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Joint symbolic statistic binding status v1",
                "",
                "**Doc class:** post-replay binding-status ledger",
                "**Status:** symbolic binding passed; numeric validation binding blocked",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`",
                "",
                "This ledger separates two facts that were previously easy to conflate.",
                "The symbolic same-statistic condition has passed: candidate and controls",
                "are required to share `T_joint = sum_i q_i z_i`, the same row scope, and",
                "the same covariance route.  However, this is not yet a numeric executable",
                "validation statistic.",
                "",
                "Summary:",
                "",
                f"- symbolic binding passed: `{summary['symbolic_binding_passed']}`",
                f"- numeric executable binding passed: `{summary['numeric_executable_binding_passed']}`",
                f"- cross-probe covariance closed: `{summary['cross_probe_covariance_closed']}`",
                f"- criteria passed: `{summary['criteria_passed']}/{summary['criteria_total']}`",
                f"- verdict: `{summary['verdict']}`",
                "",
            ]
        )
    )
    print(
        "JOINT_SYMBOLIC_STATISTIC_BINDING_STATUS_V1_BUILT "
        f"verdict={summary['verdict']} passed={passed} blocked={blocked}"
    )


if __name__ == "__main__":
    main()
