#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
ROWS_IN = ROOT / "data/derived/paper10_desi_shape_route_robustness_stress_v1.csv"
SUMMARY_IN = ROOT / "data/derived/paper10_desi_shape_route_robustness_stress_v1_summary.csv"
FIGURE_OUT = ROOT / "paper10_submission_source/figures/fig_desi_shape_route_robustness_stress.pdf"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required input: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def one_row(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def main() -> None:
    rows = read_rows(ROWS_IN)
    summary = one_row(SUMMARY_IN)
    if summary["endpoint_validation_claimed"] != "false":
        raise SystemExit("robustness figure requires non-validation summary")
    if summary["physical_validation_claimed"] != "false":
        raise SystemExit("robustness figure requires non-physical-validation summary")

    ordered_ids = [
        "candidate_CLOCK_SLOPE_SHAPE",
        "drop_shape_row_0",
        "drop_shape_row_1",
        "drop_shape_row_2",
        "drop_shape_row_3",
        "drop_shape_rows_0_3",
    ]
    labels = [
        "candidate",
        "drop 0",
        "drop 1",
        "drop 2",
        "drop 3",
        "best\nleave-two",
    ]
    row_by_id = {row["test_id"]: row for row in rows}
    missing = [test_id for test_id in ordered_ids if test_id not in row_by_id]
    if missing:
        raise SystemExit(f"missing robustness rows: {missing}")

    scores = [float(row_by_id[test_id]["shape_quadratic_score"]) for test_id in ordered_ids]
    fractions = [
        float(row_by_id[test_id]["score_fraction_of_full_candidate"]) for test_id in ordered_ids
    ]
    colors = ["#2f5597"] + ["#b85c38"] * 4 + ["#6b7f3a"]

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    bars = ax.bar(labels, scores, color=colors, edgecolor="#1f2933", linewidth=0.8)
    ax.axhline(float(summary["candidate_score"]), color="#2f5597", linewidth=1.0, alpha=0.5)
    ax.set_ylabel("Frozen quadratic shape score")
    ax.set_title("DESI shape-route permission replay: internal robustness stress")
    ax.text(
        0.01,
        0.96,
        "not endpoint validation; not physical validation",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=8.5,
        color="#4b5563",
    )
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", linestyle=":", linewidth=0.6, alpha=0.5)
    ax.set_axisbelow(True)
    for bar, fraction in zip(bars, fractions):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.06,
            f"{fraction:.3f}x",
            ha="center",
            va="bottom",
            fontsize=8,
        )
    fig.tight_layout()
    FIGURE_OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGURE_OUT, metadata={"Title": "DESI shape-route robustness stress"})
    plt.close(fig)
    print(f"built {FIGURE_OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
