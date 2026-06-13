#!/usr/bin/env python3
from __future__ import annotations

import csv
import itertools
import math
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data/derived/joint_multichannel_endpoint_candidate_v1.csv"
MANIFEST = ROOT / "data/source_manifest/joint_best_justified_kernel_manifest_v1.csv"
OUT = ROOT / "data/derived/joint_best_justified_kernel_score_v1.csv"
CONTROLS = ROOT / "data/derived/joint_best_justified_kernel_score_v1_controls.csv"
LOO = ROOT / "data/derived/joint_best_justified_kernel_score_v1_leave_one_channel.csv"
SUMMARY = ROOT / "data/derived/joint_best_justified_kernel_score_v1_summary.csv"
DOC = ROOT / "docs/joint_best_justified_kernel_score_v1.md"
CLAIM_BOUNDARY = "joint_best_justified_kernel_prevalidation_not_joint_likelihood"
SEED = 240913
GATES = [
    "g_src",
    "g_tr",
    "g_norm",
    "g_ctrl",
    "g_leak",
    "g_dim",
    "g_proj",
]


GATE_ROWS = [
    {
        "channel_id": "distance_homogeneous_tau_shell",
        "source_role": "negative_current_proxy",
        "g_src": "0.80",
        "g_tr": "0.80",
        "g_norm": "0.80",
        "g_ctrl": "0.00",
        "g_leak": "1.00",
        "g_dim": "0.90",
        "g_proj": "0.40",
        "hard_blocker_status": "model_selection_negative_current_proxy",
        "positive_support_allowed": "false",
        "kernel_role": "negative_proxy_control",
        "rationale": "Pantheon homogeneous shell is full-covariance operational but AIC-negative; it is not positive joint support.",
    },
    {
        "channel_id": "kids_lensing_cosebis_low_mode",
        "source_role": "positive_caveated_signal",
        "g_src": "0.90",
        "g_tr": "0.75",
        "g_norm": "0.70",
        "g_ctrl": "0.70",
        "g_leak": "0.75",
        "g_dim": "0.60",
        "g_proj": "0.85",
        "hard_blocker_status": "operator_derivation_open_but_endpoint_source_frozen",
        "positive_support_allowed": "true",
        "kernel_role": "positive_support",
        "rationale": "KiDS/COSEBIs has the strongest structured low-tail endpoint signal but remains caveated by tomographic and operator-level blockers.",
    },
    {
        "channel_id": "observer_path_basis_low_z",
        "source_role": "positive_narrow_permission_only",
        "g_src": "0.70",
        "g_tr": "0.70",
        "g_norm": "0.70",
        "g_ctrl": "0.65",
        "g_leak": "0.85",
        "g_dim": "0.60",
        "g_proj": "0.90",
        "hard_blocker_status": "narrow_scope_not_population_validation",
        "positive_support_allowed": "true",
        "kernel_role": "positive_support",
        "rationale": "The narrow observer/path basis survives local controls but is only a 12-object permission replay.",
    },
    {
        "channel_id": "desi_shape_time_readout",
        "source_role": "positive_narrow_permission_only",
        "g_src": "0.75",
        "g_tr": "0.65",
        "g_norm": "0.65",
        "g_ctrl": "0.60",
        "g_leak": "0.85",
        "g_dim": "0.65",
        "g_proj": "0.75",
        "hard_blocker_status": "row_sensitive_small_margin",
        "positive_support_allowed": "true",
        "kernel_role": "positive_support",
        "rationale": "DESI shape/readout survives frozen controls with a small, row-sensitive margin.",
    },
    {
        "channel_id": "time_uncertainty_basis",
        "source_role": "control_failure_diagnostic",
        "g_src": "0.65",
        "g_tr": "0.55",
        "g_norm": "0.70",
        "g_ctrl": "0.00",
        "g_leak": "0.85",
        "g_dim": "0.70",
        "g_proj": "0.45",
        "hard_blocker_status": "fails_controls_as_time_proxy",
        "positive_support_allowed": "false",
        "kernel_role": "diagnostic_only",
        "rationale": "The CC-uncertainty time basis improves baseline but fails controls, so it cannot receive positive joint support.",
    },
    {
        "channel_id": "void_web_proxy_distance",
        "source_role": "negative_current_proxy",
        "g_src": "0.75",
        "g_tr": "0.55",
        "g_norm": "0.60",
        "g_ctrl": "0.00",
        "g_leak": "0.85",
        "g_dim": "0.75",
        "g_proj": "0.65",
        "hard_blocker_status": "source_native_void_web_not_control_surviving",
        "positive_support_allowed": "false",
        "kernel_role": "negative_proxy_control",
        "rationale": "Current void/web proxy is model-selection negative or control-limited; source-native replacement remains future work.",
    },
    {
        "channel_id": "observer_orientation_sky_z_control_negative",
        "source_role": "useful_control_negative",
        "g_src": "0.70",
        "g_tr": "0.65",
        "g_norm": "0.70",
        "g_ctrl": "0.00",
        "g_leak": "0.85",
        "g_dim": "0.60",
        "g_proj": "0.70",
        "hard_blocker_status": "one_control_beats_candidate",
        "positive_support_allowed": "false",
        "kernel_role": "diagnostic_control",
        "rationale": "Centered sky-z is retained as an observer/path control-negative variant.",
    },
    {
        "channel_id": "act_kpath_lensing_path",
        "source_role": "control_dominated_guarded_replay",
        "g_src": "0.80",
        "g_tr": "0.65",
        "g_norm": "0.55",
        "g_ctrl": "0.00",
        "g_leak": "0.85",
        "g_dim": "0.30",
        "g_proj": "0.70",
        "hard_blocker_status": "curl_null_best_control_physical_units_open",
        "positive_support_allowed": "false",
        "kernel_role": "k_null_diagnostic",
        "rationale": "The latest ACT caveated K_path replay is control-dominated, so ACT is not positive joint-kernel support.",
    },
]


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def quality(row: dict[str, str]) -> float:
    if row["positive_support_allowed"] != "true":
        return 0.0
    vals = [float(row[key]) for key in GATES]
    if min(vals) <= 0.0:
        return 0.0
    return math.prod(vals) ** (1.0 / len(vals))


