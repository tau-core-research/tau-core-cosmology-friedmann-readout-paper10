#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OVERLAP = ROOT / "data/derived/joint_numeric_t_joint_source_route_overlap_metric_v1_summary.csv"
CONTROL_SUITE = ROOT / "data/derived/joint_numeric_t_joint_control_suite_v1.csv"
DESI_AUDIT = ROOT / "data/derived/joint_numeric_t_joint_desi_small_n_balance_audit_v1_summary.csv"
OUT = ROOT / "data/derived/joint_numeric_t_joint_channel_penalty_symmetry_gate_v1.csv"
SUMMARY = ROOT / "data/derived/joint_numeric_t_joint_channel_penalty_symmetry_gate_v1_summary.csv"
DOC = ROOT / "docs/joint_numeric_t_joint_channel_penalty_symmetry_gate_v1.md"
CLAIM_BOUNDARY = "joint_numeric_t_joint_channel_penalty_symmetry_gate_not_scoring_not_validation"


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
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    overlap = read_one(OVERLAP)
    desi = read_one(DESI_AUDIT)
    controls = [row for row in read_rows(CONTROL_SUITE) if row["numeric_t_joint_control"] != "not_applicable"]
    if overlap["numeric_t_joint_rescoring_allowed"] != "false":
        raise SystemExit("overlap scaffold must not allow rescoring")
    if desi["penalty_admissible_now"] != "false":
        raise SystemExit("DESI small-N audit must keep penalty inadmissible")

    control_count = len(controls)
    rows = [
        {
            "gate_id": "JOINT_NUMERIC_T_JOINT_CHANNEL_PENALTY_SYMMETRY_GATE_V1",
            "check_id": "CPS_C1_ROUTE_TAGS_FROZEN",
            "status": "SATISFIED",
            "evidence": f"channel_pair={overlap['channel_pair']}; jaccard_distance={overlap['jaccard_distance']}",
            "interpretation": "route-tag overlap is computed from frozen channel route descriptors, not candidate/control scores",
            "numeric_t_joint_rescoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "JOINT_NUMERIC_T_JOINT_CHANNEL_PENALTY_SYMMETRY_GATE_V1",
            "check_id": "CPS_C2_CANDIDATE_CONTROL_SYMMETRY",
            "status": "SATISFIED_SCAFFOLD_ONLY",
            "evidence": f"numeric_control_count={control_count}; route_metric_depends_on_channel_pair_not_row_values",
            "interpretation": "the same route-distance value is available for candidate and controls, but it is not yet a row-level penalty",
            "numeric_t_joint_rescoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "JOINT_NUMERIC_T_JOINT_CHANNEL_PENALTY_SYMMETRY_GATE_V1",
            "check_id": "CPS_C3_NONTRIVIAL_ROW_LEVEL_RULE",
            "status": "OPEN",
            "evidence": "current route-distance is constant across candidate and controls and would not add row-level discrimination",
            "interpretation": "a future penalty needs a residual-blind row-level or covariance-level rule before any scoring use",
            "numeric_t_joint_rescoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "JOINT_NUMERIC_T_JOINT_CHANNEL_PENALTY_SYMMETRY_GATE_V1",
            "check_id": "CPS_C4_DESI_CAVEAT_PROPAGATION",
            "status": "OPEN_CAVEATED",
            "evidence": f"desi_status={desi['small_n_balance_status']}; matched_control_count={desi['matched_control_count']}",
            "interpretation": "candidate/control symmetry does not remove the DESI small-N and row-sensitivity caveats",
            "numeric_t_joint_rescoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    satisfied = sum(row["status"].startswith("SATISFIED") for row in rows)
    open_count = len(rows) - satisfied
    summary = {
        "gate_id": "JOINT_NUMERIC_T_JOINT_CHANNEL_PENALTY_SYMMETRY_GATE_V1",
        "checks_total": str(len(rows)),
        "checks_satisfied_or_scaffold_satisfied": str(satisfied),
        "checks_open_or_caveated": str(open_count),
        "candidate_control_symmetry_scaffold_available": "true",
        "nontrivial_row_level_penalty_available": "false",
        "penalty_admissible_now": "false",
        "numeric_t_joint_rescoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "verdict": "SYMMETRY_SCAFFOLD_AVAILABLE_BUT_NO_NONTRIVIAL_PENALTY",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(OUT, rows)
    write_csv(SUMMARY, [summary])
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Joint numeric T_joint channel-penalty symmetry gate v1",
                "",
                "**Doc class:** candidate/control symmetry gate.",
                "**Status:** scaffold available; no penalty; not scoring; not validation.",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`.",
                "",
                "The route-tag overlap scaffold is candidate/control symmetric because it",
                "depends only on frozen channel route descriptors. The same value is",
                "available for every candidate/control row. That symmetry is useful, but",
                "it also means the current scaffold is not a nontrivial row-level penalty.",
                "",
                f"Verdict: `{summary['verdict']}`.",
                "",
            ]
        )
    )
    print(
        "JOINT_NUMERIC_T_JOINT_CHANNEL_PENALTY_SYMMETRY_GATE_V1_BUILT "
        f"open={summary['checks_open_or_caveated']}"
    )


if __name__ == "__main__":
    main()
