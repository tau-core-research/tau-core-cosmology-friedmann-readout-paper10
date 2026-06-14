#!/usr/bin/env python3
from __future__ import annotations

import csv
import statistics
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCORES = ROOT / "data/derived/joint_numeric_t_joint_permission_only_endpoint_scoring_v1.csv"
SUMMARY = ROOT / "data/derived/joint_numeric_t_joint_permission_only_endpoint_scoring_v1_summary.csv"
FAMILY_OUT = ROOT / "data/derived/joint_numeric_t_joint_shuffle_margin_diagnostic_v1.csv"
CLOSEST_OUT = ROOT / "data/derived/joint_numeric_t_joint_shuffle_margin_closest_controls_v1.csv"
SUMMARY_OUT = ROOT / "data/derived/joint_numeric_t_joint_shuffle_margin_diagnostic_v1_summary.csv"
DOC = ROOT / "docs/joint_numeric_t_joint_shuffle_margin_diagnostic_v1.md"
CLAIM_BOUNDARY = "joint_numeric_t_joint_shuffle_margin_diagnostic_not_validation"


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
    endpoint = read_one(SUMMARY)
    rows = read_rows(SCORES)
    if endpoint["verdict"] != "permission_only_endpoint_score_candidate_exceeds_all_controls_not_validation":
        raise SystemExit("permission-only endpoint scoring summary has unexpected verdict")
    if endpoint["endpoint_validation_claimed"] != "false":
        raise SystemExit("endpoint validation must remain false")
    by_family: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_family[row["control_family"]].append(row)

    family_rows = []
    for family, family_controls in sorted(by_family.items()):
        margins = [as_float(row["candidate_minus_control"]) for row in family_controls]
        best_row = min(family_controls, key=lambda row: as_float(row["candidate_minus_control"]))
        family_rows.append(
            {
                "diagnostic_id": "JOINT_NUMERIC_T_JOINT_SHUFFLE_MARGIN_DIAGNOSTIC_V1",
                "control_family": family,
                "control_count": str(len(family_controls)),
                "min_candidate_minus_control": f"{min(margins):.12e}",
                "median_candidate_minus_control": f"{statistics.median(margins):.12e}",
                "mean_candidate_minus_control": f"{statistics.mean(margins):.12e}",
                "max_candidate_minus_control": f"{max(margins):.12e}",
                "closest_control_id": best_row["control_id"],
                "closest_control_numeric_t_joint": best_row["control_numeric_t_joint"],
                "candidate_exceeds_all_controls_in_family": str(all(margin > 0 for margin in margins)).lower(),
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    closest_rows = []
    for rank, row in enumerate(sorted(rows, key=lambda r: as_float(r["candidate_minus_control"]))[:10], start=1):
        closest_rows.append(
            {
                "diagnostic_id": "JOINT_NUMERIC_T_JOINT_SHUFFLE_MARGIN_DIAGNOSTIC_V1",
                "rank": str(rank),
                "control_id": row["control_id"],
                "control_family": row["control_family"],
                "candidate_numeric_t_joint": row["candidate_numeric_t_joint"],
                "control_numeric_t_joint": row["control_numeric_t_joint"],
                "candidate_minus_control": row["candidate_minus_control"],
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    shuffle = next(row for row in family_rows if row["control_family"] == "shuffled_channel_labels")
    next_best = sorted(
        [row for row in family_rows if row["control_family"] != "shuffled_channel_labels"],
        key=lambda row: as_float(row["min_candidate_minus_control"]),
    )[0]
    ratio = as_float(next_best["min_candidate_minus_control"]) / as_float(shuffle["min_candidate_minus_control"])
    summary = {
        "diagnostic_id": "JOINT_NUMERIC_T_JOINT_SHUFFLE_MARGIN_DIAGNOSTIC_V1",
        "candidate_numeric_t_joint": endpoint["candidate_numeric_t_joint"],
        "numeric_control_count": endpoint["numeric_control_count"],
        "controls_beating_or_equal_candidate": endpoint["controls_beating_or_equal_candidate"],
        "closest_control_id": endpoint["best_control_id"],
        "closest_control_family": endpoint["best_control_family"],
        "closest_margin": endpoint["candidate_minus_best_control"],
        "shuffle_family_min_margin": shuffle["min_candidate_minus_control"],
        "next_best_family": next_best["control_family"],
        "next_best_family_min_margin": next_best["min_candidate_minus_control"],
        "next_best_to_shuffle_min_margin_ratio": f"{ratio:.12e}",
        "verdict": "candidate_exceeds_all_controls_but_shuffle_margin_is_thin_not_validation",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
    }

    write_csv(FAMILY_OUT, family_rows)
    write_csv(CLOSEST_OUT, closest_rows)
    write_csv(SUMMARY_OUT, [summary])
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Joint numeric T_joint shuffle-margin diagnostic v1",
                "",
                "**Doc class:** permission-only endpoint diagnostic follow-up.",
                "**Status:** not validation.",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`.",
                "",
                f"Candidate numeric `T_joint`: `{summary['candidate_numeric_t_joint']}`.",
                f"Controls beating/equal candidate: `{summary['controls_beating_or_equal_candidate']}/{summary['numeric_control_count']}`.",
                f"Closest control: `{summary['closest_control_id']}` in `{summary['closest_control_family']}`.",
                f"Closest margin: `{summary['closest_margin']}`.",
                f"Next-best family minimum margin is `{summary['next_best_to_shuffle_min_margin_ratio']}` times the shuffled-channel minimum margin.",
                "",
                "Interpretation: the candidate exceeds all frozen numeric controls,",
                "but the shuffled-channel family is the thin-margin direction. This",
                "is a robustness diagnostic, not endpoint validation, cosmological",
                "validation, or physical validation.",
                "",
            ]
        )
    )
    print("JOINT_NUMERIC_T_JOINT_SHUFFLE_MARGIN_DIAGNOSTIC_V1_BUILT")


if __name__ == "__main__":
    main()
