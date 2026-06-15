#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data" / "derived"

AUTH = DERIVED / "joint_row_level_penalized_t_joint_endpoint_authorization_review_completed_summary_v1.csv"
BASE_T = DERIVED / "joint_numeric_t_joint_ledger_v1_summary.csv"
BASE_CONTROLS = DERIVED / "joint_numeric_t_joint_control_suite_v1.csv"
PENALTY_VALUES = DERIVED / "joint_row_level_numeric_penalty_values_v1.csv"
ALIGNED_CONTROLS = DERIVED / "joint_row_level_aligned_control_values_v1.csv"
OUT = DERIVED / "joint_row_level_penalized_t_joint_endpoint_scoring_v1.csv"
SUMMARY = DERIVED / "joint_row_level_penalized_t_joint_endpoint_scoring_v1_summary.csv"
DOC = ROOT / "docs" / "joint_row_level_penalized_t_joint_endpoint_scoring_v1.md"
CLAIM_BOUNDARY = "joint_row_level_penalized_t_joint_endpoint_scoring_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def as_float(value: str) -> float:
    return float(value)


def control_base_map() -> dict[int, dict[str, str]]:
    rows = {}
    for row in read_rows(BASE_CONTROLS):
        cid = row["control_id"]
        if not cid.startswith("matched_index_"):
            continue
        idx = int(cid.rsplit("_", 1)[1])
        rows[idx] = row
    return rows


