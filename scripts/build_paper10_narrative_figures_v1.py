#!/usr/bin/env python3
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from textwrap import fill

from matplotlib.patches import FancyBboxPatch
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "paper10_submission_source/figures"
PDF_DATE = datetime(2026, 1, 1, tzinfo=timezone.utc)


def save(fig: plt.Figure, name: str) -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    out = FIG_DIR / name
    fig.savefig(
        out,
        metadata={
            "Title": name.replace("_", " ").replace(".pdf", ""),
            "CreationDate": PDF_DATE,
            "ModDate": PDF_DATE,
        },
    )
    plt.close(fig)
    print(f"built {out.relative_to(ROOT)}")


def style_axis(ax):
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", linestyle=":", linewidth=0.6, alpha=0.55)
    ax.set_axisbelow(True)


def build_claim_ladder() -> None:
    steps = [
        ("Source-side readiness", "declared / frozen"),
        ("Single-channel replay", "mixed record"),
        ("Joint preflight", "CURRENT PAPER"),
        ("Future joint endpoint likelihood", "not reached"),
        ("Cosmological validation", "not claimed"),
    ]
    x = np.arange(len(steps))
    colors = ["#90caf9", "#90caf9", "#2f5597", "#d6dbe1", "#d6dbe1"]

    fig, ax = plt.subplots(figsize=(11.2, 4.8))
    ax.set_xlim(-0.72, len(steps) - 0.28)
    ax.set_ylim(-0.35, 1.65)
    ax.axis("off")
    box_w = 0.82
    box_h = 0.78
    box_y = 0.52
    for i, ((label, status), color) in enumerate(zip(steps, colors)):
        box = FancyBboxPatch(
            (i - box_w / 2, box_y - box_h / 2),
            box_w,
            box_h,
            boxstyle="round,pad=0.035,rounding_size=0.045",
            facecolor=color,
            edgecolor="#1f2933",
            linewidth=1.1,
        )
        ax.add_patch(box)
        text_color = "white" if i == 2 else "#111827"
        status_color = "white" if i == 2 else "#374151"
        ax.text(
            i,
            box_y + 0.13,
            fill(label, width=14),
            ha="center",
            va="center",
            fontsize=8.7,
            fontweight="bold",
            color=text_color,
            linespacing=1.08,
        )
        ax.text(
            i,
            box_y - 0.20,
            fill(status, width=14),
            ha="center",
            va="center",
            fontsize=7.8,
            color=status_color,
            linespacing=1.08,
        )
        if i < len(steps) - 1:
            ax.annotate("", xy=(i + 0.55, box_y), xytext=(i + 0.45, box_y),
                        arrowprops=dict(arrowstyle="->", lw=1.7, color="#4b5563"))
    ax.text(2, 1.25, "prevalidation / not validation", ha="center", va="center",
            fontsize=10.5, color="#b91c1c", fontweight="bold")
    fig.suptitle("Evidence hierarchy and current Paper 10 position", fontsize=13, fontweight="bold")
    fig.text(0.02, 0.03,
             "Claim boundary: current numerical quantities are internal audit statistics, not p-values, likelihood ratios, or validation evidence.",
             fontsize=8.3, color="#4b5563")
    fig.tight_layout(rect=(0, 0.06, 1, 0.9))
    save(fig, "fig_paper10_claim_ladder_v1.pdf")


def build_channel_matrix() -> None:
    rows = [
        ("KiDS/COSEBIs", ["pass", "pass", "caveat", "pass", "blocked", "pass"]),
        ("Observer/path low-z", ["pass", "pass", "caveat", "pass", "blocked", "pass"]),
        ("DESI shape/readout", ["pass", "caveat", "caveat", "pass", "blocked", "pass"]),
        ("Void/web", ["caveat", "caveat", "blocked", "negative", "blocked", "zero"]),
        ("Time/clock", ["caveat", "caveat", "blocked", "diagnostic", "blocked", "zero"]),
        ("ACT Kpath", ["pass", "pass", "caveat", "diagnostic", "blocked", "zero"]),
    ]
    cols = ["Source\nfrozen", "Controls\navailable", "Replay\nallowed",
            "Positive\naudit support", "Validation\nblocker open", "Joint\nQ_i>0"]
    code = {"pass": 3, "caveat": 2, "diagnostic": 1, "zero": 0, "negative": -1, "blocked": -2}
    labels = {
        3: "pass", 2: "caveated", 1: "diagnostic", 0: "zero", -1: "negative", -2: "blocked"
    }
    colors = {
        3: "#2e7d32", 2: "#f9a825", 1: "#9e9e9e", 0: "#cfd8dc", -1: "#c62828", -2: "#b71c1c"
    }
    matrix = np.array([[code[v] for v in vals] for _, vals in rows])

    fig, ax = plt.subplots(figsize=(10.2, 5.2))
    ax.set_xlim(-0.5, len(cols) - 0.5)
    ax.set_ylim(len(rows) - 0.5, -0.5)
    for r in range(len(rows)):
        for c in range(len(cols)):
            val = matrix[r, c]
            ax.add_patch(plt.Rectangle((c - 0.5, r - 0.5), 1, 1,
                                       color=colors[val], ec="white", lw=1.5))
            ax.text(c, r, labels[val], ha="center", va="center", fontsize=7.2,
                    color="white" if val in {3, -1, -2} else "#111827")
    ax.set_xticks(np.arange(len(cols)))
    ax.set_xticklabels(cols, fontsize=8)
    ax.set_yticks(np.arange(len(rows)))
    ax.set_yticklabels([r[0] for r in rows], fontsize=9)
    ax.tick_params(length=0)
    ax.set_title("Channel status matrix: why only three channels enter the positive-support kernel",
                 fontsize=12, fontweight="bold", pad=14)
    ax.text(-0.5, len(rows) + 0.05,
            "Legend: green=pass/usable; yellow=caveated; red=blocked/negative; gray=diagnostic or zero-support.",
            fontsize=8.2, color="#4b5563", ha="left", va="bottom")
    ax.text(-0.5, len(rows) + 0.38,
            "Positive audit support = source-frozen survival under this protocol, not physical confirmation.",
            fontsize=8.0, color="#4b5563", ha="left", va="bottom")
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.tight_layout()
    save(fig, "fig_paper10_channel_status_matrix_v1.pdf")


