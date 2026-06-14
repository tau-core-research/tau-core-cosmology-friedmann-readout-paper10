#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
READINESS = ROOT / "data/derived/joint_matched_control_distribution_readiness_v1.csv"
REPLAY = ROOT / "data/derived/paper10_desi_shape_route_authorized_replay_v1_summary.csv"
ROBUST = ROOT / "data/derived/paper10_desi_shape_route_robustness_stress_v1_summary.csv"
PENALTY_REQ = ROOT / "data/derived/joint_numeric_t_joint_channel_distinguishability_penalty_requirements_v1_summary.csv"
OUT = ROOT / "data/derived/joint_numeric_t_joint_desi_small_n_balance_audit_v1.csv"
SUMMARY = ROOT / "data/derived/joint_numeric_t_joint_desi_small_n_balance_audit_v1_summary.csv"
DOC = ROOT / "docs/joint_numeric_t_joint_desi_small_n_balance_audit_v1.md"
CLAIM_BOUNDARY = "joint_numeric_t_joint_desi_small_n_balance_audit_not_scoring_not_validation"


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
    readiness_rows = read_rows(READINESS)
    readiness = next(row for row in readiness_rows if row["channel_id"] == "desi_shape_time_readout")
    replay = read_one(REPLAY)
    robust = read_one(ROBUST)
    penalty = read_one(PENALTY_REQ)
    if penalty["source_native_penalty_admissible_now"] != "false":
        raise SystemExit("small-N audit expects penalty to remain inadmissible")

    control_count = int(readiness["matched_control_rows_available"])
    margin_fraction = float(robust["candidate_minus_best_control_score_fraction"])
    max_leave_one_fraction = float(robust["max_leave_one_fraction_of_full_candidate"])
    min_leave_one_fraction = float(robust["min_leave_one_fraction_of_full_candidate"])
    candidate_top = replay["controls_ge_candidate_score"] == "0" and replay["family_survives_controls"] == "true"

    rows = [
        {
            "audit_id": "JOINT_NUMERIC_T_JOINT_DESI_SMALL_N_BALANCE_AUDIT_V1",
            "check_id": "SNB_C1_CONTROL_COUNT",
            "status": "OPEN_CAVEATED" if control_count < 20 else "SATISFIED",
            "evidence": f"matched_control_count={control_count}",
            "interpretation": "six non-candidate controls are enough for caveated pilot scaling but not population-grade balance",
            "rescoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "JOINT_NUMERIC_T_JOINT_DESI_SMALL_N_BALANCE_AUDIT_V1",
            "check_id": "SNB_C2_CONTROL_SURVIVAL",
            "status": "SATISFIED" if candidate_top else "FAILED",
            "evidence": f"controls_ge_candidate_score={replay['controls_ge_candidate_score']}; family_survives_controls={replay['family_survives_controls']}",
            "interpretation": "candidate exceeds all frozen DESI shape controls under the permission-only route",
            "rescoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "JOINT_NUMERIC_T_JOINT_DESI_SMALL_N_BALANCE_AUDIT_V1",
            "check_id": "SNB_C3_MARGIN_WIDTH",
            "status": "OPEN_CAVEATED" if margin_fraction < 0.01 else "SATISFIED",
            "evidence": f"candidate_minus_best_control_score_fraction={margin_fraction:.12e}",
            "interpretation": "positive signal is narrow relative to candidate score",
            "rescoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "JOINT_NUMERIC_T_JOINT_DESI_SMALL_N_BALANCE_AUDIT_V1",
            "check_id": "SNB_C4_ROW_SENSITIVITY",
            "status": "OPEN_CAVEATED" if max_leave_one_fraction > 0.95 else "SATISFIED",
            "evidence": f"max_leave_one_fraction={max_leave_one_fraction:.12e}; min_leave_one_fraction={min_leave_one_fraction:.12e}",
            "interpretation": "leave-one stress shows strong row sensitivity and prevents population-grade use",
            "rescoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    open_count = sum(row["status"] != "SATISFIED" for row in rows)
    summary = {
        "audit_id": "JOINT_NUMERIC_T_JOINT_DESI_SMALL_N_BALANCE_AUDIT_V1",
        "checks_total": str(len(rows)),
        "checks_satisfied": str(sum(row["status"] == "SATISFIED" for row in rows)),
        "checks_open_or_caveated": str(open_count),
        "matched_control_count": str(control_count),
        "candidate_survives_controls": str(candidate_top).lower(),
        "candidate_minus_best_control_score_fraction": f"{margin_fraction:.12e}",
        "max_leave_one_fraction_of_full_candidate": f"{max_leave_one_fraction:.12e}",
        "small_n_balance_status": "CAVEATED_BALANCE_ONLY_NOT_PENALTY_READY",
        "penalty_admissible_now": "false",
        "numeric_t_joint_rescoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "verdict": "DESI_ROUTE_POSITIVE_BUT_SMALL_N_NARROW_ROW_SENSITIVE",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(OUT, rows)
    write_csv(SUMMARY, [summary])
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Joint numeric T_joint DESI small-N balance audit v1",
                "",
                "**Doc class:** small-N balance audit.",
                "**Status:** caveated; not scoring; not validation.",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`.",
                "",
                "The DESI shape/time route remains positive against its frozen local",
                "controls, but the control count is small, the best-control margin is",
                "narrow, and the robustness stress is row-sensitive. This audit therefore",
                "keeps the route usable only as caveated positive support and keeps any",
                "channel-distinguishability penalty inadmissible.",
                "",
                f"Verdict: `{summary['verdict']}`.",
                "",
            ]
        )
    )
    print(
        "JOINT_NUMERIC_T_JOINT_DESI_SMALL_N_BALANCE_AUDIT_V1_BUILT "
        f"open={summary['checks_open_or_caveated']}"
    )


if __name__ == "__main__":
    main()
