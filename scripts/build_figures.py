#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
import shutil
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "figures"
SUBMISSION_FIGURES = ROOT / "paper10_submission_source" / "figures"
SUMMARY = ROOT / "data" / "derived" / "pantheon_full_cov_pilot_scoring_v1_summary.csv"
GRID = ROOT / "data" / "derived" / "pantheon_full_cov_pilot_scoring_v1_grid.csv"

FIGURE_NAME = "fig_pantheon_full_cov_pilot_branch_diagnostics.pdf"
STALE_FIGURES = [
    "fig_bridge_map.pdf",
    "fig_leakage_ladder.pdf",
    "fig_pilot_score_panel.pdf",
    "fig_pantheon_pilot_diagnostics.pdf",
    "fig_pantheon_pilot_branch_diagnostics.pdf",
]


plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 8.5,
        "axes.titlesize": 9.5,
        "axes.labelsize": 8.5,
        "xtick.labelsize": 7.6,
        "ytick.labelsize": 7.6,
        "legend.fontsize": 7.4,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    }
)


BRANCH_LABELS = {
    "baseline_only": "LCDM",
    "tau_shell": "Tau",
    "wrong_activation": "wrong",
    "deterministic_shuffled_activation": "shuffled",
}
BRANCH_COLORS = {
    "baseline_only": "#4d5f73",
    "tau_shell": "#2c73b9",
    "wrong_activation": "#c57a2c",
    "deterministic_shuffled_activation": "#7d6bb1",
}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def finite_grid() -> list[dict[str, str]]:
    return [row for row in read_rows(GRID) if row["chi2"] != "inf"]


def best_by_branch(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    grouped: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        grouped.setdefault(row["branch"], []).append(row)
    return {branch: min(items, key=lambda r: float(r["chi2"])) for branch, items in grouped.items()}


def copy_figure(out: Path) -> None:
    SUBMISSION_FIGURES.mkdir(parents=True, exist_ok=True)
    shutil.copy2(out, SUBMISSION_FIGURES / out.name)


def cleanup_stale_figures() -> None:
    for directory in [FIGURES, SUBMISSION_FIGURES]:
        for name in STALE_FIGURES:
            path = directory / name
            if path.exists():
                path.unlink()


def panel_branch_scatter(ax, rows: list[dict[str, str]], best: dict[str, dict[str, str]], metric: str) -> None:
    base = float(best["baseline_only"][metric])
    order = [
        "baseline_only",
        "tau_shell",
        "wrong_activation",
        "deterministic_shuffled_activation",
    ]
    rng = np.random.default_rng(20260608)
    for i, branch in enumerate(order):
        vals = [float(row[metric]) - base for row in rows if row["branch"] == branch]
        jitter = rng.normal(0.0, 0.025, size=len(vals))
        ax.scatter(
            np.full(len(vals), i) + jitter,
            vals,
            s=10,
            color=BRANCH_COLORS[branch],
            alpha=0.42,
            linewidths=0,
            label=BRANCH_LABELS[branch],
        )
        best_val = float(best[branch][metric]) - base
        ax.scatter(
            [i],
            [best_val],
            s=58,
            color=BRANCH_COLORS[branch],
            edgecolor="black",
            linewidth=0.7,
            zorder=4,
        )
        ax.text(i, best_val, f" {best_val:+.3f}", va="center", fontsize=7.1, color="#202633")
    ax.axhline(0, color="#303846", linewidth=0.8)
    ax.set_xticks(range(len(order)))
    ax.set_xticklabels([BRANCH_LABELS[b] for b in order])
    ax.set_ylabel(f"Delta {metric}")
    ax.grid(axis="y", color="#d7dce5", linewidth=0.55, alpha=0.85)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def build_pantheon_pilot_branch_diagnostics() -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    cleanup_stale_figures()
    rows = finite_grid()
    best = best_by_branch(rows)
    summary = read_one(SUMMARY)

    fig, (ax_chi2, ax_aic) = plt.subplots(1, 2, figsize=(7.4, 3.55), sharex=False)
    fig.suptitle("Pantheon+ full-covariance pilot diagnostics under the frozen Paper 10 grammar", fontsize=11.2, fontweight="bold", y=0.98)
    panel_branch_scatter(ax_chi2, rows, best, "chi2")
    ax_chi2.set_title("All frozen-grid scores: chi2")
    panel_branch_scatter(ax_aic, rows, best, "aic")
    ax_aic.set_title("All frozen-grid scores: AIC")
    fig.text(
        0.5,
        0.018,
        (
            f"n={summary['n_rows']}; full STAT+SYS covariance pilot; "
            f"Tau: Delta chi2={float(summary['delta_chi2_tau_minus_baseline']):+.3f}, "
            f"Delta AIC={float(summary['delta_aic_tau_minus_baseline']):+.3f}.\n"
            "Filled markers denote branch minima. This is not validation."
        ),
        ha="center",
        fontsize=7.8,
        color="#3d4658",
    )
    fig.subplots_adjust(left=0.08, right=0.985, bottom=0.24, top=0.82, wspace=0.24)
    out = FIGURES / FIGURE_NAME
    fig.savefig(
        out,
        bbox_inches="tight",
        pad_inches=0.05,
        metadata={
            "Title": "Paper10 Pantheon full-covariance pilot diagnostics",
            "Author": "tau-core-paper10-reproducibility-package",
            "Subject": "Frozen-grid diagnostic figure; not validation",
            "Keywords": "Tau Core, Pantheon, reproducibility, pilot",
            "Creator": "scripts/build_figures.py",
            "Producer": "matplotlib",
            "CreationDate": None,
            "ModDate": None,
        },
    )
    copy_figure(out)
    plt.close(fig)


def main() -> None:
    build_pantheon_pilot_branch_diagnostics()
    print(f"PAPER10_FIGURES_BUILT files=1 figure={FIGURE_NAME}")


if __name__ == "__main__":
    main()