def main() -> None:
    auth = read_one(AUTH)
    base_t = read_one(BASE_T)
    penalties = read_rows(PENALTY_VALUES)
    aligned = read_rows(ALIGNED_CONTROLS)
    base_controls = control_base_map()

    if auth["decision"] != "AUTHORIZE_PENALIZED_T_JOINT_LEDGER_AND_ONE_GUARDED_ENDPOINT_SCORING_REPLAY_NOT_VALIDATION":
        raise SystemExit("penalized endpoint scoring is not authorized")
    if auth["penalized_t_joint_ledger_authorized"] != "true":
        raise SystemExit("penalized ledger authorization flag is not true")
    if auth["guarded_endpoint_scoring_replay_authorized"] != "true":
        raise SystemExit("guarded endpoint replay authorization flag is not true")
    for field in [
        "endpoint_scoring_run_by_this_review",
        "endpoint_validation_claimed",
        "cosmological_validation_claimed",
        "physical_validation_claimed",
        "forbidden_inputs_used",
    ]:
        if auth[field] != "false":
            raise SystemExit(f"unsafe authorization field {field}")

    lambda_row = as_float(auth["lambda_row_numeric_value"])
    t_candidate = as_float(base_t["numeric_t_joint"])
    candidate_penalty_rows = [
        row
        for row in penalties
        if row["row_type"] == "candidate" and row["joint_penalty_contribution_allowed"] == "true"
    ]
    active_channels = sorted(row["channel_id"] for row in candidate_penalty_rows)
    if len(active_channels) != 3:
        raise SystemExit(f"expected three candidate penalty channels, got {active_channels}")
    p_candidate = sum(as_float(row["P_i"]) for row in candidate_penalty_rows)
    t_candidate_penalized = t_candidate + lambda_row * p_candidate

    rows = []
    for control in aligned:
        idx = int(control["alignment_index"])
        if idx not in base_controls:
            raise SystemExit(f"missing matched_index base control for alignment {idx}")
        base = base_controls[idx]
        p_control = as_float(control["P_row_control"])
        t_control = as_float(base["numeric_t_joint_control"])
        t_control_penalized = t_control + lambda_row * p_control
        margin = t_candidate_penalized - t_control_penalized
        rows.append(
            {
                "run_id": "JOINT_ROW_LEVEL_PENALIZED_T_JOINT_ENDPOINT_SCORING_V1",
                "alignment_index": control["alignment_index"],
                "control_id": base["control_id"],
                "control_family": base["control_family"],
                "candidate_T_joint": f"{t_candidate:.12e}",
                "candidate_P_row": f"{p_candidate:.12e}",
                "lambda_row": f"{lambda_row:.12e}",
                "candidate_T_joint_penalized": f"{t_candidate_penalized:.12e}",
                "control_T_joint": f"{t_control:.12e}",
                "control_P_row": f"{p_control:.12e}",
                "control_T_joint_penalized": f"{t_control_penalized:.12e}",
                "candidate_minus_control_penalized": f"{margin:.12e}",
                "control_beats_or_equals_candidate": str(t_control_penalized >= t_candidate_penalized).lower(),
                "control_ids_by_channel": control["control_ids_by_channel"],
                "control_families_by_channel": control["control_families_by_channel"],
                "same_penalty_formula": "true",
                "same_lambda_row": "true",
                "same_alignment_rule": "true",
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    rows_sorted = sorted(rows, key=lambda r: as_float(r["control_T_joint_penalized"]), reverse=True)
    for rank, row in enumerate(rows_sorted, start=1):
        row["control_rank_desc"] = str(rank)
    write_csv(OUT, rows_sorted)

    beating = sum(1 for row in rows_sorted if row["control_beats_or_equals_candidate"] == "true")
    best = rows_sorted[0]
    margins = [as_float(row["candidate_minus_control_penalized"]) for row in rows_sorted]
    summary = {
        "run_id": "JOINT_ROW_LEVEL_PENALIZED_T_JOINT_ENDPOINT_SCORING_V1",
        "status": "GUARDED_ENDPOINT_SCORING_COMPLETE_NOT_VALIDATION",
        "base_candidate_T_joint": f"{t_candidate:.12e}",
        "lambda_row": f"{lambda_row:.12e}",
        "candidate_P_row": f"{p_candidate:.12e}",
        "candidate_T_joint_penalized": f"{t_candidate_penalized:.12e}",
        "aligned_control_count": str(len(rows_sorted)),
        "controls_beating_or_equal_candidate": str(beating),
        "fraction_beating_or_equal_candidate": f"{beating / len(rows_sorted):.12e}",
        "candidate_rank_among_controls_plus_candidate": str(1 + beating),
        "best_control_id": best["control_id"],
        "best_control_family": best["control_family"],
        "best_control_T_joint_penalized": best["control_T_joint_penalized"],
        "candidate_minus_best_control_penalized": best["candidate_minus_control_penalized"],
        "min_candidate_minus_control_penalized": f"{min(margins):.12e}",
        "mean_candidate_minus_control_penalized": f"{sum(margins) / len(margins):.12e}",
        "active_candidate_penalty_channels": "|".join(active_channels),
        "control_scope": "six_deterministically_aligned_row_level_controls_only",
        "endpoint_scoring_allowed_by_completed_review": "true",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "verdict": "penalized_endpoint_score_candidate_exceeds_all_aligned_controls_not_validation"
        if beating == 0
        else "penalized_endpoint_score_has_aligned_controls_beating_candidate_not_validation",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(SUMMARY, [summary])

    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Joint row-level penalized T_joint endpoint scoring v1",
                "",
                "**Doc class:** guarded endpoint-scoring ledger.",
                "**Status:** complete; not validation.",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`.",
                "",
                "The replay uses the completed consolidated authorization response.",
                "It scores only the six deterministically aligned row-level controls,",
                "because those are the controls with frozen `P_row` values.",
                "",
                f"Candidate penalized statistic: `{summary['candidate_T_joint_penalized']}`.",
                f"Controls beating/equal candidate: `{summary['controls_beating_or_equal_candidate']}/{summary['aligned_control_count']}`.",
                f"Best aligned control: `{summary['best_control_id']}` with penalized margin",
                f"`{summary['candidate_minus_best_control_penalized']}`.",
                "",
                "This is guarded endpoint scoring / preflight evidence only. It is",
                "not endpoint validation, cosmological validation, or physical validation.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(
        "JOINT_ROW_LEVEL_PENALIZED_T_JOINT_ENDPOINT_SCORING_V1_COMPLETE "
        f"controls_beating={beating} candidate={summary['candidate_T_joint_penalized']}"
    )


if __name__ == "__main__":
    main()
