#!/usr/bin/env python3
from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_IN = ROOT / "data/source_manifest/joint_best_justified_kernel_manifest_v1.csv"
ROBUSTNESS_IN = ROOT / "data/derived/joint_best_justified_kernel_robustness_v1_summary.csv"
FIGURE_OUT = ROOT / "paper10_submission_source/figures/fig_joint_best_justified_kernel_v1.pdf"
PDF_DATE = datetime(2026, 1, 1, tzinfo=timezone.utc)


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required input: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    manifest = read_rows(MANIFEST_IN)
    robustness = read_rows(ROBUSTNESS_IN)
    scheme_rows = [row for row in robustness if row["scheme_id"]]
    aggregate_rows = [
        row for row in robustness
        if row["robustness_id"] == "JOINT_BEST_JUSTIFIED_KERNEL_ROBUSTNESS_V1"
    ]
    if len(aggregate_rows) != 1:
        raise SystemExit("missing unique robustness aggregate row")
    aggregate = aggregate_rows[0]
    if aggregate["endpoint_validation_claimed"] != "false":
        raise SystemExit("figure requires endpoint_validation_claimed=false")
    if aggregate["cosmological_validation_claimed"] != "false":
        raise SystemExit("figure requires cosmological_validation_claimed=false")

    positive = [row for row in manifest if row["positive_support_allowed"] == "true"]
    nonpositive = [row for row in manifest if row["positive_support_allowed"] != "true"]
    positive = sorted(positive, key=lambda row: float(row["Q_i"]), reverse=True)
    nonpositive = sorted(nonpositive, key=lambda row: row["channel_id"])
    channels = positive + nonpositive

    channel_labels = [
        {
            "kids_lensing_cosebis_low_mode": "KiDS\nCOSEBIs",
            "observer_path_basis_low_z": "observer/path\nlow-z",
            "desi_shape_time_readout": "DESI\nshape",
            "act_kpath_lensing_path": "ACT\nKpath",
            "distance_homogeneous_tau_shell": "distance\nshell",
            "observer_orientation_sky_z_control_negative": "sky-z\ncontrol",
            "time_uncertainty_basis": "time\nbasis",
            "void_web_proxy_distance": "void/web\nproxy",
        }.get(row["channel_id"], row["channel_id"].replace("_", "\n"))
        for row in channels
    ]
    q_values = [float(row["Q_i"]) for row in channels]
    colors = [
        "#2f5597" if row["positive_support_allowed"] == "true" else "#c7cbd1"
        for row in channels
    ]

    scheme_labels = [
        {
            "equal_geometric": "equal\ngeometric",
            "source_heavy": "source\nheavy",
            "control_heavy": "control\nheavy",
            "projection_heavy": "projection\nheavy",
            "conservative_min_gate": "min-gate",
        }.get(row["scheme_id"], row["scheme_id"].replace("_", "\n"))
        for row in scheme_rows
    ]
    norm_scores = [float(row["normalized_score"]) for row in scheme_rows]
    combined_p = [
        float(row["combined_control_one_sided_p_ge_observed"])
        for row in scheme_rows
    ]
    scheme_colors = ["#2f5597", "#4878a8", "#5f8ab5", "#759cc2", "#8a6f3d"]

    fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.55), gridspec_kw={"width_ratios": [1.18, 1.0]})
    ax0, ax1 = axes

    ax0.bar(range(len(channels)), q_values, color=colors, edgecolor="#1f2933", linewidth=0.7)
    ax0.set_xticks(range(len(channels)))
    ax0.set_xticklabels(channel_labels, fontsize=7.5)
    ax0.set_ylim(0.0, 0.82)
    ax0.set_ylabel(r"source-side support $Q_i$")
    ax0.set_title("A. Frozen channel support ledger", loc="left", fontsize=10.5, fontweight="bold")
    ax0.axhline(0.0, color="#1f2933", linewidth=0.8)
    ax0.text(
        0.02,
        0.96,
        "blue = positive support; gray = control/negative/diagnostic",
        transform=ax0.transAxes,
        ha="left",
        va="top",
        fontsize=7.8,
        color="#4b5563",
    )

    bars = ax1.bar(range(len(scheme_rows)), norm_scores, color=scheme_colors, edgecolor="#1f2933", linewidth=0.7)
    ax1.set_xticks(range(len(scheme_rows)))
    ax1.set_xticklabels(scheme_labels, fontsize=7.5)
    ax1.set_ylim(0.65, 0.75)
    ax1.set_ylabel(r"normalized preflight score $\widehat S_{\rm bj}$")
    ax1.set_title("B. Weighting-rule robustness", loc="left", fontsize=10.5, fontweight="bold")
    ax1.axhline(0.0, color="#1f2933", linewidth=0.8)
    for bar, p_value in zip(bars, combined_p):
        ax1.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.002,
            f"p={p_value:.3f}",
            ha="center",
            va="bottom",
            fontsize=7.0,
            rotation=90,
            color="#374151",
        )

    for ax in axes:
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", linestyle=":", linewidth=0.6, alpha=0.55)
        ax.set_axisbelow(True)

    fig.suptitle(
        "Best-justified joint kernel: prevalidation support and robustness",
        fontsize=12.0,
        fontweight="bold",
        y=0.985,
    )
    fig.text(
        0.01,
        0.01,
        "Claim boundary: preflight only; not a joint likelihood, endpoint validation, or cosmological validation.",
        ha="left",
        va="bottom",
        fontsize=8.0,
        color="#4b5563",
    )
    fig.tight_layout(rect=(0, 0.045, 1, 0.91))
    FIGURE_OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(
        FIGURE_OUT,
        metadata={
            "Title": "Best-justified joint kernel prevalidation figure",
            "CreationDate": PDF_DATE,
            "ModDate": PDF_DATE,
        },
    )
    plt.close(fig)
    print(f"built {FIGURE_OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
