#!/usr/bin/env python3
from __future__ import annotations

import os
import csv
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper10_submission_source" / "main.tex"


def run(cmd: list[str], cwd: Path = ROOT) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, cwd=cwd, check=True)


def read_one_csv(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise RuntimeError(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def main() -> None:
    env = os.environ.copy()
    env.setdefault("SOURCE_DATE_EPOCH", "1780876800")
    run(["python", "scripts/validate_source_freeze.py"])
    run(["python", "scripts/validate_cosmology_channel_manifest_v1.py"])
    run(["python", "scripts/validate_cosmology_activation_rule_manifest_v1.py"])
    run(["python", "scripts/validate_cosmology_activation_parameter_freeze_plan_v1.py"])
    run(["python", "scripts/validate_cosmology_source_grounding_gate_v1.py"])
    run(["python", "scripts/validate_cosmology_flrw_consistency_channel_audit_v1.py"])
    run(["python", "scripts/validate_cached_source_pages.py"])
    run(["python", "scripts/validate_product_freeze_plan.py"])
    run(["python", "scripts/validate_void_web_source_native_freeze_plan_v1.py"])
    run(["python", "scripts/validate_void_web_source_native_products_v1.py"])
    run(["python", "scripts/build_void_web_source_native_inventory_v1.py"])
    run(["python", "scripts/validate_void_web_source_native_inventory_v1.py"])
    run(["python", "scripts/validate_pilot_products.py"])
    run(["python", "scripts/build_pantheon_scope_v1.py"])
    run(["python", "scripts/validate_pantheon_scope_v1.py"])
    run(["python", "scripts/validate_pantheon_scoring_protocol_v1.py"])
    run(["python", "scripts/build_pantheon_design_matrix_v1.py"])
    run(["python", "scripts/validate_pantheon_design_matrix_v1.py"])
    run(["python", "scripts/run_pantheon_pilot_scoring_v1.py"])
    run(["python", "scripts/validate_pantheon_pilot_scoring_v1.py"])
    run(["python", "scripts/run_pantheon_full_cov_pilot_scoring_v1.py"])
    run(["python", "scripts/validate_pantheon_full_cov_pilot_scoring_v1.py"])
    run(["python", "scripts/run_pantheon_void_web_proxy_full_cov_pilot_v1.py"])
    run(["python", "scripts/validate_pantheon_void_web_proxy_full_cov_pilot_v1.py"])
    run(["python", "scripts/build_pantheon_void_web_source_native_design_matrix_v1.py"])
    run(["python", "scripts/validate_pantheon_void_web_source_native_design_matrix_v1.py"])
    run(["python", "scripts/run_pantheon_void_web_source_native_full_cov_pilot_v1.py"])
    run(["python", "scripts/validate_pantheon_void_web_source_native_full_cov_pilot_v1.py"])
    run(["python", "scripts/validate_sdss_final_bao_rsd_growth_summary_v1.py"])
    run(["python", "scripts/build_growth_web_source_native_design_matrix_v1.py"])
    run(["python", "scripts/validate_growth_web_source_native_design_matrix_v1.py"])
    run(["python", "scripts/run_growth_web_source_native_pilot_v1.py"])
    run(["python", "scripts/validate_growth_web_source_native_pilot_v1.py"])
    run(["python", "scripts/validate_sdss_multitracer_bao_rsd_products_v1.py"])
    run(["python", "scripts/build_sdss_multitracer_bao_rsd_design_matrix_v1.py"])
    run(["python", "scripts/validate_sdss_multitracer_bao_rsd_design_matrix_v1.py"])
    run(["python", "scripts/run_sdss_multitracer_bao_rsd_full_cov_pilot_v1.py"])
    run(["python", "scripts/validate_sdss_multitracer_bao_rsd_full_cov_pilot_v1.py"])
    run(["python", "scripts/build_cmb_safety_lowz_support_v1.py"])
    run(["python", "scripts/validate_cmb_safety_lowz_support_v1.py"])
    run(["python", "scripts/build_void_web_endpoint_readiness_after_flrw_audit_v1.py"])
    run(["python", "scripts/validate_void_web_endpoint_readiness_after_flrw_audit_v1.py"])
    run(["python", "scripts/validate_void_web_combined_multiblock_endpoint_protocol_v1.py"])
    run(["python", "scripts/build_void_web_combined_multiblock_endpoint_authorization_review_template_v1.py"])
    run(["python", "scripts/validate_void_web_combined_multiblock_endpoint_authorization_review_template_v1.py"])
    run(["python", "scripts/build_void_web_combined_multiblock_endpoint_authorization_review_package_v1.py"])
    run(["python", "scripts/validate_void_web_combined_multiblock_endpoint_authorization_review_package_v1.py"])
    run(["python", "scripts/validate_void_web_combined_multiblock_endpoint_authorization_review_response_v1.py"])
    run(["python", "scripts/run_void_web_combined_multiblock_authorized_endpoint_v1.py"])
    run(["python", "scripts/validate_void_web_combined_multiblock_authorized_endpoint_v1.py"])
    run(["python", "scripts/build_void_web_combined_endpoint_diagnostics_v1.py"])
    run(["python", "scripts/validate_void_web_combined_endpoint_diagnostics_v1.py"])
    run(["python", "scripts/build_void_channel_inactivity_diagnostic_v1.py"])
    run(["python", "scripts/validate_void_channel_inactivity_diagnostic_v1.py"])
    run(["python", "scripts/build_void_source_basis_audit_v1.py"])
    run(["python", "scripts/validate_void_source_basis_audit_v1.py"])
    run(["python", "scripts/build_void_channel_remediation_gate_v1.py"])
    run(["python", "scripts/validate_void_channel_remediation_gate_v1.py"])
    run(["python", "scripts/build_low_z_pantheon_void_scope_candidate_v1.py"])
    run(["python", "scripts/validate_low_z_pantheon_void_scope_candidate_v1.py"])
    run(["python", "scripts/build_low_z_pantheon_void_scope_replay_authorization_review_template_v1.py"])
    run(["python", "scripts/validate_low_z_pantheon_void_scope_replay_authorization_review_template_v1.py"])
    run(["python", "scripts/build_low_z_pantheon_void_scope_replay_authorization_review_package_v1.py"])
    run(["python", "scripts/validate_low_z_pantheon_void_scope_replay_authorization_review_package_v1.py"])
    response = ROOT / "data" / "derived" / "low_z_pantheon_void_scope_replay_authorization_review_response_v1.csv"
    if response.exists():
        run(["python", "scripts/validate_low_z_pantheon_void_scope_replay_authorization_review_response_v1.py", str(response)])
    run(["python", "scripts/validate_low_z_pantheon_void_replay_protocol_v1.py"])
    if response.exists():
        run(["python", "scripts/run_low_z_pantheon_void_replay_v1.py"])
        run(["python", "scripts/validate_low_z_pantheon_void_replay_v1.py"])
        run(["python", "scripts/build_low_z_void_replay_diagnostics_v1.py"])
        run(["python", "scripts/validate_low_z_void_replay_diagnostics_v1.py"])
        run(["python", "scripts/build_void_source_basis_refinement_gate_v1.py"])
        run(["python", "scripts/validate_void_source_basis_refinement_gate_v1.py"])
        run(["python", "scripts/build_void_source_basis_refinement_acquisition_manifest_v1.py"])
        run(["python", "scripts/validate_void_source_basis_refinement_acquisition_manifest_v1.py"])
        run(["python", "scripts/build_void_source_basis_refinement_r1_r3_source_attachment_v1.py"])
        run(["python", "scripts/validate_void_source_basis_refinement_r1_r3_source_attachment_v1.py"])
        run(["python", "scripts/build_void_source_basis_refinement_r4_independence_preflight_v1.py"])
        run(["python", "scripts/validate_void_source_basis_refinement_r4_independence_preflight_v1.py"])
        run(["python", "scripts/build_void_source_basis_refinement_r5_control_resistance_preflight_v1.py"])
        run(["python", "scripts/validate_void_source_basis_refinement_r5_control_resistance_preflight_v1.py"])
        run(["python", "scripts/build_void_source_basis_refinement_r6_reviewer_template_v1.py"])
        run(["python", "scripts/validate_void_source_basis_refinement_r6_reviewer_template_v1.py"])
        run(["python", "scripts/build_void_source_basis_refinement_r6_reviewer_handoff_package_v1.py"])
        run(["python", "scripts/validate_void_source_basis_refinement_r6_reviewer_handoff_package_v1.py"])
        r6_response = ROOT / "data" / "derived" / "void_source_basis_refinement_r6_completed_reviewer_response_v1.csv"
        if r6_response.exists():
            run(
                [
                    "python",
                    "scripts/validate_void_source_basis_refinement_r6_completed_reviewer_response_v1.py",
                    str(r6_response),
                    "--summary-out",
                    "data/derived/void_source_basis_refinement_r6_completed_reviewer_response_v1_summary.csv",
                ]
            )
            run(["python", "scripts/build_void_source_basis_refinement_endpoint_replay_authorization_review_template_v1.py"])
            run(["python", "scripts/validate_void_source_basis_refinement_endpoint_replay_authorization_review_template_v1.py"])
            run(["python", "scripts/build_void_source_basis_refinement_endpoint_replay_authorization_review_package_v1.py"])
            run(["python", "scripts/validate_void_source_basis_refinement_endpoint_replay_authorization_review_package_v1.py"])
            refined_auth_response = (
                ROOT
                / "data"
                / "derived"
                / "void_source_basis_refinement_endpoint_replay_authorization_review_response_v1.csv"
            )
            if refined_auth_response.exists():
                run(
                    [
                        "python",
                        "scripts/validate_void_source_basis_refinement_endpoint_replay_authorization_review_response_v1.py",
                        str(refined_auth_response),
                        "--summary-out",
                        "data/derived/void_source_basis_refinement_endpoint_replay_authorization_review_response_v1_summary.csv",
                    ]
                )
                run(["python", "scripts/run_void_source_basis_refinement_authorized_replay_v1.py"])
                run(["python", "scripts/validate_void_source_basis_refinement_authorized_replay_v1.py"])
                run(["python", "scripts/build_void_source_basis_refinement_control_dominance_audit_v1.py"])
                run(["python", "scripts/validate_void_source_basis_refinement_control_dominance_audit_v1.py"])
                run(["python", "scripts/build_void_source_basis_refinement_v2_void_morphology_values_v1.py"])
                run(["python", "scripts/validate_void_source_basis_refinement_v2_void_morphology_values_v1.py"])
                run(["python", "scripts/build_void_source_basis_refinement_v2_web_morphology_values_v1.py"])
                run(["python", "scripts/validate_void_source_basis_refinement_v2_web_morphology_values_v1.py"])
                run(["python", "scripts/build_void_source_basis_refinement_v2_cmb_safety_values_v1.py"])
                run(["python", "scripts/validate_void_source_basis_refinement_v2_cmb_safety_values_v1.py"])
                run(["python", "scripts/build_void_source_basis_refinement_v2_path_projection_crossmap_audit_v1.py"])
                run(["python", "scripts/validate_void_source_basis_refinement_v2_path_projection_crossmap_audit_v1.py"])
                run(["python", "scripts/build_void_source_basis_refinement_v2_path_partial_scope_policy_v1.py"])
                run(["python", "scripts/validate_void_source_basis_refinement_v2_path_partial_scope_policy_v1.py"])
                run(["python", "scripts/build_void_source_basis_refinement_v2_path_partial_scope_values_v1.py"])
                run(["python", "scripts/validate_void_source_basis_refinement_v2_path_partial_scope_values_v1.py"])
                run(
                    [
                        "python",
                        "scripts/build_void_source_basis_refinement_v2_path_partial_scope_reviewer_package_v1.py",
                    ]
                )
                run(
                    [
                        "python",
                        "scripts/validate_void_source_basis_refinement_v2_path_partial_scope_reviewer_package_v1.py",
                    ]
                )
                completed_path_review = (
                    ROOT
                    / "data"
                    / "derived"
                    / "void_source_basis_refinement_v2_path_partial_scope_completed_review_response_v1.csv"
                )
                if completed_path_review.exists():
                    run(
                        [
                            "python",
                            "scripts/validate_void_source_basis_refinement_v2_path_partial_scope_completed_review_response_v1.py",
                        ]
                    )
                    run(
                        [
                            "python",
                            "scripts/build_void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_template_v1.py",
                        ]
                    )
                    run(
                        [
                            "python",
                            "scripts/validate_void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_template_v1.py",
                        ]
                    )
                    run(
                        [
                            "python",
                            "scripts/build_void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_package_v1.py",
                        ]
                    )
                    run(
                        [
                            "python",
                            "scripts/validate_void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_package_v1.py",
                        ]
                    )
                    partial_path_auth_response = (
                        ROOT
                        / "data"
                        / "derived"
                        / "void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_response_v1.csv"
                    )
                    if partial_path_auth_response.exists():
                        run(
                            [
                                "python",
                                "scripts/validate_void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_response_v1.py",
                            ]
                        )
                        run(
                            [
                                "python",
                                "scripts/run_void_source_basis_refinement_v2_path_partial_scope_authorized_replay_v1.py",
                            ]
                        )
                        run(
                            [
                                "python",
                                "scripts/validate_void_source_basis_refinement_v2_path_partial_scope_authorized_replay_v1.py",
                            ]
                        )
                        run(
                            [
                                "python",
                                "scripts/run_void_source_basis_refinement_v2_path_coupled_projection_screen_v1.py",
                            ]
                        )
                        run(
                            [
                                "python",
                                "scripts/validate_void_source_basis_refinement_v2_path_coupled_projection_screen_v1.py",
                            ]
                        )
                        run(
                            [
                                "python",
                                "scripts/run_void_source_basis_refinement_v2_path_transform_bank_screen_v1.py",
                            ]
                        )
                        run(
                            [
                                "python",
                                "scripts/validate_void_source_basis_refinement_v2_path_transform_bank_screen_v1.py",
                            ]
                        )
                        run(
                            [
                                "python",
                                "scripts/run_void_source_basis_refinement_v2_path_sky_environment_screen_v1.py",
                            ]
                        )
                        run(
                            [
                                "python",
                                "scripts/validate_void_source_basis_refinement_v2_path_sky_environment_screen_v1.py",
                            ]
                        )
                        run(
                            [
                                "python",
                                "scripts/build_void_source_basis_refinement_v2_observer_dependence_followup_template_v1.py",
                            ]
                        )
                        run(
                            [
                                "python",
                                "scripts/validate_void_source_basis_refinement_v2_observer_dependence_followup_template_v1.py",
                            ]
                        )
                        run(
                            [
                                "python",
                                "scripts/build_void_source_basis_refinement_v2_observer_dependence_followup_package_v1.py",
                            ]
                        )
                        run(
                            [
                                "python",
                                "scripts/validate_void_source_basis_refinement_v2_observer_dependence_followup_package_v1.py",
                            ]
                        )
                        run(
                            [
                                "python",
                                "scripts/build_void_source_basis_refinement_v2_sky_z_replay_authorization_review_template_v1.py",
                            ]
                        )
                        run(
                            [
                                "python",
                                "scripts/validate_void_source_basis_refinement_v2_sky_z_replay_authorization_review_template_v1.py",
                            ]
                        )
                        run(
                            [
                                "python",
                                "scripts/build_void_source_basis_refinement_v2_sky_z_replay_authorization_review_package_v1.py",
                            ]
                        )
                        run(
                            [
                                "python",
                                "scripts/validate_void_source_basis_refinement_v2_sky_z_replay_authorization_review_package_v1.py",
                            ]
                        )
                        sky_z_auth_response = (
                            ROOT
                            / "data"
                            / "derived"
                            / "void_source_basis_refinement_v2_sky_z_replay_authorization_review_response_v1.csv"
                        )
                        if sky_z_auth_response.exists():
                            run(
                                [
                                    "python",
                                    "scripts/validate_void_source_basis_refinement_v2_sky_z_replay_authorization_review_response_v1.py",
                                ]
                            )
                            run(["python", "scripts/run_void_source_basis_refinement_v2_sky_z_authorized_replay_v1.py"])
                            run(["python", "scripts/validate_void_source_basis_refinement_v2_sky_z_authorized_replay_v1.py"])
                            run(["python", "scripts/build_void_source_basis_refinement_v2_sky_z_source_audit_v1.py"])
                            run(["python", "scripts/validate_void_source_basis_refinement_v2_sky_z_source_audit_v1.py"])
                            run(["python", "scripts/build_void_source_basis_refinement_v2_observer_orientation_kernel_v2.py"])
                            run(["python", "scripts/validate_void_source_basis_refinement_v2_observer_orientation_kernel_v2.py"])
                            run(
                                [
                                    "python",
                                    "scripts/build_void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_template.py",
                                ]
                            )
                            run(
                                [
                                    "python",
                                    "scripts/validate_void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_template.py",
                                ]
                            )
                            run(
                                [
                                    "python",
                                    "scripts/build_void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_package.py",
                                ]
                            )
                            run(
                                [
                                    "python",
                                    "scripts/validate_void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_package.py",
                                ]
                            )
                            observer_orientation_v2_auth_response = (
                                ROOT
                                / "data"
                                / "derived"
                                / "void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_response_v1.csv"
                            )
                            if observer_orientation_v2_auth_response.exists():
                                run(
                                    [
                                        "python",
                                        "scripts/validate_void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_response.py",
                                    ]
                                )
                                run(
                                    [
                                        "python",
                                        "scripts/run_void_source_basis_refinement_v2_observer_orientation_kernel_v2_authorized_replay.py",
                                    ]
                                )
                                run(
                                    [
                                        "python",
                                        "scripts/validate_void_source_basis_refinement_v2_observer_orientation_kernel_v2_authorized_replay.py",
                                    ]
                                )
                            run(["python", "scripts/run_void_source_basis_refinement_v2_observer_basis_fast_screen_v1.py"])
                            run(["python", "scripts/validate_void_source_basis_refinement_v2_observer_basis_fast_screen_v1.py"])
                            run(
                                [
                                    "python",
                                    "scripts/build_void_source_basis_refinement_v2_observer_basis_candidate_review_package_v1.py",
                                ]
                            )
                            run(
                                [
                                    "python",
                                    "scripts/validate_void_source_basis_refinement_v2_observer_basis_candidate_review_package_v1.py",
                                ]
                            )
                            observer_basis_candidate_review_response = (
                                ROOT
                                / "data"
                                / "derived"
                                / "void_source_basis_refinement_v2_observer_basis_candidate_review_response_v1.csv"
                            )
                            if observer_basis_candidate_review_response.exists():
                                run(
                                    [
                                        "python",
                                        "scripts/validate_void_source_basis_refinement_v2_observer_basis_candidate_review_response_v1.py",
                                    ]
                                )
                                run(
                                    [
                                        "python",
                                        "scripts/build_void_source_basis_refinement_v2_observer_basis_replay_authorization_package_v1.py",
                                    ]
                                )
                                run(
                                    [
                                        "python",
                                        "scripts/validate_void_source_basis_refinement_v2_observer_basis_replay_authorization_package_v1.py",
                                    ]
                                )
                                observer_basis_replay_auth_response = (
                                    ROOT
                                    / "data"
                                    / "derived"
                                    / "void_source_basis_refinement_v2_observer_basis_replay_authorization_response_v1.csv"
                                )
                                if observer_basis_replay_auth_response.exists():
                                    run(
                                        [
                                            "python",
                                            "scripts/validate_void_source_basis_refinement_v2_observer_basis_replay_authorization_response_v1.py",
                                        ]
                                    )
                                    run(
                                        [
                                            "python",
                                            "scripts/run_void_source_basis_refinement_v2_observer_basis_authorized_replay_v1.py",
                                        ]
                                    )
                                    run(
                                        [
                                            "python",
                                            "scripts/validate_void_source_basis_refinement_v2_observer_basis_authorized_replay_v1.py",
                                        ]
                                    )
                                    run(
                                        [
                                            "python",
                                            "scripts/run_void_source_basis_refinement_v2_full_kernel_proxy_fast_screen_v1.py",
                                        ]
                                    )
                                    run(
                                        [
                                            "python",
                                            "scripts/validate_void_source_basis_refinement_v2_full_kernel_proxy_fast_screen_v1.py",
                                        ]
                                    )
                                    run(
                                        [
                                            "python",
                                            "scripts/build_void_source_basis_refinement_v2_full_kernel_proxy_component_audit_v1.py",
                                        ]
                                    )
                                    run(
                                        [
                                            "python",
                                            "scripts/validate_void_source_basis_refinement_v2_full_kernel_proxy_component_audit_v1.py",
                                        ]
                                    )
                                    run(["python", "scripts/validate_full_observer_path_kernel_source_requirements_v1.py"])
                                    run(["python", "scripts/build_low_z_pantheon_los_radial_profile_v1.py"])
                                    run(["python", "scripts/validate_low_z_pantheon_los_radial_profile_v1.py"])
                                    run(["python", "scripts/build_low_z_pantheon_path_aware_void_geometry_v1.py"])
                                    run(["python", "scripts/validate_low_z_pantheon_path_aware_void_geometry_v1.py"])
                                    run(["python", "scripts/build_low_z_pantheon_directional_web_anisotropy_v1.py"])
                                    run(["python", "scripts/validate_low_z_pantheon_directional_web_anisotropy_v1.py"])
                                    run(["python", "scripts/build_low_z_pantheon_metric_lensing_path_route_audit_v1.py"])
                                    run(["python", "scripts/validate_low_z_pantheon_metric_lensing_path_route_audit_v1.py"])
                                    run(["python", "scripts/build_low_z_pantheon_time_readout_source_audit_v1.py"])
                                    run(["python", "scripts/validate_low_z_pantheon_time_readout_source_audit_v1.py"])
                                    run(["python", "scripts/build_low_z_pantheon_time_readout_clock_scale_candidate_v1.py"])
                                    run(["python", "scripts/validate_low_z_pantheon_time_readout_clock_scale_candidate_v1.py"])
                                    run(["python", "scripts/build_low_z_pantheon_time_readout_redshift_bin_policy_candidate_v1.py"])
                                    run(["python", "scripts/validate_low_z_pantheon_time_readout_redshift_bin_policy_candidate_v1.py"])
                                    run(["python", "scripts/build_low_z_pantheon_time_readout_delta_clock_uncertainty_candidate_v1.py"])
                                    run(["python", "scripts/validate_low_z_pantheon_time_readout_delta_clock_uncertainty_candidate_v1.py"])
                                    run(["python", "scripts/build_low_z_pantheon_w_time_uncertainty_basis_candidate_v1.py"])
                                    run(["python", "scripts/validate_low_z_pantheon_w_time_uncertainty_basis_candidate_v1.py"])
                                    run(["python", "scripts/build_low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_template_v1.py"])
                                    run(["python", "scripts/validate_low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_template_v1.py"])
                                    run(["python", "scripts/build_low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_package_v1.py"])
                                    run(["python", "scripts/validate_low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_package_v1.py"])
                                    run(["python", "scripts/run_low_z_pantheon_observer_time_combined_fast_screen_v1.py"])
                                    run(["python", "scripts/validate_low_z_pantheon_observer_time_combined_fast_screen_v1.py"])
                                    run(["python", "scripts/build_low_z_pantheon_time_readout_clock_rate_phase_candidate_v1.py"])
                                    run(["python", "scripts/validate_low_z_pantheon_time_readout_clock_rate_phase_candidate_v1.py"])
                                    run(["python", "scripts/run_low_z_pantheon_clock_rate_phase_fast_screen_v1.py"])
                                    run(["python", "scripts/validate_low_z_pantheon_clock_rate_phase_fast_screen_v1.py"])
                                    run(["python", "scripts/build_low_z_pantheon_clock_rate_phase_rank_control_audit_v1.py"])
                                    run(["python", "scripts/validate_low_z_pantheon_clock_rate_phase_rank_control_audit_v1.py"])
                                    run(["python", "scripts/build_pantheon_time_readout_clock_rate_phase_cc_support_candidate_v1.py"])
                                    run(["python", "scripts/validate_pantheon_time_readout_clock_rate_phase_cc_support_candidate_v1.py"])
                                    run(["python", "scripts/run_pantheon_clock_rate_phase_cc_support_fast_screen_v1.py"])
                                    run(["python", "scripts/validate_pantheon_clock_rate_phase_cc_support_fast_screen_v1.py"])
                                    run(["python", "scripts/build_pantheon_clock_slope_route_gate_v1.py"])
                                    run(["python", "scripts/validate_pantheon_clock_slope_route_gate_v1.py"])
                                    run(["python", "scripts/build_pantheon_clock_slope_route_replay_authorization_review_template_v1.py"])
                                    run(["python", "scripts/validate_pantheon_clock_slope_route_replay_authorization_review_template_v1.py"])
                                    run(["python", "scripts/build_pantheon_clock_slope_route_replay_authorization_review_package_v1.py"])
                                    run(["python", "scripts/validate_pantheon_clock_slope_route_replay_authorization_review_package_v1.py"])
                                    run(["python", "scripts/build_sdss_bao_time_readout_observable_route_audit_v1.py"])
                                    run(["python", "scripts/validate_sdss_bao_time_readout_observable_route_audit_v1.py"])
                                    run(["python", "scripts/build_paper10_joint_cc_bao_time_route_consistency_audit_v1.py"])
                                    run(["python", "scripts/validate_paper10_joint_cc_bao_time_route_consistency_audit_v1.py"])
                                    run(["python", "scripts/build_paper10_time_readout_route_synthesis_gate_v1.py"])
                                    run(["python", "scripts/validate_paper10_time_readout_route_synthesis_gate_v1.py"])
                                    run(["python", "scripts/build_paper10_time_readout_level_slope_route_split_ledger_v1.py"])
                                    run(["python", "scripts/validate_paper10_time_readout_level_slope_route_split_ledger_v1.py"])
                                    run(["python", "scripts/validate_paper10_time_level_route_nuisance_interface_freeze_plan_v1.py"])
                                    run(["python", "scripts/build_paper10_bao_rd_cancelled_time_level_difference_audit_v1.py"])
                                    run(["python", "scripts/validate_paper10_bao_rd_cancelled_time_level_difference_audit_v1.py"])
                                    run(["python", "scripts/validate_paper10_time_level_rd_policy_selection_gate_v1.py"])
                                    run(["python", "scripts/validate_paper10_external_rd_prior_freeze_protocol_v1.py"])
                                    run(["python", "scripts/validate_paper10_external_rd_prior_freeze_response_v1.py"])
                                    run(["python", "scripts/validate_paper10_bao_rd_marginalization_protocol_v1.py"])
                                    run(["python", "scripts/validate_paper10_time_level_endpoint_control_suite_protocol_v1.py"])
                                    run(["python", "scripts/validate_paper10_time_level_bao_support_expansion_manifest_v1.py"])
                                    run(["python", "scripts/build_paper10_desi_dr2_bao_source_inventory_v1.py"])
                                    run(["python", "scripts/validate_paper10_desi_dr2_bao_source_inventory_v1.py"])
                                    run(["python", "scripts/build_paper10_desi_dr2_radial_bao_time_interface_v1.py"])
                                    run(["python", "scripts/validate_paper10_desi_dr2_radial_bao_time_interface_v1.py"])
                                    run(["python", "scripts/build_paper10_desi_dr2_radial_bao_cc_match_v1.py"])
                                    run(["python", "scripts/validate_paper10_desi_dr2_radial_bao_cc_match_v1.py"])
                                    run(["python", "scripts/validate_paper10_desi_dr2_high_z_bao_policy_v1.py"])
                                    run(["python", "scripts/validate_paper10_desi_time_level_control_seed_manifest_v1.py"])
                                    run(["python", "scripts/build_paper10_time_level_route_external_rd_readiness_gate_v1.py"])
                                    run(["python", "scripts/validate_paper10_time_level_route_external_rd_readiness_gate_v1.py"])
                                    run(
                                        [
                                            "python",
                                            "scripts/build_paper10_desi_time_level_endpoint_authorization_review_template_v1.py",
                                        ]
                                    )
                                    run(
                                        [
                                            "python",
                                            "scripts/validate_paper10_desi_time_level_endpoint_authorization_review_template_v1.py",
                                        ]
                                    )
                                    run(
                                        [
                                            "python",
                                            "scripts/build_paper10_desi_time_level_endpoint_authorization_review_package_v1.py",
                                        ]
                                    )
                                    run(
                                        [
                                            "python",
                                            "scripts/validate_paper10_desi_time_level_endpoint_authorization_review_package_v1.py",
                                        ]
                                    )
                                    desi_endpoint_auth_response = (
                                        ROOT
                                        / "data"
                                        / "derived"
                                        / "paper10_desi_time_level_endpoint_authorization_review_response_v1.csv"
                                    )
                                    if desi_endpoint_auth_response.exists():
                                        run(
                                            [
                                                "python",
                                                "scripts/validate_paper10_desi_time_level_endpoint_authorization_review_response_v1.py",
                                            ]
                                        )
                                        run(
                                            [
                                                "python",
                                                "scripts/run_paper10_desi_time_level_endpoint_authorized_replay_v1.py",
                                            ]
                                        )
                                        run(
                                            [
                                                "python",
                                                "scripts/validate_paper10_desi_time_level_endpoint_authorized_replay_v1.py",
                                            ]
                                        )
                                        run(
                                            [
                                                "python",
                                                "scripts/build_paper10_desi_time_level_negative_control_diagnostic_v1.py",
                                            ]
                                        )
                                        run(
                                            [
                                                "python",
                                                "scripts/validate_paper10_desi_time_level_negative_control_diagnostic_v1.py",
                                            ]
                                        )
                                        run(
                                            [
                                                "python",
                                                "scripts/build_paper10_desi_time_level_negative_control_response_gate_v1.py",
                                            ]
                                        )
                                        run(
                                            [
                                                "python",
                                                "scripts/validate_paper10_desi_time_level_negative_control_response_gate_v1.py",
                                            ]
                                        )
                                        run(
                                            [
                                                "python",
                                                "scripts/validate_paper10_desi_time_readout_expansion_manifest_v1.py",
                                            ]
                                        )
                                        run(
                                            [
                                                "python",
                                                "scripts/build_paper10_desi_high_z_independent_clock_support_audit_v1.py",
                                            ]
                                        )
                                        run(
                                            [
                                                "python",
                                                "scripts/validate_paper10_desi_high_z_independent_clock_support_audit_v1.py",
                                            ]
                                        )
                                        run(
                                            [
                                                "python",
                                                "scripts/build_paper10_desi_time_readout_shape_observable_gate_v1.py",
                                            ]
                                        )
                                        run(
                                            [
                                                "python",
                                                "scripts/validate_paper10_desi_time_readout_shape_observable_gate_v1.py",
                                            ]
                                        )
                                        run(
                                            [
                                                "python",
                                                "scripts/build_paper10_desi_time_readout_shape_projection_induction_v1.py",
                                            ]
                                        )
                                        run(
                                            [
                                                "python",
                                                "scripts/validate_paper10_desi_time_readout_shape_projection_induction_v1.py",
                                            ]
                                        )
                                        run(
                                            [
                                                "python",
                                                "scripts/build_paper10_desi_ordering_control_suite_v1.py",
                                            ]
                                        )
                                        run(
                                            [
                                                "python",
                                                "scripts/validate_paper10_desi_ordering_control_suite_v1.py",
                                            ]
                                        )
                                        run(
                                            [
                                                "python",
                                                "scripts/build_paper10_desi_cc_window_stress_binding_v1.py",
                                            ]
                                        )
                                        run(
                                            [
                                                "python",
                                                "scripts/validate_paper10_desi_cc_window_stress_binding_v1.py",
                                            ]
                                        )
                                        run(
                                            [
                                                "python",
                                                "scripts/build_paper10_desi_shape_bound_control_vectors_v1.py",
                                            ]
                                        )
                                        run(
                                            [
                                                "python",
                                                "scripts/validate_paper10_desi_shape_bound_control_vectors_v1.py",
                                            ]
                                        )
                                        run(
                                            [
                                                "python",
                                                "scripts/build_paper10_desi_multi_clock_support_per_bao_row_audit_v1.py",
                                            ]
                                        )
                                        run(
                                            [
                                                "python",
                                                "scripts/validate_paper10_desi_multi_clock_support_per_bao_row_audit_v1.py",
                                            ]
                                        )
                                        run(
                                            [
                                                "python",
                                                "scripts/build_paper10_desi_time_readout_shape_independent_review_package_v1.py",
                                            ]
                                        )
                                        run(
                                            [
                                                "python",
                                                "scripts/validate_paper10_desi_time_readout_shape_independent_review_package_v1.py",
                                            ]
                                        )
                                        run(
                                            [
                                                "python",
                                                "scripts/build_paper10_desi_shape_route_replay_authorization_review_package_v1.py",
                                            ]
                                        )
                                        run(
                                            [
                                                "python",
                                                "scripts/validate_paper10_desi_shape_route_replay_authorization_review_package_v1.py",
                                            ]
                                        )
                                        response = (
                                            ROOT
                                            / "data"
                                            / "derived"
                                            / "paper10_desi_shape_route_replay_authorization_review_response_v1.csv"
                                        )
                                        if response.exists():
                                            run(
                                                [
                                                    "python",
                                                    "scripts/validate_paper10_desi_shape_route_replay_authorization_review_response_v1.py",
                                                    str(response),
                                                ]
                                            )
                                        run(
                                            [
                                                "python",
                                                "scripts/validate_paper10_desi_shape_route_replay_run_template_v1.py",
                                            ]
                                        )
                                        if response.exists():
                                            run(
                                                [
                                                    "python",
                                                    "scripts/run_paper10_desi_shape_route_authorized_replay_v1.py",
                                                ]
                                            )
                                            run(
                                                [
                                                    "python",
                                                    "scripts/validate_paper10_desi_shape_route_authorized_replay_v1.py",
                                                ]
                                            )
                                            run(
                                                [
                                                    "python",
                                                    "scripts/build_paper10_desi_shape_route_robustness_stress_v1.py",
                                                ]
                                            )
                                            run(
                                                [
                                                    "python",
                                                    "scripts/validate_paper10_desi_shape_route_robustness_stress_v1.py",
                                                ]
                                            )
                                            run(
                                                [
                                                    "python",
                                                    "scripts/build_paper10_desi_shape_route_robustness_figure_v1.py",
                                                ]
                                            )
                                            run(
                                                [
                                                    "python",
                                                    "scripts/validate_paper10_desi_shape_route_robustness_figure_v1.py",
                                                ]
                                            )
                                            run(
                                                [
                                                    "python",
                                                    "scripts/build_paper10_desi_shape_row_sensitivity_source_audit_v1.py",
                                                ]
                                            )
                                            run(
                                                [
                                                    "python",
                                                    "scripts/validate_paper10_desi_shape_row_sensitivity_source_audit_v1.py",
                                                ]
                                            )
                                            run(
                                                [
                                                    "python",
                                                    "scripts/build_paper10_desi_shape_core_source_acquisition_manifest_v1.py",
                                                ]
                                            )
                                            run(
                                                [
                                                    "python",
                                                    "scripts/validate_paper10_desi_shape_core_source_acquisition_manifest_v1.py",
                                                ]
                                            )
                                            run(
                                                [
                                                    "python",
                                                    "scripts/build_paper10_desi_shape_core_source_support_scan_v1.py",
                                                ]
                                            )
                                            run(
                                                [
                                                    "python",
                                                    "scripts/validate_paper10_desi_shape_core_source_support_scan_v1.py",
                                                ]
                                            )
                                            run(
                                                [
                                                    "python",
                                                    "scripts/build_paper10_desi_shape_row1_confirmatory_source_attachment_v1.py",
                                                ]
                                            )
                                            run(
                                                [
                                                    "python",
                                                    "scripts/validate_paper10_desi_shape_row1_confirmatory_source_attachment_v1.py",
                                                ]
                                            )
                                            run(
                                                [
                                                    "python",
                                                    "scripts/build_paper10_desi_shape_row1_confirmatory_source_review_package_v1.py",
                                                ]
                                            )
                                            run(
                                                [
                                                    "python",
                                                    "scripts/validate_paper10_desi_shape_row1_confirmatory_source_review_package_v1.py",
                                                ]
                                            )
                                            row1_review_response = (
                                                ROOT
                                                / "data/derived/paper10_desi_shape_row1_confirmatory_source_review_response_v1.csv"
                                            )
                                            if row1_review_response.exists():
                                                run(
                                                    [
                                                        "python",
                                                        "scripts/validate_paper10_desi_shape_row1_confirmatory_source_review_response_v1.py",
                                                    ]
                                                )
                                            run(
                                                [
                                                    "python",
                                                    "scripts/build_paper10_desi_shape_row2_moresco2012_source_attachment_v1.py",
                                                ]
                                            )
                                            run(
                                                [
                                                    "python",
                                                    "scripts/validate_paper10_desi_shape_row2_moresco2012_source_attachment_v1.py",
                                                ]
                                            )
                                            run(
                                                [
                                                    "python",
                                                    "scripts/build_paper10_desi_shape_row2_moresco2012_source_attachment_review_package_v1.py",
                                                ]
                                            )
                                            run(
                                                [
                                                    "python",
                                                    "scripts/validate_paper10_desi_shape_row2_moresco2012_source_attachment_review_package_v1.py",
                                                ]
                                            )
                                            row2_attachment_response = (
                                                ROOT
                                                / "data"
                                                / "derived"
                                                / "paper10_desi_shape_row2_moresco2012_source_attachment_review_response_v1.csv"
                                            )
                                            if row2_attachment_response.exists():
                                                run(
                                                    [
                                                        "python",
                                                        "scripts/validate_paper10_desi_shape_row2_moresco2012_source_attachment_review_response_v1.py",
                                                    ]
                                                )
                                                run(
                                                    [
                                                        "python",
                                                        "scripts/build_paper10_desi_shape_row2_promotion_readiness_gate_v1.py",
                                                    ]
                                                )
                                                run(
                                                    [
                                                        "python",
                                                        "scripts/validate_paper10_desi_shape_row2_promotion_readiness_gate_v1.py",
                                                    ]
                                                )
                                                run(
                                                    [
                                                        "python",
                                                        "scripts/build_paper10_desi_shape_row2_endpoint_pair_independence_scout_v1.py",
                                                    ]
                                                )
                                                run(
                                                    [
                                                        "python",
                                                        "scripts/validate_paper10_desi_shape_row2_endpoint_pair_independence_scout_v1.py",
                                                    ]
                                                )
                                                run(
                                                    [
                                                        "python",
                                                        "scripts/build_paper10_desi_shape_row2_left_endpoint_nearmiss_freeze_v1.py",
                                                    ]
                                                )
                                                run(
                                                    [
                                                        "python",
                                                        "scripts/validate_paper10_desi_shape_row2_left_endpoint_nearmiss_freeze_v1.py",
                                                    ]
                                                )
                                                run(
                                                    [
                                                        "python",
                                                        "scripts/build_paper10_desi_shape_row2_left_endpoint_window_review_package_v1.py",
                                                    ]
                                                )
                                                run(
                                                    [
                                                        "python",
                                                        "scripts/validate_paper10_desi_shape_row2_left_endpoint_window_review_package_v1.py",
                                                    ]
                                                )
                                                row2_left_window_response = (
                                                    ROOT
                                                    / "data"
                                                    / "derived"
                                                    / "paper10_desi_shape_row2_left_endpoint_window_review_response_v1.csv"
                                                )
                                                if row2_left_window_response.exists():
                                                    run(
                                                        [
                                                            "python",
                                                            "scripts/validate_paper10_desi_shape_row2_left_endpoint_window_review_response_v1.py",
                                                        ]
                                                    )
                                                run(
                                                    [
                                                        "python",
                                                        "scripts/build_paper10_desi_shape_row2_left_endpoint_window_decision_gate_v1.py",
                                                    ]
                                                )
                                                run(
                                                    [
                                                        "python",
                                                        "scripts/validate_paper10_desi_shape_row2_left_endpoint_window_decision_gate_v1.py",
                                                    ]
                                                )
                                                run(
                                                    [
                                                        "python",
                                                        "scripts/build_paper10_desi_shape_row2_post_window_review_source_plan_v1.py",
                                                    ]
                                                )
                                                run(
                                                    [
                                                        "python",
                                                        "scripts/validate_paper10_desi_shape_row2_post_window_review_source_plan_v1.py",
                                                    ]
                                                )
                                                run(
                                                    [
                                                        "python",
                                                        "scripts/build_paper10_desi_shape_row2_left_strict_support_scout_v1.py",
                                                    ]
                                                )
                                                run(
                                                    [
                                                        "python",
                                                        "scripts/validate_paper10_desi_shape_row2_left_strict_support_scout_v1.py",
                                                    ]
                                                )
                                                run(
                                                    [
                                                        "python",
                                                        "scripts/build_paper10_desi_shape_row2_source_native_shape_support_scout_v1.py",
                                                    ]
                                                )
                                                run(
                                                    [
                                                        "python",
                                                        "scripts/validate_paper10_desi_shape_row2_source_native_shape_support_scout_v1.py",
                                                    ]
                                                )
                                                run(
                                                    [
                                                        "python",
                                                        "scripts/build_paper10_desi_shape_row2_source_native_shape_support_review_package_v1.py",
                                                    ]
                                                )
                                                run(
                                                    [
                                                        "python",
                                                        "scripts/validate_paper10_desi_shape_row2_source_native_shape_support_review_package_v1.py",
                                                    ]
                                                )
                                                row2_source_native_shape_response = (
                                                    ROOT
                                                    / "data"
                                                    / "derived"
                                                    / "paper10_desi_shape_row2_source_native_shape_support_review_response_v1.csv"
                                                )
                                                if row2_source_native_shape_response.exists():
                                                    run(
                                                        [
                                                            "python",
                                                            "scripts/validate_paper10_desi_shape_row2_source_native_shape_support_review_response_v1.py",
                                                        ]
                                                    )
                                                run(
                                                    [
                                                        "python",
                                                        "scripts/build_paper10_desi_shape_row2_gate_status_ledger_v1.py",
                                                    ]
                                                )
                                                run(
                                                    [
                                                        "python",
                                                        "scripts/validate_paper10_desi_shape_row2_gate_status_ledger_v1.py",
                                                    ]
                                                )
                                                run(
                                                    [
                                                        "python",
                                                        "scripts/build_paper10_desi_shape_row2_promotion_review_package_v1.py",
                                                    ]
                                                )
                                                run(
                                                    [
                                                        "python",
                                                        "scripts/validate_paper10_desi_shape_row2_promotion_review_package_v1.py",
                                                    ]
                                                )
                                                row2_promotion_response = (
                                                    ROOT
                                                    / "data/derived/paper10_desi_shape_row2_promotion_review_response_v1.csv"
                                                )
                                                if row2_promotion_response.exists():
                                                    run(
                                                        [
                                                            "python",
                                                            "scripts/validate_paper10_desi_shape_row2_promotion_review_response_v1.py",
                                                        ]
                                                    )
                                                    run(
                                                        [
                                                            "python",
                                                            "scripts/build_paper10_desi_shape_row2_gate_status_ledger_v1.py",
                                                        ]
                                                    )
                                                    run(
                                                        [
                                                            "python",
                                                            "scripts/validate_paper10_desi_shape_row2_gate_status_ledger_v1.py",
                                                        ]
                                                    )
                                                    row2_gate_status = read_one_csv(
                                                        ROOT
                                                        / "data/derived/paper10_desi_shape_row2_gate_status_ledger_v1_summary.csv"
                                                    )["status"]
                                                    if (
                                                        row2_gate_status
                                                        == "ROW2_SEPARATE_REPLAY_AUTH_REVIEW_ALLOWED_NOT_REPLAY"
                                                    ):
                                                        run(
                                                            [
                                                                "python",
                                                                "scripts/build_paper10_desi_shape_row2_replay_authorization_review_package_v1.py",
                                                            ]
                                                        )
                                                        run(
                                                            [
                                                                "python",
                                                                "scripts/validate_paper10_desi_shape_row2_replay_authorization_review_package_v1.py",
                                                            ]
                                                        )
                                                    elif (
                                                        row2_gate_status
                                                        == "ROW2_PERMISSION_ONLY_REPLAY_AUTHORIZED_NOT_VALIDATION"
                                                    ):
                                                        print(
                                                            "Row2 replay authorization package validation skipped "
                                                            "because the completed authorization response has already "
                                                            "advanced the gate to permission-only replay."
                                                        )
                                                    else:
                                                        print(
                                                            "Row2 replay authorization package build skipped "
                                                            f"because gate status is {row2_gate_status}"
                                                        )
                                                    row2_replay_auth_response = (
                                                        ROOT
                                                        / "data/derived/paper10_desi_shape_row2_replay_authorization_review_response_v1.csv"
                                                    )
                                                    if row2_replay_auth_response.exists():
                                                        run(
                                                            [
                                                                "python",
                                                                "scripts/validate_paper10_desi_shape_row2_replay_authorization_review_response_v1.py",
                                                            ]
                                                        )
                                                        run(
                                                            [
                                                                "python",
                                                                "scripts/build_paper10_desi_shape_row2_gate_status_ledger_v1.py",
                                                            ]
                                                        )
                                                        run(
                                                            [
                                                                "python",
                                                                "scripts/validate_paper10_desi_shape_row2_gate_status_ledger_v1.py",
                                                            ]
                                                        )
                                                        if (
                                                            ROOT
                                                            / "data/source_manifest/paper10_desi_shape_row2_authorized_replay_run_v1.csv"
                                                        ).exists():
                                                            run(
                                                                [
                                                                    "python",
                                                                    "scripts/run_paper10_desi_shape_row2_authorized_replay_v1.py",
                                                                ]
                                                            )
                                                            run(
                                                                [
                                                                    "python",
                                                                    "scripts/validate_paper10_desi_shape_row2_authorized_replay_v1.py",
                                                                ]
                                                            )
                                                            run(
                                                                [
                                                                    "python",
                                                                    "scripts/build_paper10_desi_shape_core_support_synthesis_gate_v1.py",
                                                                ]
                                                            )
                                                            run(
                                                                [
                                                                    "python",
                                                                    "scripts/validate_paper10_desi_shape_core_support_synthesis_gate_v1.py",
                                                                ]
                                                            )
                                                            run(
                                                                [
                                                                    "python",
                                                                    "scripts/build_paper10_desi_shape_route_source_synthesis_review_package_v1.py",
                                                                ]
                                                            )
                                                            run(
                                                                [
                                                                    "python",
                                                                    "scripts/validate_paper10_desi_shape_route_source_synthesis_review_package_v1.py",
                                                                ]
                                                            )
                                                            source_synthesis_response = (
                                                                ROOT
                                                                / "data/derived/paper10_desi_shape_route_source_synthesis_review_response_v1.csv"
                                                            )
                                                            if source_synthesis_response.exists():
                                                                run(
                                                                    [
                                                                        "python",
                                                                        "scripts/validate_paper10_desi_shape_route_source_synthesis_review_response_v1.py",
                                                                    ]
                                                                )
                                                                run(
                                                                    [
                                                                        "python",
                                                                        "scripts/build_paper10_desi_shape_post_synthesis_gate_authorization_review_package_v1.py",
                                                                    ]
                                                                )
                                                                run(
                                                                    [
                                                                        "python",
                                                                        "scripts/validate_paper10_desi_shape_post_synthesis_gate_authorization_review_package_v1.py",
                                                                    ]
                                                                )
                                                                post_synthesis_gate_response = (
                                                                    ROOT
                                                                    / "data/derived/paper10_desi_shape_post_synthesis_gate_authorization_review_response_v1.csv"
                                                                )
                                                                if post_synthesis_gate_response.exists():
                                                                    run(
                                                                        [
                                                                            "python",
                                                                            "scripts/validate_paper10_desi_shape_post_synthesis_gate_authorization_review_response_v1.py",
                                                                        ]
                                                                    )
                                                                    run(
                                                                        [
                                                                            "python",
                                                                            "scripts/build_paper10_desi_shape_validation_oriented_gate_review_package_v1.py",
                                                                        ]
                                                                    )
                                                                    run(
                                                                        [
                                                                            "python",
                                                                            "scripts/validate_paper10_desi_shape_validation_oriented_gate_review_package_v1.py",
                                                                        ]
                                                                    )
                                                                    validation_oriented_gate_response = (
                                                                        ROOT
                                                                        / "data/derived/paper10_desi_shape_validation_oriented_gate_review_response_v1.csv"
                                                                    )
                                                                    if validation_oriented_gate_response.exists():
                                                                        run(
                                                                            [
                                                                                "python",
                                                                                "scripts/validate_paper10_desi_shape_validation_oriented_gate_review_response_v1.py",
                                                                            ]
                                                                        )
                                                                        run(
                                                                            [
                                                                                "python",
                                                                                "scripts/build_paper10_desi_shape_validation_permission_replay_authorization_review_package_v1.py",
                                                                            ]
                                                                        )
                                                                        run(
                                                                            [
                                                                                "python",
                                                                                "scripts/validate_paper10_desi_shape_validation_permission_replay_authorization_review_package_v1.py",
                                                                            ]
                                                                        )
                                                                        validation_permission_response = (
                                                                            ROOT
                                                                            / "data/derived/paper10_desi_shape_validation_permission_replay_authorization_review_response_v1.csv"
                                                                        )
                                                                        if validation_permission_response.exists():
                                                                            run(
                                                                                [
                                                                                    "python",
                                                                                    "scripts/validate_paper10_desi_shape_validation_permission_replay_authorization_review_response_v1.py",
                                                                                ]
                                                                            )
                                                                            run(
                                                                                [
                                                                                    "python",
                                                                                    "scripts/run_paper10_desi_shape_validation_permission_authorized_replay_v1.py",
                                                                                ]
                                                                            )
                                                                            run(
                                                                                [
                                                                                    "python",
                                                                                    "scripts/validate_paper10_desi_shape_validation_permission_authorized_replay_v1.py",
                                                                                ]
                                                                            )
                                        run(
                                            [
                                                "python",
                                                "scripts/build_paper10_desi_clock_support_acquisition_manifest_v1.py",
                                            ]
                                        )
                                        run(
                                            [
                                                "python",
                                                "scripts/validate_paper10_desi_clock_support_acquisition_manifest_v1.py",
                                            ]
                                        )
                                        run(
                                            [
                                                "python",
                                                "scripts/build_paper10_desi_clock_support_source_candidate_scan_v1.py",
                                            ]
                                        )
                                        run(
                                            [
                                                "python",
                                                "scripts/validate_paper10_desi_clock_support_source_candidate_scan_v1.py",
                                            ]
                                        )
                                        run(
                                            [
                                                "python",
                                                "scripts/build_paper10_desi_clock_support_blocker_verdict_v1.py",
                                            ]
                                        )
                                        run(
                                            [
                                                "python",
                                                "scripts/validate_paper10_desi_clock_support_blocker_verdict_v1.py",
                                            ]
                                        )
                                        run(
                                            [
                                                "python",
                                                "scripts/validate_paper10_desi_clock_support_blocker_external_review_response_v1.py",
                                            ]
                                        )
                                        run(
                                            [
                                                "python",
                                                "scripts/build_paper10_desi_row4_clock_reopen_manifest_v1.py",
                                            ]
                                        )
                                        run(
                                            [
                                                "python",
                                                "scripts/validate_paper10_desi_row4_clock_reopen_manifest_v1.py",
                                            ]
                                        )
                                        run(
                                            [
                                                "python",
                                                "scripts/build_paper10_desi_row4_cc_bracket_source_freeze_v1.py",
                                            ]
                                        )
                                        run(
                                            [
                                                "python",
                                                "scripts/validate_paper10_desi_row4_cc_bracket_source_freeze_v1.py",
                                            ]
                                        )
                                        run(
                                            [
                                                "python",
                                                "scripts/build_paper10_desi_row4_non_simon_clock_search_v1.py",
                                            ]
                                        )
                                        run(
                                            [
                                                "python",
                                                "scripts/validate_paper10_desi_row4_non_simon_clock_search_v1.py",
                                            ]
                                        )
                                        run(
                                            [
                                                "python",
                                                "scripts/build_paper10_desi_row4_window_review_package_v1.py",
                                            ]
                                        )
                                        run(
                                            [
                                                "python",
                                                "scripts/validate_paper10_desi_row4_window_review_package_v1.py",
                                            ]
                                        )
                                        run(
                                            [
                                                "python",
                                                "scripts/build_paper10_desi_row4_window_decision_gate_v1.py",
                                            ]
                                        )
                                        run(
                                            [
                                                "python",
                                                "scripts/validate_paper10_desi_row4_window_decision_gate_v1.py",
                                            ]
                                        )
                                        run(
                                            [
                                                "python",
                                                "scripts/build_paper10_desi_row5_high_z_review_package_v1.py",
                                            ]
                                        )
                                        run(
                                            [
                                                "python",
                                                "scripts/validate_paper10_desi_row5_high_z_review_package_v1.py",
                                            ]
                                        )
                                        run(
                                            [
                                                "python",
                                                "scripts/build_paper10_desi_row5_high_z_decision_gate_v1.py",
                                            ]
                                        )
                                        run(
                                            [
                                                "python",
                                                "scripts/validate_paper10_desi_row5_high_z_decision_gate_v1.py",
                                            ]
                                        )
                                        run(
                                            [
                                                "python",
                                                "scripts/build_paper10_desi_time_route_closure_status_v1.py",
                                            ]
                                        )
                                        run(
                                            [
                                                "python",
                                                "scripts/validate_paper10_desi_time_route_closure_status_v1.py",
                                            ]
                                        )
                                    run(
                                        [
                                            "python",
                                            "scripts/validate_paper10_desi_time_level_endpoint_replay_run_template_v1.py",
                                        ]
                                    )
                run(["python", "scripts/build_void_source_basis_refinement_v2_path_projection_route_ledger_v1.py"])
                run(["python", "scripts/validate_void_source_basis_refinement_v2_path_projection_route_ledger_v1.py"])
                run(["python", "scripts/build_void_source_basis_refinement_v2_time_readout_route_ledger_v1.py"])
                run(["python", "scripts/validate_void_source_basis_refinement_v2_time_readout_route_ledger_v1.py"])
                run(["python", "scripts/build_void_source_basis_refinement_v2_multichannel_coupling_ledger_v1.py"])
                run(["python", "scripts/validate_void_source_basis_refinement_v2_multichannel_coupling_ledger_v1.py"])
                run(["python", "scripts/build_void_source_basis_refinement_v2_projection_morphology_gate_v1.py"])
                run(["python", "scripts/validate_void_source_basis_refinement_v2_projection_morphology_gate_v1.py"])
    run(["python", "scripts/check_kids1000_lensing_route_v1.py"])
    run(["python", "scripts/validate_kids1000_lensing_route_v1.py"])
    run(["python", "scripts/validate_kids1000_lensing_products_v1.py"])
    run(["python", "scripts/build_kids1000_lensing_inventory_v1.py"])
    run(["python", "scripts/validate_kids1000_lensing_inventory_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_hdu_inventory_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_hdu_inventory_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_tomographic_mode_inventory_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_tomographic_mode_inventory_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_covariance_readiness_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_covariance_readiness_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_mask_modecut_inventory_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_mask_modecut_inventory_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_tomographic_weight_inventory_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_tomographic_weight_inventory_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_covariance_subselection_inventory_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_covariance_subselection_inventory_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_covariance_inversion_readiness_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_covariance_inversion_readiness_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_theory_vector_template_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_theory_vector_template_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_mapping_template_join_contract_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_mapping_template_join_contract_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_redshift_kernel_inventory_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_redshift_kernel_inventory_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_path_mask_depth_gap_inventory_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_path_mask_depth_gap_inventory_v1.py"])
    run(["python", "scripts/validate_kids1000_dr4_path_mask_route_scripts_v1.py"])
    run(["python", "scripts/build_kids1000_dr4_path_mask_route_tile_inventory_v1.py"])
    run(["python", "scripts/validate_kids1000_dr4_path_mask_route_tile_inventory_v1.py"])
    run(["python", "scripts/validate_kids1000_dr4_path_mask_head_sample_v1.py"])
    run(["python", "scripts/validate_kids1000_dr4_path_mask_subset_v1.py"])
    run(["python", "scripts/build_kids1000_dr4_path_mask_observable_shell_v1.py"])
    run(["python", "scripts/validate_kids1000_dr4_path_mask_observable_shell_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_path_mapping_design_skeleton_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_path_mapping_design_skeleton_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_path_mapping_domain_skeleton_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_path_mapping_domain_skeleton_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_f_overlap_rule_shell_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_f_overlap_rule_shell_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_f_overlap_source_availability_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_f_overlap_source_availability_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_f_overlap_full_mask_acquisition_manifest_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_f_overlap_full_mask_acquisition_manifest_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_f_overlap_full_mask_batch_plan_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_f_overlap_full_mask_batch_plan_v1.py"])
    run(["python", "scripts/acquire_kids1000_cosebis_f_overlap_full_mask_batch_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_f_overlap_full_mask_batch_dry_run_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_f_overlap_batch_promotion_review_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_f_overlap_batch_promotion_review_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_f_overlap_execution_review_schema_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_f_overlap_execution_review_schema_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_f_overlap_execution_review_template_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_f_overlap_execution_review_template_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_f_overlap_full_route_cache_inventory_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_f_overlap_header_footprint_rule_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_f_overlap_header_footprint_degeneracy_audit_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_f_overlap_pixel_fraction_pilot_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_f_overlap_pixel_fraction_pilot_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_f_overlap_full_route_pixel_fraction_rule_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_d_path_full_route_mask_load_rule_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_e_web_null_control_rule_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_c_norm_source_side_rule_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_c_norm_source_side_rule_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_path_weight_construction_rule_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_path_weight_construction_rule_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_path_factor_acquisition_plan_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_path_factor_acquisition_plan_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_path_source_product_route_manifest_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_path_source_product_route_manifest_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_source_frozen_mapping_vector_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_source_frozen_mapping_vector_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_source_frozen_theory_vector_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_source_frozen_theory_vector_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_theory_vector_readiness_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_theory_vector_readiness_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_web_path_mapping_readiness_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_web_path_mapping_readiness_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_null_control_seed_inventory_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_null_control_seed_inventory_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_null_control_theory_replay_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_null_control_theory_replay_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_null_control_readiness_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_null_control_readiness_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_endpoint_family_geometry_audit_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_endpoint_family_geometry_audit_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_path_mapping_source_preflight_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_path_mapping_source_preflight_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_path_blocker_resolution_order_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_path_blocker_resolution_order_v1.py"])
    run(
        [
            "python",
            "scripts/validate_kids1000_cosebis_f_overlap_filled_execution_review_artifact_v1.py",
            "--input",
            "data/derived/kids1000_cosebis_f_overlap_execution_review_template_v1.csv",
            "--mode",
            "template",
        ]
    )
    run(["python", "scripts/build_kids1000_cosebis_f_overlap_resolution_decision_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_f_overlap_resolution_decision_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_partial_control_scoring_protocol_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_partial_control_mapping_shell_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_partial_control_mapping_shell_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_partial_control_mapping_values_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_partial_control_mapping_values_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_partial_control_design_matrix_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_partial_control_design_matrix_v1.py"])
    run(["python", "scripts/run_kids1000_cosebis_partial_control_diagnostic_scoring_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_partial_control_diagnostic_scoring_v1.py"])
    run(["python", "scripts/run_kids1000_cosebis_partial_control_null_replay_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_partial_control_null_replay_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_partial_control_degeneracy_audit_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_partial_control_degeneracy_audit_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_non_degenerate_mapping_promotion_gate_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_non_degenerate_mapping_promotion_gate_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_endpoint_scoring_readiness_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_endpoint_scoring_readiness_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_endpoint_scoring_protocol_v1.py"])
    run(["python", "scripts/run_kids1000_cosebis_endpoint_scoring_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_endpoint_scoring_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_endpoint_scoring_diagnostics_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_endpoint_scoring_diagnostics_v1.py"])
    run(["python", "scripts/run_kids1000_cosebis_tomographic_structure_robustness_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_tomographic_structure_robustness_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_tomographic_control_plausibility_audit_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_tomographic_control_plausibility_audit_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_tomographic_holdout_calibration_gate_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_tomographic_holdout_calibration_gate_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_source_frozen_tomographic_holdout_manifest_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_source_frozen_tomographic_holdout_manifest_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_photoz_tomographic_calibration_evidence_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_photoz_tomographic_calibration_evidence_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_external_photoz_calibration_acquisition_plan_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_external_photoz_calibration_acquisition_plan_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_external_photoz_calibration_source_manifest_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_external_photoz_calibration_source_manifest_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_external_photoz_calibration_leakage_review_preflight_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_external_photoz_calibration_leakage_review_preflight_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_external_photoz_calibration_reviewer_attestation_template_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_external_photoz_calibration_reviewer_attestation_template_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_external_photoz_calibration_reviewer_handoff_package_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_external_photoz_calibration_reviewer_handoff_package_v1.py"])
    run([
        "python",
        "scripts/validate_kids1000_cosebis_external_photoz_calibration_completed_reviewer_response_v1.py",
        "data/derived/kids1000_cosebis_external_photoz_calibration_completed_reviewer_response_v1.csv",
        "--summary-out",
        "data/derived/kids1000_cosebis_external_photoz_calibration_completed_reviewer_response_v1_summary.csv",
    ])
    run(["python", "scripts/build_kids1000_cosebis_external_photoz_calibration_closure_ledger_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_external_photoz_calibration_closure_ledger_v1.py"])
    run([
        "python",
        "scripts/validate_kids1000_cosebis_endpoint_replay_authorization_review_response_v1.py",
        "data/derived/kids1000_cosebis_endpoint_replay_authorization_review_response_v1.csv",
        "--summary-out",
        "data/derived/kids1000_cosebis_endpoint_replay_authorization_review_response_v1_summary.csv",
    ])
    run(["python", "scripts/run_kids1000_cosebis_authorized_endpoint_replay_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_authorized_endpoint_replay_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_tomographic_control_disambiguation_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_tomographic_control_disambiguation_v1.py"])
    run(["python", "scripts/run_kids1000_cosebis_tomographic_holdout_replay_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_tomographic_holdout_replay_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_best_tomographic_control_source_evidence_gate_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_best_tomographic_control_source_evidence_gate_v1.py"])
    run(["python", "scripts/run_kids1000_cosebis_endpoint_jackknife_robustness_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_endpoint_jackknife_robustness_v1.py"])
    run(["python", "scripts/run_kids1000_cosebis_endpoint_mode_localization_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_endpoint_mode_localization_v1.py"])
    run(["python", "scripts/run_kids1000_cosebis_endpoint_mode_shape_stress_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_endpoint_mode_shape_stress_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_endpoint_scoring_synthesis_ledger_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_endpoint_scoring_synthesis_ledger_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_low_mode_carrier_source_grounding_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_low_mode_carrier_source_grounding_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_low_mode_kernel_envelope_derivation_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_low_mode_kernel_envelope_derivation_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_log_band_prior_eligibility_gate_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_log_band_prior_eligibility_gate_v1.py"])
    run(["python", "scripts/run_kids1000_cosebis_log_band_prior_mock_sanity_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_log_band_prior_mock_sanity_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_survey_native_path_kernel_derivation_gate_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_survey_native_path_kernel_derivation_gate_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_mode_response_operator_spec_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_mode_response_operator_spec_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_mode_response_spectrum_attempt_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_mode_response_spectrum_attempt_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_operator_null_safety_gate_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_operator_null_safety_gate_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_pure_mask_response_gate_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_pure_mask_response_gate_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_mask_mode_leakage_audit_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_mask_mode_leakage_audit_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_operator_leakage_theorem_requirements_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_operator_leakage_theorem_requirements_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_operator_leakage_proof_plan_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_operator_leakage_proof_plan_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_operator_leakage_domain_decomposition_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_operator_leakage_domain_decomposition_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_operator_leakage_projection_criterion_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_operator_leakage_projection_criterion_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_gauge_quotient_descent_gate_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_gauge_quotient_descent_gate_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_survey_native_operator_construction_attempt_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_survey_native_operator_construction_attempt_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_physical_operator_units_gate_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_physical_operator_units_gate_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_source_side_amplitude_map_attempt_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_source_side_amplitude_map_attempt_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_physical_amplitude_requirements_gate_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_physical_amplitude_requirements_gate_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_standard_lensing_null_amplitude_theorem_requirements_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_standard_lensing_null_amplitude_theorem_requirements_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_response_unit_normalization_requirements_gate_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_response_unit_normalization_requirements_gate_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_physical_promotion_blocker_ledger_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_physical_promotion_blocker_ledger_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_physical_promotion_dependency_order_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_physical_promotion_dependency_order_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_validation_readiness_ledger_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_validation_readiness_ledger_v1.py"])
    run(["python", "scripts/build_kids1000_cosebis_tomographic_photoz_closure_status_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_tomographic_photoz_closure_status_v1.py"])
    run(["python", "scripts/build_joint_existing_artifact_meta_score_v1.py"])
    run(["python", "scripts/validate_joint_existing_artifact_meta_score_v1.py"])
    run(["python", "scripts/run_joint_multichannel_endpoint_candidate_v1.py"])
    run(["python", "scripts/validate_joint_multichannel_endpoint_candidate_v1.py"])
    run(["python", "scripts/run_joint_multichannel_block_score_v1.py"])
    run(["python", "scripts/validate_joint_multichannel_block_score_v1.py"])
    run(["python", "scripts/run_joint_best_justified_kernel_score_v1.py"])
    run(["python", "scripts/validate_joint_best_justified_kernel_score_v1.py"])
    run(["python", "scripts/run_joint_best_justified_kernel_robustness_v1.py"])
    run(["python", "scripts/validate_joint_best_justified_kernel_robustness_v1.py"])
    run(["python", "scripts/build_joint_best_justified_kernel_figure_v1.py"])
    run(["python", "scripts/validate_joint_best_justified_qi_review_package_v1.py"])
    run(["python", "scripts/validate_joint_best_justified_qi_review_response_v1.py"])
    run(["python", "scripts/build_joint_likelihood_surrogate_requirements_gate_v1.py"])
    run(["python", "scripts/validate_joint_likelihood_surrogate_requirements_gate_v1.py"])
    run(["python", "scripts/build_joint_covariance_model_requirements_gate_v1.py"])
    run(["python", "scripts/validate_joint_covariance_model_requirements_gate_v1.py"])
    run(["python", "scripts/build_joint_non_lensing_lift_diagnostic_v1.py"])
    run(["python", "scripts/validate_joint_non_lensing_lift_diagnostic_v1.py"])
    run(["python", "scripts/build_observer_path_strengthening_gate_v1.py"])
    run(["python", "scripts/validate_observer_path_strengthening_gate_v1.py"])
    run(["python", "scripts/build_observer_path_metric_product_requirements_package_v1.py"])
    run(["python", "scripts/validate_observer_path_metric_product_requirements_package_v1.py"])
    run(["python", "scripts/validate_observer_path_metric_product_requirements_review_response_v1.py"])
    run(["python", "scripts/build_observer_path_metric_environment_product_v1.py"])
    run(["python", "scripts/validate_observer_path_metric_environment_product_v1.py"])
    run(["python", "scripts/build_observer_path_metric_product_acquisition_status_v1.py"])
    run(["python", "scripts/validate_observer_path_metric_product_acquisition_status_v1.py"])
    run(["python", "scripts/run_observer_path_metric_environment_fast_screen_v1.py"])
    run(["python", "scripts/validate_observer_path_metric_environment_fast_screen_v1.py"])
    run(["python", "scripts/build_observer_path_metric_environment_ordering_diagnostic_v1.py"])
    run(["python", "scripts/validate_observer_path_metric_environment_ordering_diagnostic_v1.py"])
    run(["python", "scripts/build_observer_path_source_native_ordering_kernel_v1.py"])
    run(["python", "scripts/validate_observer_path_source_native_ordering_kernel_v1.py"])
    run(["python", "scripts/run_observer_path_source_native_ordering_fast_screen_v1.py"])
    run(["python", "scripts/validate_observer_path_source_native_ordering_fast_screen_v1.py"])
    run(["python", "scripts/build_observer_path_metric_lensing_next_gate_v1.py"])
    run(["python", "scripts/validate_observer_path_metric_lensing_next_gate_v1.py"])
    run(["python", "scripts/build_act_dr6_lensing_product_v1.py"])
    run(["python", "scripts/validate_act_dr6_lensing_product_v1.py"])
    run(["python", "scripts/build_act_dr6_lensing_inventory_v1.py"])
    run(["python", "scripts/validate_act_dr6_lensing_inventory_v1.py"])
    run(["python", "scripts/build_act_dr6_lensing_low_z_sampling_pilot_v1.py"])
    run(["python", "scripts/validate_act_dr6_lensing_low_z_sampling_pilot_v1.py"])
    run(["python", "scripts/build_act_dr6_lensing_path_weight_candidate_v1.py"])
    run(["python", "scripts/validate_act_dr6_lensing_path_weight_candidate_v1.py"])
    run(["python", "scripts/build_act_dr6_lensing_observer_path_source_object_v1.py"])
    run(["python", "scripts/validate_act_dr6_lensing_observer_path_source_object_v1.py"])
    run(["python", "scripts/build_act_dr6_lensing_e_mode_route_v1.py"])
    run(["python", "scripts/validate_act_dr6_lensing_e_mode_route_v1.py"])
    run(["python", "scripts/build_act_dr6_lensing_curl_null_policy_v1.py"])
    run(["python", "scripts/validate_act_dr6_lensing_curl_null_policy_v1.py"])
    run(["python", "scripts/build_act_dr6_lensing_mask_coverage_policy_v1.py"])
    run(["python", "scripts/validate_act_dr6_lensing_mask_coverage_policy_v1.py"])
    run(["python", "scripts/build_act_dr6_lensing_units_normalization_policy_v1.py"])
    run(["python", "scripts/validate_act_dr6_lensing_units_normalization_policy_v1.py"])
    run(["python", "scripts/build_act_dr6_lensing_channel_handoff_policy_v1.py"])
    run(["python", "scripts/validate_act_dr6_lensing_channel_handoff_policy_v1.py"])
    run(["python", "scripts/build_act_dr6_lensing_control_suite_policy_v1.py"])
    run(["python", "scripts/validate_act_dr6_lensing_control_suite_policy_v1.py"])
    run(["python", "scripts/build_act_dr6_lensing_path_weight_replay_authorization_review_package_v1.py"])
    run(["python", "scripts/validate_act_dr6_lensing_path_weight_replay_authorization_review_package_v1.py"])
    run(["python", "scripts/build_act_dr6_lensing_path_weight_replay_run_template_v1.py"])
    run(["python", "scripts/validate_act_dr6_lensing_path_weight_replay_run_template_v1.py"])
    if (ROOT / "data/derived/act_dr6_lensing_path_weight_authorized_replay_v1_summary.csv").exists():
        run(["python", "scripts/build_act_dr6_lensing_path_weight_control_dominance_diagnostic_v1.py"])
        run(["python", "scripts/validate_act_dr6_lensing_path_weight_control_dominance_diagnostic_v1.py"])
        run(["python", "scripts/build_act_dr6_lensing_path_weight_paper11_control_veto_gate_v1.py"])
        run(["python", "scripts/validate_act_dr6_lensing_path_weight_paper11_control_veto_gate_v1.py"])
        run(["python", "scripts/build_act_dr6_lensing_path_weight_source_basis_freeze_or_demote_gate_v1.py"])
        run(["python", "scripts/validate_act_dr6_lensing_path_weight_source_basis_freeze_or_demote_gate_v1.py"])
        run(["python", "scripts/build_act_dr6_lensing_reopen_closure_ledger_v1.py"])
        run(["python", "scripts/validate_act_dr6_lensing_reopen_closure_ledger_v1.py"])
        run(["python", "scripts/build_act_dr6_lensing_next_source_basis_design_scaffold_v1.py"])
        run(["python", "scripts/validate_act_dr6_lensing_next_source_basis_design_scaffold_v1.py"])
        run(["python", "scripts/build_act_dr6_lensing_caveated_kpath_source_design_v1.py"])
        run(["python", "scripts/validate_act_dr6_lensing_caveated_kpath_source_design_v1.py"])
        run(["python", "scripts/build_act_dr6_lensing_caveated_kpath_source_design_review_package_v1.py"])
        run(["python", "scripts/validate_act_dr6_lensing_caveated_kpath_source_design_review_package_v1.py"])
        run(["python", "scripts/build_act_dr6_lensing_caveated_kpath_replay_authorization_review_package_v1.py"])
        run(["python", "scripts/validate_act_dr6_lensing_caveated_kpath_replay_authorization_review_package_v1.py"])
        if (ROOT / "data/derived/act_dr6_lensing_caveated_kpath_replay_authorization_review_response_v1_summary.csv").exists():
            run(["python", "scripts/validate_act_dr6_lensing_caveated_kpath_replay_authorization_review_response_v1.py"])
            run(["python", "scripts/build_act_dr6_lensing_caveated_kpath_guarded_replay_package_v1.py"])
            run(["python", "scripts/validate_act_dr6_lensing_caveated_kpath_guarded_replay_package_v1.py"])
            run(["python", "scripts/run_act_dr6_lensing_caveated_kpath_guarded_replay_v1.py"])
            run(["python", "scripts/validate_act_dr6_lensing_caveated_kpath_guarded_replay_v1.py"])
    run(["python", "scripts/build_figures.py"])
    print("+ tectonic paper10_submission_source/main.tex")
    subprocess.run(["tectonic", PAPER.name], cwd=PAPER.parent, env=env, check=True)
    run(["python", "scripts/build_arxiv_source.py"])
    run(["python", "-m", "pytest", "-q"])
    print("PAPER10_REPRODUCTION_COMPLETE")


if __name__ == "__main__":
    main()