def build_validation_blocker_dashboard() -> None:
    rows = [
        ("Validation-grade joint likelihood", "NOT CLOSED", "#b71c1c"),
        ("Cross-probe covariance", "NOT CLOSED", "#b71c1c"),
        ("Source-native $Q_i$ review", "NOT CLOSED", "#b71c1c"),
        ("Strict aligned-control population", "TOO SMALL", "#f9a825"),
        ("KiDS operator / theorem promotion", "NOT CLOSED", "#b71c1c"),
        ("DESI row-sensitive margin", "OPEN CAVEAT", "#f9a825"),
        ("Observer/path population source-native", "NOT CLOSED", "#b71c1c"),
    ]
    fig, ax = plt.subplots(figsize=(10.6, 4.9))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, len(rows) + 1.3)
    ax.axis("off")
    ax.text(
        0.02,
        len(rows) + 0.82,
        "Validation blocker dashboard",
        fontsize=13,
        fontweight="bold",
        color="#111827",
        va="center",
    )
    ax.text(
        0.02,
        len(rows) + 0.42,
        "These blockers prevent validation-grade interpretation of the positive preflight signal.",
        fontsize=8.8,
        color="#4b5563",
        va="center",
    )
    for idx, (label, status, color) in enumerate(rows):
        y = len(rows) - idx - 0.25
        ax.add_patch(
            FancyBboxPatch(
                (0.02, y - 0.34),
                0.68,
                0.54,
                boxstyle="round,pad=0.02,rounding_size=0.025",
                facecolor="#eef2f6",
                edgecolor="#c7d0d9",
                linewidth=0.8,
            )
        )
        ax.add_patch(
            FancyBboxPatch(
                (0.73, y - 0.34),
                0.25,
                0.54,
                boxstyle="round,pad=0.02,rounding_size=0.025",
                facecolor=color,
                edgecolor="#1f2933",
                linewidth=0.8,
            )
        )
        ax.text(0.05, y - 0.07, label, fontsize=9.2, color="#111827", va="center")
        ax.text(0.855, y - 0.07, status, fontsize=8.7, color="white" if color == "#b71c1c" else "#111827",
                fontweight="bold", va="center", ha="center")
    fig.text(
        0.02,
        0.025,
        "Claim boundary: Paper 10 records prevalidation support and explicit blockers; it does not claim cosmological validation.",
        fontsize=8.0,
        color="#4b5563",
    )
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    save(fig, "fig_paper10_validation_blocker_dashboard_v1.pdf")


