#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_existing_artifact_meta_score_v1.csv"
SUMMARY = ROOT / "data/derived/joint_existing_artifact_meta_score_v1_summary.csv"
DOC = ROOT / "docs/joint_existing_artifact_meta_score_v1.md"
CLAIM_BOUNDARY = "joint_existing_artifact_meta_score_prevalidation_not_cosmological_validation"


def read_one(path: Path) -> dict[str, str]:
    if not path.exists():
        raise SystemExit(f"missing required input: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def boolish(value: str) -> bool:
    return value.strip().lower() == "true"


def channel_row(
    *,
    channel_id: str,
    artifact: str,
    evidence_class: str,
    meta_weight: float,
    sign: str,
    primary_metric: str,
    metric_value: str,
    control_status: str,
    covariance_status: str,
    independence_status: str,
    interpretation: str,
) -> dict[str, str]:
    return {
        "meta_score_id": "JOINT_EXISTING_ARTIFACT_META_SCORE_V1",
        "channel_id": channel_id,
        "source_artifact": artifact,
        "evidence_class": evidence_class,
        "meta_weight": f"{meta_weight:.3f}",
        "sign": sign,
        "primary_metric": primary_metric,
        "metric_value": metric_value,
        "control_status": control_status,
        "covariance_status": covariance_status,
        "independence_status": independence_status,
        "claim_safe_interpretation": interpretation,
        "endpoint_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "dark_sector_verdict_allowed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def main() -> None:
    pantheon = read_one(ROOT / "data/derived/pantheon_full_cov_pilot_scoring_v1_summary.csv")
    kids = read_one(ROOT / "data/derived/kids1000_cosebis_authorized_endpoint_replay_v1_summary.csv")
    observer = read_one(
        ROOT / "data/derived/void_source_basis_refinement_v2_observer_basis_authorized_replay_v1_summary.csv"
    )
    desi_shape = read_one(
        ROOT / "data/derived/paper10_desi_shape_validation_permission_authorized_replay_v1_summary.csv"
    )
    w_time = read_one(ROOT / "data/derived/low_z_pantheon_w_time_uncertainty_basis_authorized_replay_v1_summary.csv")
    void_web = read_one(ROOT / "data/derived/pantheon_void_web_proxy_full_cov_pilot_v1_summary.csv")
    observer_orientation = read_one(
        ROOT / "data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2_authorized_replay_summary.csv"
    )

    rows: list[dict[str, str]] = []

    rows.append(
        channel_row(
            channel_id="distance_homogeneous_tau_shell",
            artifact="data/derived/pantheon_full_cov_pilot_scoring_v1_summary.csv",
            evidence_class="weak_negative_model_selection",
            meta_weight=-0.5,
            sign="negative_against_minimal_proxy",
            primary_metric="delta_aic_tau_minus_baseline",
            metric_value=pantheon["delta_aic_tau_minus_baseline"],
            control_status="wrong_and_shuffled_controls_present",
            covariance_status="full_covariance",
            independence_status="single_probe_distance_only",
            interpretation=(
                "Minimal homogeneous W_tau(a) slightly improves chi-square but loses under AIC; "
                "this is evidence against the minimal proxy, not against the multi-channel framework."
            ),
        )
    )

    rows.append(
        channel_row(
            channel_id="kids_lensing_cosebis_low_mode",
            artifact="data/derived/kids1000_cosebis_authorized_endpoint_replay_v1_summary.csv",
            evidence_class="low_tail_endpoint_signal_not_validation",
            meta_weight=1.5,
            sign="positive_caveated",
            primary_metric="plus_one_tail_fraction_chi2",
            metric_value=kids["plus_one_tail_fraction_chi2"],
            control_status="low_tail_but_not_absolute_control_winner",
            covariance_status="endpoint_specific_covariance",
            independence_status="separate_lensing_probe",
            interpretation=(
                "KiDS COSEBIs gives a structured low-tail endpoint signal, while validation remains blocked "
                "by tomographic and physical-promotion caveats."
            ),
        )
    )

    rows.append(
        channel_row(
            channel_id="observer_path_basis_low_z",
            artifact="data/derived/void_source_basis_refinement_v2_observer_basis_authorized_replay_v1_summary.csv",
            evidence_class="control_surviving_permission_only_replay",
            meta_weight=1.0,
            sign="positive_narrow",
            primary_metric="delta_chi2_candidate_minus_best_control",
            metric_value=observer["delta_chi2_candidate_minus_best_control"],
            control_status="survives_frozen_local_controls",
            covariance_status="low_z_permission_replay",
            independence_status="observer_path_channel",
            interpretation=(
                "The restricted observer/path basis survives its immediate controls, but remains a narrow "
                "permission-only diagnostic rather than population validation."
            ),
        )
    )

    rows.append(
        channel_row(
            channel_id="desi_shape_time_readout",
            artifact="data/derived/paper10_desi_shape_validation_permission_authorized_replay_v1_summary.csv",
            evidence_class="positive_but_very_narrow_permission_only_replay",
            meta_weight=1.0,
            sign="positive_narrow",
            primary_metric="delta_candidate_minus_best_control_score",
            metric_value=desi_shape["delta_candidate_minus_best_control_score"],
            control_status="exceeds_all_frozen_controls_but_row_sensitive",
            covariance_status="desi_shape_route_permission_only",
            independence_status="desi_shape_time_readout_channel",
            interpretation=(
                "DESI shape/time-readout is positive against frozen controls, but the margin is very small "
                "and row-sensitive."
            ),
        )
    )

    rows.append(
        channel_row(
            channel_id="time_uncertainty_basis",
            artifact="data/derived/low_z_pantheon_w_time_uncertainty_basis_authorized_replay_v1_summary.csv",
            evidence_class="control_failure_diagnostic",
            meta_weight=0.0,
            sign="neutral_diagnostic",
            primary_metric="controls_better_than_candidate_chi2",
            metric_value=w_time["controls_better_than_candidate_chi2"],
            control_status="not_control_resistant",
            covariance_status="low_z_permission_replay",
            independence_status="time_readout_proxy_only",
            interpretation=(
                "The narrow W_time uncertainty basis improves the baseline but fails controls; this is a "
                "route diagnostic, not positive evidence."
            ),
        )
    )

    rows.append(
        channel_row(
            channel_id="void_web_proxy_distance",
            artifact="data/derived/pantheon_void_web_proxy_full_cov_pilot_v1_summary.csv",
            evidence_class="weak_negative_current_proxy",
            meta_weight=-0.5,
            sign="negative_against_current_proxy",
            primary_metric="delta_aic_void_web_minus_baseline",
            metric_value=void_web["delta_aic_void_web_minus_baseline"],
            control_status="wrong_or_shuffled_controls_can_match_or_beat",
            covariance_status="full_covariance_distance_only",
            independence_status="proxy_basis_not_source_native",
            interpretation=(
                "The current redshift/scale-factor void-web proxy is model-selection negative; it argues "
                "for source-native void/web observables before validation."
            ),
        )
    )

    rows.append(
        channel_row(
            channel_id="observer_orientation_sky_z_control_negative",
            artifact="data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2_authorized_replay_summary.csv",
            evidence_class="useful_control_negative",
            meta_weight=0.0,
            sign="neutral_constraint",
            primary_metric="controls_better_than_candidate_chi2",
            metric_value=observer_orientation["controls_better_than_candidate_chi2"],
            control_status="one_control_beats_candidate",
            covariance_status="low_z_permission_replay",
            independence_status="observer_orientation_variant",
            interpretation=(
                "The centered sky-z observer variant improves the baseline but fails control resistance; "
                "it constrains rather than validates the observer/path channel."
            ),
        )
    )

    positive_weight = sum(float(r["meta_weight"]) for r in rows if float(r["meta_weight"]) > 0)
    negative_weight = sum(float(r["meta_weight"]) for r in rows if float(r["meta_weight"]) < 0)
    net_weight = positive_weight + negative_weight
    positive_rows = sum(1 for r in rows if float(r["meta_weight"]) > 0)
    negative_rows = sum(1 for r in rows if float(r["meta_weight"]) < 0)
    neutral_rows = len(rows) - positive_rows - negative_rows

    if net_weight > 1.0 and positive_rows >= 3 and negative_rows >= 1:
        verdict = "MULTI_CHANNEL_VIABILITY_PATTERN_PRESENT_NOT_VALIDATION"
    else:
        verdict = "MULTI_CHANNEL_META_SCORE_INCONCLUSIVE_NOT_VALIDATION"

    summary = {
        "meta_score_id": "JOINT_EXISTING_ARTIFACT_META_SCORE_V1",
        "channels_audited": str(len(rows)),
        "positive_caveated_channels": str(positive_rows),
        "neutral_or_control_negative_channels": str(neutral_rows),
        "negative_proxy_channels": str(negative_rows),
        "positive_meta_weight": f"{positive_weight:.3f}",
        "negative_meta_weight": f"{negative_weight:.3f}",
        "net_meta_weight": f"{net_weight:.3f}",
        "verdict": verdict,
        "joint_endpoint_claimed": "false",
        "endpoint_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "dark_sector_verdict_allowed": "false",
        "next_required_gate": "predeclared_joint_multichannel_endpoint_with_covariance_and_shuffled_channel_controls",
        "claim_boundary": CLAIM_BOUNDARY,
    }

    write_csv(OUT, rows)
    write_csv(SUMMARY, [summary])

    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Joint existing-artifact meta-score v1",
                "",
                "**Doc class:** cross-channel coherence audit",
                "**Reader role:** reviewer / paper reader",
                "**Status:** pre-validation meta-score; not a joint endpoint; not cosmological validation",
                "**Canonical parent:** Paper10 conclusion",
                "",
                "This audit combines already frozen Paper10 summary artifacts into a",
                "claim-safe cross-channel ledger.  It does not recompute likelihoods,",
                "does not fit a new parameter, and does not use endpoint residuals beyond",
                "the already recorded branch summaries.",
                "",
                "The meta weights are protocol labels, not physical likelihood weights:",
                "",
                "- `+1.5`: structured low-tail endpoint signal, still caveated.",
                "- `+1.0`: positive but narrow permission-only replay.",
                "- `0.0`: diagnostic control failure or neutral constraint.",
                "- `-0.5`: negative result against the current proxy, not against the broader framework.",
                "",
                f"Verdict: `{verdict}`",
                "",
                "Summary:",
                "",
                f"- channels audited: `{summary['channels_audited']}`",
                f"- positive caveated channels: `{summary['positive_caveated_channels']}`",
                f"- neutral/control-negative channels: `{summary['neutral_or_control_negative_channels']}`",
                f"- negative proxy channels: `{summary['negative_proxy_channels']}`",
                f"- net meta weight: `{summary['net_meta_weight']}`",
                "",
                "Claim boundary:",
                "",
                "```text",
                CLAIM_BOUNDARY,
                "```",
                "",
                "The allowed interpretation is multi-channel viability evidence.  The",
                "forbidden interpretation is empirical validation of Tau Core cosmology,",
                "dark energy, or a dark-sector response layer.",
                "",
            ]
        )
    )

    print(
        "JOINT_EXISTING_ARTIFACT_META_SCORE_V1_BUILT "
        f"channels={summary['channels_audited']} net_meta_weight={summary['net_meta_weight']} "
        f"verdict={verdict}"
    )


if __name__ == "__main__":
    main()
