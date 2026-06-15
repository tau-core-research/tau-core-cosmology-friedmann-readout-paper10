#!/usr/bin/env python3
from __future__ import annotations

import csv
import statistics
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data" / "derived"
DOCS = ROOT / "docs"

SCORING = DERIVED / "joint_row_level_penalized_t_joint_endpoint_scoring_v1.csv"
SCORING_SUMMARY = DERIVED / "joint_row_level_penalized_t_joint_endpoint_scoring_v1_summary.csv"
OUT_SWEEP = DERIVED / "joint_row_level_penalized_t_joint_lambda_sensitivity_v1.csv"
OUT_LOO = DERIVED / "joint_row_level_penalized_t_joint_leave_one_control_out_v1.csv"
SUMMARY = DERIVED / "joint_row_level_penalized_t_joint_robustness_v1_summary.csv"
DOC = DOCS / "joint_row_level_penalized_t_joint_robustness_v1.md"
CLAIM_BOUNDARY = "joint_row_level_penalized_t_joint_robustness_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def f(value: str) -> float:
    return float(value)


def main() -> None:
    base_summary = read_one(SCORING_SUMMARY)
    rows = read_rows(SCORING)
    if base_summary["status"] != "GUARDED_ENDPOINT_SCORING_COMPLETE_NOT_VALIDATION":
        raise SystemExit("base scoring summary is not the guarded scoring result")
    if len(rows) != 6:
        raise SystemExit("robustness v1 expects six aligned controls")

    base_t = f(base_summary["base_candidate_T_joint"])
    p_candidate = f(base_summary["candidate_P_row"])
    lambdas = [0.0, 0.5, 1.0, 2.0]

    sweep_rows: list[dict[str, str]] = []
    for lam in lambdas:
        candidate = base_t + lam * p_candidate
        margins = []
        beat_count = 0
        best_control_id = ""
        best_control_value = float("-inf")
        for row in rows:
            control = f(row["control_T_joint"]) + lam * f(row["control_P_row"])
            margins.append(candidate - control)
            if control >= candidate:
                beat_count += 1
            if control > best_control_value:
                best_control_value = control
                best_control_id = row["control_id"]
        sweep_rows.append(
            {
                "run_id": "JOINT_ROW_LEVEL_PENALIZED_T_JOINT_LAMBDA_SENSITIVITY_V1",
                "lambda_row": f"{lam:.12e}",
                "candidate_T_joint_penalized": f"{candidate:.12e}",
                "aligned_control_count": str(len(rows)),
                "controls_beating_or_equal_candidate": str(beat_count),
                "candidate_rank_among_controls_plus_candidate": str(1 + beat_count),
                "best_control_id": best_control_id,
                "best_control_T_joint_penalized": f"{best_control_value:.12e}",
                "min_margin": f"{min(margins):.12e}",
                "median_margin": f"{statistics.median(margins):.12e}",
                "mean_margin": f"{statistics.mean(margins):.12e}",
                "endpoint_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(OUT_SWEEP, sweep_rows)

    loo_rows: list[dict[str, str]] = []
    for omitted in rows:
        kept = [row for row in rows if row["control_id"] != omitted["control_id"]]
        margins = [f(row["candidate_minus_control_penalized"]) for row in kept]
        beat_count = sum(1 for row in kept if row["control_beats_or_equals_candidate"] == "true")
        loo_rows.append(
            {
                "run_id": "JOINT_ROW_LEVEL_PENALIZED_T_JOINT_LEAVE_ONE_CONTROL_OUT_V1",
                "omitted_control_id": omitted["control_id"],
                "kept_control_count": str(len(kept)),
                "controls_beating_or_equal_candidate": str(beat_count),
                "candidate_rank_among_controls_plus_candidate": str(1 + beat_count),
                "min_margin": f"{min(margins):.12e}",
                "median_margin": f"{statistics.median(margins):.12e}",
                "mean_margin": f"{statistics.mean(margins):.12e}",
                "endpoint_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(OUT_LOO, loo_rows)

    base_margins = [f(row["candidate_minus_control_penalized"]) for row in rows]
    lambda_failures = sum(1 for row in sweep_rows if row["controls_beating_or_equal_candidate"] != "0")
    loo_failures = sum(1 for row in loo_rows if row["controls_beating_or_equal_candidate"] != "0")
    summary = {
        "run_id": "JOINT_ROW_LEVEL_PENALIZED_T_JOINT_ROBUSTNESS_V1",
        "base_lambda_row": base_summary["lambda_row"],
        "base_candidate_T_joint_penalized": base_summary["candidate_T_joint_penalized"],
        "aligned_control_count": base_summary["aligned_control_count"],
        "base_controls_beating_or_equal_candidate": base_summary["controls_beating_or_equal_candidate"],
        "base_min_margin": f"{min(base_margins):.12e}",
        "base_median_margin": f"{statistics.median(base_margins):.12e}",
        "base_mean_margin": f"{statistics.mean(base_margins):.12e}",
        "lambda_values_tested": "|".join(f"{x:g}" for x in lambdas),
        "lambda_sensitivity_failures": str(lambda_failures),
        "leave_one_control_out_failures": str(loo_failures),
        "worst_lambda_min_margin": f"{min(f(row['min_margin']) for row in sweep_rows):.12e}",
        "worst_loo_min_margin": f"{min(f(row['min_margin']) for row in loo_rows):.12e}",
        "endpoint_validation_claimed": "false",
        "verdict": "ROBUSTNESS_POSITIVE_ON_ALIGNED_CONTROL_SCOPE_NOT_VALIDATION"
        if lambda_failures == 0 and loo_failures == 0
        else "ROBUSTNESS_CAVEATED_ON_ALIGNED_CONTROL_SCOPE_NOT_VALIDATION",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(SUMMARY, [summary])

    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Joint row-level penalized T_joint robustness v1",
                "",
                "**Doc class:** robustness ledger.",
                "**Status:** complete; not validation.",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`.",
                "",
                "This artifact checks only the already authorized six-control",
                "aligned row-level scope. It does not add new data or broaden the",
                "control universe.",
                "",
                f"Base min margin: `{summary['base_min_margin']}`.",
                f"Base median margin: `{summary['base_median_margin']}`.",
                f"Lambda values tested: `{summary['lambda_values_tested']}`.",
                f"Lambda-sensitivity failures: `{summary['lambda_sensitivity_failures']}`.",
                f"Leave-one-control-out failures: `{summary['leave_one_control_out_failures']}`.",
                "",
                "The result is preflight robustness evidence only, not endpoint",
                "validation or cosmological validation.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(
        "JOINT_ROW_LEVEL_PENALIZED_T_JOINT_ROBUSTNESS_V1_COMPLETE "
        f"lambda_failures={lambda_failures} loo_failures={loo_failures}"
    )


if __name__ == "__main__":
    main()