def main() -> None:
    score_rows = {row["channel_id"]: row for row in read_rows(INPUT)}
    manifest_rows = []
    q_by_channel: dict[str, float] = {}
    for row in GATE_ROWS:
        q = quality(row)
        q_by_channel[row["channel_id"]] = q
        manifest_rows.append(
            {
                **row,
                "Q_i": f"{q:.9f}",
                "alpha_rule": "equal_geometric_1_over_7",
                "forbidden_endpoint_fields": "endpoint_residuals;fit_improvements;posterior_chains;post_score_control_ranks",
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    q_sum = sum(q_by_channel.values())
    if q_sum <= 0.0:
        raise SystemExit("no positive-support channels available for best-justified kernel")

    out_rows = []
    active_rows = []
    for row in manifest_rows:
        channel = row["channel_id"]
        bounded_score = float(score_rows[channel]["bounded_channel_score"]) if channel in score_rows else 0.0
        weight = q_by_channel[channel] / q_sum if q_by_channel[channel] > 0 else 0.0
        weighted = weight * bounded_score
        out = {
            "run_id": "JOINT_BEST_JUSTIFIED_KERNEL_SCORE_V1",
            "channel_id": channel,
            "kernel_role": row["kernel_role"],
            "bounded_channel_score": f"{bounded_score:.9f}",
            "Q_i": row["Q_i"],
            "w_i": f"{weight:.9f}",
            "weighted_channel_score": f"{weighted:.9f}",
            "included_in_best_justified_kernel": str(weight > 0).lower(),
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        out_rows.append(out)
        if weight > 0:
            active_rows.append(out)

    obs_score = sum(float(row["weighted_channel_score"]) for row in active_rows)
    weights = [float(row["w_i"]) for row in active_rows]
    sigma = math.sqrt(sum(w * w for w in weights))
    normalized = obs_score / sigma if sigma else 0.0

    controls = []
    values = [float(row["weighted_channel_score"]) for row in active_rows]
    for idx, signs in enumerate(itertools.product([-1, 1], repeat=len(values))):
        s = sum(sign * value for sign, value in zip(signs, values, strict=True))
        norm = s / sigma if sigma else 0.0
        controls.append(
            {
                "control_id": f"exact_sign_flip_{idx:03d}",
                "control_family": "exact_sign_flip_active_best_justified_channels",
                "seed": "deterministic_complete_enumeration",
                "control_score": f"{norm:.9f}",
                "beats_observed": str(norm >= normalized).lower(),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    rng = random.Random(SEED)
    active_scores = [float(row["bounded_channel_score"]) for row in active_rows]
    for idx in range(1000):
        shuffled = weights[:]
        rng.shuffle(shuffled)
        s = sum(w * score for w, score in zip(shuffled, active_scores, strict=True))
        sh_sigma = math.sqrt(sum(w * w for w in shuffled))
        norm = s / sh_sigma if sh_sigma else 0.0
        controls.append(
            {
                "control_id": f"seeded_weight_shuffle_{idx:04d}",
                "control_family": "seeded_best_justified_weight_shuffle",
                "seed": str(SEED),
                "control_score": f"{norm:.9f}",
                "beats_observed": str(norm >= normalized).lower(),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    loo_rows = []
    for drop in active_rows:
        subset = [row for row in active_rows if row["channel_id"] != drop["channel_id"]]
        raw = sum(float(row["weighted_channel_score"]) for row in subset)
        sub_weights = [float(row["w_i"]) for row in subset]
        sub_sigma = math.sqrt(sum(w * w for w in sub_weights))
        norm = raw / sub_sigma if sub_sigma else 0.0
        loo_rows.append(
            {
                "run_id": "JOINT_BEST_JUSTIFIED_KERNEL_SCORE_V1",
                "dropped_channel_id": drop["channel_id"],
                "leave_one_weighted_sum": f"{raw:.9f}",
                "leave_one_normalized_score": f"{norm:.9f}",
                "retains_positive_score": str(raw > 0).lower(),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    p_all = sum(1 for row in controls if row["beats_observed"] == "true") / len(controls)
    p_sign = sum(
        1
        for row in controls
        if row["control_family"] == "exact_sign_flip_active_best_justified_channels"
        and row["beats_observed"] == "true"
    ) / (2 ** len(active_rows))
    loo_positive = sum(1 for row in loo_rows if row["retains_positive_score"] == "true")
    if normalized > 0 and p_sign < 0.25 and loo_positive == len(loo_rows):
        verdict = "BEST_JUSTIFIED_JOINT_KERNEL_POSITIVE_PREFLIGHT_NOT_VALIDATION"
    else:
        verdict = "BEST_JUSTIFIED_JOINT_KERNEL_INCONCLUSIVE_PREFLIGHT_NOT_VALIDATION"

    summary = {
        "run_id": "JOINT_BEST_JUSTIFIED_KERNEL_SCORE_V1",
        "manifest_rows": str(len(manifest_rows)),
        "positive_support_channels": str(len(active_rows)),
        "positive_support_channel_order": ";".join(row["channel_id"] for row in active_rows),
        "weighted_sum": f"{obs_score:.9f}",
        "normalized_score": f"{normalized:.9f}",
        "exact_sign_flip_control_count": str(2 ** len(active_rows)),
        "exact_sign_flip_one_sided_p_ge_observed": f"{p_sign:.9f}",
        "combined_control_count": str(len(controls)),
        "combined_control_one_sided_p_ge_observed": f"{p_all:.9f}",
        "leave_one_positive_count": str(loo_positive),
        "leave_one_total_count": str(len(loo_rows)),
        "verdict": verdict,
        "joint_likelihood_claimed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "next_required_gate": "validation_grade_joint_likelihood_with_covariance_and_source_native_Q_i_review",
        "claim_boundary": CLAIM_BOUNDARY,
    }

    write_csv(MANIFEST, manifest_rows)
    write_csv(OUT, out_rows)
    write_csv(CONTROLS, controls)
    write_csv(LOO, loo_rows)
    write_csv(SUMMARY, [summary])

    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Joint best-justified kernel score v1",
                "",
                "**Doc class:** source-side weighted joint-kernel preflight",
                "**Status:** not a joint likelihood; not endpoint validation",
                "",
                "This artifact implements the admissible joint-kernel rule from the paper:",
                "",
                "```text",
                "Q_i = product_a (g_i^a)^(1/7)",
                "w_i = Q_i / sum_j Q_j",
                "K_joint = sum_i w_i K_i",
                "```",
                "",
                "Only channels with `positive_support_allowed=true` and nonzero hard-gate",
                "support receive positive joint weight. Control-dominated or source-incomplete",
                "branches remain diagnostic/control rows.",
                "",
                "Summary:",
                "",
                f"- positive-support channels: `{summary['positive_support_channels']}`",
                f"- channel order: `{summary['positive_support_channel_order']}`",
                f"- weighted sum: `{summary['weighted_sum']}`",
                f"- normalized score: `{summary['normalized_score']}`",
                f"- exact sign-flip p(score >= observed): `{summary['exact_sign_flip_one_sided_p_ge_observed']}`",
                f"- combined-control p(score >= observed): `{summary['combined_control_one_sided_p_ge_observed']}`",
                f"- leave-one positive: `{summary['leave_one_positive_count']}/{summary['leave_one_total_count']}`",
                f"- verdict: `{summary['verdict']}`",
                "",
                "Claim boundary:",
                "",
                "```text",
                CLAIM_BOUNDARY,
                "```",
                "",
            ]
        )
    )

    print(
        "JOINT_BEST_JUSTIFIED_KERNEL_SCORE_V1_RUN "
        f"normalized_score={summary['normalized_score']} "
        f"p_sign={summary['exact_sign_flip_one_sided_p_ge_observed']} "
        f"verdict={verdict}"
    )


if __name__ == "__main__":
    main()
