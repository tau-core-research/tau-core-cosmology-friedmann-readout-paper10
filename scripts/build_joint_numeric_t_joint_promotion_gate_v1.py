#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SHELL = ROOT / "data/derived/joint_single_statistic_protocol_shell_v1_summary.csv"
BINDING = ROOT / "data/derived/joint_symbolic_statistic_binding_status_v1_summary.csv"
COVERAGE = ROOT / "data/derived/joint_same_statistic_control_coverage_status_v1_summary.csv"
COVARIANCE = ROOT / "data/derived/joint_covariance_resolution_plan_v1_summary.csv"
ZI_LEDGER = ROOT / "data/derived/joint_numeric_zi_distribution_ledger_v1_summary.csv"
TJOINT_LEDGER = ROOT / "data/derived/joint_numeric_t_joint_ledger_v1_summary.csv"
TJOINT_BLOCKER = ROOT / "data/derived/joint_numeric_t_joint_blocker_status_v1_summary.csv"
OUT = ROOT / "data/derived/joint_numeric_t_joint_promotion_gate_v1.csv"
SUMMARY = ROOT / "data/derived/joint_numeric_t_joint_promotion_gate_v1_summary.csv"
DOC = ROOT / "docs/joint_numeric_t_joint_promotion_gate_v1.md"
CLAIM_BOUNDARY = "joint_numeric_t_joint_promotion_gate_not_scoring_not_validation"


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def gate_row(
    criterion_id: str,
    criterion: str,
    status: str,
    evidence: str,
    required_before_numeric: str = "true",
) -> dict[str, str]:
    return {
        "gate_id": "JOINT_NUMERIC_T_JOINT_PROMOTION_GATE_V1",
        "criterion_id": criterion_id,
        "criterion": criterion,
        "status": status,
        "evidence": evidence,
        "required_before_numeric_promotion": required_before_numeric,
        "computes_numeric_statistic_now": "false",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def main() -> None:
    shell = read_one(SHELL)
    binding = read_one(BINDING)
    coverage = read_one(COVERAGE)
    covariance = read_one(COVARIANCE)
    zi_rows = read_rows(ZI_LEDGER)
    zi_aggregate = [row for row in zi_rows if row.get("channel_id") == "all_channels"]
    if len(zi_aggregate) != 1:
        raise SystemExit("numeric z_i ledger summary must contain one all_channels aggregate row")
    zi_ledger = zi_aggregate[0]
    tjoint_ledger = read_one(TJOINT_LEDGER)
    tjoint_blocker = read_one(TJOINT_BLOCKER)

    if shell["symbolic_joint_statistic"] != "T_joint = sum_i q_i z_i":
        raise SystemExit("unexpected symbolic joint statistic")
    if binding["symbolic_binding_passed"] != "true":
        raise SystemExit("symbolic binding must pass before numeric promotion gate")
    if coverage["verdict"] != "SAME_STATISTIC_CONTROL_COVERAGE_SYMBOLIC_PROGRESS_NUMERIC_BLOCKED":
        raise SystemExit("control coverage status must be current")
    if zi_ledger["numeric_z_i_defined"] != "true":
        raise SystemExit("numeric z_i ledger must define all channel z_i values")
    if tjoint_ledger["numeric_t_joint_allowed"] != "true":
        raise SystemExit("numeric T_joint ledger must be authorized")
    if tjoint_ledger["computes_endpoint_score_now"] != "false":
        raise SystemExit("numeric T_joint ledger must not compute endpoint score")
    if tjoint_blocker["current_blocker"] != "numeric_t_joint_ledger_built_endpoint_scoring_authorization_missing":
        raise SystemExit("numeric T_joint blocker status is not current")

    rows = [
        gate_row(
            "NTJ_01_SYMBOLIC_FORM_FROZEN",
            "The symbolic statistic form is frozen.",
            "pass",
            shell["symbolic_joint_statistic"],
        ),
        gate_row(
            "NTJ_02_CHANNEL_WEIGHTS_FROZEN",
            "Channel weights q_i are frozen in the protocol shell.",
            "pass",
            f"active_channels={shell['active_channel_count']}",
        ),
        gate_row(
            "NTJ_03_SAME_ROWS_FORMULA_COVARIANCE_REQUIRED",
            "Candidate and controls require the same rows, formula, and covariance route.",
            "pass",
            "same_formula=true; same_rows=true; same_covariance=true",
        ),
        gate_row(
            "NTJ_04_SYMBOLIC_CONTROLS_PARTLY_COMPLETE",
            "Same-statistic controls have at least symbolic coverage.",
            "pass",
            (
                f"symbolic_complete={coverage['symbolic_complete_families']}; "
                f"symbolic_partial={coverage['symbolic_partial_families']}; "
                f"design_ready_numeric_blocked={coverage['design_ready_numeric_blocked_families']}"
            ),
        ),
        gate_row(
            "NTJ_05_NUMERIC_CHANNEL_ZI_BINDING",
            "Numeric z_i definitions and input artifacts are executable for every active channel.",
            "pass",
            "joint_numeric_zi_distribution_ledger_v1_summary.csv; numeric_z_i_defined=true",
        ),
        gate_row(
            "NTJ_06_NUMERIC_T_JOINT_LEDGER_BUILT",
            "The frozen numeric T_joint ledger has been built once from q_i and z_i.",
            "pass",
            f"T_joint={tjoint_ledger['numeric_t_joint']}; computes_endpoint_score_now=false",
        ),
        gate_row(
            "NTJ_07_NUMERIC_CONTROL_EXECUTION_BINDING",
            "Matched controls are executable under the same numeric T_joint.",
            "blocked",
            "sign_flip_and_block_drop_are_symbolic_only; shuffled/wrong/scope controls not numeric",
        ),
        gate_row(
            "NTJ_08_CROSS_PROBE_COVARIANCE_CLOSURE",
            "Cross-probe covariance or reviewed surrogate is closed for candidate and controls together.",
            "blocked",
            f"cross_probe_covariance_defined={covariance['cross_probe_covariance_defined']}",
        ),
        gate_row(
            "NTJ_09_NO_ENDPOINT_SCORING_AUTHORIZATION_YET",
            "A separate validation authorization package is required after numeric binding.",
            "blocked",
            tjoint_blocker["current_blocker"],
        ),
    ]

    passed = sum(row["status"] == "pass" for row in rows)
    blocked = sum(row["status"] == "blocked" for row in rows)
    summary = {
        "gate_id": "JOINT_NUMERIC_T_JOINT_PROMOTION_GATE_V1",
        "symbolic_joint_statistic": shell["symbolic_joint_statistic"],
        "criteria_total": str(len(rows)),
        "criteria_passed": str(passed),
        "criteria_blocked": str(blocked),
        "numeric_t_joint_promotion_ready": "false",
        "cross_probe_covariance_closed": covariance["cross_probe_covariance_defined"],
        "same_statistic_control_symbolic_complete_families": coverage["symbolic_complete_families"],
        "same_statistic_control_numeric_ready": "false",
        "numeric_zi_defined": zi_ledger["numeric_z_i_defined"],
        "numeric_t_joint_ledger_built": "true",
        "numeric_t_joint": tjoint_ledger["numeric_t_joint"],
        "computes_numeric_statistic_now": "false",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "next_required_action": "prepare_or_build_same_numeric_T_joint_control_suite_and_separate_endpoint_scoring_authorization",
        "verdict": "NUMERIC_T_JOINT_LEDGER_BUILT_PROMOTION_STILL_BLOCKED_FOR_ENDPOINT_SCORING",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(OUT, rows)
    write_csv(SUMMARY, [summary])
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Joint numeric T_joint promotion gate v1",
                "",
                "**Doc class:** numeric-promotion gate",
                "**Status:** blocked; not scoring; not validation",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`",
                "",
                "This gate separates the symbolic same-statistic shell from a future",
                "numeric executable joint statistic. It records what has already passed",
                "symbolically and what must still be closed before any endpoint scoring",
                "or validation package can be prepared.",
                "",
                "Current result:",
                "",
                f"- criteria passed: `{summary['criteria_passed']}/{summary['criteria_total']}`",
                f"- numeric T_joint ledger built: `{summary['numeric_t_joint_ledger_built']}`",
                f"- numeric T_joint: `{summary['numeric_t_joint']}`",
                f"- numeric T_joint promotion ready: `{summary['numeric_t_joint_promotion_ready']}`",
                f"- cross-probe covariance closed: `{summary['cross_probe_covariance_closed']}`",
                f"- same-statistic numeric controls ready: `{summary['same_statistic_control_numeric_ready']}`",
                f"- verdict: `{summary['verdict']}`",
                "",
            ]
        )
    )
    print(
        "JOINT_NUMERIC_T_JOINT_PROMOTION_GATE_V1_BUILT "
        f"verdict={summary['verdict']} passed={passed} blocked={blocked}"
    )


if __name__ == "__main__":
    main()