def build_tjoint_controls() -> None:
    ledger = pd.read_csv(ROOT / "data/derived/joint_numeric_t_joint_ledger_v1.csv")
    controls = pd.read_csv(ROOT / "data/derived/joint_numeric_t_joint_permission_only_endpoint_scoring_v1.csv")
    contrib = ledger["q_i_z_i_contribution"].astype(float).to_numpy()
    labels = ["KiDS/COSEBIs", "observer/path", "DESI shape"]
    candidate = float(controls["candidate_numeric_t_joint"].iloc[0])
    controls_sorted = controls.sort_values("control_numeric_t_joint", ascending=False).reset_index(drop=True)
    control_vals = controls_sorted["control_numeric_t_joint"].astype(float).to_numpy()
    control_fams = controls_sorted["control_family"].astype(str).to_numpy()
    colors = ["#7b1fa2" if "shuffle" in fam else "#90a4ae" for fam in control_fams]

    fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.3), gridspec_kw={"width_ratios": [0.9, 1.25]})
    ax0, ax1 = axes
    ax0.bar(labels, contrib, color=["#2f5597", "#4e79a7", "#76a5af"], edgecolor="#1f2933")
    ax0.axhline(0, color="#1f2933", lw=0.8)
    ax0.set_ylabel(r"contribution to $T_{\rm joint}$")
    ax0.set_title("A. Same-statistic channel contributions", loc="left", fontsize=10.5, fontweight="bold")
    ax0.text(0.5, max(contrib) * 0.88, rf"total $T_{{\rm joint}}={candidate:.3f}$",
             ha="center", va="center", fontsize=9, color="#111827")
    ax0.tick_params(axis="x", labelrotation=18)
    style_axis(ax0)

    ax1.scatter(np.arange(len(control_vals)), control_vals, c=colors, s=35, edgecolor="#1f2933", linewidth=0.4)
    ax1.axhline(candidate, color="#b91c1c", lw=1.8, label="candidate")
    best = control_vals[0]
    ax1.annotate("closest shuffled margin\n$2.964\\times10^{-3}$",
                 xy=(0, best), xytext=(4.0, candidate - 0.33),
                 arrowprops=dict(arrowstyle="->", color="#b91c1c", lw=1.0),
                 fontsize=8.2, color="#b91c1c")
    ax1.set_xlabel("control rank")
    ax1.set_ylabel(r"control $T_{\rm joint}$")
    ax1.set_title("B. Candidate versus 26 same-statistic controls", loc="left", fontsize=10.5, fontweight="bold")
    style_axis(ax1)
    ax1.legend(frameon=False, fontsize=8, loc="lower left")

    fig.suptitle("Same-statistic ledger: positive but with a thin channel-assignment margin",
                 fontsize=12.3, fontweight="bold")
    fig.text(0.01, 0.01,
             "Claim boundary: permission-only diagnostic; not a p-value, likelihood ratio, endpoint validation, or cosmological validation.",
             fontsize=8.0, color="#4b5563")
    fig.tight_layout(rect=(0, 0.04, 1, 0.91))
    save(fig, "fig_paper10_tjoint_contributions_controls_v1.pdf")


def build_row_level_stress() -> None:
    strict = pd.read_csv(ROOT / "data/derived/joint_row_level_penalized_t_joint_endpoint_scoring_v1.csv")
    relaxed = pd.read_csv(ROOT / "data/derived/joint_row_level_relaxed_cyclic_penalized_stress_v1.csv")
    candidate = float(strict["candidate_T_joint_penalized"].iloc[0])
    strict_vals = strict.sort_values("control_T_joint_penalized", ascending=False)["control_T_joint_penalized"].astype(float).to_numpy()
    cand_penalty = float(relaxed["candidate_P_row"].iloc[0])
    relaxed_vals = relaxed.sort_values("control_P_row", ascending=False)["control_P_row"].astype(float).to_numpy()

    fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.25), gridspec_kw={"width_ratios": [1.0, 1.0]})
    ax0, ax1 = axes
    ax0.scatter(np.arange(len(strict_vals)), strict_vals, color="#4e79a7", s=42, edgecolor="#1f2933", linewidth=0.4)
    ax0.axhline(candidate, color="#2e7d32", lw=1.8, label="candidate")
    ax0.set_xlabel("strict aligned control rank")
    ax0.set_ylabel(r"$T_{\rm joint}^{\rm penalized}$")
    ax0.set_title("A. Strict six-control replay", loc="left", fontsize=10.5, fontweight="bold")
    ax0.text(0.03, 0.08, "0/6 controls beat candidate", transform=ax0.transAxes,
             fontsize=8.5, color="#2e7d32", fontweight="bold")
    style_axis(ax0)
    ax0.legend(frameon=False, fontsize=8, loc="upper right")

    exceeds = relaxed_vals >= cand_penalty
    ax1.bar(np.arange(len(relaxed_vals)), relaxed_vals,
            color=["#b71c1c" if ex else "#90a4ae" for ex in exceeds],
            edgecolor="#1f2933", linewidth=0.25)
    ax1.axhline(cand_penalty, color="#2f5597", lw=1.8, label="candidate penalty")
    ax1.set_xlabel("relaxed cyclic control rank")
    ax1.set_ylabel(r"row-level penalty $P_{\rm row}$")
    ax1.set_title("B. Relaxed 25-control stress", loc="left", fontsize=10.5, fontweight="bold")
    ax1.text(0.03, 0.88, "17/25 controls >= candidate", transform=ax1.transAxes,
             fontsize=8.5, color="#b71c1c", fontweight="bold")
    style_axis(ax1)
    ax1.legend(frameon=False, fontsize=8, loc="upper right")

    fig.suptitle("Row-level penalty: strict positive replay, relaxed caveated-negative stress",
                 fontsize=12.3, fontweight="bold")
    fig.text(0.01, 0.01,
             "Claim boundary: strict replay has only six aligned controls; relaxed cyclic expansion is a stress test, not validation.",
             fontsize=8.0, color="#4b5563")
    fig.tight_layout(rect=(0, 0.04, 1, 0.91))
    save(fig, "fig_paper10_row_level_strict_relaxed_stress_v1.pdf")


def main() -> None:
    build_claim_ladder()
    build_channel_matrix()
    build_validation_blocker_dashboard()
    build_tjoint_controls()
    build_row_level_stress()


if __name__ == "__main__":
    main()
