#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUTH = ROOT / "data/derived/joint_numeric_t_joint_endpoint_scoring_authorization_response_v1_summary.csv"
CONTROL_SUITE = ROOT / "data/derived/joint_numeric_t_joint_control_suite_v1.csv"
CONTROL_SUITE_SUMMARY = ROOT / "data/derived/joint_numeric_t_joint_control_suite_v1_summary.csv"
OUT = ROOT / "data/derived/joint_numeric_t_joint_permission_only_endpoint_scoring_v1.csv"
SUMMARY = ROOT / "data/derived/joint_numeric_t_joint_permission_only_endpoint_scoring_v1_summary.csv"
DOC = ROOT / "docs/joint_numeric_t_joint_permission_only_endpoint_scoring_v1.md"
CLAIM_BOUNDARY = "joint_numeric_t_joint_permission_only_endpoint_scoring_not_validation"


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


def as_float(value: str) -> float:
    return float(value)


def main() -> None:
    auth = read_one(AUTH)
    suite_summary = read_one(CONTROL_SUITE_SUMMARY)
    controls = read_rows(CONTROL_SUITE)

    if auth["decision"] != "AUTHORIZE_PERMISSION_ONLY_ENDPOINT_SCORING_NOT_VALIDATION":
        raise SystemExit("permission-only endpoint scoring is not authorized")
    if auth["one_time_permission_only_endpoint_scoring_replay_allowed"] != "true":
        raise SystemExit("one-time permission-only replay flag is not true")
    for field in ["endpoint_validation_claimed", "cosmological_validation_claimed", "physical_validation_claimed"]:
        if auth[field] != "false":
            raise SystemExit(f"authorization unsafe field {field}")
    if suite_summary["verdict"] != "NUMERIC_T_JOINT_CONTROL_SUITE_BUILT_PREVALIDATION_NOT_ENDPOINT_SCORING":
        raise SystemExit("control suite is not the frozen prevalidation suite")
    if suite_summary["controls_beating_or_equal_candidate"] != "0":
        raise SystemExit("control-suite summary no longer has expected 0 controls beating/equal candidate")

    candidate = as_float(suite_summary["candidate_numeric_t_joint"])
    rows = []
    guard_rows = []
    for row in controls:
        if row["numeric_t_joint_control"] == "not_applicable":
            guard_rows.append(row)
            continue
        control = as_float(row["numeric_t_joint_control"])
        margin = candidate - control
        rows.append(
            {
                "run_id": "JOINT_NUMERIC_T_JOINT_PERMISSION_ONLY_ENDPOINT_SCORING_V1",
                "control_id": row["control_id"],
                "control_family": row["control_family"],
                "candidate_numeric_t_joint": f"{candidate:.12e}",
                "control_numeric_t_joint": f"{control:.12e}",
                "candidate_minus_control": f"{margin:.12e}",
                "control_beats_or_equals_candidate": str(control >= candidate).lower(),
                "same_t_joint_formula": row["same_t_joint_formula"],
                "same_q_i_weights": row["same_q_i_weights"],
                "same_sign_and_standardization_rule": row["same_sign_and_standardization_rule"],
                "same_row_scope_boundary": row["same_row_scope_boundary"],
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    if len(rows) != int(suite_summary["numeric_control_count"]):
        raise SystemExit("numeric control row count does not match suite summary")
    rows_sorted = sorted(rows, key=lambda r: as_float(r["control_numeric_t_joint"]), reverse=True)
    for idx, row in enumerate(rows_sorted, start=1):
        row["control_rank_desc"] = str(idx)
    write_csv(OUT, rows_sorted)

    best = rows_sorted[0]
    controls_beating = sum(1 for row in rows_sorted if row["control_beats_or_equals_candidate"] == "true")
    candidate_rank_among_controls_plus_candidate = 1 + controls_beating
    min_margin = min(as_float(row["candidate_minus_control"]) for row in rows_sorted)
    mean_margin = sum(as_float(row["candidate_minus_control"]) for row in rows_sorted) / len(rows_sorted)
    summary = {
        "run_id": "JOINT_NUMERIC_T_JOINT_PERMISSION_ONLY_ENDPOINT_SCORING_V1",
        "status": "PERMISSION_ONLY_ENDPOINT_SCORING_COMPLETE_NOT_VALIDATION",
        "candidate_numeric_t_joint": f"{candidate:.12e}",
        "numeric_control_count": str(len(rows_sorted)),
        "controls_beating_or_equal_candidate": str(controls_beating),
        "fraction_beating_or_equal_candidate": f"{controls_beating / len(rows_sorted):.12e}",
        "candidate_rank_among_controls_plus_candidate": str(candidate_rank_among_controls_plus_candidate),
        "best_control_id": best["control_id"],
        "best_control_family": best["control_family"],
        "best_control_numeric_t_joint": best["control_numeric_t_joint"],
        "candidate_minus_best_control": best["candidate_minus_control"],
        "min_candidate_minus_control": f"{min_margin:.12e}",
        "mean_candidate_minus_control": f"{mean_margin:.12e}",
        "same_statistic_controls_required": "true",
        "non_numeric_guard_rows_excluded_from_rank": str(len(guard_rows)),
        "permission_only_endpoint_scoring_allowed": "true",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "verdict": "permission_only_endpoint_score_candidate_exceeds_all_controls_not_validation",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(SUMMARY, [summary])
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Joint numeric T_joint permission-only endpoint scoring v1",
                "",
                "**Doc class:** permission-only endpoint scoring ledger.",
                "**Status:** complete; not validation.",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`.",
                "",
                f"Candidate numeric `T_joint`: `{summary['candidate_numeric_t_joint']}`.",
                f"Controls beating/equal candidate: `{summary['controls_beating_or_equal_candidate']}/{summary['numeric_control_count']}`.",
                f"Best control: `{summary['best_control_id']}` (`{summary['best_control_family']}`),",
                f"candidate-minus-best-control `{summary['candidate_minus_best_control']}`.",
                "",
                "This artifact is a permission-only diagnostic endpoint score under",
                "a completed external authorization response. It is not endpoint",
                "validation, cosmological validation, or physical validation.",
                "",
            ]
        )
    )
    print(
        "JOINT_NUMERIC_T_JOINT_PERMISSION_ONLY_ENDPOINT_SCORING_V1_COMPLETE "
        f"controls_beating={controls_beating}"
    )


if __name__ == "__main__":
    main()
