from __future__ import annotations

import csv
import os
import subprocess
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_public_files_exist() -> None:
    required = [
        "README.md",
        "DATA_NOTICE.md",
        "CITATION.cff",
        "LICENSE",
        "paper10_submission_source/main.tex",
        "paper10_submission_source/supplement_route_ledgers.tex",
        "paper10_submission_source/refs.bib",
        "paper10_submission_source/main.pdf",
        "arxiv_submission_source.zip",
        "data/derived/audit_gate_inventory.csv",
        "data/source_manifest/paper10_source_freeze_manifest.csv",
        "data/source_manifest/cosmology_channel_manifest_v1.csv",
        "data/source_manifest/cosmology_activation_rule_manifest_v1.csv",
        "data/source_manifest/cosmology_activation_parameter_freeze_plan_v1.csv",
        "data/source_manifest/cosmology_source_grounding_gate_v1.csv",
        "data/source_manifest/cosmology_flrw_consistency_channel_audit_v1.csv",
        "docs/cosmology_channel_manifest_v1.md",
        "docs/cosmology_activation_rule_manifest_v1.md",
        "docs/cosmology_activation_parameter_freeze_plan_v1.md",
        "docs/cosmology_source_grounding_gate_v1.md",
        "docs/cosmology_flrw_consistency_channel_audit_v1.md",
        "docs/source_freeze_protocol.md",
        "docs/source_selection_audit_001.md",
        "scripts/validate_source_freeze.py",
        "scripts/validate_cosmology_channel_manifest_v1.py",
        "scripts/validate_cosmology_activation_rule_manifest_v1.py",
        "scripts/validate_cosmology_activation_parameter_freeze_plan_v1.py",
        "scripts/validate_cosmology_source_grounding_gate_v1.py",
        "scripts/validate_cosmology_flrw_consistency_channel_audit_v1.py",
        "scripts/acquire_source_pages.py",
        "scripts/validate_cached_source_pages.py",
        "data/source_manifest/source_page_cache_manifest.csv",
        "data/source_manifest/paper10_product_freeze_plan.csv",
        "docs/product_freeze_plan.md",
        "scripts/validate_product_freeze_plan.py",
        "data/source_manifest/void_web_source_native_freeze_plan_v1.csv",
        "docs/void_web_source_native_freeze_plan_v1.md",
        "scripts/validate_void_web_source_native_freeze_plan_v1.py",
        "data/source_manifest/void_web_source_native_frozen_products_v1.csv",
        "data/derived/void_web_source_native_inventory_v1.csv",
        "data/source_manifest/void_web_source_native_transform_rule_v1.csv",
        "data/derived/pantheon_void_web_source_native_design_matrix_v1.csv",
        "data/derived/pantheon_void_web_source_native_design_matrix_v1_summary.csv",
        "data/source_manifest/pantheon_void_web_source_native_full_cov_pilot_v1.csv",
        "data/derived/pantheon_void_web_source_native_full_cov_pilot_v1_summary.csv",
        "data/derived/pantheon_void_web_source_native_full_cov_pilot_v1_grid.csv",
        "data/source_manifest/sdss_final_bao_rsd_growth_summary_v1.csv",
        "data/source_manifest/growth_web_source_native_transform_rule_v1.csv",
        "data/source_manifest/growth_web_source_native_pilot_v1.csv",
        "data/derived/growth_web_source_native_design_matrix_v1.csv",
        "data/derived/growth_web_source_native_design_matrix_v1_summary.csv",
        "data/derived/growth_web_source_native_pilot_v1_summary.csv",
        "data/derived/growth_web_source_native_pilot_v1_grid.csv",
        "data/source_manifest/sdss_multitracer_bao_rsd_products_v1.csv",
        "data/source_manifest/sdss_multitracer_bao_rsd_transform_rule_v1.csv",
        "data/source_manifest/sdss_multitracer_bao_rsd_full_cov_pilot_v1.csv",
        "data/derived/sdss_multitracer_bao_rsd_design_matrix_v1.csv",
        "data/derived/sdss_multitracer_bao_rsd_design_matrix_v1_summary.csv",
        "data/derived/sdss_multitracer_bao_rsd_full_cov_pilot_v1_summary.csv",
        "data/derived/sdss_multitracer_bao_rsd_full_cov_pilot_v1_grid.csv",
        "data/source_manifest/cmb_safety_lowz_support_v1.csv",
        "data/derived/cmb_safety_lowz_support_v1.csv",
        "data/derived/cmb_safety_lowz_support_v1_summary.csv",
        "data/source_manifest/void_web_endpoint_readiness_after_flrw_audit_policy_v1.csv",
        "data/derived/void_web_endpoint_readiness_after_flrw_audit_v1.csv",
        "data/derived/void_web_endpoint_readiness_after_flrw_audit_v1_summary.csv",
        "docs/void_web_endpoint_readiness_after_flrw_audit_v1.md",
        "scripts/build_void_web_endpoint_readiness_after_flrw_audit_v1.py",
        "scripts/validate_void_web_endpoint_readiness_after_flrw_audit_v1.py",
        "data/source_manifest/void_web_combined_multiblock_endpoint_protocol_v1.csv",
        "docs/void_web_combined_multiblock_endpoint_protocol_v1.md",
        "scripts/validate_void_web_combined_multiblock_endpoint_protocol_v1.py",
        "data/source_manifest/void_web_combined_multiblock_endpoint_authorization_review_policy_v1.csv",
        "data/derived/void_web_combined_multiblock_endpoint_authorization_review_response_template_v1.csv",
        "data/derived/void_web_combined_multiblock_endpoint_authorization_review_template_v1_summary.csv",
        "docs/void_web_combined_multiblock_endpoint_authorization_review_v1.md",
        "scripts/build_void_web_combined_multiblock_endpoint_authorization_review_template_v1.py",
        "scripts/validate_void_web_combined_multiblock_endpoint_authorization_review_template_v1.py",
        "REVIEWER_README_VOID_WEB_COMBINED_ENDPOINT_AUTHORIZATION.md",
        "data/derived/void_web_combined_multiblock_endpoint_authorization_review_package_v1.zip",
        "data/derived/void_web_combined_multiblock_endpoint_authorization_review_package_v1.zip.sha256",
        "data/derived/void_web_combined_multiblock_endpoint_authorization_review_package_v1_manifest.csv",
        "data/derived/void_web_combined_multiblock_endpoint_authorization_review_package_v1_summary.csv",
        "scripts/build_void_web_combined_multiblock_endpoint_authorization_review_package_v1.py",
        "scripts/validate_void_web_combined_multiblock_endpoint_authorization_review_package_v1.py",
        "data/derived/void_web_combined_multiblock_endpoint_authorization_review_response_v1.csv",
        "data/derived/void_web_combined_multiblock_endpoint_authorization_review_response_v1_summary.csv",
        "data/derived/void_web_combined_multiblock_endpoint_authorization_review_response_v1_validation_report.txt",
        "docs/void_web_combined_multiblock_endpoint_authorization_review_response_v1.md",
        "scripts/validate_void_web_combined_multiblock_endpoint_authorization_review_response_v1.py",
        "data/source_manifest/void_web_combined_multiblock_authorized_endpoint_run_v1.csv",
        "data/derived/void_web_combined_multiblock_authorized_endpoint_v1_summary.csv",
        "data/derived/void_web_combined_multiblock_authorized_endpoint_v1_grid.csv",
        "data/derived/void_web_combined_multiblock_authorized_endpoint_v1_block_drop.csv",
        "docs/void_web_combined_multiblock_authorized_endpoint_v1.md",
        "scripts/run_void_web_combined_multiblock_authorized_endpoint_v1.py",
        "scripts/validate_void_web_combined_multiblock_authorized_endpoint_v1.py",
        "data/derived/void_web_combined_endpoint_diagnostics_v1_summary.csv",
        "data/derived/void_web_combined_endpoint_diagnostics_v1_branch_summary.csv",
        "data/derived/void_web_combined_endpoint_diagnostics_v1_block_drop_summary.csv",
        "docs/void_web_combined_endpoint_diagnostics_v1.md",
        "scripts/build_void_web_combined_endpoint_diagnostics_v1.py",
        "scripts/validate_void_web_combined_endpoint_diagnostics_v1.py",
        "data/derived/void_channel_inactivity_diagnostic_v1_summary.csv",
        "data/derived/void_channel_inactivity_diagnostic_v1_profile.csv",
        "docs/void_channel_inactivity_diagnostic_v1.md",
        "scripts/build_void_channel_inactivity_diagnostic_v1.py",
        "scripts/validate_void_channel_inactivity_diagnostic_v1.py",
        "data/derived/void_source_basis_audit_v1_summary.csv",
        "data/derived/void_source_basis_audit_v1_redshift_bins.csv",
        "docs/void_source_basis_audit_v1.md",
        "scripts/build_void_source_basis_audit_v1.py",
        "scripts/validate_void_source_basis_audit_v1.py",
        "data/source_manifest/void_channel_remediation_policy_v1.csv",
        "data/derived/void_channel_remediation_gate_v1.csv",
        "docs/void_channel_remediation_gate_v1.md",
        "scripts/build_void_channel_remediation_gate_v1.py",
        "scripts/validate_void_channel_remediation_gate_v1.py",
        "data/source_manifest/low_z_pantheon_void_scope_candidate_policy_v1.csv",
        "data/derived/low_z_pantheon_void_scope_candidate_v1_row_mask.csv",
        "data/derived/low_z_pantheon_void_scope_candidate_v1_summary.csv",
        "docs/low_z_pantheon_void_scope_candidate_v1.md",
        "scripts/build_low_z_pantheon_void_scope_candidate_v1.py",
        "scripts/validate_low_z_pantheon_void_scope_candidate_v1.py",
        "REVIEWER_README_LOW_Z_VOID_SCOPE_REPLAY_AUTHORIZATION.md",
        "data/source_manifest/low_z_pantheon_void_scope_replay_authorization_review_policy_v1.csv",
        "data/derived/low_z_pantheon_void_scope_replay_authorization_review_response_template_v1.csv",
        "data/derived/low_z_pantheon_void_scope_replay_authorization_review_template_v1_summary.csv",
        "data/derived/low_z_pantheon_void_scope_replay_authorization_review_package_v1.zip",
        "data/derived/low_z_pantheon_void_scope_replay_authorization_review_package_v1.zip.sha256",
        "data/derived/low_z_pantheon_void_scope_replay_authorization_review_package_v1_manifest.csv",
        "data/derived/low_z_pantheon_void_scope_replay_authorization_review_package_v1_summary.csv",
        "docs/low_z_pantheon_void_scope_replay_authorization_review_v1.md",
        "scripts/build_low_z_pantheon_void_scope_replay_authorization_review_template_v1.py",
        "scripts/validate_low_z_pantheon_void_scope_replay_authorization_review_template_v1.py",
        "scripts/build_low_z_pantheon_void_scope_replay_authorization_review_package_v1.py",
        "scripts/validate_low_z_pantheon_void_scope_replay_authorization_review_package_v1.py",
        "scripts/validate_low_z_pantheon_void_scope_replay_authorization_review_response_v1.py",
        "data/source_manifest/low_z_pantheon_void_replay_protocol_v1.csv",
        "docs/low_z_pantheon_void_replay_protocol_v1.md",
        "scripts/validate_low_z_pantheon_void_replay_protocol_v1.py",
        "data/source_manifest/low_z_pantheon_void_replay_run_v1.csv",
        "docs/low_z_pantheon_void_replay_v1.md",
        "scripts/run_low_z_pantheon_void_replay_v1.py",
        "scripts/validate_low_z_pantheon_void_replay_v1.py",
        "docs/low_z_void_replay_diagnostics_v1.md",
        "scripts/build_low_z_void_replay_diagnostics_v1.py",
        "scripts/validate_low_z_void_replay_diagnostics_v1.py",
        "data/source_manifest/void_source_basis_refinement_gate_policy_v1.csv",
        "docs/void_source_basis_refinement_gate_v1.md",
        "scripts/build_void_source_basis_refinement_gate_v1.py",
        "scripts/validate_void_source_basis_refinement_gate_v1.py",
        "data/source_manifest/void_source_basis_refinement_acquisition_manifest_policy_v1.csv",
        "docs/void_source_basis_refinement_acquisition_manifest_v1.md",
        "scripts/build_void_source_basis_refinement_acquisition_manifest_v1.py",
        "scripts/validate_void_source_basis_refinement_acquisition_manifest_v1.py",
        "docs/void_source_basis_refinement_r1_r3_source_attachment_v1.md",
        "data/derived/void_source_basis_refinement_r1_r3_source_attachment_v1.csv",
        "data/derived/void_source_basis_refinement_r1_r3_source_attachment_v1_summary.csv",
        "data/derived/low_z_pantheon_void_geometry_join_v1.csv",
        "data/derived/low_z_pantheon_los_environment_v1.csv",
        "scripts/build_void_source_basis_refinement_r1_r3_source_attachment_v1.py",
        "scripts/validate_void_source_basis_refinement_r1_r3_source_attachment_v1.py",
        "docs/void_source_basis_refinement_r4_independence_preflight_v1.md",
        "data/derived/void_source_basis_refinement_r4_independence_preflight_v1.csv",
        "data/derived/void_source_basis_refinement_r4_independence_preflight_v1_summary.csv",
        "scripts/build_void_source_basis_refinement_r4_independence_preflight_v1.py",
        "scripts/validate_void_source_basis_refinement_r4_independence_preflight_v1.py",
        "docs/void_source_basis_refinement_r5_control_resistance_preflight_v1.md",
        "data/derived/void_source_basis_refinement_r5_control_resistance_preflight_v1.csv",
        "data/derived/void_source_basis_refinement_r5_control_vectors_v1.csv",
        "data/derived/void_source_basis_refinement_r5_control_resistance_preflight_v1_summary.csv",
        "scripts/build_void_source_basis_refinement_r5_control_resistance_preflight_v1.py",
        "scripts/validate_void_source_basis_refinement_r5_control_resistance_preflight_v1.py",
        "data/source_manifest/void_source_basis_refinement_r6_reviewer_template_policy_v1.csv",
        "data/source_manifest/void_source_basis_refinement_r6_reviewer_handoff_package_policy_v1.csv",
        "data/source_manifest/void_source_basis_refinement_r6_completed_reviewer_response_policy_v1.csv",
        "docs/void_source_basis_refinement_r6_external_reviewer_instructions_v1.md",
        "docs/void_source_basis_refinement_r6_reviewer_template_v1.md",
        "docs/void_source_basis_refinement_r6_reviewer_handoff_package_v1.md",
        "data/derived/void_source_basis_refinement_r6_reviewer_template_v1.csv",
        "data/derived/void_source_basis_refinement_r6_reviewer_template_v1_summary.csv",
        "data/derived/void_source_basis_refinement_r6_reviewer_handoff_package_v1.zip",
        "data/derived/void_source_basis_refinement_r6_reviewer_handoff_package_v1.zip.sha256",
        "data/derived/void_source_basis_refinement_r6_reviewer_handoff_package_v1_manifest.csv",
        "data/derived/void_source_basis_refinement_r6_reviewer_handoff_package_v1_summary.csv",
        "data/derived/void_source_basis_refinement_r6_completed_reviewer_response_v1.csv",
        "data/derived/void_source_basis_refinement_r6_completed_reviewer_response_v1_summary.csv",
        "docs/void_source_basis_refinement_endpoint_replay_authorization_review_v1.md",
        "data/source_manifest/void_source_basis_refinement_endpoint_replay_authorization_review_policy_v1.csv",
        "data/source_manifest/void_source_basis_refinement_authorized_replay_run_v1.csv",
        "data/derived/void_source_basis_refinement_endpoint_replay_authorization_review_response_template_v1.csv",
        "data/derived/void_source_basis_refinement_endpoint_replay_authorization_review_template_v1_summary.csv",
        "data/derived/void_source_basis_refinement_endpoint_replay_authorization_review_package_v1.zip",
        "data/derived/void_source_basis_refinement_endpoint_replay_authorization_review_package_v1.zip.sha256",
        "data/derived/void_source_basis_refinement_endpoint_replay_authorization_review_package_v1_manifest.csv",
        "data/derived/void_source_basis_refinement_endpoint_replay_authorization_review_package_v1_summary.csv",
        "data/derived/void_source_basis_refinement_endpoint_replay_authorization_review_response_v1.csv",
        "data/derived/void_source_basis_refinement_endpoint_replay_authorization_review_response_v1_summary.csv",
        "data/derived/void_source_basis_refinement_authorized_replay_v1_grid.csv",
        "data/derived/void_source_basis_refinement_authorized_replay_v1_summary.csv",
        "data/derived/void_source_basis_refinement_control_dominance_audit_v1_branches.csv",
        "data/derived/void_source_basis_refinement_control_dominance_audit_v1_summary.csv",
        "docs/void_source_basis_refinement_v2_projection_morphology_gate_v1.md",
        "data/source_manifest/void_source_basis_refinement_v2_projection_morphology_policy.csv",
        "data/derived/void_source_basis_refinement_v2_void_morphology_values.csv",
        "data/derived/void_source_basis_refinement_v2_void_morphology_values_summary.csv",
        "data/derived/void_source_basis_refinement_v2_web_morphology_values.csv",
        "data/derived/void_source_basis_refinement_v2_web_morphology_values_summary.csv",
        "data/derived/void_source_basis_refinement_v2_cmb_safety_values.csv",
        "data/derived/void_source_basis_refinement_v2_cmb_safety_values_summary.csv",
        "data/derived/void_source_basis_refinement_v2_path_projection_crossmap_audit.csv",
        "data/derived/void_source_basis_refinement_v2_path_projection_crossmap_audit_summary.csv",
        "data/derived/void_source_basis_refinement_v2_path_partial_scope_policy.csv",
        "data/derived/void_source_basis_refinement_v2_path_partial_scope_policy_summary.csv",
        "data/derived/void_source_basis_refinement_v2_path_partial_scope_values.csv",
        "data/derived/void_source_basis_refinement_v2_path_partial_scope_values_summary.csv",
        "docs/void_source_basis_refinement_v2_path_partial_scope_reviewer_package_v1.md",
        "data/source_manifest/void_source_basis_refinement_v2_path_partial_scope_reviewer_package_policy_v1.csv",
        "data/derived/void_source_basis_refinement_v2_path_partial_scope_reviewer_response_template_v1.csv",
        "data/derived/void_source_basis_refinement_v2_path_partial_scope_reviewer_package_v1.zip",
        "data/derived/void_source_basis_refinement_v2_path_partial_scope_reviewer_package_v1.zip.sha256",
        "data/derived/void_source_basis_refinement_v2_path_partial_scope_reviewer_package_v1_manifest.csv",
        "data/derived/void_source_basis_refinement_v2_path_partial_scope_reviewer_package_v1_summary.csv",
        "docs/void_source_basis_refinement_v2_path_partial_scope_completed_review_notes_v1.md",
        "data/derived/void_source_basis_refinement_v2_path_partial_scope_completed_review_response_v1.csv",
        "data/derived/void_source_basis_refinement_v2_path_partial_scope_completed_review_response_v1_summary.csv",
        "data/derived/void_source_basis_refinement_v2_path_partial_scope_completed_review_summary_v1.csv",
        "data/derived/void_source_basis_refinement_v2_path_partial_scope_completed_review_validation_log_v1.txt",
        "docs/void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_v1.md",
        "data/source_manifest/void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_policy_v1.csv",
        "data/derived/void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_response_template_v1.csv",
        "data/derived/void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_template_v1_summary.csv",
        "data/derived/void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_package_v1.zip",
        "data/derived/void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_package_v1.zip.sha256",
        "data/derived/void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_package_v1_manifest.csv",
        "data/derived/void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_package_v1_summary.csv",
        "docs/void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_response_v1.md",
        "data/derived/void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_response_v1.csv",
        "data/derived/void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_response_v1_summary.csv",
        "data/derived/void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_response_v1_validation_log.txt",
        "docs/void_source_basis_refinement_v2_path_partial_scope_authorized_replay_v1.md",
        "data/source_manifest/void_source_basis_refinement_v2_path_partial_scope_authorized_replay_run_v1.csv",
        "data/derived/void_source_basis_refinement_v2_path_partial_scope_authorized_replay_v1_grid.csv",
        "data/derived/void_source_basis_refinement_v2_path_partial_scope_authorized_replay_v1_summary.csv",
        "docs/void_source_basis_refinement_v2_path_coupled_projection_screen_v1.md",
        "data/source_manifest/void_source_basis_refinement_v2_path_coupled_projection_screen_v1.csv",
        "data/derived/void_source_basis_refinement_v2_path_coupled_projection_screen_v1_grid.csv",
        "data/derived/void_source_basis_refinement_v2_path_coupled_projection_screen_v1_summary.csv",
        "scripts/run_void_source_basis_refinement_v2_path_coupled_projection_screen_v1.py",
        "scripts/validate_void_source_basis_refinement_v2_path_coupled_projection_screen_v1.py",
        "docs/void_source_basis_refinement_v2_path_transform_bank_screen_v1.md",
        "data/source_manifest/void_source_basis_refinement_v2_path_transform_bank_screen_v1.csv",
        "data/derived/void_source_basis_refinement_v2_path_transform_bank_screen_v1_grid.csv",
        "data/derived/void_source_basis_refinement_v2_path_transform_bank_screen_v1_family_summary.csv",
        "data/derived/void_source_basis_refinement_v2_path_transform_bank_screen_v1_summary.csv",
        "scripts/run_void_source_basis_refinement_v2_path_transform_bank_screen_v1.py",
        "scripts/validate_void_source_basis_refinement_v2_path_transform_bank_screen_v1.py",
        "docs/void_source_basis_refinement_v2_path_sky_environment_screen_v1.md",
        "data/source_manifest/void_source_basis_refinement_v2_path_sky_environment_screen_v1.csv",
        "data/derived/void_source_basis_refinement_v2_path_sky_environment_screen_v1_grid.csv",
        "data/derived/void_source_basis_refinement_v2_path_sky_environment_screen_v1_family_summary.csv",
        "data/derived/void_source_basis_refinement_v2_path_sky_environment_screen_v1_summary.csv",
        "scripts/run_void_source_basis_refinement_v2_path_sky_environment_screen_v1.py",
        "scripts/validate_void_source_basis_refinement_v2_path_sky_environment_screen_v1.py",
        "docs/void_source_basis_refinement_v2_observer_dependence_followup_v1.md",
        "data/source_manifest/void_source_basis_refinement_v2_observer_dependence_followup_policy_v1.csv",
        "data/derived/void_source_basis_refinement_v2_observer_dependence_followup_response_template_v1.csv",
        "data/derived/void_source_basis_refinement_v2_observer_dependence_followup_template_v1_summary.csv",
        "data/derived/void_source_basis_refinement_v2_observer_dependence_followup_package_v1.zip",
        "data/derived/void_source_basis_refinement_v2_observer_dependence_followup_package_v1.zip.sha256",
        "data/derived/void_source_basis_refinement_v2_observer_dependence_followup_package_v1_manifest.csv",
        "data/derived/void_source_basis_refinement_v2_observer_dependence_followup_package_v1_summary.csv",
        "scripts/build_void_source_basis_refinement_v2_observer_dependence_followup_template_v1.py",
        "scripts/validate_void_source_basis_refinement_v2_observer_dependence_followup_template_v1.py",
        "scripts/build_void_source_basis_refinement_v2_observer_dependence_followup_package_v1.py",
        "scripts/validate_void_source_basis_refinement_v2_observer_dependence_followup_package_v1.py",
        "docs/void_source_basis_refinement_v2_sky_z_replay_authorization_review_v1.md",
        "data/source_manifest/void_source_basis_refinement_v2_sky_z_replay_authorization_review_policy_v1.csv",
        "data/derived/void_source_basis_refinement_v2_sky_z_replay_authorization_review_response_template_v1.csv",
        "data/derived/void_source_basis_refinement_v2_sky_z_replay_authorization_review_template_v1_summary.csv",
        "data/derived/void_source_basis_refinement_v2_sky_z_replay_authorization_review_package_v1.zip",
        "data/derived/void_source_basis_refinement_v2_sky_z_replay_authorization_review_package_v1.zip.sha256",
        "data/derived/void_source_basis_refinement_v2_sky_z_replay_authorization_review_package_v1_manifest.csv",
        "data/derived/void_source_basis_refinement_v2_sky_z_replay_authorization_review_package_v1_summary.csv",
        "scripts/build_void_source_basis_refinement_v2_sky_z_replay_authorization_review_template_v1.py",
        "scripts/validate_void_source_basis_refinement_v2_sky_z_replay_authorization_review_template_v1.py",
        "scripts/build_void_source_basis_refinement_v2_sky_z_replay_authorization_review_package_v1.py",
        "scripts/validate_void_source_basis_refinement_v2_sky_z_replay_authorization_review_package_v1.py",
        "scripts/validate_void_source_basis_refinement_v2_sky_z_replay_authorization_review_response_v1.py",
        "docs/void_source_basis_refinement_v2_sky_z_authorized_replay_v1.md",
        "data/source_manifest/void_source_basis_refinement_v2_sky_z_authorized_replay_run_v1.csv",
        "data/derived/void_source_basis_refinement_v2_sky_z_replay_authorization_review_response_v1.csv",
        "data/derived/void_source_basis_refinement_v2_sky_z_replay_authorization_review_response_v1_summary.csv",
        "data/derived/void_source_basis_refinement_v2_sky_z_replay_authorization_review_completed_summary_v1.csv",
        "data/derived/void_source_basis_refinement_v2_sky_z_replay_authorization_review_response_v1_validation_log.txt",
        "docs/void_source_basis_refinement_v2_sky_z_replay_authorization_review_response_v1.md",
        "data/derived/void_source_basis_refinement_v2_sky_z_authorized_replay_v1_grid.csv",
        "data/derived/void_source_basis_refinement_v2_sky_z_authorized_replay_v1_summary.csv",
        "scripts/run_void_source_basis_refinement_v2_sky_z_authorized_replay_v1.py",
        "scripts/validate_void_source_basis_refinement_v2_sky_z_authorized_replay_v1.py",
        "docs/void_source_basis_refinement_v2_sky_z_source_audit_v1.md",
        "data/derived/void_source_basis_refinement_v2_sky_z_source_audit_v1.csv",
        "data/derived/void_source_basis_refinement_v2_sky_z_source_audit_v1_summary.csv",
        "scripts/build_void_source_basis_refinement_v2_sky_z_source_audit_v1.py",
        "scripts/validate_void_source_basis_refinement_v2_sky_z_source_audit_v1.py",
        "docs/void_source_basis_refinement_v2_observer_orientation_kernel_v2.md",
        "data/source_manifest/void_source_basis_refinement_v2_observer_orientation_kernel_v2_manifest.csv",
        "data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2.csv",
        "data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2_summary.csv",
        "scripts/build_void_source_basis_refinement_v2_observer_orientation_kernel_v2.py",
        "scripts/validate_void_source_basis_refinement_v2_observer_orientation_kernel_v2.py",
        "docs/void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization.md",
        "data/source_manifest/void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_policy.csv",
        "data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_response_template.csv",
        "data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_template_summary.csv",
        "data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_package.zip",
        "data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_package.zip.sha256",
        "data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_package_manifest.csv",
        "data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_package_summary.csv",
        "scripts/build_void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_template.py",
        "scripts/validate_void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_template.py",
        "scripts/build_void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_package.py",
        "scripts/validate_void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_package.py",
        "docs/void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_review_notes_v1.md",
        "data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_response_v1.csv",
        "data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_response_v1_summary.csv",
        "data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_review_completed_summary_v1.csv",
        "data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_response_v1_validation_log.txt",
        "scripts/validate_void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_response.py",
        "docs/void_source_basis_refinement_v2_observer_orientation_kernel_v2_authorized_replay.md",
        "data/source_manifest/void_source_basis_refinement_v2_observer_orientation_kernel_v2_authorized_replay_run.csv",
        "data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2_authorized_replay_grid.csv",
        "data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2_authorized_replay_summary.csv",
        "scripts/run_void_source_basis_refinement_v2_observer_orientation_kernel_v2_authorized_replay.py",
        "scripts/validate_void_source_basis_refinement_v2_observer_orientation_kernel_v2_authorized_replay.py",
        "docs/void_source_basis_refinement_v2_observer_basis_fast_screen_v1.md",
        "data/source_manifest/void_source_basis_refinement_v2_observer_basis_fast_screen_v1.csv",
        "data/derived/void_source_basis_refinement_v2_observer_basis_fast_screen_v1_grid.csv",
        "data/derived/void_source_basis_refinement_v2_observer_basis_fast_screen_v1_family_summary.csv",
        "data/derived/void_source_basis_refinement_v2_observer_basis_fast_screen_v1_summary.csv",
        "scripts/run_void_source_basis_refinement_v2_observer_basis_fast_screen_v1.py",
        "scripts/validate_void_source_basis_refinement_v2_observer_basis_fast_screen_v1.py",
        "docs/void_source_basis_refinement_v2_observer_basis_candidate_review_v1.md",
        "data/source_manifest/void_source_basis_refinement_v2_observer_basis_candidate_review_policy_v1.csv",
        "data/derived/void_source_basis_refinement_v2_observer_basis_candidate_review_response_template_v1.csv",
        "data/derived/void_source_basis_refinement_v2_observer_basis_candidate_review_package_v1.zip",
        "data/derived/void_source_basis_refinement_v2_observer_basis_candidate_review_package_v1.zip.sha256",
        "data/derived/void_source_basis_refinement_v2_observer_basis_candidate_review_package_v1_manifest.csv",
        "data/derived/void_source_basis_refinement_v2_observer_basis_candidate_review_package_v1_summary.csv",
        "scripts/build_void_source_basis_refinement_v2_observer_basis_candidate_review_package_v1.py",
        "scripts/validate_void_source_basis_refinement_v2_observer_basis_candidate_review_package_v1.py",
        "docs/void_source_basis_refinement_v2_observer_basis_candidate_review_notes_v1.md",
        "data/derived/void_source_basis_refinement_v2_observer_basis_candidate_review_response_v1.csv",
        "data/derived/void_source_basis_refinement_v2_observer_basis_candidate_review_response_v1_summary.csv",
        "data/derived/void_source_basis_refinement_v2_observer_basis_candidate_review_completed_summary_v1.csv",
        "data/derived/void_source_basis_refinement_v2_observer_basis_candidate_review_response_v1_validation_log.txt",
        "scripts/validate_void_source_basis_refinement_v2_observer_basis_candidate_review_response_v1.py",
        "docs/void_source_basis_refinement_v2_observer_basis_replay_authorization_v1.md",
        "data/source_manifest/void_source_basis_refinement_v2_observer_basis_replay_authorization_policy_v1.csv",
        "data/derived/void_source_basis_refinement_v2_observer_basis_replay_authorization_response_template_v1.csv",
        "data/derived/void_source_basis_refinement_v2_observer_basis_replay_authorization_package_v1.zip",
        "data/derived/void_source_basis_refinement_v2_observer_basis_replay_authorization_package_v1.zip.sha256",
        "data/derived/void_source_basis_refinement_v2_observer_basis_replay_authorization_package_v1_manifest.csv",
        "data/derived/void_source_basis_refinement_v2_observer_basis_replay_authorization_package_v1_summary.csv",
        "scripts/build_void_source_basis_refinement_v2_observer_basis_replay_authorization_package_v1.py",
        "scripts/validate_void_source_basis_refinement_v2_observer_basis_replay_authorization_package_v1.py",
        "docs/void_source_basis_refinement_v2_observer_basis_replay_authorization_review_notes_v1.md",
        "data/derived/void_source_basis_refinement_v2_observer_basis_replay_authorization_response_v1.csv",
        "data/derived/void_source_basis_refinement_v2_observer_basis_replay_authorization_response_v1_summary.csv",
        "data/derived/void_source_basis_refinement_v2_observer_basis_replay_authorization_review_completed_summary_v1.csv",
        "data/derived/void_source_basis_refinement_v2_observer_basis_replay_authorization_response_v1_validation_log.txt",
        "scripts/validate_void_source_basis_refinement_v2_observer_basis_replay_authorization_response_v1.py",
        "docs/void_source_basis_refinement_v2_observer_basis_authorized_replay_v1.md",
        "data/source_manifest/void_source_basis_refinement_v2_observer_basis_authorized_replay_run_v1.csv",
        "data/derived/void_source_basis_refinement_v2_observer_basis_authorized_replay_v1_grid.csv",
        "data/derived/void_source_basis_refinement_v2_observer_basis_authorized_replay_v1_summary.csv",
        "scripts/run_void_source_basis_refinement_v2_observer_basis_authorized_replay_v1.py",
        "scripts/validate_void_source_basis_refinement_v2_observer_basis_authorized_replay_v1.py",
        "docs/void_source_basis_refinement_v2_full_kernel_proxy_fast_screen_v1.md",
        "data/source_manifest/void_source_basis_refinement_v2_full_kernel_proxy_fast_screen_v1.csv",
        "data/derived/void_source_basis_refinement_v2_full_kernel_proxy_fast_screen_v1_grid.csv",
        "data/derived/void_source_basis_refinement_v2_full_kernel_proxy_fast_screen_v1_family_summary.csv",
        "data/derived/void_source_basis_refinement_v2_full_kernel_proxy_fast_screen_v1_summary.csv",
        "scripts/run_void_source_basis_refinement_v2_full_kernel_proxy_fast_screen_v1.py",
        "scripts/validate_void_source_basis_refinement_v2_full_kernel_proxy_fast_screen_v1.py",
        "docs/void_source_basis_refinement_v2_full_kernel_proxy_component_audit_v1.md",
        "data/derived/void_source_basis_refinement_v2_full_kernel_proxy_component_audit_v1.csv",
        "data/derived/void_source_basis_refinement_v2_full_kernel_proxy_component_audit_v1_class_summary.csv",
        "data/derived/void_source_basis_refinement_v2_full_kernel_proxy_component_audit_v1_summary.csv",
        "scripts/build_void_source_basis_refinement_v2_full_kernel_proxy_component_audit_v1.py",
        "scripts/validate_void_source_basis_refinement_v2_full_kernel_proxy_component_audit_v1.py",
        "docs/full_observer_path_kernel_source_requirements_v1.md",
        "data/source_manifest/full_observer_path_kernel_source_requirements_v1.csv",
        "scripts/validate_full_observer_path_kernel_source_requirements_v1.py",
        "docs/low_z_pantheon_los_radial_profile_v1.md",
        "data/source_manifest/low_z_pantheon_los_radial_profile_policy_v1.csv",
        "data/derived/low_z_pantheon_los_radial_profile_v1.csv",
        "data/derived/low_z_pantheon_los_radial_profile_v1_summary.csv",
        "scripts/build_low_z_pantheon_los_radial_profile_v1.py",
        "scripts/validate_low_z_pantheon_los_radial_profile_v1.py",
        "docs/low_z_pantheon_path_aware_void_geometry_v1.md",
        "data/source_manifest/low_z_pantheon_path_aware_void_geometry_policy_v1.csv",
        "data/derived/low_z_pantheon_path_aware_void_geometry_v1.csv",
        "data/derived/low_z_pantheon_path_aware_void_geometry_v1_summary.csv",
        "scripts/build_low_z_pantheon_path_aware_void_geometry_v1.py",
        "scripts/validate_low_z_pantheon_path_aware_void_geometry_v1.py",
        "docs/low_z_pantheon_directional_web_anisotropy_v1.md",
        "data/source_manifest/low_z_pantheon_directional_web_anisotropy_policy_v1.csv",
        "data/derived/low_z_pantheon_directional_web_anisotropy_v1.csv",
        "data/derived/low_z_pantheon_directional_web_anisotropy_v1_summary.csv",
        "scripts/build_low_z_pantheon_directional_web_anisotropy_v1.py",
        "scripts/validate_low_z_pantheon_directional_web_anisotropy_v1.py",
        "docs/low_z_pantheon_metric_lensing_path_route_audit_v1.md",
        "data/source_manifest/low_z_pantheon_metric_lensing_path_route_audit_policy_v1.csv",
        "data/derived/low_z_pantheon_metric_lensing_path_route_audit_v1.csv",
        "data/derived/low_z_pantheon_metric_lensing_path_route_audit_v1_summary.csv",
        "scripts/build_low_z_pantheon_metric_lensing_path_route_audit_v1.py",
        "scripts/validate_low_z_pantheon_metric_lensing_path_route_audit_v1.py",
        "docs/low_z_pantheon_time_readout_source_audit_v1.md",
        "data/source_manifest/low_z_pantheon_time_readout_source_audit_policy_v1.csv",
        "data/derived/low_z_pantheon_time_readout_source_audit_v1.csv",
        "data/derived/low_z_pantheon_time_readout_source_audit_v1_summary.csv",
        "scripts/build_low_z_pantheon_time_readout_source_audit_v1.py",
        "scripts/validate_low_z_pantheon_time_readout_source_audit_v1.py",
        "docs/low_z_pantheon_time_readout_clock_scale_candidate_v1.md",
        "data/source_manifest/low_z_pantheon_time_readout_clock_scale_candidate_policy_v1.csv",
        "data/derived/low_z_pantheon_time_readout_clock_scale_candidate_v1.csv",
        "data/derived/low_z_pantheon_time_readout_clock_scale_candidate_v1_summary.csv",
        "scripts/build_low_z_pantheon_time_readout_clock_scale_candidate_v1.py",
        "scripts/validate_low_z_pantheon_time_readout_clock_scale_candidate_v1.py",
        "docs/low_z_pantheon_time_readout_redshift_bin_policy_candidate_v1.md",
        "data/source_manifest/low_z_pantheon_time_readout_redshift_bin_policy_candidate_policy_v1.csv",
        "data/derived/low_z_pantheon_time_readout_redshift_bin_policy_candidate_v1.csv",
        "data/derived/low_z_pantheon_time_readout_redshift_bin_policy_candidate_v1_summary.csv",
        "scripts/build_low_z_pantheon_time_readout_redshift_bin_policy_candidate_v1.py",
        "scripts/validate_low_z_pantheon_time_readout_redshift_bin_policy_candidate_v1.py",
        "docs/low_z_pantheon_time_readout_delta_clock_uncertainty_candidate_v1.md",
        "data/source_manifest/low_z_pantheon_time_readout_delta_clock_uncertainty_candidate_policy_v1.csv",
        "data/derived/low_z_pantheon_time_readout_delta_clock_uncertainty_candidate_v1.csv",
        "data/derived/low_z_pantheon_time_readout_delta_clock_uncertainty_candidate_v1_summary.csv",
        "scripts/build_low_z_pantheon_time_readout_delta_clock_uncertainty_candidate_v1.py",
        "scripts/validate_low_z_pantheon_time_readout_delta_clock_uncertainty_candidate_v1.py",
        "docs/low_z_pantheon_w_time_uncertainty_basis_candidate_v1.md",
        "data/source_manifest/low_z_pantheon_w_time_uncertainty_basis_candidate_policy_v1.csv",
        "data/derived/low_z_pantheon_w_time_uncertainty_basis_candidate_v1.csv",
        "data/derived/low_z_pantheon_w_time_uncertainty_basis_candidate_v1_summary.csv",
        "scripts/build_low_z_pantheon_w_time_uncertainty_basis_candidate_v1.py",
        "scripts/validate_low_z_pantheon_w_time_uncertainty_basis_candidate_v1.py",
        "docs/low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_v1.md",
        "data/source_manifest/low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_policy_v1.csv",
        "data/derived/low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_response_template_v1.csv",
        "data/derived/low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_template_v1_summary.csv",
        "data/derived/low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_package_v1.zip",
        "data/derived/low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_package_v1.zip.sha256",
        "data/derived/low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_package_v1_manifest.csv",
        "data/derived/low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_package_v1_summary.csv",
        "data/derived/low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_response_v1.csv",
        "data/derived/low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_response_v1_summary.csv",
        "data/derived/low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_completed_summary_v1.csv",
        "data/derived/low_z_pantheon_w_time_uncertainty_basis_replay_authorization_validation_log_v1.txt",
        "docs/low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_notes_v1.md",
        "scripts/build_low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_template_v1.py",
        "scripts/validate_low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_template_v1.py",
        "scripts/build_low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_package_v1.py",
        "scripts/validate_low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_package_v1.py",
        "scripts/validate_low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_response_v1.py",
        "scripts/import_low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_response_v1.py",
        "docs/low_z_pantheon_w_time_uncertainty_basis_replay_run_template_v1.md",
        "data/source_manifest/low_z_pantheon_w_time_uncertainty_basis_replay_run_template_v1.csv",
        "data/derived/low_z_pantheon_w_time_uncertainty_basis_authorized_replay_v1_grid.csv",
        "data/derived/low_z_pantheon_w_time_uncertainty_basis_authorized_replay_v1_summary.csv",
        "scripts/run_low_z_pantheon_w_time_uncertainty_basis_authorized_replay_v1.py",
        "scripts/validate_low_z_pantheon_w_time_uncertainty_basis_authorized_replay_v1.py",
        "docs/low_z_pantheon_w_time_uncertainty_basis_gate_status_ledger_v1.md",
        "data/derived/low_z_pantheon_w_time_uncertainty_basis_gate_status_ledger_v1.csv",
        "data/derived/low_z_pantheon_w_time_uncertainty_basis_gate_status_ledger_v1_summary.csv",
        "scripts/build_low_z_pantheon_w_time_uncertainty_basis_gate_status_ledger_v1.py",
        "scripts/validate_low_z_pantheon_w_time_uncertainty_basis_gate_status_ledger_v1.py",
        "docs/low_z_pantheon_observer_time_combined_fast_screen_v1.md",
        "data/source_manifest/low_z_pantheon_observer_time_combined_fast_screen_v1.csv",
        "data/derived/low_z_pantheon_observer_time_combined_fast_screen_v1_grid.csv",
        "data/derived/low_z_pantheon_observer_time_combined_fast_screen_v1_family_summary.csv",
        "data/derived/low_z_pantheon_observer_time_combined_fast_screen_v1_summary.csv",
        "scripts/run_low_z_pantheon_observer_time_combined_fast_screen_v1.py",
        "scripts/validate_low_z_pantheon_observer_time_combined_fast_screen_v1.py",
        "docs/low_z_pantheon_time_readout_clock_rate_phase_candidate_v1.md",
        "data/source_manifest/low_z_pantheon_time_readout_clock_rate_phase_candidate_policy_v1.csv",
        "data/derived/low_z_pantheon_time_readout_clock_rate_phase_candidate_v1.csv",
        "data/derived/low_z_pantheon_time_readout_clock_rate_phase_candidate_v1_summary.csv",
        "scripts/build_low_z_pantheon_time_readout_clock_rate_phase_candidate_v1.py",
        "scripts/validate_low_z_pantheon_time_readout_clock_rate_phase_candidate_v1.py",
        "docs/low_z_pantheon_clock_rate_phase_fast_screen_v1.md",
        "data/source_manifest/low_z_pantheon_clock_rate_phase_fast_screen_v1.csv",
        "data/derived/low_z_pantheon_clock_rate_phase_fast_screen_v1_grid.csv",
        "data/derived/low_z_pantheon_clock_rate_phase_fast_screen_v1_family_summary.csv",
        "data/derived/low_z_pantheon_clock_rate_phase_fast_screen_v1_summary.csv",
        "scripts/run_low_z_pantheon_clock_rate_phase_fast_screen_v1.py",
        "scripts/validate_low_z_pantheon_clock_rate_phase_fast_screen_v1.py",
        "docs/low_z_pantheon_clock_rate_phase_rank_control_audit_v1.md",
        "data/source_manifest/low_z_pantheon_clock_rate_phase_rank_control_audit_v1.csv",
        "data/derived/low_z_pantheon_clock_rate_phase_rank_control_audit_v1.csv",
        "data/derived/low_z_pantheon_clock_rate_phase_rank_control_audit_v1_summary.csv",
        "scripts/build_low_z_pantheon_clock_rate_phase_rank_control_audit_v1.py",
        "scripts/validate_low_z_pantheon_clock_rate_phase_rank_control_audit_v1.py",
        "docs/pantheon_time_readout_clock_rate_phase_cc_support_candidate_v1.md",
        "data/source_manifest/pantheon_time_readout_clock_rate_phase_cc_support_candidate_policy_v1.csv",
        "data/derived/pantheon_time_readout_clock_rate_phase_cc_support_candidate_v1.csv",
        "data/derived/pantheon_time_readout_clock_rate_phase_cc_support_candidate_v1_summary.csv",
        "scripts/build_pantheon_time_readout_clock_rate_phase_cc_support_candidate_v1.py",
        "scripts/validate_pantheon_time_readout_clock_rate_phase_cc_support_candidate_v1.py",
        "docs/pantheon_clock_rate_phase_cc_support_fast_screen_v1.md",
        "data/source_manifest/pantheon_clock_rate_phase_cc_support_fast_screen_v1.csv",
        "data/derived/pantheon_clock_rate_phase_cc_support_fast_screen_v1_grid.csv",
        "data/derived/pantheon_clock_rate_phase_cc_support_fast_screen_v1_family_summary.csv",
        "data/derived/pantheon_clock_rate_phase_cc_support_fast_screen_v1_summary.csv",
        "scripts/run_pantheon_clock_rate_phase_cc_support_fast_screen_v1.py",
        "scripts/validate_pantheon_clock_rate_phase_cc_support_fast_screen_v1.py",
        "docs/pantheon_clock_slope_route_gate_v1.md",
        "data/source_manifest/pantheon_clock_slope_route_gate_policy_v1.csv",
        "data/derived/pantheon_clock_slope_route_gate_v1.csv",
        "scripts/build_pantheon_clock_slope_route_gate_v1.py",
        "scripts/validate_pantheon_clock_slope_route_gate_v1.py",
        "docs/pantheon_clock_slope_route_replay_authorization_review_v1.md",
        "data/source_manifest/pantheon_clock_slope_route_replay_authorization_review_policy_v1.csv",
        "data/derived/pantheon_clock_slope_route_replay_authorization_review_response_template_v1.csv",
        "data/derived/pantheon_clock_slope_route_replay_authorization_review_template_v1_summary.csv",
        "data/derived/pantheon_clock_slope_route_replay_authorization_review_package_v1.zip",
        "data/derived/pantheon_clock_slope_route_replay_authorization_review_package_v1.zip.sha256",
        "data/derived/pantheon_clock_slope_route_replay_authorization_review_package_v1_manifest.csv",
        "data/derived/pantheon_clock_slope_route_replay_authorization_review_package_v1_summary.csv",
        "scripts/build_pantheon_clock_slope_route_replay_authorization_review_template_v1.py",
        "scripts/validate_pantheon_clock_slope_route_replay_authorization_review_template_v1.py",
        "scripts/build_pantheon_clock_slope_route_replay_authorization_review_package_v1.py",
        "scripts/validate_pantheon_clock_slope_route_replay_authorization_review_package_v1.py",
        "docs/sdss_bao_time_readout_observable_route_audit_v1.md",
        "data/source_manifest/sdss_bao_time_readout_observable_route_audit_policy_v1.csv",
        "data/derived/sdss_bao_time_readout_observable_route_audit_v1.csv",
        "data/derived/sdss_bao_time_readout_observable_route_audit_v1_summary.csv",
        "scripts/build_sdss_bao_time_readout_observable_route_audit_v1.py",
        "scripts/validate_sdss_bao_time_readout_observable_route_audit_v1.py",
        "docs/paper10_joint_cc_bao_time_route_consistency_audit_v1.md",
        "data/source_manifest/paper10_joint_cc_bao_time_route_consistency_audit_policy_v1.csv",
        "data/derived/paper10_joint_cc_bao_time_route_consistency_audit_v1.csv",
        "data/derived/paper10_joint_cc_bao_time_route_consistency_audit_v1_summary.csv",
        "scripts/build_paper10_joint_cc_bao_time_route_consistency_audit_v1.py",
        "scripts/validate_paper10_joint_cc_bao_time_route_consistency_audit_v1.py",
        "docs/paper10_time_readout_route_synthesis_gate_v1.md",
        "data/source_manifest/paper10_time_readout_route_synthesis_gate_v1.csv",
        "data/derived/paper10_time_readout_route_synthesis_gate_v1.csv",
        "scripts/build_paper10_time_readout_route_synthesis_gate_v1.py",
        "scripts/validate_paper10_time_readout_route_synthesis_gate_v1.py",
        "docs/paper10_time_readout_level_slope_route_split_ledger_v1.md",
        "data/source_manifest/paper10_time_readout_level_slope_route_split_ledger_policy_v1.csv",
        "data/derived/paper10_time_readout_level_slope_route_split_ledger_v1.csv",
        "data/derived/paper10_time_readout_level_slope_route_split_ledger_v1_summary.csv",
        "scripts/build_paper10_time_readout_level_slope_route_split_ledger_v1.py",
        "scripts/validate_paper10_time_readout_level_slope_route_split_ledger_v1.py",
        "docs/paper10_time_level_route_nuisance_interface_freeze_plan_v1.md",
        "data/source_manifest/paper10_time_level_route_nuisance_interface_freeze_plan_v1.csv",
        "data/derived/paper10_time_level_route_nuisance_interface_freeze_plan_v1_summary.csv",
        "scripts/validate_paper10_time_level_route_nuisance_interface_freeze_plan_v1.py",
        "docs/paper10_bao_rd_cancelled_time_level_difference_audit_v1.md",
        "data/source_manifest/paper10_bao_rd_cancelled_time_level_difference_audit_policy_v1.csv",
        "data/derived/paper10_bao_rd_cancelled_time_level_difference_audit_v1.csv",
        "data/derived/paper10_bao_rd_cancelled_time_level_difference_audit_v1_summary.csv",
        "scripts/build_paper10_bao_rd_cancelled_time_level_difference_audit_v1.py",
        "scripts/validate_paper10_bao_rd_cancelled_time_level_difference_audit_v1.py",
        "docs/paper10_time_level_rd_policy_selection_gate_v1.md",
        "data/source_manifest/paper10_time_level_rd_policy_selection_gate_v1.csv",
        "data/derived/paper10_time_level_rd_policy_selection_gate_v1_summary.csv",
        "scripts/validate_paper10_time_level_rd_policy_selection_gate_v1.py",
        "docs/paper10_external_rd_prior_freeze_protocol_v1.md",
        "data/source_manifest/paper10_external_rd_prior_freeze_protocol_v1.csv",
        "data/derived/paper10_external_rd_prior_freeze_response_template_v1.csv",
        "data/derived/paper10_external_rd_prior_freeze_protocol_v1_summary.csv",
        "scripts/validate_paper10_external_rd_prior_freeze_protocol_v1.py",
        "docs/paper10_external_rd_prior_freeze_response_v1.md",
        "data/derived/paper10_external_rd_prior_freeze_response_v1.csv",
        "data/derived/paper10_external_rd_prior_freeze_response_v1_summary.csv",
        "scripts/validate_paper10_external_rd_prior_freeze_response_v1.py",
        "docs/paper10_bao_rd_marginalization_protocol_v1.md",
        "data/source_manifest/paper10_bao_rd_marginalization_protocol_v1.csv",
        "data/derived/paper10_bao_rd_marginalization_protocol_v1_summary.csv",
        "scripts/validate_paper10_bao_rd_marginalization_protocol_v1.py",
        "docs/paper10_time_level_endpoint_control_suite_protocol_v1.md",
        "data/source_manifest/paper10_time_level_endpoint_control_suite_protocol_v1.csv",
        "data/derived/paper10_time_level_endpoint_control_suite_protocol_v1_summary.csv",
        "scripts/validate_paper10_time_level_endpoint_control_suite_protocol_v1.py",
        "docs/paper10_time_level_bao_support_expansion_manifest_v1.md",
        "data/source_manifest/paper10_time_level_bao_support_expansion_manifest_v1.csv",
        "data/derived/paper10_time_level_bao_support_expansion_manifest_v1_summary.csv",
        "scripts/validate_paper10_time_level_bao_support_expansion_manifest_v1.py",
        "docs/paper10_desi_dr2_bao_source_inventory_v1.md",
        "data/source_manifest/paper10_desi_dr2_bao_source_inventory_policy_v1.csv",
        "data/raw/desi_dr2_bao/desi_gaussian_bao_ALL_GCcomb_mean.txt",
        "data/raw/desi_dr2_bao/desi_gaussian_bao_ALL_GCcomb_cov.txt",
        "data/derived/paper10_desi_dr2_bao_source_inventory_v1.csv",
        "data/derived/paper10_desi_dr2_bao_source_inventory_v1_summary.csv",
        "scripts/build_paper10_desi_dr2_bao_source_inventory_v1.py",
        "scripts/validate_paper10_desi_dr2_bao_source_inventory_v1.py",
        "docs/paper10_desi_dr2_radial_bao_time_interface_v1.md",
        "data/source_manifest/paper10_desi_dr2_radial_bao_time_interface_policy_v1.csv",
        "data/derived/paper10_desi_dr2_radial_bao_time_interface_v1.csv",
        "data/derived/paper10_desi_dr2_radial_bao_time_interface_covariance_v1.csv",
        "data/derived/paper10_desi_dr2_radial_bao_time_interface_v1_summary.csv",
        "scripts/build_paper10_desi_dr2_radial_bao_time_interface_v1.py",
        "scripts/validate_paper10_desi_dr2_radial_bao_time_interface_v1.py",
        "docs/paper10_desi_dr2_radial_bao_cc_match_v1.md",
        "data/source_manifest/paper10_desi_dr2_radial_bao_cc_match_policy_v1.csv",
        "data/derived/paper10_desi_dr2_radial_bao_cc_match_v1.csv",
        "data/derived/paper10_desi_dr2_radial_bao_cc_match_v1_summary.csv",
        "scripts/build_paper10_desi_dr2_radial_bao_cc_match_v1.py",
        "scripts/validate_paper10_desi_dr2_radial_bao_cc_match_v1.py",
        "docs/paper10_desi_dr2_high_z_bao_policy_v1.md",
        "data/source_manifest/paper10_desi_dr2_high_z_bao_policy_v1.csv",
        "data/derived/paper10_desi_dr2_high_z_bao_policy_v1_summary.csv",
        "scripts/validate_paper10_desi_dr2_high_z_bao_policy_v1.py",
        "docs/paper10_desi_time_level_control_seed_manifest_v1.md",
        "data/source_manifest/paper10_desi_time_level_control_seed_manifest_v1.csv",
        "data/derived/paper10_desi_time_level_control_seed_manifest_v1_summary.csv",
        "scripts/validate_paper10_desi_time_level_control_seed_manifest_v1.py",
        "docs/paper10_time_level_route_external_rd_readiness_gate_v1.md",
        "data/source_manifest/paper10_time_level_route_external_rd_readiness_gate_v1.csv",
        "data/derived/paper10_time_level_route_external_rd_readiness_gate_v1.csv",
        "data/derived/paper10_time_level_route_external_rd_readiness_gate_v1_summary.csv",
        "scripts/build_paper10_time_level_route_external_rd_readiness_gate_v1.py",
        "scripts/validate_paper10_time_level_route_external_rd_readiness_gate_v1.py",
        "docs/paper10_desi_time_level_endpoint_authorization_review_v1.md",
        "data/source_manifest/paper10_desi_time_level_endpoint_authorization_review_policy_v1.csv",
        "data/derived/paper10_desi_time_level_endpoint_authorization_review_response_template_v1.csv",
        "data/derived/paper10_desi_time_level_endpoint_authorization_review_template_v1_summary.csv",
        "data/derived/paper10_desi_time_level_endpoint_authorization_review_package_v1.zip",
        "data/derived/paper10_desi_time_level_endpoint_authorization_review_package_v1.zip.sha256",
        "data/derived/paper10_desi_time_level_endpoint_authorization_review_package_v1_manifest.csv",
        "data/derived/paper10_desi_time_level_endpoint_authorization_review_package_v1_summary.csv",
        "scripts/build_paper10_desi_time_level_endpoint_authorization_review_template_v1.py",
        "scripts/validate_paper10_desi_time_level_endpoint_authorization_review_template_v1.py",
        "scripts/build_paper10_desi_time_level_endpoint_authorization_review_package_v1.py",
        "scripts/validate_paper10_desi_time_level_endpoint_authorization_review_package_v1.py",
        "scripts/validate_paper10_desi_time_level_endpoint_authorization_review_response_v1.py",
        "scripts/import_paper10_desi_time_level_endpoint_authorization_review_response_v1.py",
        "docs/paper10_desi_time_level_endpoint_authorization_review_response_v1.md",
        "data/derived/paper10_desi_time_level_endpoint_authorization_review_response_v1.csv",
        "data/derived/paper10_desi_time_level_endpoint_authorization_review_response_v1_summary.csv",
        "docs/paper10_desi_time_level_endpoint_replay_run_template_v1.md",
        "data/source_manifest/paper10_desi_time_level_endpoint_replay_run_template_v1.csv",
        "scripts/validate_paper10_desi_time_level_endpoint_replay_run_template_v1.py",
        "docs/paper10_desi_time_level_endpoint_authorized_replay_v1.md",
        "data/derived/paper10_desi_time_level_endpoint_authorized_replay_v1_grid.csv",
        "data/derived/paper10_desi_time_level_endpoint_authorized_replay_v1_summary.csv",
        "scripts/run_paper10_desi_time_level_endpoint_authorized_replay_v1.py",
        "scripts/validate_paper10_desi_time_level_endpoint_authorized_replay_v1.py",
        "docs/paper10_desi_time_level_negative_control_diagnostic_v1.md",
        "data/derived/paper10_desi_time_level_negative_control_diagnostic_v1_rows.csv",
        "data/derived/paper10_desi_time_level_negative_control_diagnostic_v1_branches.csv",
        "data/derived/paper10_desi_time_level_negative_control_diagnostic_v1_summary.csv",
        "paper10_submission_source/figures/fig_desi_time_level_negative_control_diagnostic.pdf",
        "scripts/build_paper10_desi_time_level_negative_control_diagnostic_v1.py",
        "scripts/validate_paper10_desi_time_level_negative_control_diagnostic_v1.py",
        "docs/paper10_desi_time_level_negative_control_response_gate_v1.md",
        "data/source_manifest/paper10_desi_time_level_negative_control_response_gate_v1.csv",
        "data/derived/paper10_desi_time_level_negative_control_response_gate_v1.csv",
        "data/derived/paper10_desi_time_level_negative_control_response_gate_v1_summary.csv",
        "scripts/build_paper10_desi_time_level_negative_control_response_gate_v1.py",
        "scripts/validate_paper10_desi_time_level_negative_control_response_gate_v1.py",
        "docs/paper10_desi_time_readout_expansion_manifest_v1.md",
        "data/source_manifest/paper10_desi_time_readout_expansion_manifest_v1.csv",
        "data/derived/paper10_desi_time_readout_expansion_manifest_v1_summary.csv",
        "scripts/validate_paper10_desi_time_readout_expansion_manifest_v1.py",
        "docs/paper10_desi_high_z_independent_clock_support_audit_v1.md",
        "data/source_manifest/paper10_desi_high_z_independent_clock_support_audit_policy_v1.csv",
        "data/derived/paper10_desi_high_z_independent_clock_support_audit_v1.csv",
        "data/derived/paper10_desi_high_z_independent_clock_support_audit_v1_summary.csv",
        "scripts/build_paper10_desi_high_z_independent_clock_support_audit_v1.py",
        "scripts/validate_paper10_desi_high_z_independent_clock_support_audit_v1.py",
        "docs/paper10_desi_time_readout_shape_observable_gate_v1.md",
        "data/source_manifest/paper10_desi_time_readout_shape_observable_gate_policy_v1.csv",
        "data/derived/paper10_desi_time_readout_shape_observable_gate_v1.csv",
        "data/derived/paper10_desi_time_readout_shape_observable_gate_v1_summary.csv",
        "scripts/build_paper10_desi_time_readout_shape_observable_gate_v1.py",
        "scripts/validate_paper10_desi_time_readout_shape_observable_gate_v1.py",
        "docs/paper10_desi_time_readout_shape_projection_induction_v1.md",
        "data/source_manifest/paper10_desi_time_readout_shape_projection_induction_policy_v1.csv",
        "data/derived/paper10_desi_time_readout_shape_projection_induction_v1.csv",
        "data/derived/paper10_desi_time_readout_shape_projection_induction_v1_summary.csv",
        "scripts/build_paper10_desi_time_readout_shape_projection_induction_v1.py",
        "scripts/validate_paper10_desi_time_readout_shape_projection_induction_v1.py",
        "docs/paper10_desi_ordering_control_suite_v1.md",
        "data/source_manifest/paper10_desi_ordering_control_suite_policy_v1.csv",
        "data/derived/paper10_desi_ordering_control_suite_v1.csv",
        "data/derived/paper10_desi_ordering_control_suite_v1_summary.csv",
        "scripts/build_paper10_desi_ordering_control_suite_v1.py",
        "scripts/validate_paper10_desi_ordering_control_suite_v1.py",
        "docs/paper10_desi_cc_window_stress_binding_v1.md",
        "data/source_manifest/paper10_desi_cc_window_stress_binding_policy_v1.csv",
        "data/derived/paper10_desi_cc_window_stress_binding_v1.csv",
        "data/derived/paper10_desi_cc_window_stress_binding_v1_summary.csv",
        "scripts/build_paper10_desi_cc_window_stress_binding_v1.py",
        "scripts/validate_paper10_desi_cc_window_stress_binding_v1.py",
        "docs/paper10_desi_shape_bound_control_vectors_v1.md",
        "data/source_manifest/paper10_desi_shape_bound_control_vectors_policy_v1.csv",
        "data/derived/paper10_desi_shape_bound_control_vectors_v1.csv",
        "data/derived/paper10_desi_shape_bound_control_vectors_v1_summary.csv",
        "scripts/build_paper10_desi_shape_bound_control_vectors_v1.py",
        "scripts/validate_paper10_desi_shape_bound_control_vectors_v1.py",
        "docs/paper10_desi_multi_clock_support_per_bao_row_audit_v1.md",
        "data/source_manifest/paper10_desi_multi_clock_support_per_bao_row_audit_policy_v1.csv",
        "data/derived/paper10_desi_multi_clock_support_per_bao_row_audit_v1.csv",
        "data/derived/paper10_desi_multi_clock_support_per_bao_row_audit_v1_summary.csv",
        "scripts/build_paper10_desi_multi_clock_support_per_bao_row_audit_v1.py",
        "scripts/validate_paper10_desi_multi_clock_support_per_bao_row_audit_v1.py",
        "docs/paper10_desi_time_readout_shape_independent_review_v1.md",
        "data/source_manifest/paper10_desi_time_readout_shape_independent_review_policy_v1.csv",
        "data/derived/paper10_desi_time_readout_shape_independent_review_response_template_v1.csv",
        "data/derived/paper10_desi_time_readout_shape_independent_review_package_v1.zip",
        "data/derived/paper10_desi_time_readout_shape_independent_review_package_v1.zip.sha256",
        "data/derived/paper10_desi_time_readout_shape_independent_review_package_v1_manifest.csv",
        "data/derived/paper10_desi_time_readout_shape_independent_review_package_v1_summary.csv",
        "scripts/build_paper10_desi_time_readout_shape_independent_review_package_v1.py",
        "scripts/validate_paper10_desi_time_readout_shape_independent_review_package_v1.py",
        "scripts/validate_paper10_desi_time_readout_shape_independent_review_response_v1.py",
        "scripts/import_paper10_desi_time_readout_shape_independent_review_response_v1.py",
        "docs/paper10_desi_shape_route_replay_authorization_review_v1.md",
        "data/source_manifest/paper10_desi_shape_route_replay_authorization_review_policy_v1.csv",
        "data/derived/paper10_desi_shape_route_replay_authorization_review_response_template_v1.csv",
        "data/derived/paper10_desi_shape_route_replay_authorization_review_package_v1.zip",
        "data/derived/paper10_desi_shape_route_replay_authorization_review_package_v1.zip.sha256",
        "data/derived/paper10_desi_shape_route_replay_authorization_review_package_v1_manifest.csv",
        "data/derived/paper10_desi_shape_route_replay_authorization_review_package_v1_summary.csv",
        "data/derived/paper10_desi_shape_route_replay_authorization_review_response_v1.csv",
        "data/derived/paper10_desi_shape_route_replay_authorization_review_response_v1_summary.csv",
        "data/derived/paper10_desi_shape_route_replay_authorization_review_completed_summary_v1.csv",
        "data/derived/paper10_desi_shape_route_replay_authorization_validation_log_v1.txt",
        "docs/paper10_desi_shape_route_replay_authorization_review_notes_v1.md",
        "scripts/build_paper10_desi_shape_route_replay_authorization_review_package_v1.py",
        "scripts/validate_paper10_desi_shape_route_replay_authorization_review_package_v1.py",
        "scripts/validate_paper10_desi_shape_route_replay_authorization_review_response_v1.py",
        "scripts/import_paper10_desi_shape_route_replay_authorization_review_response_v1.py",
        "docs/paper10_desi_shape_route_replay_run_template_v1.md",
        "data/source_manifest/paper10_desi_shape_route_replay_run_template_v1.csv",
        "scripts/validate_paper10_desi_shape_route_replay_run_template_v1.py",
        "data/derived/paper10_desi_shape_route_authorized_replay_v1_grid.csv",
        "data/derived/paper10_desi_shape_route_authorized_replay_v1_summary.csv",
        "scripts/run_paper10_desi_shape_route_authorized_replay_v1.py",
        "scripts/validate_paper10_desi_shape_route_authorized_replay_v1.py",
        "docs/paper10_desi_shape_route_robustness_stress_v1.md",
        "data/source_manifest/paper10_desi_shape_route_robustness_stress_policy_v1.csv",
        "data/derived/paper10_desi_shape_route_robustness_stress_v1.csv",
        "data/derived/paper10_desi_shape_route_robustness_stress_v1_summary.csv",
        "paper10_submission_source/figures/fig_desi_shape_route_robustness_stress.pdf",
        "scripts/build_paper10_desi_shape_route_robustness_stress_v1.py",
        "scripts/validate_paper10_desi_shape_route_robustness_stress_v1.py",
        "scripts/build_paper10_desi_shape_route_robustness_figure_v1.py",
        "scripts/validate_paper10_desi_shape_route_robustness_figure_v1.py",
        "docs/paper10_desi_shape_row_sensitivity_source_audit_v1.md",
        "data/source_manifest/paper10_desi_shape_row_sensitivity_source_audit_policy_v1.csv",
        "data/derived/paper10_desi_shape_row_sensitivity_source_audit_v1.csv",
        "data/derived/paper10_desi_shape_row_sensitivity_source_audit_v1_summary.csv",
        "scripts/build_paper10_desi_shape_row_sensitivity_source_audit_v1.py",
        "scripts/validate_paper10_desi_shape_row_sensitivity_source_audit_v1.py",
        "docs/paper10_desi_shape_core_source_acquisition_manifest_v1.md",
        "data/source_manifest/paper10_desi_shape_core_source_acquisition_manifest_policy_v1.csv",
        "data/derived/paper10_desi_shape_core_source_acquisition_manifest_v1.csv",
        "data/derived/paper10_desi_shape_core_source_acquisition_manifest_v1_summary.csv",
        "scripts/build_paper10_desi_shape_core_source_acquisition_manifest_v1.py",
        "scripts/validate_paper10_desi_shape_core_source_acquisition_manifest_v1.py",
        "docs/paper10_desi_shape_core_source_support_scan_v1.md",
        "data/source_manifest/paper10_desi_shape_core_source_support_scan_policy_v1.csv",
        "data/derived/paper10_desi_shape_core_source_support_scan_v1.csv",
        "data/derived/paper10_desi_shape_core_source_support_scan_v1_summary.csv",
        "scripts/build_paper10_desi_shape_core_source_support_scan_v1.py",
        "scripts/validate_paper10_desi_shape_core_source_support_scan_v1.py",
        "docs/paper10_desi_shape_row1_confirmatory_source_attachment_v1.md",
        "data/source_manifest/paper10_desi_shape_row1_confirmatory_source_attachment_policy_v1.csv",
        "data/derived/paper10_desi_shape_row1_confirmatory_source_attachment_v1.csv",
        "data/derived/paper10_desi_shape_row1_confirmatory_source_attachment_v1_summary.csv",
        "scripts/build_paper10_desi_shape_row1_confirmatory_source_attachment_v1.py",
        "scripts/validate_paper10_desi_shape_row1_confirmatory_source_attachment_v1.py",
        "docs/paper10_desi_shape_row1_confirmatory_source_review_v1.md",
        "data/source_manifest/paper10_desi_shape_row1_confirmatory_source_review_policy_v1.csv",
        "data/derived/paper10_desi_shape_row1_confirmatory_source_review_response_template_v1.csv",
        "data/derived/paper10_desi_shape_row1_confirmatory_source_review_package_v1.zip",
        "data/derived/paper10_desi_shape_row1_confirmatory_source_review_package_v1.zip.sha256",
        "data/derived/paper10_desi_shape_row1_confirmatory_source_review_package_v1_manifest.csv",
        "data/derived/paper10_desi_shape_row1_confirmatory_source_review_package_v1_summary.csv",
        "scripts/build_paper10_desi_shape_row1_confirmatory_source_review_package_v1.py",
        "scripts/validate_paper10_desi_shape_row1_confirmatory_source_review_package_v1.py",
        "scripts/validate_paper10_desi_shape_row1_confirmatory_source_review_response_v1.py",
        "scripts/import_paper10_desi_shape_row1_confirmatory_source_review_response_v1.py",
        "data/derived/paper10_desi_shape_row1_confirmatory_source_review_response_v1.csv",
        "data/derived/paper10_desi_shape_row1_confirmatory_source_review_response_v1_summary.csv",
        "data/derived/paper10_desi_shape_row1_confirmatory_source_review_completed_summary_v1.csv",
        "data/derived/paper10_desi_shape_row1_confirmatory_source_review_validation_log_v1.txt",
        "docs/paper10_desi_shape_row1_confirmatory_source_review_notes_v1.md",
        "docs/paper10_desi_shape_row2_moresco2012_source_attachment_v1.md",
        "data/source_manifest/paper10_desi_shape_row2_moresco2012_source_attachment_policy_v1.csv",
        "data/derived/paper10_desi_shape_row2_moresco2012_source_attachment_v1.csv",
        "data/derived/paper10_desi_shape_row2_moresco2012_source_attachment_v1_summary.csv",
        "scripts/build_paper10_desi_shape_row2_moresco2012_source_attachment_v1.py",
        "scripts/validate_paper10_desi_shape_row2_moresco2012_source_attachment_v1.py",
        "docs/paper10_desi_shape_row2_moresco2012_source_attachment_review_v1.md",
        "data/source_manifest/paper10_desi_shape_row2_moresco2012_source_attachment_review_policy_v1.csv",
        "data/derived/paper10_desi_shape_row2_moresco2012_source_attachment_review_response_template_v1.csv",
        "data/derived/paper10_desi_shape_row2_moresco2012_source_attachment_review_package_v1.zip",
        "data/derived/paper10_desi_shape_row2_moresco2012_source_attachment_review_package_v1.zip.sha256",
        "data/derived/paper10_desi_shape_row2_moresco2012_source_attachment_review_package_v1_manifest.csv",
        "data/derived/paper10_desi_shape_row2_moresco2012_source_attachment_review_package_v1_summary.csv",
        "scripts/build_paper10_desi_shape_row2_moresco2012_source_attachment_review_package_v1.py",
        "scripts/validate_paper10_desi_shape_row2_moresco2012_source_attachment_review_package_v1.py",
        "scripts/validate_paper10_desi_shape_row2_moresco2012_source_attachment_review_response_v1.py",
        "scripts/import_paper10_desi_shape_row2_moresco2012_source_attachment_review_response_v1.py",
        "data/derived/paper10_desi_shape_row2_moresco2012_source_attachment_review_response_v1.csv",
        "data/derived/paper10_desi_shape_row2_moresco2012_source_attachment_review_response_v1_summary.csv",
        "docs/paper10_desi_shape_row2_moresco2012_source_attachment_review_notes_v1.md",
        "data/derived/paper10_desi_shape_row2_moresco2012_source_attachment_review_validation_log_v1.txt",
        "docs/paper10_desi_shape_row2_promotion_readiness_gate_v1.md",
        "data/source_manifest/paper10_desi_shape_row2_promotion_readiness_gate_policy_v1.csv",
        "data/derived/paper10_desi_shape_row2_promotion_readiness_gate_v1.csv",
        "data/derived/paper10_desi_shape_row2_promotion_readiness_gate_v1_summary.csv",
        "scripts/build_paper10_desi_shape_row2_promotion_readiness_gate_v1.py",
        "scripts/validate_paper10_desi_shape_row2_promotion_readiness_gate_v1.py",
        "docs/paper10_desi_shape_row2_endpoint_pair_independence_scout_v1.md",
        "data/source_manifest/paper10_desi_shape_row2_endpoint_pair_independence_scout_policy_v1.csv",
        "data/derived/paper10_desi_shape_row2_endpoint_pair_independence_scout_v1.csv",
        "data/derived/paper10_desi_shape_row2_endpoint_pair_independence_scout_v1_summary.csv",
        "scripts/build_paper10_desi_shape_row2_endpoint_pair_independence_scout_v1.py",
        "scripts/validate_paper10_desi_shape_row2_endpoint_pair_independence_scout_v1.py",
        "docs/paper10_desi_shape_row2_left_endpoint_nearmiss_freeze_v1.md",
        "data/source_manifest/paper10_desi_shape_row2_left_endpoint_nearmiss_freeze_policy_v1.csv",
        "data/derived/paper10_desi_shape_row2_left_endpoint_nearmiss_freeze_v1.csv",
        "data/derived/paper10_desi_shape_row2_left_endpoint_nearmiss_freeze_v1_summary.csv",
        "scripts/build_paper10_desi_shape_row2_left_endpoint_nearmiss_freeze_v1.py",
        "scripts/validate_paper10_desi_shape_row2_left_endpoint_nearmiss_freeze_v1.py",
        "docs/paper10_desi_shape_row2_left_endpoint_window_review_v1.md",
        "data/source_manifest/paper10_desi_shape_row2_left_endpoint_window_review_policy_v1.csv",
        "data/derived/paper10_desi_shape_row2_left_endpoint_window_review_response_template_v1.csv",
        "data/derived/paper10_desi_shape_row2_left_endpoint_window_review_package_v1.zip",
        "data/derived/paper10_desi_shape_row2_left_endpoint_window_review_package_v1.zip.sha256",
        "data/derived/paper10_desi_shape_row2_left_endpoint_window_review_package_v1_manifest.csv",
        "data/derived/paper10_desi_shape_row2_left_endpoint_window_review_package_v1_summary.csv",
        "scripts/build_paper10_desi_shape_row2_left_endpoint_window_review_package_v1.py",
        "scripts/validate_paper10_desi_shape_row2_left_endpoint_window_review_package_v1.py",
        "scripts/validate_paper10_desi_shape_row2_left_endpoint_window_review_response_v1.py",
        "scripts/import_paper10_desi_shape_row2_left_endpoint_window_review_response_v1.py",
        "data/derived/paper10_desi_shape_row2_left_endpoint_window_review_response_v1.csv",
        "data/derived/paper10_desi_shape_row2_left_endpoint_window_review_response_v1_summary.csv",
        "docs/paper10_desi_shape_row2_left_endpoint_window_review_notes_v1.md",
        "data/derived/paper10_desi_shape_row2_left_endpoint_window_review_validation_log_v1.txt",
        "docs/paper10_desi_shape_row2_left_endpoint_window_decision_gate_v1.md",
        "data/source_manifest/paper10_desi_shape_row2_left_endpoint_window_decision_gate_policy_v1.csv",
        "data/derived/paper10_desi_shape_row2_left_endpoint_window_decision_gate_v1.csv",
        "data/derived/paper10_desi_shape_row2_left_endpoint_window_decision_gate_v1_summary.csv",
        "scripts/build_paper10_desi_shape_row2_left_endpoint_window_decision_gate_v1.py",
        "scripts/validate_paper10_desi_shape_row2_left_endpoint_window_decision_gate_v1.py",
        "docs/paper10_desi_shape_row2_post_window_review_source_plan_v1.md",
        "data/source_manifest/paper10_desi_shape_row2_post_window_review_source_plan_policy_v1.csv",
        "data/derived/paper10_desi_shape_row2_post_window_review_source_plan_v1.csv",
        "data/derived/paper10_desi_shape_row2_post_window_review_source_plan_v1_summary.csv",
        "scripts/build_paper10_desi_shape_row2_post_window_review_source_plan_v1.py",
        "scripts/validate_paper10_desi_shape_row2_post_window_review_source_plan_v1.py",
        "docs/paper10_desi_shape_row2_left_strict_support_scout_v1.md",
        "data/source_manifest/paper10_desi_shape_row2_left_strict_support_scout_policy_v1.csv",
        "data/derived/paper10_desi_shape_row2_left_strict_support_scout_v1.csv",
        "data/derived/paper10_desi_shape_row2_left_strict_support_scout_v1_summary.csv",
        "scripts/build_paper10_desi_shape_row2_left_strict_support_scout_v1.py",
        "scripts/validate_paper10_desi_shape_row2_left_strict_support_scout_v1.py",
        "docs/paper10_desi_shape_row2_source_native_shape_support_scout_v1.md",
        "data/source_manifest/paper10_desi_shape_row2_source_native_shape_support_scout_policy_v1.csv",
        "data/derived/paper10_desi_shape_row2_source_native_shape_support_scout_v1.csv",
        "data/derived/paper10_desi_shape_row2_source_native_shape_support_scout_v1_summary.csv",
        "scripts/build_paper10_desi_shape_row2_source_native_shape_support_scout_v1.py",
        "scripts/validate_paper10_desi_shape_row2_source_native_shape_support_scout_v1.py",
        "docs/paper10_desi_shape_row2_source_native_shape_support_review_v1.md",
        "data/source_manifest/paper10_desi_shape_row2_source_native_shape_support_review_policy_v1.csv",
        "data/derived/paper10_desi_shape_row2_source_native_shape_support_review_response_template_v1.csv",
        "data/derived/paper10_desi_shape_row2_source_native_shape_support_review_package_v1.zip",
        "data/derived/paper10_desi_shape_row2_source_native_shape_support_review_package_v1.zip.sha256",
        "data/derived/paper10_desi_shape_row2_source_native_shape_support_review_package_v1_manifest.csv",
        "data/derived/paper10_desi_shape_row2_source_native_shape_support_review_package_v1_summary.csv",
        "scripts/build_paper10_desi_shape_row2_source_native_shape_support_review_package_v1.py",
        "scripts/validate_paper10_desi_shape_row2_source_native_shape_support_review_package_v1.py",
        "scripts/validate_paper10_desi_shape_row2_source_native_shape_support_review_response_v1.py",
        "scripts/import_paper10_desi_shape_row2_source_native_shape_support_review_response_v1.py",
        "data/derived/paper10_desi_shape_row2_source_native_shape_support_review_response_v1.csv",
        "data/derived/paper10_desi_shape_row2_source_native_shape_support_review_response_v1_summary.csv",
        "docs/paper10_desi_shape_row2_source_native_shape_support_review_notes_v1.md",
        "data/derived/paper10_desi_shape_row2_source_native_shape_support_review_validation_log_v1.txt",
        "docs/paper10_desi_shape_row2_gate_status_ledger_v1.md",
        "data/source_manifest/paper10_desi_shape_row2_gate_status_ledger_policy_v1.csv",
        "data/derived/paper10_desi_shape_row2_gate_status_ledger_v1.csv",
        "data/derived/paper10_desi_shape_row2_gate_status_ledger_v1_summary.csv",
        "scripts/build_paper10_desi_shape_row2_gate_status_ledger_v1.py",
        "scripts/validate_paper10_desi_shape_row2_gate_status_ledger_v1.py",
        "docs/paper10_desi_shape_row2_promotion_review_v1.md",
        "data/source_manifest/paper10_desi_shape_row2_promotion_review_policy_v1.csv",
        "data/derived/paper10_desi_shape_row2_promotion_review_response_template_v1.csv",
        "data/derived/paper10_desi_shape_row2_promotion_review_package_v1.zip",
        "data/derived/paper10_desi_shape_row2_promotion_review_package_v1.zip.sha256",
        "data/derived/paper10_desi_shape_row2_promotion_review_package_v1_manifest.csv",
        "data/derived/paper10_desi_shape_row2_promotion_review_package_v1_summary.csv",
        "scripts/build_paper10_desi_shape_row2_promotion_review_package_v1.py",
        "scripts/validate_paper10_desi_shape_row2_promotion_review_package_v1.py",
        "scripts/validate_paper10_desi_shape_row2_promotion_review_response_v1.py",
        "scripts/import_paper10_desi_shape_row2_promotion_review_response_v1.py",
        "data/derived/paper10_desi_shape_row2_promotion_review_response_v1.csv",
        "data/derived/paper10_desi_shape_row2_promotion_review_response_v1_summary.csv",
        "docs/paper10_desi_shape_row2_promotion_review_notes_v1.md",
        "data/derived/paper10_desi_shape_row2_promotion_review_validation_log_v1.txt",
        "docs/paper10_desi_shape_row2_replay_authorization_review_v1.md",
        "data/source_manifest/paper10_desi_shape_row2_replay_authorization_review_policy_v1.csv",
        "data/derived/paper10_desi_shape_row2_replay_authorization_review_response_template_v1.csv",
        "data/derived/paper10_desi_shape_row2_replay_authorization_review_package_v1.zip",
        "data/derived/paper10_desi_shape_row2_replay_authorization_review_package_v1.zip.sha256",
        "data/derived/paper10_desi_shape_row2_replay_authorization_review_package_v1_manifest.csv",
        "data/derived/paper10_desi_shape_row2_replay_authorization_review_package_v1_summary.csv",
        "scripts/build_paper10_desi_shape_row2_replay_authorization_review_package_v1.py",
        "scripts/validate_paper10_desi_shape_row2_replay_authorization_review_package_v1.py",
        "scripts/validate_paper10_desi_shape_row2_replay_authorization_review_response_v1.py",
        "scripts/import_paper10_desi_shape_row2_replay_authorization_review_response_v1.py",
        "data/derived/paper10_desi_shape_row2_replay_authorization_review_response_v1.csv",
        "data/derived/paper10_desi_shape_row2_replay_authorization_review_response_v1_summary.csv",
        "data/derived/paper10_desi_shape_row2_replay_authorization_review_completed_summary_v1.csv",
        "data/derived/paper10_desi_shape_row2_replay_authorization_review_validation_log_v1.txt",
        "docs/paper10_desi_shape_row2_replay_authorization_review_notes_v1.md",
        "data/source_manifest/paper10_desi_shape_row2_authorized_replay_run_v1.csv",
        "data/derived/paper10_desi_shape_row2_authorized_replay_v1_grid.csv",
        "data/derived/paper10_desi_shape_row2_authorized_replay_v1_summary.csv",
        "docs/paper10_desi_shape_row2_authorized_replay_v1.md",
        "scripts/run_paper10_desi_shape_row2_authorized_replay_v1.py",
        "scripts/validate_paper10_desi_shape_row2_authorized_replay_v1.py",
        "docs/paper10_desi_shape_core_support_synthesis_gate_v1.md",
        "data/source_manifest/paper10_desi_shape_core_support_synthesis_gate_policy_v1.csv",
        "data/derived/paper10_desi_shape_core_support_synthesis_gate_v1.csv",
        "data/derived/paper10_desi_shape_core_support_synthesis_gate_v1_summary.csv",
        "scripts/build_paper10_desi_shape_core_support_synthesis_gate_v1.py",
        "scripts/validate_paper10_desi_shape_core_support_synthesis_gate_v1.py",
        "docs/paper10_desi_shape_route_source_synthesis_review_v1.md",
        "data/source_manifest/paper10_desi_shape_route_source_synthesis_review_policy_v1.csv",
        "data/derived/paper10_desi_shape_route_source_synthesis_review_response_template_v1.csv",
        "data/derived/paper10_desi_shape_route_source_synthesis_review_package_v1.zip",
        "data/derived/paper10_desi_shape_route_source_synthesis_review_package_v1.zip.sha256",
        "data/derived/paper10_desi_shape_route_source_synthesis_review_package_v1_manifest.csv",
        "data/derived/paper10_desi_shape_route_source_synthesis_review_package_v1_summary.csv",
        "scripts/build_paper10_desi_shape_route_source_synthesis_review_package_v1.py",
        "scripts/validate_paper10_desi_shape_route_source_synthesis_review_package_v1.py",
        "data/derived/paper10_desi_shape_route_source_synthesis_review_response_v1.csv",
        "data/derived/paper10_desi_shape_route_source_synthesis_review_response_v1_summary.csv",
        "data/derived/paper10_desi_shape_route_source_synthesis_review_completed_summary_v1.csv",
        "data/derived/paper10_desi_shape_route_source_synthesis_review_validation_log_v1.txt",
        "docs/paper10_desi_shape_route_source_synthesis_review_notes_v1.md",
        "scripts/import_paper10_desi_shape_route_source_synthesis_review_response_v1.py",
        "scripts/validate_paper10_desi_shape_route_source_synthesis_review_response_v1.py",
        "docs/paper10_desi_shape_post_synthesis_gate_authorization_review_v1.md",
        "data/source_manifest/paper10_desi_shape_post_synthesis_gate_authorization_review_policy_v1.csv",
        "data/derived/paper10_desi_shape_post_synthesis_gate_authorization_review_response_template_v1.csv",
        "data/derived/paper10_desi_shape_post_synthesis_gate_authorization_review_package_v1.zip",
        "data/derived/paper10_desi_shape_post_synthesis_gate_authorization_review_package_v1.zip.sha256",
        "data/derived/paper10_desi_shape_post_synthesis_gate_authorization_review_package_v1_manifest.csv",
        "data/derived/paper10_desi_shape_post_synthesis_gate_authorization_review_package_v1_summary.csv",
        "scripts/build_paper10_desi_shape_post_synthesis_gate_authorization_review_package_v1.py",
        "scripts/validate_paper10_desi_shape_post_synthesis_gate_authorization_review_package_v1.py",
        "data/derived/paper10_desi_shape_post_synthesis_gate_authorization_review_response_v1.csv",
        "data/derived/paper10_desi_shape_post_synthesis_gate_authorization_review_response_v1_summary.csv",
        "data/derived/paper10_desi_shape_post_synthesis_gate_authorization_review_completed_summary_v1.csv",
        "data/derived/paper10_desi_shape_post_synthesis_gate_authorization_review_validation_log_v1.txt",
        "docs/paper10_desi_shape_post_synthesis_gate_authorization_review_notes_v1.md",
        "scripts/import_paper10_desi_shape_post_synthesis_gate_authorization_review_response_v1.py",
        "scripts/validate_paper10_desi_shape_post_synthesis_gate_authorization_review_response_v1.py",
        "docs/paper10_desi_shape_validation_oriented_gate_review_v1.md",
        "data/source_manifest/paper10_desi_shape_validation_oriented_gate_review_policy_v1.csv",
        "data/derived/paper10_desi_shape_validation_oriented_gate_review_response_template_v1.csv",
        "data/derived/paper10_desi_shape_validation_oriented_gate_review_package_v1.zip",
        "data/derived/paper10_desi_shape_validation_oriented_gate_review_package_v1.zip.sha256",
        "data/derived/paper10_desi_shape_validation_oriented_gate_review_package_v1_manifest.csv",
        "data/derived/paper10_desi_shape_validation_oriented_gate_review_package_v1_summary.csv",
        "scripts/build_paper10_desi_shape_validation_oriented_gate_review_package_v1.py",
        "scripts/validate_paper10_desi_shape_validation_oriented_gate_review_package_v1.py",
        "data/derived/paper10_desi_shape_validation_oriented_gate_review_response_v1.csv",
        "data/derived/paper10_desi_shape_validation_oriented_gate_review_response_v1_summary.csv",
        "data/derived/paper10_desi_shape_validation_oriented_gate_review_completed_summary_v1.csv",
        "data/derived/paper10_desi_shape_validation_oriented_gate_review_validation_log_v1.txt",
        "docs/paper10_desi_shape_validation_oriented_gate_review_notes_v1.md",
        "scripts/import_paper10_desi_shape_validation_oriented_gate_review_response_v1.py",
        "scripts/validate_paper10_desi_shape_validation_oriented_gate_review_response_v1.py",
        "docs/paper10_desi_shape_validation_permission_replay_authorization_review_v1.md",
        "data/source_manifest/paper10_desi_shape_validation_permission_replay_authorization_review_policy_v1.csv",
        "data/derived/paper10_desi_shape_validation_permission_replay_authorization_review_response_template_v1.csv",
        "data/derived/paper10_desi_shape_validation_permission_replay_authorization_review_package_v1.zip",
        "data/derived/paper10_desi_shape_validation_permission_replay_authorization_review_package_v1.zip.sha256",
        "data/derived/paper10_desi_shape_validation_permission_replay_authorization_review_package_v1_manifest.csv",
        "data/derived/paper10_desi_shape_validation_permission_replay_authorization_review_package_v1_summary.csv",
        "scripts/build_paper10_desi_shape_validation_permission_replay_authorization_review_package_v1.py",
        "scripts/validate_paper10_desi_shape_validation_permission_replay_authorization_review_package_v1.py",
        "data/derived/paper10_desi_shape_validation_permission_replay_authorization_review_response_v1.csv",
        "data/derived/paper10_desi_shape_validation_permission_replay_authorization_review_response_v1_summary.csv",
        "data/derived/paper10_desi_shape_validation_permission_replay_authorization_review_completed_summary_v1.csv",
        "data/derived/paper10_desi_shape_validation_permission_replay_authorization_review_validation_log_v1.txt",
        "docs/paper10_desi_shape_validation_permission_replay_authorization_review_notes_v1.md",
        "scripts/import_paper10_desi_shape_validation_permission_replay_authorization_review_response_v1.py",
        "scripts/validate_paper10_desi_shape_validation_permission_replay_authorization_review_response_v1.py",
        "data/derived/paper10_desi_shape_validation_permission_authorized_replay_v1_grid.csv",
        "data/derived/paper10_desi_shape_validation_permission_authorized_replay_v1_summary.csv",
        "scripts/run_paper10_desi_shape_validation_permission_authorized_replay_v1.py",
        "scripts/validate_paper10_desi_shape_validation_permission_authorized_replay_v1.py",
        "docs/paper10_desi_clock_support_acquisition_manifest_v1.md",
        "data/source_manifest/paper10_desi_clock_support_acquisition_manifest_policy_v1.csv",
        "data/derived/paper10_desi_clock_support_acquisition_manifest_v1.csv",
        "data/derived/paper10_desi_clock_support_acquisition_manifest_v1_summary.csv",
        "scripts/build_paper10_desi_clock_support_acquisition_manifest_v1.py",
        "scripts/validate_paper10_desi_clock_support_acquisition_manifest_v1.py",
        "docs/paper10_desi_clock_support_source_candidate_scan_v1.md",
        "data/source_manifest/paper10_desi_clock_support_source_candidate_scan_policy_v1.csv",
        "data/derived/paper10_desi_clock_support_source_candidate_scan_v1.csv",
        "data/derived/paper10_desi_clock_support_source_candidate_scan_v1_summary.csv",
        "scripts/build_paper10_desi_clock_support_source_candidate_scan_v1.py",
        "scripts/validate_paper10_desi_clock_support_source_candidate_scan_v1.py",
        "docs/paper10_desi_clock_support_blocker_verdict_v1.md",
        "data/source_manifest/paper10_desi_clock_support_blocker_verdict_policy_v1.csv",
        "data/derived/paper10_desi_clock_support_blocker_verdict_v1.csv",
        "data/derived/paper10_desi_clock_support_blocker_verdict_v1_summary.csv",
        "scripts/build_paper10_desi_clock_support_blocker_verdict_v1.py",
        "scripts/validate_paper10_desi_clock_support_blocker_verdict_v1.py",
        "docs/paper10_desi_row4_clock_reopen_manifest_v1.md",
        "data/source_manifest/paper10_desi_row4_clock_reopen_manifest_policy_v1.csv",
        "data/derived/paper10_desi_row4_clock_reopen_manifest_v1.csv",
        "data/derived/paper10_desi_row4_clock_reopen_manifest_v1_summary.csv",
        "scripts/build_paper10_desi_row4_clock_reopen_manifest_v1.py",
        "scripts/validate_paper10_desi_row4_clock_reopen_manifest_v1.py",
        "docs/paper10_desi_row4_cc_bracket_source_freeze_v1.md",
        "data/source_manifest/paper10_desi_row4_cc_bracket_source_freeze_policy_v1.csv",
        "data/derived/paper10_desi_row4_cc_bracket_source_freeze_v1.csv",
        "data/derived/paper10_desi_row4_cc_bracket_source_freeze_v1_summary.csv",
        "scripts/build_paper10_desi_row4_cc_bracket_source_freeze_v1.py",
        "scripts/validate_paper10_desi_row4_cc_bracket_source_freeze_v1.py",
        "docs/paper10_desi_row4_non_simon_clock_search_v1.md",
        "data/source_manifest/paper10_desi_row4_non_simon_clock_search_policy_v1.csv",
        "data/derived/paper10_desi_row4_non_simon_clock_search_v1.csv",
        "data/derived/paper10_desi_row4_non_simon_clock_search_v1_summary.csv",
        "scripts/build_paper10_desi_row4_non_simon_clock_search_v1.py",
        "scripts/validate_paper10_desi_row4_non_simon_clock_search_v1.py",
        "docs/paper10_desi_row4_window_review_v1.md",
        "data/source_manifest/paper10_desi_row4_window_review_policy_v1.csv",
        "data/derived/paper10_desi_row4_window_review_response_template_v1.csv",
        "data/derived/paper10_desi_row4_window_review_package_v1.zip",
        "data/derived/paper10_desi_row4_window_review_package_v1.zip.sha256",
        "data/derived/paper10_desi_row4_window_review_package_v1_manifest.csv",
        "data/derived/paper10_desi_row4_window_review_package_v1_summary.csv",
        "scripts/build_paper10_desi_row4_window_review_package_v1.py",
        "scripts/validate_paper10_desi_row4_window_review_package_v1.py",
        "scripts/validate_paper10_desi_row4_window_review_response_v1.py",
        "scripts/import_paper10_desi_row4_window_review_response_v1.py",
        "docs/paper10_desi_row4_window_decision_gate_v1.md",
        "data/source_manifest/paper10_desi_row4_window_decision_gate_policy_v1.csv",
        "data/derived/paper10_desi_row4_window_decision_gate_v1.csv",
        "data/derived/paper10_desi_row4_window_decision_gate_v1_summary.csv",
        "scripts/build_paper10_desi_row4_window_decision_gate_v1.py",
        "scripts/validate_paper10_desi_row4_window_decision_gate_v1.py",
        "docs/paper10_desi_time_route_closure_status_v1.md",
        "data/source_manifest/paper10_desi_time_route_closure_status_policy_v1.csv",
        "data/derived/paper10_desi_time_route_closure_status_v1.csv",
        "data/derived/paper10_desi_time_route_closure_status_v1_summary.csv",
        "scripts/build_paper10_desi_time_route_closure_status_v1.py",
        "scripts/validate_paper10_desi_time_route_closure_status_v1.py",
        "docs/paper10_desi_row5_high_z_review_v1.md",
        "data/source_manifest/paper10_desi_row5_high_z_review_policy_v1.csv",
        "data/derived/paper10_desi_row5_high_z_review_response_template_v1.csv",
        "data/derived/paper10_desi_row5_high_z_review_package_v1.zip",
        "data/derived/paper10_desi_row5_high_z_review_package_v1.zip.sha256",
        "data/derived/paper10_desi_row5_high_z_review_package_v1_manifest.csv",
        "data/derived/paper10_desi_row5_high_z_review_package_v1_summary.csv",
        "scripts/build_paper10_desi_row5_high_z_review_package_v1.py",
        "scripts/validate_paper10_desi_row5_high_z_review_package_v1.py",
        "scripts/validate_paper10_desi_row5_high_z_review_response_v1.py",
        "scripts/import_paper10_desi_row5_high_z_review_response_v1.py",
        "docs/paper10_desi_row5_high_z_decision_gate_v1.md",
        "data/source_manifest/paper10_desi_row5_high_z_decision_gate_policy_v1.csv",
        "data/derived/paper10_desi_row5_high_z_decision_gate_v1.csv",
        "data/derived/paper10_desi_row5_high_z_decision_gate_v1_summary.csv",
        "scripts/build_paper10_desi_row5_high_z_decision_gate_v1.py",
        "scripts/validate_paper10_desi_row5_high_z_decision_gate_v1.py",
        "data/derived/void_source_basis_refinement_v2_path_projection_route_ledger.csv",
        "data/derived/void_source_basis_refinement_v2_path_projection_route_ledger_summary.csv",
        "data/derived/void_source_basis_refinement_v2_time_readout_route_ledger.csv",
        "data/derived/void_source_basis_refinement_v2_time_readout_route_ledger_summary.csv",
        "data/derived/void_source_basis_refinement_v2_multichannel_coupling_ledger.csv",
        "data/derived/void_source_basis_refinement_v2_multichannel_coupling_ledger_summary.csv",
        "data/derived/void_source_basis_refinement_v2_projection_morphology_gate_v1.csv",
        "data/derived/void_source_basis_refinement_v2_projection_morphology_gate_v1_summary.csv",
        "scripts/build_void_source_basis_refinement_endpoint_replay_authorization_review_template_v1.py",
        "scripts/validate_void_source_basis_refinement_endpoint_replay_authorization_review_template_v1.py",
        "scripts/build_void_source_basis_refinement_endpoint_replay_authorization_review_package_v1.py",
        "scripts/validate_void_source_basis_refinement_endpoint_replay_authorization_review_package_v1.py",
        "scripts/validate_void_source_basis_refinement_endpoint_replay_authorization_review_response_v1.py",
        "scripts/run_void_source_basis_refinement_authorized_replay_v1.py",
        "scripts/validate_void_source_basis_refinement_authorized_replay_v1.py",
        "scripts/build_void_source_basis_refinement_control_dominance_audit_v1.py",
        "scripts/validate_void_source_basis_refinement_control_dominance_audit_v1.py",
        "scripts/build_void_source_basis_refinement_v2_void_morphology_values_v1.py",
        "scripts/validate_void_source_basis_refinement_v2_void_morphology_values_v1.py",
        "scripts/build_void_source_basis_refinement_v2_web_morphology_values_v1.py",
        "scripts/validate_void_source_basis_refinement_v2_web_morphology_values_v1.py",
        "scripts/build_void_source_basis_refinement_v2_cmb_safety_values_v1.py",
        "scripts/validate_void_source_basis_refinement_v2_cmb_safety_values_v1.py",
        "scripts/build_void_source_basis_refinement_v2_path_projection_crossmap_audit_v1.py",
        "scripts/validate_void_source_basis_refinement_v2_path_projection_crossmap_audit_v1.py",
        "scripts/build_void_source_basis_refinement_v2_path_partial_scope_policy_v1.py",
        "scripts/validate_void_source_basis_refinement_v2_path_partial_scope_policy_v1.py",
        "scripts/build_void_source_basis_refinement_v2_path_partial_scope_values_v1.py",
        "scripts/validate_void_source_basis_refinement_v2_path_partial_scope_values_v1.py",
        "scripts/build_void_source_basis_refinement_v2_path_partial_scope_reviewer_package_v1.py",
        "scripts/validate_void_source_basis_refinement_v2_path_partial_scope_reviewer_package_v1.py",
        "scripts/validate_void_source_basis_refinement_v2_path_partial_scope_completed_review_response_v1.py",
        "scripts/build_void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_template_v1.py",
        "scripts/validate_void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_template_v1.py",
        "scripts/build_void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_package_v1.py",
        "scripts/validate_void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_package_v1.py",
        "scripts/validate_void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_response_v1.py",
        "scripts/run_void_source_basis_refinement_v2_path_partial_scope_authorized_replay_v1.py",
        "scripts/validate_void_source_basis_refinement_v2_path_partial_scope_authorized_replay_v1.py",
        "scripts/build_void_source_basis_refinement_v2_path_projection_route_ledger_v1.py",
        "scripts/validate_void_source_basis_refinement_v2_path_projection_route_ledger_v1.py",
        "scripts/build_void_source_basis_refinement_v2_time_readout_route_ledger_v1.py",
        "scripts/validate_void_source_basis_refinement_v2_time_readout_route_ledger_v1.py",
        "scripts/build_void_source_basis_refinement_v2_multichannel_coupling_ledger_v1.py",
        "scripts/validate_void_source_basis_refinement_v2_multichannel_coupling_ledger_v1.py",
        "scripts/build_void_source_basis_refinement_v2_projection_morphology_gate_v1.py",
        "scripts/validate_void_source_basis_refinement_v2_projection_morphology_gate_v1.py",
        "scripts/build_void_source_basis_refinement_r6_reviewer_template_v1.py",
        "scripts/validate_void_source_basis_refinement_r6_reviewer_template_v1.py",
        "scripts/build_void_source_basis_refinement_r6_reviewer_handoff_package_v1.py",
        "scripts/validate_void_source_basis_refinement_r6_reviewer_handoff_package_v1.py",
        "scripts/validate_void_source_basis_refinement_r6_completed_reviewer_response_v1.py",
        "data/source_manifest/kids1000_lensing_route_v1.csv",
        "data/derived/kids1000_lensing_route_v1_head.csv",
        "data/derived/kids1000_lensing_route_v1_summary.csv",
        "data/source_manifest/kids1000_lensing_products_v1.csv",
        "data/source_manifest/kids1000_cosebis_lensing_route_v1.csv",
        "data/raw/weak_lensing/kids1000/KiDS1000_cosmic_shear_data_release.tgz",
        "data/derived/kids1000_lensing_inventory_v1.csv",
        "data/derived/kids1000_lensing_inventory_v1_summary.csv",
        "data/source_manifest/kids1000_cosebis_hdu_policy_v1.csv",
        "data/derived/kids1000_cosebis_hdu_inventory_v1.csv",
        "data/derived/kids1000_cosebis_hdu_inventory_v1_summary.csv",
        "data/source_manifest/kids1000_cosebis_tomographic_mode_policy_v1.csv",
        "data/derived/kids1000_cosebis_tomographic_mode_inventory_v1.csv",
        "data/derived/kids1000_cosebis_tomographic_mode_inventory_v1_summary.csv",
        "data/source_manifest/kids1000_cosebis_covariance_readiness_policy_v1.csv",
        "data/derived/kids1000_cosebis_covariance_readiness_v1.csv",
        "data/derived/kids1000_cosebis_covariance_readiness_v1_summary.csv",
        "data/source_manifest/kids1000_cosebis_mask_modecut_policy_v1.csv",
        "data/derived/kids1000_cosebis_mask_modecut_inventory_v1.csv",
        "data/derived/kids1000_cosebis_mask_modecut_inventory_v1_summary.csv",
        "data/source_manifest/kids1000_cosebis_tomographic_weight_policy_v1.csv",
        "data/derived/kids1000_cosebis_tomographic_weight_inventory_v1.csv",
        "data/derived/kids1000_cosebis_tomographic_weight_inventory_v1_summary.csv",
        "data/source_manifest/kids1000_cosebis_covariance_subselection_policy_v1.csv",
        "data/derived/kids1000_cosebis_covariance_subselection_inventory_v1.csv",
        "data/derived/kids1000_cosebis_covariance_subselection_inventory_v1_summary.csv",
        "data/source_manifest/kids1000_cosebis_covariance_inversion_policy_v1.csv",
        "data/derived/kids1000_cosebis_covariance_inversion_readiness_v1.csv",
        "data/derived/kids1000_cosebis_covariance_inversion_readiness_v1_summary.csv",
        "data/source_manifest/kids1000_cosebis_theory_vector_policy_v1.csv",
        "data/derived/kids1000_cosebis_theory_vector_readiness_v1.csv",
        "data/derived/kids1000_cosebis_theory_vector_readiness_v1_summary.csv",
        "data/source_manifest/kids1000_cosebis_source_frozen_theory_vector_policy_v1.csv",
        "data/derived/kids1000_cosebis_source_frozen_theory_vector_v1.csv",
        "data/derived/kids1000_cosebis_source_frozen_theory_vector_v1_summary.csv",
        "data/source_manifest/kids1000_cosebis_theory_vector_template_policy_v1.csv",
        "data/derived/kids1000_cosebis_theory_vector_template_v1.csv",
        "data/derived/kids1000_cosebis_theory_vector_template_v1_summary.csv",
        "data/source_manifest/kids1000_cosebis_mapping_template_join_contract_policy_v1.csv",
        "data/derived/kids1000_cosebis_mapping_template_join_contract_v1.csv",
        "data/derived/kids1000_cosebis_mapping_template_join_contract_v1_summary.csv",
        "data/source_manifest/kids1000_cosebis_web_path_mapping_policy_v1.csv",
        "data/derived/kids1000_cosebis_web_path_mapping_readiness_v1.csv",
        "data/derived/kids1000_cosebis_web_path_mapping_readiness_v1_summary.csv",
        "data/source_manifest/kids1000_cosebis_source_frozen_mapping_vector_policy_v1.csv",
        "data/derived/kids1000_cosebis_source_frozen_mapping_domain_weights_v1.csv",
        "data/derived/kids1000_cosebis_source_frozen_mapping_vector_v1.csv",
        "data/derived/kids1000_cosebis_source_frozen_mapping_vector_v1_summary.csv",
        "data/source_manifest/kids1000_cosebis_redshift_kernel_policy_v1.csv",
        "data/derived/kids1000_cosebis_redshift_kernel_inventory_v1.csv",
        "data/derived/kids1000_cosebis_redshift_kernel_inventory_v1_summary.csv",
        "data/source_manifest/kids1000_cosebis_path_mask_depth_gap_policy_v1.csv",
        "data/derived/kids1000_cosebis_path_mask_depth_gap_inventory_v1.csv",
        "data/derived/kids1000_cosebis_path_mask_depth_gap_inventory_v1_summary.csv",
        "data/source_manifest/kids1000_dr4_path_mask_route_scripts_v1.csv",
        "data/raw/weak_lensing/kids1000_path_masks/kids_dr4.1_9band_msk_wget.sh",
        "data/raw/weak_lensing/kids1000_path_masks/kids_dr4.0_9band_msk_wget.sh",
        "data/raw/weak_lensing/kids1000_path_masks/kids_dr4.0_msk_wget.sh",
        "data/derived/kids1000_dr4_path_mask_route_scripts_inventory_v1.csv",
        "data/derived/kids1000_dr4_path_mask_route_scripts_inventory_v1_summary.csv",
        "data/source_manifest/kids1000_dr4_path_mask_route_tile_inventory_policy_v1.csv",
        "data/derived/kids1000_dr4_path_mask_route_tile_inventory_v1.csv",
        "data/derived/kids1000_dr4_path_mask_route_tile_inventory_v1_summary.csv",
        "data/source_manifest/kids1000_dr4_path_mask_head_sample_policy_v1.csv",
        "data/derived/kids1000_dr4_path_mask_head_sample_v1.csv",
        "data/derived/kids1000_dr4_path_mask_head_sample_v1_summary.csv",
        "data/source_manifest/kids1000_dr4_path_mask_subset_policy_v1.csv",
        "data/raw/weak_lensing/kids1000_path_masks/mask_subset_v1/KiDS_DR4.1_0.0_-28.2_ugriZYJHKs_msk.fits.gz",
        "data/raw/weak_lensing/kids1000_path_masks/mask_subset_v1/KiDS_DR4.1_206.0_1.5_ugriZYJHKs_msk.fits.gz",
        "data/raw/weak_lensing/kids1000_path_masks/mask_subset_v1/KiDS_DR4.1_5.6_-28.2_ugriZYJHKs_msk.fits.gz",
        "data/derived/kids1000_dr4_path_mask_subset_inventory_v1.csv",
        "data/derived/kids1000_dr4_path_mask_subset_inventory_v1_summary.csv",
        "data/source_manifest/kids1000_dr4_path_mask_observable_shell_policy_v1.csv",
        "data/derived/kids1000_dr4_path_mask_observable_shell_v1.csv",
        "data/derived/kids1000_dr4_path_mask_observable_shell_v1_summary.csv",
        "data/source_manifest/kids1000_cosebis_path_mapping_design_skeleton_policy_v1.csv",
        "data/derived/kids1000_cosebis_path_mapping_design_skeleton_v1.csv",
        "data/derived/kids1000_cosebis_path_mapping_design_skeleton_v1_summary.csv",
        "data/source_manifest/kids1000_cosebis_path_mapping_domain_skeleton_policy_v1.csv",
        "data/derived/kids1000_cosebis_path_mapping_domain_skeleton_v1.csv",
        "data/derived/kids1000_cosebis_path_mapping_domain_skeleton_v1_summary.csv",
        "data/source_manifest/kids1000_cosebis_path_weight_construction_rule_v1.csv",
        "data/derived/kids1000_cosebis_path_weight_construction_rule_v1.csv",
        "data/derived/kids1000_cosebis_path_weight_construction_rule_v1_summary.csv",
        "data/source_manifest/kids1000_cosebis_path_factor_acquisition_plan_v1.csv",
        "data/derived/kids1000_cosebis_path_factor_acquisition_plan_v1.csv",
        "data/derived/kids1000_cosebis_path_factor_acquisition_plan_v1_summary.csv",
        "data/source_manifest/kids1000_cosebis_path_source_product_route_policy_v1.csv",
        "data/derived/kids1000_cosebis_path_source_product_route_manifest_v1.csv",
        "data/derived/kids1000_cosebis_path_source_product_route_manifest_v1_summary.csv",
        "data/source_manifest/kids1000_cosebis_path_blocker_resolution_order_policy_v1.csv",
        "data/derived/kids1000_cosebis_path_blocker_resolution_order_v1.csv",
        "data/derived/kids1000_cosebis_path_blocker_resolution_order_v1_summary.csv",
        "data/source_manifest/kids1000_cosebis_f_overlap_rule_shell_policy_v1.csv",
        "data/derived/kids1000_cosebis_f_overlap_rule_shell_v1.csv",
        "data/derived/kids1000_cosebis_f_overlap_rule_shell_v1_summary.csv",
        "data/source_manifest/kids1000_cosebis_f_overlap_source_availability_policy_v1.csv",
        "data/derived/kids1000_cosebis_f_overlap_source_availability_v1.csv",
        "data/derived/kids1000_cosebis_f_overlap_source_availability_v1_summary.csv",
        "data/source_manifest/kids1000_cosebis_f_overlap_full_mask_acquisition_policy_v1.csv",
        "data/derived/kids1000_cosebis_f_overlap_full_mask_acquisition_manifest_v1.csv",
        "data/derived/kids1000_cosebis_f_overlap_full_mask_acquisition_manifest_v1_summary.csv",
        "data/source_manifest/kids1000_cosebis_f_overlap_full_mask_batch_plan_policy_v1.csv",
        "data/derived/kids1000_cosebis_f_overlap_full_mask_batch_plan_v1.csv",
        "data/derived/kids1000_cosebis_f_overlap_full_mask_batch_plan_v1_summary.csv",
        "data/source_manifest/kids1000_cosebis_f_overlap_full_mask_batch_dry_run_policy_v1.csv",
        "data/derived/kids1000_cosebis_f_overlap_full_mask_batch_dry_run_v1.csv",
        "data/derived/kids1000_cosebis_f_overlap_full_mask_batch_dry_run_v1_summary.csv",
        "data/source_manifest/kids1000_cosebis_f_overlap_batch_promotion_review_policy_v1.csv",
        "data/derived/kids1000_cosebis_f_overlap_batch_promotion_review_v1.csv",
        "data/derived/kids1000_cosebis_f_overlap_batch_promotion_review_v1_summary.csv",
        "data/source_manifest/kids1000_cosebis_f_overlap_execution_review_schema_policy_v1.csv",
        "data/derived/kids1000_cosebis_f_overlap_execution_review_schema_v1.csv",
        "data/derived/kids1000_cosebis_f_overlap_execution_review_schema_v1_summary.csv",
        "data/source_manifest/kids1000_cosebis_f_overlap_execution_review_template_policy_v1.csv",
        "data/derived/kids1000_cosebis_f_overlap_execution_review_template_v1.csv",
        "data/derived/kids1000_cosebis_f_overlap_execution_review_template_v1_summary.csv",
        "data/source_manifest/kids1000_cosebis_f_overlap_resolution_decision_policy_v1.csv",
        "data/derived/kids1000_cosebis_f_overlap_resolution_decision_v1.csv",
        "data/derived/kids1000_cosebis_f_overlap_resolution_decision_v1_summary.csv",
        "data/source_manifest/kids1000_cosebis_f_overlap_pixel_fraction_pilot_policy_v1.csv",
        "data/derived/kids1000_cosebis_f_overlap_pixel_fraction_pilot_tile_v1.csv",
        "data/derived/kids1000_cosebis_f_overlap_pixel_fraction_pilot_v1_summary.csv",
        "data/source_manifest/kids1000_cosebis_f_overlap_full_route_pixel_fraction_rule_policy_v1.csv",
        "data/derived/kids1000_cosebis_f_overlap_full_route_pixel_fraction_tile_rule_v1.csv",
        "data/derived/kids1000_cosebis_f_overlap_full_route_pixel_fraction_rule_v1.csv",
        "data/derived/kids1000_cosebis_f_overlap_full_route_pixel_fraction_rule_v1_summary.csv",
        "data/source_manifest/kids1000_cosebis_d_path_full_route_mask_load_rule_policy_v1.csv",
        "data/derived/kids1000_cosebis_d_path_full_route_mask_load_tile_rule_v1.csv",
        "data/derived/kids1000_cosebis_d_path_full_route_mask_load_rule_v1.csv",
        "data/derived/kids1000_cosebis_d_path_full_route_mask_load_rule_v1_summary.csv",
        "data/source_manifest/kids1000_cosebis_e_web_null_control_rule_policy_v1.csv",
        "data/derived/kids1000_cosebis_e_web_null_control_tile_rule_v1.csv",
        "data/derived/kids1000_cosebis_e_web_null_control_rule_v1.csv",
        "data/derived/kids1000_cosebis_e_web_null_control_rule_v1_summary.csv",
        "data/source_manifest/kids1000_cosebis_c_norm_source_side_rule_policy_v1.csv",
        "data/derived/kids1000_cosebis_c_norm_source_side_domain_rule_v1.csv",
        "data/derived/kids1000_cosebis_c_norm_source_side_rule_v1_summary.csv",
        "docs/kids1000_cosebis_c_norm_source_side_rule_v1.md",
        "scripts/build_kids1000_cosebis_c_norm_source_side_rule_v1.py",
        "scripts/validate_kids1000_cosebis_c_norm_source_side_rule_v1.py",
        "data/source_manifest/kids1000_cosebis_partial_control_scoring_protocol_v1.csv",
        "data/source_manifest/kids1000_cosebis_partial_control_mapping_shell_policy_v1.csv",
        "data/derived/kids1000_cosebis_partial_control_mapping_shell_v1.csv",
        "data/derived/kids1000_cosebis_partial_control_mapping_shell_v1_summary.csv",
        "data/source_manifest/kids1000_cosebis_partial_control_mapping_values_policy_v1.csv",
        "data/derived/kids1000_cosebis_partial_control_mapping_values_v1.csv",
        "data/derived/kids1000_cosebis_partial_control_mapping_values_v1_summary.csv",
        "data/source_manifest/kids1000_cosebis_partial_control_design_matrix_policy_v1.csv",
        "data/derived/kids1000_cosebis_partial_control_design_matrix_v1.csv",
        "data/derived/kids1000_cosebis_partial_control_design_matrix_v1_summary.csv",
        "data/source_manifest/kids1000_cosebis_partial_control_diagnostic_scoring_v1.csv",
        "data/derived/kids1000_cosebis_partial_control_diagnostic_scoring_v1_grid.csv",
        "data/derived/kids1000_cosebis_partial_control_diagnostic_scoring_v1_summary.csv",
        "data/source_manifest/kids1000_cosebis_partial_control_null_replay_v1.csv",
        "data/derived/kids1000_cosebis_partial_control_null_replay_v1_grid.csv",
        "data/derived/kids1000_cosebis_partial_control_null_replay_v1_summary.csv",
        "data/source_manifest/kids1000_cosebis_partial_control_degeneracy_audit_policy_v1.csv",
        "data/derived/kids1000_cosebis_partial_control_degeneracy_audit_v1_pair_grid.csv",
        "data/derived/kids1000_cosebis_partial_control_degeneracy_audit_v1_summary.csv",
        "data/source_manifest/kids1000_cosebis_non_degenerate_mapping_promotion_gate_policy_v1.csv",
        "data/source_manifest/kids1000_cosebis_endpoint_family_geometry_audit_policy_v1.csv",
        "data/derived/kids1000_cosebis_endpoint_family_geometry_audit_v1.csv",
        "data/derived/kids1000_cosebis_endpoint_family_geometry_audit_v1_summary.csv",
        "data/derived/kids1000_cosebis_non_degenerate_mapping_promotion_gate_v1.csv",
        "data/derived/kids1000_cosebis_non_degenerate_mapping_promotion_gate_v1_summary.csv",
        "docs/kids1000_cosebis_f_overlap_filled_execution_review_validator_v1.md",
        "scripts/validate_kids1000_cosebis_f_overlap_filled_execution_review_artifact_v1.py",
        "data/source_manifest/kids1000_cosebis_endpoint_scoring_readiness_policy_v1.csv",
        "data/derived/kids1000_cosebis_endpoint_scoring_readiness_v1.csv",
        "data/derived/kids1000_cosebis_endpoint_scoring_readiness_v1_summary.csv",
        "docs/kids1000_cosebis_endpoint_scoring_readiness_v1.md",
        "scripts/build_kids1000_cosebis_endpoint_scoring_readiness_v1.py",
        "scripts/validate_kids1000_cosebis_endpoint_scoring_readiness_v1.py",
        "data/source_manifest/kids1000_cosebis_endpoint_scoring_protocol_v1.csv",
        "docs/kids1000_cosebis_endpoint_scoring_protocol_v1.md",
        "scripts/validate_kids1000_cosebis_endpoint_scoring_protocol_v1.py",
        "data/source_manifest/kids1000_cosebis_endpoint_scoring_run_v1.csv",
        "data/derived/kids1000_cosebis_endpoint_scoring_v1_results.csv",
        "data/derived/kids1000_cosebis_endpoint_scoring_v1_residuals.csv",
        "data/derived/kids1000_cosebis_endpoint_scoring_v1_grid.csv",
        "data/derived/kids1000_cosebis_endpoint_scoring_v1_null_controls.csv",
        "data/derived/kids1000_cosebis_endpoint_scoring_v1_summary.csv",
        "docs/kids1000_cosebis_endpoint_scoring_v1.md",
        "scripts/run_kids1000_cosebis_endpoint_scoring_v1.py",
        "scripts/validate_kids1000_cosebis_endpoint_scoring_v1.py",
        "data/source_manifest/kids1000_cosebis_endpoint_scoring_diagnostics_policy_v1.csv",
        "data/derived/kids1000_cosebis_endpoint_scoring_diagnostics_v1_family_summary.csv",
        "data/derived/kids1000_cosebis_endpoint_scoring_diagnostics_v1_top_nulls.csv",
        "data/derived/kids1000_cosebis_endpoint_scoring_diagnostics_v1_summary.csv",
        "scripts/build_kids1000_cosebis_endpoint_scoring_diagnostics_v1.py",
        "scripts/validate_kids1000_cosebis_endpoint_scoring_diagnostics_v1.py",
        "data/source_manifest/kids1000_cosebis_tomographic_structure_robustness_policy_v1.csv",
        "data/derived/kids1000_cosebis_tomographic_structure_robustness_v1_controls.csv",
        "data/derived/kids1000_cosebis_tomographic_structure_robustness_v1_family_summary.csv",
        "data/derived/kids1000_cosebis_tomographic_structure_robustness_v1_top_controls.csv",
        "data/derived/kids1000_cosebis_tomographic_structure_robustness_v1_summary.csv",
        "docs/kids1000_cosebis_tomographic_structure_robustness_v1.md",
        "scripts/run_kids1000_cosebis_tomographic_structure_robustness_v1.py",
        "scripts/validate_kids1000_cosebis_tomographic_structure_robustness_v1.py",
        "data/source_manifest/kids1000_cosebis_tomographic_control_plausibility_audit_policy_v1.csv",
        "data/derived/kids1000_cosebis_tomographic_control_plausibility_audit_v1.csv",
        "data/derived/kids1000_cosebis_tomographic_control_plausibility_audit_v1_summary.csv",
        "docs/kids1000_cosebis_tomographic_control_plausibility_audit_v1.md",
        "scripts/build_kids1000_cosebis_tomographic_control_plausibility_audit_v1.py",
        "scripts/validate_kids1000_cosebis_tomographic_control_plausibility_audit_v1.py",
        "data/source_manifest/kids1000_cosebis_tomographic_control_disambiguation_policy_v1.csv",
        "data/derived/kids1000_cosebis_tomographic_control_disambiguation_v1.csv",
        "data/derived/kids1000_cosebis_tomographic_control_disambiguation_v1_summary.csv",
        "docs/kids1000_cosebis_tomographic_control_disambiguation_v1.md",
        "scripts/build_kids1000_cosebis_tomographic_control_disambiguation_v1.py",
        "scripts/validate_kids1000_cosebis_tomographic_control_disambiguation_v1.py",
        "data/source_manifest/kids1000_cosebis_tomographic_holdout_replay_policy_v1.csv",
        "data/derived/kids1000_cosebis_tomographic_holdout_replay_v1_grid.csv",
        "data/derived/kids1000_cosebis_tomographic_holdout_replay_v1_summary.csv",
        "docs/kids1000_cosebis_tomographic_holdout_replay_v1.md",
        "scripts/run_kids1000_cosebis_tomographic_holdout_replay_v1.py",
        "scripts/validate_kids1000_cosebis_tomographic_holdout_replay_v1.py",
        "data/source_manifest/kids1000_cosebis_best_tomographic_control_source_evidence_gate_policy_v1.csv",
        "data/derived/kids1000_cosebis_best_tomographic_control_source_evidence_gate_v1.csv",
        "data/derived/kids1000_cosebis_best_tomographic_control_source_evidence_gate_v1_summary.csv",
        "docs/kids1000_cosebis_best_tomographic_control_source_evidence_gate_v1.md",
        "scripts/build_kids1000_cosebis_best_tomographic_control_source_evidence_gate_v1.py",
        "scripts/validate_kids1000_cosebis_best_tomographic_control_source_evidence_gate_v1.py",
        "data/source_manifest/kids1000_cosebis_tomographic_holdout_calibration_gate_policy_v1.csv",
        "data/derived/kids1000_cosebis_tomographic_holdout_calibration_gate_v1.csv",
        "data/derived/kids1000_cosebis_tomographic_holdout_calibration_gate_v1_summary.csv",
        "docs/kids1000_cosebis_tomographic_holdout_calibration_gate_v1.md",
        "scripts/build_kids1000_cosebis_tomographic_holdout_calibration_gate_v1.py",
        "scripts/validate_kids1000_cosebis_tomographic_holdout_calibration_gate_v1.py",
        "data/source_manifest/kids1000_cosebis_source_frozen_tomographic_holdout_manifest_policy_v1.csv",
        "data/derived/kids1000_cosebis_source_frozen_tomographic_holdout_bins_v1.csv",
        "data/derived/kids1000_cosebis_source_frozen_tomographic_holdout_pairs_v1.csv",
        "data/derived/kids1000_cosebis_source_frozen_tomographic_holdout_manifest_v1_summary.csv",
        "docs/kids1000_cosebis_source_frozen_tomographic_holdout_manifest_v1.md",
        "scripts/build_kids1000_cosebis_source_frozen_tomographic_holdout_manifest_v1.py",
        "scripts/validate_kids1000_cosebis_source_frozen_tomographic_holdout_manifest_v1.py",
        "data/source_manifest/kids1000_cosebis_photoz_tomographic_calibration_evidence_policy_v1.csv",
        "data/derived/kids1000_cosebis_photoz_tomographic_calibration_evidence_v1.csv",
        "data/derived/kids1000_cosebis_photoz_tomographic_calibration_evidence_v1_summary.csv",
        "docs/kids1000_cosebis_photoz_tomographic_calibration_evidence_v1.md",
        "scripts/build_kids1000_cosebis_photoz_tomographic_calibration_evidence_v1.py",
        "scripts/validate_kids1000_cosebis_photoz_tomographic_calibration_evidence_v1.py",
        "data/source_manifest/kids1000_cosebis_external_photoz_calibration_acquisition_plan_policy_v1.csv",
        "data/derived/kids1000_cosebis_external_photoz_calibration_acquisition_plan_v1.csv",
        "data/derived/kids1000_cosebis_external_photoz_calibration_acquisition_plan_v1_summary.csv",
        "docs/kids1000_cosebis_external_photoz_calibration_acquisition_plan_v1.md",
        "scripts/build_kids1000_cosebis_external_photoz_calibration_acquisition_plan_v1.py",
        "scripts/validate_kids1000_cosebis_external_photoz_calibration_acquisition_plan_v1.py",
        "data/source_manifest/kids1000_cosebis_external_photoz_calibration_source_manifest_policy_v1.csv",
        "data/source_manifest/source_page_cache/kids1000_photoz_calibration_v1/KIDS1000_PHOTOZ_CALIBRATION_AANDA.html",
        "data/source_manifest/source_page_cache/kids1000_photoz_calibration_v1/KIDS1000_PHOTOZ_CALIBRATION_ARXIV.html",
        "data/source_manifest/source_page_cache/kids1000_photoz_calibration_v1/KIDS1000_SOM_GOLD_CATALOGUE.html",
        "data/derived/kids1000_cosebis_external_photoz_calibration_source_manifest_v1.csv",
        "data/derived/kids1000_cosebis_external_photoz_calibration_source_manifest_v1_summary.csv",
        "docs/kids1000_cosebis_external_photoz_calibration_source_manifest_v1.md",
        "scripts/build_kids1000_cosebis_external_photoz_calibration_source_manifest_v1.py",
        "scripts/validate_kids1000_cosebis_external_photoz_calibration_source_manifest_v1.py",
        "data/source_manifest/kids1000_cosebis_external_photoz_calibration_leakage_review_preflight_policy_v1.csv",
        "data/derived/kids1000_cosebis_external_photoz_calibration_leakage_review_preflight_v1.csv",
        "data/derived/kids1000_cosebis_external_photoz_calibration_leakage_review_preflight_v1_summary.csv",
        "docs/kids1000_cosebis_external_photoz_calibration_leakage_review_preflight_v1.md",
        "scripts/build_kids1000_cosebis_external_photoz_calibration_leakage_review_preflight_v1.py",
        "scripts/validate_kids1000_cosebis_external_photoz_calibration_leakage_review_preflight_v1.py",
        "data/source_manifest/kids1000_cosebis_external_photoz_calibration_reviewer_attestation_template_policy_v1.csv",
        "data/derived/kids1000_cosebis_external_photoz_calibration_reviewer_attestation_template_v1.csv",
        "data/derived/kids1000_cosebis_external_photoz_calibration_reviewer_attestation_template_v1_summary.csv",
        "docs/kids1000_cosebis_external_photoz_calibration_reviewer_attestation_template_v1.md",
        "scripts/build_kids1000_cosebis_external_photoz_calibration_reviewer_attestation_template_v1.py",
        "scripts/validate_kids1000_cosebis_external_photoz_calibration_reviewer_attestation_template_v1.py",
        "data/source_manifest/kids1000_cosebis_external_photoz_calibration_reviewer_handoff_package_policy_v1.csv",
        "REVIEWER_README_KIDS1000_PHOTOZ_HANDOFF.md",
        "data/derived/kids1000_cosebis_external_photoz_calibration_reviewer_handoff_package_v1.zip",
        "data/derived/kids1000_cosebis_external_photoz_calibration_reviewer_handoff_package_v1.zip.sha256",
        "data/derived/kids1000_cosebis_external_photoz_calibration_reviewer_handoff_package_v1_manifest.csv",
        "data/derived/kids1000_cosebis_external_photoz_calibration_reviewer_handoff_package_v1_summary.csv",
        "docs/kids1000_cosebis_external_photoz_calibration_external_reviewer_instructions_v1.md",
        "docs/kids1000_cosebis_external_photoz_calibration_reviewer_handoff_package_v1.md",
        "scripts/build_kids1000_cosebis_external_photoz_calibration_reviewer_handoff_package_v1.py",
        "scripts/validate_kids1000_cosebis_external_photoz_calibration_reviewer_handoff_package_v1.py",
        "data/source_manifest/kids1000_cosebis_external_photoz_calibration_completed_reviewer_response_policy_v1.csv",
        "data/derived/kids1000_cosebis_external_photoz_calibration_completed_reviewer_response_v1.csv",
        "data/derived/kids1000_cosebis_external_photoz_calibration_completed_reviewer_response_v1_summary.csv",
        "docs/kids1000_cosebis_external_photoz_calibration_completed_review_notes_v1.md",
        "docs/kids1000_cosebis_external_photoz_calibration_completed_reviewer_response_v1.md",
        "scripts/validate_kids1000_cosebis_external_photoz_calibration_completed_reviewer_response_v1.py",
        "data/source_manifest/kids1000_cosebis_external_photoz_calibration_closure_ledger_policy_v1.csv",
        "data/derived/kids1000_cosebis_external_photoz_calibration_closure_ledger_v1.csv",
        "data/derived/kids1000_cosebis_external_photoz_calibration_closure_ledger_v1_summary.csv",
        "docs/kids1000_cosebis_external_photoz_calibration_closure_ledger_v1.md",
        "scripts/build_kids1000_cosebis_external_photoz_calibration_closure_ledger_v1.py",
        "scripts/validate_kids1000_cosebis_external_photoz_calibration_closure_ledger_v1.py",
        "data/source_manifest/kids1000_cosebis_endpoint_jackknife_robustness_policy_v1.csv",
        "data/derived/kids1000_cosebis_endpoint_jackknife_robustness_v1_grid.csv",
        "data/derived/kids1000_cosebis_endpoint_jackknife_robustness_v1_summary.csv",
        "docs/kids1000_cosebis_endpoint_jackknife_robustness_v1.md",
        "scripts/run_kids1000_cosebis_endpoint_jackknife_robustness_v1.py",
        "scripts/validate_kids1000_cosebis_endpoint_jackknife_robustness_v1.py",
        "data/source_manifest/kids1000_cosebis_endpoint_mode_localization_policy_v1.csv",
        "data/derived/kids1000_cosebis_endpoint_mode_localization_v1_grid.csv",
        "data/derived/kids1000_cosebis_endpoint_mode_localization_v1_summary.csv",
        "docs/kids1000_cosebis_endpoint_mode_localization_v1.md",
        "scripts/run_kids1000_cosebis_endpoint_mode_localization_v1.py",
        "scripts/validate_kids1000_cosebis_endpoint_mode_localization_v1.py",
        "data/source_manifest/kids1000_cosebis_endpoint_mode_shape_stress_policy_v1.csv",
        "data/derived/kids1000_cosebis_endpoint_mode_shape_stress_v1_grid.csv",
        "data/derived/kids1000_cosebis_endpoint_mode_shape_stress_v1_summary.csv",
        "docs/kids1000_cosebis_endpoint_mode_shape_stress_v1.md",
        "scripts/run_kids1000_cosebis_endpoint_mode_shape_stress_v1.py",
        "scripts/validate_kids1000_cosebis_endpoint_mode_shape_stress_v1.py",
        "data/source_manifest/kids1000_cosebis_endpoint_scoring_synthesis_ledger_policy_v1.csv",
        "data/derived/kids1000_cosebis_endpoint_scoring_synthesis_ledger_v1.csv",
        "data/derived/kids1000_cosebis_endpoint_scoring_synthesis_ledger_v1_summary.csv",
        "docs/kids1000_cosebis_endpoint_scoring_synthesis_ledger_v1.md",
        "scripts/build_kids1000_cosebis_endpoint_scoring_synthesis_ledger_v1.py",
        "scripts/validate_kids1000_cosebis_endpoint_scoring_synthesis_ledger_v1.py",
        "data/source_manifest/kids1000_cosebis_low_mode_carrier_source_grounding_policy_v1.csv",
        "data/derived/kids1000_cosebis_low_mode_carrier_source_grounding_v1.csv",
        "data/derived/kids1000_cosebis_low_mode_carrier_source_grounding_v1_summary.csv",
        "docs/kids1000_cosebis_low_mode_carrier_source_grounding_v1.md",
        "scripts/build_kids1000_cosebis_low_mode_carrier_source_grounding_v1.py",
        "scripts/validate_kids1000_cosebis_low_mode_carrier_source_grounding_v1.py",
        "data/source_manifest/kids1000_cosebis_low_mode_kernel_envelope_derivation_policy_v1.csv",
        "data/derived/kids1000_cosebis_low_mode_kernel_envelope_derivation_v1.csv",
        "data/derived/kids1000_cosebis_low_mode_kernel_envelope_derivation_v1_mode_weights.csv",
        "data/derived/kids1000_cosebis_low_mode_kernel_envelope_derivation_v1_summary.csv",
        "docs/kids1000_cosebis_low_mode_kernel_envelope_derivation_v1.md",
        "scripts/build_kids1000_cosebis_low_mode_kernel_envelope_derivation_v1.py",
        "scripts/validate_kids1000_cosebis_low_mode_kernel_envelope_derivation_v1.py",
        "data/source_manifest/kids1000_cosebis_log_band_prior_eligibility_gate_policy_v1.csv",
        "data/derived/kids1000_cosebis_log_band_prior_eligibility_gate_v1.csv",
        "data/derived/kids1000_cosebis_log_band_prior_eligibility_gate_v1_summary.csv",
        "docs/kids1000_cosebis_log_band_prior_eligibility_gate_v1.md",
        "scripts/build_kids1000_cosebis_log_band_prior_eligibility_gate_v1.py",
        "scripts/validate_kids1000_cosebis_log_band_prior_eligibility_gate_v1.py",
        "data/source_manifest/kids1000_cosebis_log_band_prior_mock_sanity_policy_v1.csv",
        "data/derived/kids1000_cosebis_log_band_prior_mock_sanity_v1_grid.csv",
        "data/derived/kids1000_cosebis_log_band_prior_mock_sanity_v1_summary.csv",
        "docs/kids1000_cosebis_log_band_prior_mock_sanity_v1.md",
        "scripts/run_kids1000_cosebis_log_band_prior_mock_sanity_v1.py",
        "scripts/validate_kids1000_cosebis_log_band_prior_mock_sanity_v1.py",
        "data/source_manifest/kids1000_cosebis_survey_native_path_kernel_derivation_gate_policy_v1.csv",
        "data/derived/kids1000_cosebis_survey_native_path_kernel_derivation_gate_v1.csv",
        "data/derived/kids1000_cosebis_survey_native_path_kernel_derivation_gate_v1_summary.csv",
        "docs/kids1000_cosebis_survey_native_path_kernel_derivation_gate_v1.md",
        "scripts/build_kids1000_cosebis_survey_native_path_kernel_derivation_gate_v1.py",
        "scripts/validate_kids1000_cosebis_survey_native_path_kernel_derivation_gate_v1.py",
        "data/source_manifest/kids1000_cosebis_mode_response_operator_spec_policy_v1.csv",
        "data/derived/kids1000_cosebis_mode_response_operator_spec_v1.csv",
        "data/derived/kids1000_cosebis_mode_response_operator_spec_v1_summary.csv",
        "docs/kids1000_cosebis_mode_response_operator_spec_v1.md",
        "scripts/build_kids1000_cosebis_mode_response_operator_spec_v1.py",
        "scripts/validate_kids1000_cosebis_mode_response_operator_spec_v1.py",
        "data/source_manifest/kids1000_cosebis_mode_response_spectrum_attempt_policy_v1.csv",
        "data/derived/kids1000_cosebis_mode_response_spectrum_attempt_v1.csv",
        "data/derived/kids1000_cosebis_mode_response_spectrum_attempt_v1_spectra.csv",
        "data/derived/kids1000_cosebis_mode_response_spectrum_attempt_v1_summary.csv",
        "docs/kids1000_cosebis_mode_response_spectrum_attempt_v1.md",
        "scripts/build_kids1000_cosebis_mode_response_spectrum_attempt_v1.py",
        "scripts/validate_kids1000_cosebis_mode_response_spectrum_attempt_v1.py",
        "data/source_manifest/kids1000_cosebis_operator_null_safety_gate_policy_v1.csv",
        "data/derived/kids1000_cosebis_operator_null_safety_gate_v1.csv",
        "data/derived/kids1000_cosebis_operator_null_safety_gate_v1_summary.csv",
        "docs/kids1000_cosebis_operator_null_safety_gate_v1.md",
        "scripts/build_kids1000_cosebis_operator_null_safety_gate_v1.py",
        "scripts/validate_kids1000_cosebis_operator_null_safety_gate_v1.py",
        "data/source_manifest/kids1000_cosebis_pure_mask_response_gate_policy_v1.csv",
        "data/derived/kids1000_cosebis_pure_mask_response_gate_v1.csv",
        "data/derived/kids1000_cosebis_pure_mask_response_gate_v1_summary.csv",
        "data/derived/kids1000_cosebis_pure_mask_response_tile_basis_v1.csv",
        "data/derived/kids1000_cosebis_pure_mask_response_domain_basis_v1.csv",
        "docs/kids1000_cosebis_pure_mask_response_gate_v1.md",
        "scripts/build_kids1000_cosebis_pure_mask_response_gate_v1.py",
        "scripts/validate_kids1000_cosebis_pure_mask_response_gate_v1.py",
        "data/source_manifest/kids1000_cosebis_mask_mode_leakage_audit_policy_v1.csv",
        "data/derived/kids1000_cosebis_mask_mode_leakage_audit_v1.csv",
        "data/derived/kids1000_cosebis_mask_mode_leakage_audit_v1_grid.csv",
        "data/derived/kids1000_cosebis_mask_mode_leakage_audit_v1_summary.csv",
        "docs/kids1000_cosebis_mask_mode_leakage_audit_v1.md",
        "scripts/build_kids1000_cosebis_mask_mode_leakage_audit_v1.py",
        "scripts/validate_kids1000_cosebis_mask_mode_leakage_audit_v1.py",
        "data/source_manifest/kids1000_cosebis_operator_leakage_theorem_requirements_policy_v1.csv",
        "data/derived/kids1000_cosebis_operator_leakage_theorem_requirements_v1.csv",
        "data/derived/kids1000_cosebis_operator_leakage_theorem_requirements_v1_summary.csv",
        "docs/kids1000_cosebis_operator_leakage_theorem_requirements_v1.md",
        "scripts/build_kids1000_cosebis_operator_leakage_theorem_requirements_v1.py",
        "scripts/validate_kids1000_cosebis_operator_leakage_theorem_requirements_v1.py",
        "data/source_manifest/kids1000_cosebis_gauge_quotient_descent_gate_policy_v1.csv",
        "data/derived/kids1000_cosebis_gauge_quotient_descent_gate_v1.csv",
        "data/derived/kids1000_cosebis_gauge_quotient_descent_gate_v1_summary.csv",
        "docs/kids1000_cosebis_gauge_quotient_descent_gate_v1.md",
        "scripts/build_kids1000_cosebis_gauge_quotient_descent_gate_v1.py",
        "scripts/validate_kids1000_cosebis_gauge_quotient_descent_gate_v1.py",
        "data/source_manifest/kids1000_cosebis_survey_native_operator_construction_attempt_policy_v1.csv",
        "data/derived/kids1000_cosebis_survey_native_operator_construction_attempt_v1.csv",
        "data/derived/kids1000_cosebis_survey_native_operator_construction_attempt_v1_ledger.csv",
        "data/derived/kids1000_cosebis_survey_native_operator_construction_attempt_v1_summary.csv",
        "docs/kids1000_cosebis_survey_native_operator_construction_attempt_v1.md",
        "scripts/build_kids1000_cosebis_survey_native_operator_construction_attempt_v1.py",
        "scripts/validate_kids1000_cosebis_survey_native_operator_construction_attempt_v1.py",
        "data/source_manifest/kids1000_cosebis_physical_operator_units_gate_policy_v1.csv",
        "data/derived/kids1000_cosebis_physical_operator_units_gate_v1.csv",
        "data/derived/kids1000_cosebis_physical_operator_units_gate_v1_summary.csv",
        "docs/kids1000_cosebis_physical_operator_units_gate_v1.md",
        "scripts/build_kids1000_cosebis_physical_operator_units_gate_v1.py",
        "scripts/validate_kids1000_cosebis_physical_operator_units_gate_v1.py",
        "data/source_manifest/kids1000_cosebis_source_side_amplitude_map_attempt_policy_v1.csv",
        "data/derived/kids1000_cosebis_source_side_amplitude_map_attempt_v1.csv",
        "data/derived/kids1000_cosebis_source_side_amplitude_map_attempt_v1_ledger.csv",
        "data/derived/kids1000_cosebis_source_side_amplitude_map_attempt_v1_summary.csv",
        "docs/kids1000_cosebis_source_side_amplitude_map_attempt_v1.md",
        "scripts/build_kids1000_cosebis_source_side_amplitude_map_attempt_v1.py",
        "scripts/validate_kids1000_cosebis_source_side_amplitude_map_attempt_v1.py",
        "data/source_manifest/kids1000_cosebis_physical_amplitude_requirements_gate_policy_v1.csv",
        "data/derived/kids1000_cosebis_physical_amplitude_requirements_gate_v1.csv",
        "data/derived/kids1000_cosebis_physical_amplitude_requirements_gate_v1_summary.csv",
        "docs/kids1000_cosebis_physical_amplitude_requirements_gate_v1.md",
        "scripts/build_kids1000_cosebis_physical_amplitude_requirements_gate_v1.py",
        "scripts/validate_kids1000_cosebis_physical_amplitude_requirements_gate_v1.py",
        "data/source_manifest/kids1000_cosebis_response_unit_normalization_requirements_gate_policy_v1.csv",
        "data/derived/kids1000_cosebis_response_unit_normalization_requirements_gate_v1.csv",
        "data/derived/kids1000_cosebis_response_unit_normalization_requirements_gate_v1_summary.csv",
        "docs/kids1000_cosebis_response_unit_normalization_requirements_gate_v1.md",
        "scripts/build_kids1000_cosebis_response_unit_normalization_requirements_gate_v1.py",
        "scripts/validate_kids1000_cosebis_response_unit_normalization_requirements_gate_v1.py",
        "data/source_manifest/kids1000_cosebis_standard_lensing_null_amplitude_theorem_requirements_policy_v1.csv",
        "data/derived/kids1000_cosebis_standard_lensing_null_amplitude_theorem_requirements_v1.csv",
        "data/derived/kids1000_cosebis_standard_lensing_null_amplitude_theorem_requirements_v1_summary.csv",
        "docs/kids1000_cosebis_standard_lensing_null_amplitude_theorem_requirements_v1.md",
        "scripts/build_kids1000_cosebis_standard_lensing_null_amplitude_theorem_requirements_v1.py",
        "scripts/validate_kids1000_cosebis_standard_lensing_null_amplitude_theorem_requirements_v1.py",
        "data/source_manifest/kids1000_cosebis_physical_promotion_blocker_ledger_policy_v1.csv",
        "data/derived/kids1000_cosebis_physical_promotion_blocker_ledger_v1.csv",
        "data/derived/kids1000_cosebis_physical_promotion_blocker_ledger_v1_summary.csv",
        "docs/kids1000_cosebis_physical_promotion_blocker_ledger_v1.md",
        "scripts/build_kids1000_cosebis_physical_promotion_blocker_ledger_v1.py",
        "scripts/validate_kids1000_cosebis_physical_promotion_blocker_ledger_v1.py",
        "data/source_manifest/kids1000_cosebis_validation_readiness_ledger_policy_v1.csv",
        "data/derived/kids1000_cosebis_validation_readiness_ledger_v1.csv",
        "data/derived/kids1000_cosebis_validation_readiness_ledger_v1_summary.csv",
        "docs/kids1000_cosebis_validation_readiness_ledger_v1.md",
        "scripts/build_kids1000_cosebis_validation_readiness_ledger_v1.py",
        "scripts/validate_kids1000_cosebis_validation_readiness_ledger_v1.py",
        "data/source_manifest/kids1000_cosebis_physical_promotion_dependency_order_policy_v1.csv",
        "data/derived/kids1000_cosebis_physical_promotion_dependency_order_v1.csv",
        "data/derived/kids1000_cosebis_physical_promotion_dependency_order_v1_summary.csv",
        "docs/kids1000_cosebis_physical_promotion_dependency_order_v1.md",
        "scripts/build_kids1000_cosebis_physical_promotion_dependency_order_v1.py",
        "scripts/validate_kids1000_cosebis_physical_promotion_dependency_order_v1.py",
        "data/source_manifest/kids1000_cosebis_operator_leakage_proof_plan_policy_v1.csv",
        "data/derived/kids1000_cosebis_operator_leakage_proof_plan_v1.csv",
        "data/derived/kids1000_cosebis_operator_leakage_proof_plan_v1_summary.csv",
        "docs/kids1000_cosebis_operator_leakage_proof_plan_v1.md",
        "scripts/build_kids1000_cosebis_operator_leakage_proof_plan_v1.py",
        "scripts/validate_kids1000_cosebis_operator_leakage_proof_plan_v1.py",
        "data/source_manifest/kids1000_cosebis_operator_leakage_domain_decomposition_policy_v1.csv",
        "data/derived/kids1000_cosebis_operator_leakage_domain_decomposition_v1.csv",
        "data/derived/kids1000_cosebis_operator_leakage_domain_decomposition_v1_summary.csv",
        "docs/kids1000_cosebis_operator_leakage_domain_decomposition_v1.md",
        "scripts/build_kids1000_cosebis_operator_leakage_domain_decomposition_v1.py",
        "scripts/validate_kids1000_cosebis_operator_leakage_domain_decomposition_v1.py",
        "data/source_manifest/kids1000_cosebis_operator_leakage_projection_criterion_policy_v1.csv",
        "data/derived/kids1000_cosebis_operator_leakage_projection_criterion_v1.csv",
        "data/derived/kids1000_cosebis_operator_leakage_projection_criterion_v1_summary.csv",
        "docs/kids1000_cosebis_operator_leakage_projection_criterion_v1.md",
        "scripts/build_kids1000_cosebis_operator_leakage_projection_criterion_v1.py",
        "scripts/validate_kids1000_cosebis_operator_leakage_projection_criterion_v1.py",
        "data/source_manifest/kids1000_cosebis_tomographic_photoz_closure_status_policy_v1.csv",
        "data/derived/kids1000_cosebis_tomographic_photoz_closure_status_v1.csv",
        "data/derived/kids1000_cosebis_tomographic_photoz_closure_status_v1_summary.csv",
        "docs/kids1000_cosebis_tomographic_photoz_closure_status_v1.md",
        "scripts/build_kids1000_cosebis_tomographic_photoz_closure_status_v1.py",
        "scripts/validate_kids1000_cosebis_tomographic_photoz_closure_status_v1.py",
        "data/source_manifest/kids1000_cosebis_path_mapping_source_preflight_policy_v1.csv",
        "data/derived/kids1000_cosebis_path_mapping_source_preflight_v1.csv",
        "data/derived/kids1000_cosebis_path_mapping_source_preflight_v1_summary.csv",
        "data/source_manifest/kids1000_cosebis_null_control_policy_v1.csv",
        "data/derived/kids1000_cosebis_null_control_readiness_v1.csv",
        "data/derived/kids1000_cosebis_null_control_readiness_v1_summary.csv",
        "data/source_manifest/kids1000_cosebis_null_control_seed_policy_v1.csv",
        "data/derived/kids1000_cosebis_null_control_seed_inventory_v1.csv",
        "data/derived/kids1000_cosebis_null_control_seed_inventory_v1_summary.csv",
        "data/source_manifest/kids1000_cosebis_null_control_theory_replay_policy_v1.csv",
        "data/derived/kids1000_cosebis_null_control_theory_replay_v1.csv",
        "data/derived/kids1000_cosebis_null_control_theory_replay_v1_summary.csv",
        "docs/void_web_source_native_products_v1.md",
        "docs/void_web_source_native_transform_rule_v1.md",
        "docs/pantheon_void_web_source_native_design_matrix_v1.md",
        "docs/pantheon_void_web_source_native_full_cov_pilot_v1.md",
        "docs/sdss_final_bao_rsd_growth_summary_v1.md",
        "docs/growth_web_source_native_design_matrix_v1.md",
        "docs/growth_web_source_native_pilot_v1.md",
        "docs/sdss_multitracer_bao_rsd_products_v1.md",
        "docs/sdss_multitracer_bao_rsd_transform_rule_v1.md",
        "docs/sdss_multitracer_bao_rsd_design_matrix_v1.md",
        "docs/sdss_multitracer_bao_rsd_full_cov_pilot_v1.md",
        "docs/cmb_safety_lowz_support_v1.md",
        "docs/kids1000_lensing_route_v1.md",
        "docs/kids1000_lensing_products_v1.md",
        "docs/kids1000_cosebis_lensing_route_v1.md",
        "docs/kids1000_cosebis_hdu_policy_v1.md",
        "docs/kids1000_cosebis_tomographic_mode_policy_v1.md",
        "docs/kids1000_cosebis_covariance_readiness_policy_v1.md",
        "docs/kids1000_cosebis_mask_modecut_policy_v1.md",
        "docs/kids1000_cosebis_tomographic_weight_policy_v1.md",
        "docs/kids1000_cosebis_covariance_subselection_policy_v1.md",
        "docs/kids1000_cosebis_covariance_inversion_policy_v1.md",
        "docs/kids1000_cosebis_theory_vector_policy_v1.md",
        "docs/kids1000_cosebis_source_frozen_theory_vector_v1.md",
        "docs/kids1000_cosebis_theory_vector_template_v1.md",
        "docs/kids1000_cosebis_mapping_template_join_contract_v1.md",
        "docs/kids1000_cosebis_web_path_mapping_policy_v1.md",
        "docs/kids1000_cosebis_source_frozen_mapping_vector_v1.md",
        "docs/kids1000_cosebis_redshift_kernel_policy_v1.md",
        "docs/kids1000_cosebis_path_mask_depth_gap_policy_v1.md",
        "docs/kids1000_dr4_path_mask_route_scripts_v1.md",
        "docs/kids1000_dr4_path_mask_route_tile_inventory_policy_v1.md",
        "docs/kids1000_dr4_path_mask_head_sample_policy_v1.md",
        "docs/kids1000_dr4_path_mask_subset_policy_v1.md",
        "docs/kids1000_dr4_path_mask_observable_shell_policy_v1.md",
        "docs/kids1000_cosebis_path_mapping_design_skeleton_policy_v1.md",
        "docs/kids1000_cosebis_path_mapping_domain_skeleton_policy_v1.md",
        "docs/kids1000_cosebis_path_weight_construction_rule_v1.md",
        "docs/kids1000_cosebis_path_factor_acquisition_plan_v1.md",
        "docs/kids1000_cosebis_path_source_product_route_policy_v1.md",
        "docs/kids1000_cosebis_path_blocker_resolution_order_policy_v1.md",
        "docs/kids1000_cosebis_f_overlap_rule_shell_policy_v1.md",
        "docs/kids1000_cosebis_f_overlap_source_availability_policy_v1.md",
        "docs/kids1000_cosebis_f_overlap_full_mask_acquisition_policy_v1.md",
        "docs/kids1000_cosebis_f_overlap_full_mask_batch_plan_policy_v1.md",
        "docs/kids1000_cosebis_f_overlap_full_mask_batch_dry_run_policy_v1.md",
        "docs/kids1000_cosebis_f_overlap_batch_promotion_review_policy_v1.md",
        "docs/kids1000_cosebis_f_overlap_execution_review_schema_policy_v1.md",
        "docs/kids1000_cosebis_f_overlap_execution_review_template_policy_v1.md",
        "docs/kids1000_cosebis_f_overlap_resolution_decision_v1.md",
        "docs/kids1000_cosebis_f_overlap_pixel_fraction_pilot_v1.md",
        "docs/kids1000_cosebis_f_overlap_full_route_pixel_fraction_rule_v1.md",
        "docs/kids1000_cosebis_d_path_full_route_mask_load_rule_v1.md",
        "docs/kids1000_cosebis_e_web_null_control_rule_v1.md",
        "docs/kids1000_cosebis_c_norm_source_side_rule_v1.md",
        "docs/kids1000_cosebis_partial_control_scoring_protocol_v1.md",
        "docs/kids1000_cosebis_partial_control_mapping_shell_v1.md",
        "docs/kids1000_cosebis_partial_control_mapping_values_v1.md",
        "docs/kids1000_cosebis_partial_control_design_matrix_v1.md",
        "docs/kids1000_cosebis_partial_control_diagnostic_scoring_v1.md",
        "docs/kids1000_cosebis_partial_control_null_replay_v1.md",
        "docs/kids1000_cosebis_partial_control_degeneracy_audit_v1.md",
        "docs/kids1000_cosebis_non_degenerate_mapping_promotion_gate_v1.md",
        "docs/kids1000_cosebis_endpoint_family_geometry_audit_v1.md",
        "docs/kids1000_cosebis_path_mapping_source_preflight_policy_v1.md",
        "docs/kids1000_cosebis_null_control_policy_v1.md",
        "docs/kids1000_cosebis_null_control_seed_policy_v1.md",
        "docs/kids1000_cosebis_null_control_theory_replay_v1.md",
        "scripts/acquire_void_web_source_native_products_v1.py",
        "scripts/validate_void_web_source_native_products_v1.py",
        "scripts/build_void_web_source_native_inventory_v1.py",
        "scripts/validate_void_web_source_native_inventory_v1.py",
        "scripts/build_pantheon_void_web_source_native_design_matrix_v1.py",
        "scripts/validate_pantheon_void_web_source_native_design_matrix_v1.py",
        "scripts/run_pantheon_void_web_source_native_full_cov_pilot_v1.py",
        "scripts/validate_pantheon_void_web_source_native_full_cov_pilot_v1.py",
        "scripts/validate_sdss_final_bao_rsd_growth_summary_v1.py",
        "scripts/build_growth_web_source_native_design_matrix_v1.py",
        "scripts/validate_growth_web_source_native_design_matrix_v1.py",
        "scripts/run_growth_web_source_native_pilot_v1.py",
        "scripts/validate_growth_web_source_native_pilot_v1.py",
        "scripts/acquire_sdss_multitracer_bao_rsd_products_v1.py",
        "scripts/validate_sdss_multitracer_bao_rsd_products_v1.py",
        "scripts/build_sdss_multitracer_bao_rsd_design_matrix_v1.py",
        "scripts/validate_sdss_multitracer_bao_rsd_design_matrix_v1.py",
        "scripts/run_sdss_multitracer_bao_rsd_full_cov_pilot_v1.py",
        "scripts/validate_sdss_multitracer_bao_rsd_full_cov_pilot_v1.py",
        "scripts/build_cmb_safety_lowz_support_v1.py",
        "scripts/validate_cmb_safety_lowz_support_v1.py",
        "scripts/check_kids1000_lensing_route_v1.py",
        "scripts/validate_kids1000_lensing_route_v1.py",
        "scripts/acquire_kids1000_lensing_products_v1.py",
        "scripts/validate_kids1000_lensing_products_v1.py",
        "scripts/build_kids1000_lensing_inventory_v1.py",
        "scripts/validate_kids1000_lensing_inventory_v1.py",
        "scripts/build_kids1000_cosebis_hdu_inventory_v1.py",
        "scripts/validate_kids1000_cosebis_hdu_inventory_v1.py",
        "scripts/build_kids1000_cosebis_tomographic_mode_inventory_v1.py",
        "scripts/validate_kids1000_cosebis_tomographic_mode_inventory_v1.py",
        "scripts/build_kids1000_cosebis_covariance_readiness_v1.py",
        "scripts/validate_kids1000_cosebis_covariance_readiness_v1.py",
        "scripts/build_kids1000_cosebis_mask_modecut_inventory_v1.py",
        "scripts/validate_kids1000_cosebis_mask_modecut_inventory_v1.py",
        "scripts/build_kids1000_cosebis_tomographic_weight_inventory_v1.py",
        "scripts/validate_kids1000_cosebis_tomographic_weight_inventory_v1.py",
        "scripts/build_kids1000_cosebis_covariance_subselection_inventory_v1.py",
        "scripts/validate_kids1000_cosebis_covariance_subselection_inventory_v1.py",
        "scripts/build_kids1000_cosebis_covariance_inversion_readiness_v1.py",
        "scripts/validate_kids1000_cosebis_covariance_inversion_readiness_v1.py",
        "scripts/build_kids1000_cosebis_theory_vector_readiness_v1.py",
        "scripts/validate_kids1000_cosebis_theory_vector_readiness_v1.py",
        "scripts/build_kids1000_cosebis_source_frozen_theory_vector_v1.py",
        "scripts/validate_kids1000_cosebis_source_frozen_theory_vector_v1.py",
        "scripts/build_kids1000_cosebis_theory_vector_template_v1.py",
        "scripts/validate_kids1000_cosebis_theory_vector_template_v1.py",
        "scripts/build_kids1000_cosebis_mapping_template_join_contract_v1.py",
        "scripts/validate_kids1000_cosebis_mapping_template_join_contract_v1.py",
        "scripts/build_kids1000_cosebis_web_path_mapping_readiness_v1.py",
        "scripts/validate_kids1000_cosebis_web_path_mapping_readiness_v1.py",
        "scripts/build_kids1000_cosebis_source_frozen_mapping_vector_v1.py",
        "scripts/validate_kids1000_cosebis_source_frozen_mapping_vector_v1.py",
        "scripts/build_kids1000_cosebis_redshift_kernel_inventory_v1.py",
        "scripts/validate_kids1000_cosebis_redshift_kernel_inventory_v1.py",
        "scripts/build_kids1000_cosebis_path_mask_depth_gap_inventory_v1.py",
        "scripts/validate_kids1000_cosebis_path_mask_depth_gap_inventory_v1.py",
        "scripts/acquire_kids1000_dr4_path_mask_route_scripts_v1.py",
        "scripts/validate_kids1000_dr4_path_mask_route_scripts_v1.py",
        "scripts/build_kids1000_dr4_path_mask_route_tile_inventory_v1.py",
        "scripts/validate_kids1000_dr4_path_mask_route_tile_inventory_v1.py",
        "scripts/check_kids1000_dr4_path_mask_head_sample_v1.py",
        "scripts/validate_kids1000_dr4_path_mask_head_sample_v1.py",
        "scripts/acquire_kids1000_dr4_path_mask_subset_v1.py",
        "scripts/validate_kids1000_dr4_path_mask_subset_v1.py",
        "scripts/build_kids1000_dr4_path_mask_observable_shell_v1.py",
        "scripts/validate_kids1000_dr4_path_mask_observable_shell_v1.py",
        "scripts/build_kids1000_cosebis_path_mapping_design_skeleton_v1.py",
        "scripts/validate_kids1000_cosebis_path_mapping_design_skeleton_v1.py",
        "scripts/build_kids1000_cosebis_path_mapping_domain_skeleton_v1.py",
        "scripts/validate_kids1000_cosebis_path_mapping_domain_skeleton_v1.py",
        "scripts/build_kids1000_cosebis_path_weight_construction_rule_v1.py",
        "scripts/validate_kids1000_cosebis_path_weight_construction_rule_v1.py",
        "scripts/build_kids1000_cosebis_path_factor_acquisition_plan_v1.py",
        "scripts/validate_kids1000_cosebis_path_factor_acquisition_plan_v1.py",
        "scripts/build_kids1000_cosebis_path_source_product_route_manifest_v1.py",
        "scripts/validate_kids1000_cosebis_path_source_product_route_manifest_v1.py",
        "scripts/build_kids1000_cosebis_path_blocker_resolution_order_v1.py",
        "scripts/validate_kids1000_cosebis_path_blocker_resolution_order_v1.py",
        "scripts/build_kids1000_cosebis_f_overlap_rule_shell_v1.py",
        "scripts/validate_kids1000_cosebis_f_overlap_rule_shell_v1.py",
        "scripts/build_kids1000_cosebis_f_overlap_source_availability_v1.py",
        "scripts/validate_kids1000_cosebis_f_overlap_source_availability_v1.py",
        "scripts/build_kids1000_cosebis_f_overlap_full_mask_acquisition_manifest_v1.py",
        "scripts/validate_kids1000_cosebis_f_overlap_full_mask_acquisition_manifest_v1.py",
        "scripts/build_kids1000_cosebis_f_overlap_full_mask_batch_plan_v1.py",
        "scripts/validate_kids1000_cosebis_f_overlap_full_mask_batch_plan_v1.py",
        "scripts/acquire_kids1000_cosebis_f_overlap_full_mask_batch_v1.py",
        "scripts/validate_kids1000_cosebis_f_overlap_full_mask_batch_dry_run_v1.py",
        "scripts/build_kids1000_cosebis_f_overlap_batch_promotion_review_v1.py",
        "scripts/validate_kids1000_cosebis_f_overlap_batch_promotion_review_v1.py",
        "scripts/build_kids1000_cosebis_f_overlap_execution_review_schema_v1.py",
        "scripts/validate_kids1000_cosebis_f_overlap_execution_review_schema_v1.py",
        "scripts/build_kids1000_cosebis_f_overlap_execution_review_template_v1.py",
        "scripts/validate_kids1000_cosebis_f_overlap_execution_review_template_v1.py",
        "scripts/build_kids1000_cosebis_f_overlap_resolution_decision_v1.py",
        "scripts/validate_kids1000_cosebis_f_overlap_resolution_decision_v1.py",
        "scripts/build_kids1000_cosebis_f_overlap_pixel_fraction_pilot_v1.py",
        "scripts/validate_kids1000_cosebis_f_overlap_pixel_fraction_pilot_v1.py",
        "scripts/build_kids1000_cosebis_f_overlap_full_route_pixel_fraction_rule_v1.py",
        "scripts/validate_kids1000_cosebis_f_overlap_full_route_pixel_fraction_rule_v1.py",
        "scripts/build_kids1000_cosebis_d_path_full_route_mask_load_rule_v1.py",
        "scripts/validate_kids1000_cosebis_d_path_full_route_mask_load_rule_v1.py",
        "scripts/build_kids1000_cosebis_e_web_null_control_rule_v1.py",
        "scripts/validate_kids1000_cosebis_e_web_null_control_rule_v1.py",
        "scripts/build_kids1000_cosebis_c_norm_source_side_rule_v1.py",
        "scripts/validate_kids1000_cosebis_c_norm_source_side_rule_v1.py",
        "scripts/validate_kids1000_cosebis_partial_control_scoring_protocol_v1.py",
        "scripts/build_kids1000_cosebis_partial_control_mapping_shell_v1.py",
        "scripts/validate_kids1000_cosebis_partial_control_mapping_shell_v1.py",
        "scripts/build_kids1000_cosebis_partial_control_mapping_values_v1.py",
        "scripts/validate_kids1000_cosebis_partial_control_mapping_values_v1.py",
        "scripts/build_kids1000_cosebis_partial_control_design_matrix_v1.py",
        "scripts/validate_kids1000_cosebis_partial_control_design_matrix_v1.py",
        "scripts/run_kids1000_cosebis_partial_control_diagnostic_scoring_v1.py",
        "scripts/validate_kids1000_cosebis_partial_control_diagnostic_scoring_v1.py",
        "scripts/run_kids1000_cosebis_partial_control_null_replay_v1.py",
        "scripts/validate_kids1000_cosebis_partial_control_null_replay_v1.py",
        "scripts/build_kids1000_cosebis_partial_control_degeneracy_audit_v1.py",
        "scripts/validate_kids1000_cosebis_partial_control_degeneracy_audit_v1.py",
        "scripts/build_kids1000_cosebis_non_degenerate_mapping_promotion_gate_v1.py",
        "scripts/validate_kids1000_cosebis_non_degenerate_mapping_promotion_gate_v1.py",
        "scripts/build_kids1000_cosebis_endpoint_family_geometry_audit_v1.py",
        "scripts/validate_kids1000_cosebis_endpoint_family_geometry_audit_v1.py",
        "scripts/run_kids1000_cosebis_endpoint_scoring_v1.py",
        "scripts/validate_kids1000_cosebis_endpoint_scoring_v1.py",
        "scripts/build_kids1000_cosebis_endpoint_scoring_diagnostics_v1.py",
        "scripts/validate_kids1000_cosebis_endpoint_scoring_diagnostics_v1.py",
        "scripts/run_kids1000_cosebis_tomographic_structure_robustness_v1.py",
        "scripts/validate_kids1000_cosebis_tomographic_structure_robustness_v1.py",
        "scripts/build_kids1000_cosebis_tomographic_control_plausibility_audit_v1.py",
        "scripts/validate_kids1000_cosebis_tomographic_control_plausibility_audit_v1.py",
        "scripts/build_kids1000_cosebis_tomographic_holdout_calibration_gate_v1.py",
        "scripts/validate_kids1000_cosebis_tomographic_holdout_calibration_gate_v1.py",
        "scripts/build_kids1000_cosebis_source_frozen_tomographic_holdout_manifest_v1.py",
        "scripts/validate_kids1000_cosebis_source_frozen_tomographic_holdout_manifest_v1.py",
        "scripts/build_kids1000_cosebis_photoz_tomographic_calibration_evidence_v1.py",
        "scripts/validate_kids1000_cosebis_photoz_tomographic_calibration_evidence_v1.py",
        "scripts/build_kids1000_cosebis_external_photoz_calibration_acquisition_plan_v1.py",
        "scripts/validate_kids1000_cosebis_external_photoz_calibration_acquisition_plan_v1.py",
        "scripts/build_kids1000_cosebis_external_photoz_calibration_source_manifest_v1.py",
        "scripts/validate_kids1000_cosebis_external_photoz_calibration_source_manifest_v1.py",
        "scripts/build_kids1000_cosebis_external_photoz_calibration_leakage_review_preflight_v1.py",
        "scripts/validate_kids1000_cosebis_external_photoz_calibration_leakage_review_preflight_v1.py",
        "scripts/build_kids1000_cosebis_external_photoz_calibration_reviewer_attestation_template_v1.py",
        "scripts/validate_kids1000_cosebis_external_photoz_calibration_reviewer_attestation_template_v1.py",
        "scripts/build_kids1000_cosebis_external_photoz_calibration_reviewer_handoff_package_v1.py",
        "scripts/validate_kids1000_cosebis_external_photoz_calibration_reviewer_handoff_package_v1.py",
        "scripts/validate_kids1000_cosebis_external_photoz_calibration_completed_reviewer_response_v1.py",
        "scripts/build_kids1000_cosebis_external_photoz_calibration_closure_ledger_v1.py",
        "scripts/validate_kids1000_cosebis_external_photoz_calibration_closure_ledger_v1.py",
        "scripts/run_kids1000_cosebis_endpoint_jackknife_robustness_v1.py",
        "scripts/validate_kids1000_cosebis_endpoint_jackknife_robustness_v1.py",
        "scripts/run_kids1000_cosebis_endpoint_mode_localization_v1.py",
        "scripts/validate_kids1000_cosebis_endpoint_mode_localization_v1.py",
        "scripts/run_kids1000_cosebis_endpoint_mode_shape_stress_v1.py",
        "scripts/validate_kids1000_cosebis_endpoint_mode_shape_stress_v1.py",
        "scripts/build_kids1000_cosebis_endpoint_scoring_synthesis_ledger_v1.py",
        "scripts/validate_kids1000_cosebis_endpoint_scoring_synthesis_ledger_v1.py",
        "scripts/build_kids1000_cosebis_low_mode_carrier_source_grounding_v1.py",
        "scripts/validate_kids1000_cosebis_low_mode_carrier_source_grounding_v1.py",
        "scripts/build_kids1000_cosebis_low_mode_kernel_envelope_derivation_v1.py",
        "scripts/validate_kids1000_cosebis_low_mode_kernel_envelope_derivation_v1.py",
        "scripts/build_kids1000_cosebis_log_band_prior_eligibility_gate_v1.py",
        "scripts/validate_kids1000_cosebis_log_band_prior_eligibility_gate_v1.py",
        "scripts/run_kids1000_cosebis_log_band_prior_mock_sanity_v1.py",
        "scripts/validate_kids1000_cosebis_log_band_prior_mock_sanity_v1.py",
        "scripts/build_kids1000_cosebis_survey_native_path_kernel_derivation_gate_v1.py",
        "scripts/validate_kids1000_cosebis_survey_native_path_kernel_derivation_gate_v1.py",
        "scripts/build_kids1000_cosebis_mode_response_operator_spec_v1.py",
        "scripts/validate_kids1000_cosebis_mode_response_operator_spec_v1.py",
        "scripts/build_kids1000_cosebis_mode_response_spectrum_attempt_v1.py",
        "scripts/validate_kids1000_cosebis_mode_response_spectrum_attempt_v1.py",
        "scripts/build_kids1000_cosebis_operator_null_safety_gate_v1.py",
        "scripts/validate_kids1000_cosebis_operator_null_safety_gate_v1.py",
        "scripts/build_kids1000_cosebis_pure_mask_response_gate_v1.py",
        "scripts/validate_kids1000_cosebis_pure_mask_response_gate_v1.py",
        "scripts/build_kids1000_cosebis_mask_mode_leakage_audit_v1.py",
        "scripts/validate_kids1000_cosebis_mask_mode_leakage_audit_v1.py",
        "scripts/build_kids1000_cosebis_operator_leakage_theorem_requirements_v1.py",
        "scripts/validate_kids1000_cosebis_operator_leakage_theorem_requirements_v1.py",
        "scripts/build_kids1000_cosebis_gauge_quotient_descent_gate_v1.py",
        "scripts/validate_kids1000_cosebis_gauge_quotient_descent_gate_v1.py",
        "scripts/build_kids1000_cosebis_survey_native_operator_construction_attempt_v1.py",
        "scripts/validate_kids1000_cosebis_survey_native_operator_construction_attempt_v1.py",
        "scripts/build_kids1000_cosebis_physical_operator_units_gate_v1.py",
        "scripts/validate_kids1000_cosebis_physical_operator_units_gate_v1.py",
        "scripts/build_kids1000_cosebis_source_side_amplitude_map_attempt_v1.py",
        "scripts/validate_kids1000_cosebis_source_side_amplitude_map_attempt_v1.py",
        "scripts/build_kids1000_cosebis_physical_amplitude_requirements_gate_v1.py",
        "scripts/validate_kids1000_cosebis_physical_amplitude_requirements_gate_v1.py",
        "scripts/build_kids1000_cosebis_response_unit_normalization_requirements_gate_v1.py",
        "scripts/validate_kids1000_cosebis_response_unit_normalization_requirements_gate_v1.py",
        "scripts/build_kids1000_cosebis_standard_lensing_null_amplitude_theorem_requirements_v1.py",
        "scripts/validate_kids1000_cosebis_standard_lensing_null_amplitude_theorem_requirements_v1.py",
        "scripts/build_kids1000_cosebis_physical_promotion_blocker_ledger_v1.py",
        "scripts/validate_kids1000_cosebis_physical_promotion_blocker_ledger_v1.py",
        "scripts/build_kids1000_cosebis_validation_readiness_ledger_v1.py",
        "scripts/validate_kids1000_cosebis_validation_readiness_ledger_v1.py",
        "scripts/build_kids1000_cosebis_physical_promotion_dependency_order_v1.py",
        "scripts/validate_kids1000_cosebis_physical_promotion_dependency_order_v1.py",
        "scripts/build_kids1000_cosebis_operator_leakage_proof_plan_v1.py",
        "scripts/validate_kids1000_cosebis_operator_leakage_proof_plan_v1.py",
        "scripts/build_kids1000_cosebis_operator_leakage_domain_decomposition_v1.py",
        "scripts/validate_kids1000_cosebis_operator_leakage_domain_decomposition_v1.py",
        "scripts/build_kids1000_cosebis_operator_leakage_projection_criterion_v1.py",
        "scripts/validate_kids1000_cosebis_operator_leakage_projection_criterion_v1.py",
        "scripts/build_kids1000_cosebis_tomographic_photoz_closure_status_v1.py",
        "scripts/validate_kids1000_cosebis_tomographic_photoz_closure_status_v1.py",
        "scripts/build_kids1000_cosebis_path_mapping_source_preflight_v1.py",
        "scripts/validate_kids1000_cosebis_path_mapping_source_preflight_v1.py",
        "scripts/build_kids1000_cosebis_null_control_readiness_v1.py",
        "scripts/validate_kids1000_cosebis_null_control_readiness_v1.py",
        "scripts/build_kids1000_cosebis_null_control_seed_inventory_v1.py",
        "scripts/validate_kids1000_cosebis_null_control_seed_inventory_v1.py",
        "scripts/build_kids1000_cosebis_null_control_theory_replay_v1.py",
        "scripts/validate_kids1000_cosebis_null_control_theory_replay_v1.py",
        "scripts/acquire_pilot_products.py",
        "scripts/validate_pilot_products.py",
        "data/source_manifest/pilot_frozen_product_manifest.csv",
        "docs/pilot_product_freeze_001.md",
        "data/source_manifest/pantheon_endpoint_scope_v1.csv",
        "data/derived/pantheon_scope_v1_row_mask.csv",
        "data/derived/pantheon_scope_v1_summary.csv",
        "docs/pantheon_endpoint_scope_v1.md",
        "scripts/build_pantheon_scope_v1.py",
        "scripts/validate_pantheon_scope_v1.py",
        "data/source_manifest/pantheon_scoring_protocol_v1.csv",
        "docs/pantheon_scoring_protocol_v1.md",
        "scripts/validate_pantheon_scoring_protocol_v1.py",
        "data/source_manifest/pantheon_design_matrix_protocol_v1.csv",
        "data/derived/pantheon_design_matrix_v1.csv",
        "data/derived/pantheon_design_matrix_v1_summary.csv",
        "docs/pantheon_design_matrix_v1.md",
        "scripts/build_pantheon_design_matrix_v1.py",
        "scripts/validate_pantheon_design_matrix_v1.py",
        "data/source_manifest/pantheon_pilot_scoring_v1.csv",
        "data/derived/pantheon_pilot_scoring_v1_summary.csv",
        "data/derived/pantheon_pilot_scoring_v1_grid.csv",
        "docs/pantheon_pilot_scoring_v1.md",
        "scripts/run_pantheon_pilot_scoring_v1.py",
        "scripts/validate_pantheon_pilot_scoring_v1.py",
        "data/source_manifest/pantheon_full_cov_pilot_scoring_v1.csv",
        "data/derived/pantheon_full_cov_pilot_scoring_v1_summary.csv",
        "data/derived/pantheon_full_cov_pilot_scoring_v1_grid.csv",
        "docs/pantheon_full_cov_pilot_scoring_v1.md",
        "data/source_manifest/pantheon_void_web_proxy_full_cov_pilot_v1.csv",
        "data/derived/pantheon_void_web_proxy_full_cov_pilot_v1_summary.csv",
        "data/derived/pantheon_void_web_proxy_full_cov_pilot_v1_grid.csv",
        "docs/pantheon_void_web_proxy_full_cov_pilot_v1.md",
        "docs/multi_probe_full_cov_scoring_plan_v1.md",
        "docs/general_tau_core_readout_basis.md",
        "data/derived/joint_existing_artifact_meta_score_v1.csv",
        "data/derived/joint_existing_artifact_meta_score_v1_summary.csv",
        "docs/joint_existing_artifact_meta_score_v1.md",
        "data/source_manifest/joint_multichannel_endpoint_manifest_v1.csv",
        "data/derived/joint_multichannel_endpoint_candidate_v1.csv",
        "data/derived/joint_multichannel_endpoint_candidate_v1_summary.csv",
        "docs/joint_multichannel_endpoint_candidate_v1.md",
        "data/derived/joint_multichannel_block_score_v1.csv",
        "data/derived/joint_multichannel_block_score_v1_controls.csv",
        "data/derived/joint_multichannel_block_score_v1_leave_one_channel.csv",
        "data/derived/joint_multichannel_block_score_v1_summary.csv",
        "docs/joint_multichannel_block_score_v1.md",
        "data/source_manifest/joint_best_justified_kernel_manifest_v1.csv",
        "data/derived/joint_best_justified_kernel_score_v1.csv",
        "data/derived/joint_best_justified_kernel_score_v1_controls.csv",
        "data/derived/joint_best_justified_kernel_score_v1_leave_one_channel.csv",
        "data/derived/joint_best_justified_kernel_score_v1_summary.csv",
        "docs/joint_best_justified_kernel_score_v1.md",
        "data/derived/joint_best_justified_kernel_robustness_v1.csv",
        "data/derived/joint_best_justified_kernel_robustness_v1_controls.csv",
        "data/derived/joint_best_justified_kernel_robustness_v1_summary.csv",
        "docs/joint_best_justified_kernel_robustness_v1.md",
        "paper10_submission_source/figures/fig_joint_best_justified_kernel_v1.pdf",
        "data/source_manifest/joint_best_justified_qi_review_requirements_v1.csv",
        "docs/joint_best_justified_qi_review_package_v1.md",
        "data/derived/joint_best_justified_qi_review_package_v1.zip",
        "data/derived/joint_best_justified_qi_review_package_v1.zip.sha256",
        "data/derived/joint_non_lensing_lift_diagnostic_v1.csv",
        "data/derived/joint_non_lensing_lift_diagnostic_v1_summary.csv",
        "docs/joint_non_lensing_lift_diagnostic_v1.md",
        "data/derived/observer_path_strengthening_gate_v1.csv",
        "data/derived/observer_path_strengthening_gate_v1_summary.csv",
        "docs/observer_path_strengthening_gate_v1.md",
        "data/derived/observer_path_metric_product_requirements_package_v1_summary.csv",
        "data/derived/observer_path_metric_product_requirements_package_v1_manifest.csv",
        "data/derived/observer_path_metric_product_requirements_review_response_template_v1.csv",
        "data/derived/observer_path_metric_product_requirements_package_v1.zip",
        "data/derived/observer_path_metric_product_requirements_package_v1.zip.sha256",
        "docs/observer_path_metric_product_requirements_package_v1.md",
        "docs/observer_path_metric_product_requirements_reviewer_instructions_v1.md",
        "data/derived/observer_path_metric_product_requirements_review_response_v1.csv",
        "data/derived/observer_path_metric_product_requirements_review_completed_summary_v1.csv",
        "data/derived/observer_path_metric_product_requirements_review_validation_log_v1.txt",
        "docs/observer_path_metric_product_requirements_review_notes_v1.md",
        "data/derived/observer_path_metric_environment_product_v1.csv",
        "data/derived/observer_path_metric_environment_product_v1_summary.csv",
        "docs/observer_path_metric_environment_product_v1.md",
        "data/derived/observer_path_metric_product_acquisition_status_v1.csv",
        "data/derived/observer_path_metric_product_acquisition_status_v1_summary.csv",
        "docs/observer_path_metric_product_acquisition_status_v1.md",
        "data/derived/observer_path_metric_environment_fast_screen_v1_grid.csv",
        "data/derived/observer_path_metric_environment_fast_screen_v1_family_summary.csv",
        "data/derived/observer_path_metric_environment_fast_screen_v1_summary.csv",
        "docs/observer_path_metric_environment_fast_screen_v1.md",
        "data/derived/observer_path_metric_environment_ordering_diagnostic_v1.csv",
        "data/derived/observer_path_metric_environment_ordering_diagnostic_v1_pairwise.csv",
        "data/derived/observer_path_metric_environment_ordering_diagnostic_v1_summary.csv",
        "docs/observer_path_metric_environment_ordering_diagnostic_v1.md",
        "data/derived/observer_path_source_native_ordering_kernel_v1.csv",
        "data/derived/observer_path_source_native_ordering_kernel_v1_summary.csv",
        "docs/observer_path_source_native_ordering_kernel_v1.md",
        "data/derived/observer_path_source_native_ordering_fast_screen_v1_grid.csv",
        "data/derived/observer_path_source_native_ordering_fast_screen_v1_family_summary.csv",
        "data/derived/observer_path_source_native_ordering_fast_screen_v1_summary.csv",
        "docs/observer_path_source_native_ordering_fast_screen_v1.md",
        "data/derived/observer_path_metric_lensing_next_gate_v1.csv",
        "data/derived/observer_path_metric_lensing_next_gate_v1_summary.csv",
        "docs/observer_path_metric_lensing_next_gate_v1.md",
        "scripts/run_pantheon_full_cov_pilot_scoring_v1.py",
        "scripts/validate_pantheon_full_cov_pilot_scoring_v1.py",
        "scripts/run_pantheon_void_web_proxy_full_cov_pilot_v1.py",
        "scripts/validate_pantheon_void_web_proxy_full_cov_pilot_v1.py",
        "scripts/build_joint_existing_artifact_meta_score_v1.py",
        "scripts/validate_joint_existing_artifact_meta_score_v1.py",
        "scripts/run_joint_multichannel_endpoint_candidate_v1.py",
        "scripts/validate_joint_multichannel_endpoint_candidate_v1.py",
        "scripts/run_joint_multichannel_block_score_v1.py",
        "scripts/validate_joint_multichannel_block_score_v1.py",
        "scripts/run_joint_best_justified_kernel_score_v1.py",
        "scripts/validate_joint_best_justified_kernel_score_v1.py",
        "scripts/run_joint_best_justified_kernel_robustness_v1.py",
        "scripts/validate_joint_best_justified_kernel_robustness_v1.py",
        "scripts/build_joint_best_justified_kernel_figure_v1.py",
        "scripts/validate_joint_best_justified_qi_review_package_v1.py",
        "scripts/build_joint_non_lensing_lift_diagnostic_v1.py",
        "scripts/validate_joint_non_lensing_lift_diagnostic_v1.py",
        "scripts/build_observer_path_strengthening_gate_v1.py",
        "scripts/validate_observer_path_strengthening_gate_v1.py",
        "scripts/build_observer_path_metric_product_requirements_package_v1.py",
        "scripts/validate_observer_path_metric_product_requirements_package_v1.py",
        "scripts/import_observer_path_metric_product_requirements_review_response_v1.py",
        "scripts/validate_observer_path_metric_product_requirements_review_response_v1.py",
        "scripts/build_observer_path_metric_environment_product_v1.py",
        "scripts/validate_observer_path_metric_environment_product_v1.py",
        "scripts/build_observer_path_metric_product_acquisition_status_v1.py",
        "scripts/validate_observer_path_metric_product_acquisition_status_v1.py",
        "scripts/run_observer_path_metric_environment_fast_screen_v1.py",
        "scripts/validate_observer_path_metric_environment_fast_screen_v1.py",
        "scripts/build_observer_path_metric_environment_ordering_diagnostic_v1.py",
        "scripts/validate_observer_path_metric_environment_ordering_diagnostic_v1.py",
        "scripts/build_observer_path_source_native_ordering_kernel_v1.py",
        "scripts/validate_observer_path_source_native_ordering_kernel_v1.py",
        "scripts/run_observer_path_source_native_ordering_fast_screen_v1.py",
        "scripts/validate_observer_path_source_native_ordering_fast_screen_v1.py",
        "scripts/build_observer_path_metric_lensing_next_gate_v1.py",
        "scripts/validate_observer_path_metric_lensing_next_gate_v1.py",
        "data/derived/act_dr6_lensing_path_weight_replay_authorization_review_response_v1.csv",
        "data/derived/act_dr6_lensing_path_weight_replay_authorization_review_response_v1_summary.csv",
        "data/derived/act_dr6_lensing_path_weight_authorized_replay_v1_grid.csv",
        "data/derived/act_dr6_lensing_path_weight_authorized_replay_v1_summary.csv",
        "data/derived/act_dr6_lensing_path_weight_control_dominance_diagnostic_v1_branches.csv",
        "data/derived/act_dr6_lensing_path_weight_control_dominance_diagnostic_v1_summary.csv",
        "scripts/run_act_dr6_lensing_path_weight_authorized_replay_v1.py",
        "scripts/validate_act_dr6_lensing_path_weight_authorized_replay_v1.py",
        "scripts/build_act_dr6_lensing_path_weight_control_dominance_diagnostic_v1.py",
        "scripts/validate_act_dr6_lensing_path_weight_control_dominance_diagnostic_v1.py",
        "scripts/build_figures.py",
        "figures/fig_pantheon_full_cov_pilot_branch_diagnostics.pdf",
        "paper10_submission_source/figures/fig_pantheon_full_cov_pilot_branch_diagnostics.pdf",
        "figures/fig_kids1000_cosebis_mode_localization.pdf",
        "paper10_submission_source/figures/fig_kids1000_cosebis_mode_localization.pdf",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel


def test_manuscript_claim_markers() -> None:
    text = (ROOT / "paper10_submission_source/main.tex").read_text()
    assert "A source-frozen Friedmann-readout audit protocol" in text
    assert "does not claim that Tau Core" in text
    assert "explains dark energy" in text
    assert "Lambda-like distance readout" in text
    assert "web/environment-dependent growth or lensing residual" in text
    assert "source-frozen, control-aware viability audit" in text
    assert "reproducible multi-channel viability" in text
    assert "BEST\\_JUSTIFIED\\_JOINT\\_KERNEL\\_POSITIVE" in text
    assert "PREFLIGHT\\_NOT\\_VALIDATION" in text
    assert "Low-redshift observer/path basis functions" in text
    assert "narrow observer/path replay" in text
    assert "DESI shape/readout route" in text
    assert "KiDS/COSEBIs low-mode route" in text
    assert "ACT lensing/path route" in text
    assert "control-dominated diagnostic" in text
    forbidden = [
        "we detect Tau Core",
        "we prove Tau Core explains dark energy",
        "we replace Lambda-CDM",
        "validated physical model",
    ]
    lower = text.lower()
    for phrase in forbidden:
        assert phrase.lower() not in lower


def test_arxiv_zip_is_source_only() -> None:
    zip_path = ROOT / "arxiv_submission_source.zip"
    with zipfile.ZipFile(zip_path) as zf:
        names = set(zf.namelist())
    assert "main.tex" in names
    assert "refs.bib" in names
    assert "figures/fig_pantheon_full_cov_pilot_branch_diagnostics.pdf" in names
    assert "figures/fig_kids1000_cosebis_mode_localization.pdf" in names
    assert "main.pdf" not in names
    assert not any(name.endswith(".aux") for name in names)


def test_gate_inventory_is_protocol_only() -> None:
    with (ROOT / "data/derived/audit_gate_inventory.csv").open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) >= 6
    assert {row["status"] for row in rows} == {"planned"}
    forbidden_blob = " ".join(row["forbidden_inputs"] for row in rows)
    assert "target_residuals" in forbidden_blob
    assert "endpoint_tuned_labels" in forbidden_blob


def test_source_freeze_manifest_blocks_endpoint_leakage() -> None:
    with (ROOT / "data/source_manifest/paper10_source_freeze_manifest.csv").open(newline="") as f:
        rows = list(csv.DictReader(f))
    blocks = {row["block"] for row in rows}
    assert {"distance", "void_maturity", "web_anisotropy", "growth", "lensing", "cmb_safety"} <= blocks
    statuses = {row["freeze_status"] for row in rows}
    assert statuses <= {"SOURCE_SELECTED_NOT_FETCHED", "BLOCKED_SOURCE_SELECTION", "FETCHED_FROZEN"}
    assert "FETCHED_FROZEN" not in statuses
    forbidden = ";".join(row["forbidden_endpoint_fields"] for row in rows)
    for marker in [
        "distance_residuals",
        "growth_residuals",
        "lensing_residuals",
        "fit_improvement_flags",
        "posthoc_environment_labels",
    ]:
        assert marker in forbidden


def test_cosmology_channel_manifest_v1_blocks_endpoint_leakage() -> None:
    with (ROOT / "data/source_manifest/cosmology_channel_manifest_v1.csv").open(newline="") as f:
        rows = list(csv.DictReader(f))
    channels = {row["channel_id"] for row in rows}
    assert {
        "W_VOID_MATURITY",
        "W_WEB_ANISOTROPY",
        "W_PATH_PROJECTION",
        "W_TIME_READOUT",
    } <= channels
    assert {row["endpoint_scoring_allowed"] for row in rows} == {"false"}
    assert {row["freeze_status"] for row in rows} == {"CHANNEL_DECLARED_NOT_ENDPOINT"}
    forbidden = ";".join(row["forbidden_endpoint_fields"] for row in rows)
    for marker in [
        "distance_residuals",
        "growth_residuals",
        "lensing_residuals",
        "fit_improvement_flags",
        "posthoc_environment_labels",
        "posthoc_sky_direction_selection",
        "posthoc_clock_anomaly_labels",
    ]:
        assert marker in forbidden
    for row in rows:
        assert row["activation_rule_id"].startswith("ACT_")
        assert row["activation_rule_status"] == "RULE_DECLARED_NOT_NUMERIC"
        assert row["null_control"]
        assert row["projection_induction_role"]


def test_cosmology_activation_rule_manifest_v1_is_protocol_only() -> None:
    with (ROOT / "data/source_manifest/cosmology_activation_rule_manifest_v1.csv").open(newline="") as f:
        rows = list(csv.DictReader(f))
    rules = {row["activation_rule_id"] for row in rows}
    assert {
        "ACT_VOID_MATURITY_V1",
        "ACT_WEB_ANISOTROPY_V1",
        "ACT_PATH_PROJECTION_V1",
        "ACT_TIME_READOUT_V1",
    } <= rules
    assert {row["endpoint_scoring_allowed"] for row in rows} == {"false"}
    assert {row["rule_status"] for row in rows} == {"RULE_SHELL_DECLARED_NOT_NUMERIC"}
    forbidden = ";".join(row["forbidden_inputs"] for row in rows)
    for marker in [
        "distance_residuals",
        "growth_residuals",
        "lensing_residuals",
        "fit_improvement_flags",
        "posthoc_environment_labels",
        "posthoc_sky_direction_selection",
        "posthoc_clock_anomaly_labels",
    ]:
        assert marker in forbidden
    for row in rows:
        assert "=" in row["formula_shell"]
        assert row["parameter_freeze_policy"].startswith("freeze_from_")
        assert row["output_range"] in {"[0_1]", "[-1_1]"}


def test_cosmology_activation_parameter_freeze_plan_v1_is_not_numeric() -> None:
    with (
        ROOT / "data/source_manifest/cosmology_activation_parameter_freeze_plan_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    parameters = {row["parameter_id"] for row in rows}
    assert {
        "P_VOID_S_STAR",
        "P_VOID_Q_OPTIONAL",
        "P_WEB_Q_STAR",
        "P_WEB_CLASS_WEIGHTS",
        "P_PATH_LENS_STAR",
        "P_PATH_MASK_POLICY",
        "P_TIME_CLOCK_STAR",
        "P_TIME_ZBIN_POLICY",
    } <= parameters
    assert {row["endpoint_scoring_allowed"] for row in rows} == {"false"}
    assert {row["freeze_status"] for row in rows} == {
        "PARAMETER_FREEZE_ROUTE_DECLARED_NOT_NUMERIC"
    }
    forbidden = ";".join(row["forbidden_inputs"] for row in rows)
    for marker in [
        "distance_residuals",
        "growth_residuals",
        "lensing_residuals",
        "fit_improvement_flags",
        "late_time_fit_parameters",
        "posthoc_environment_labels",
    ]:
        assert marker in forbidden
    for row in rows:
        assert row["required_future_artifact"].endswith(".csv")
        assert row["null_control"]
        assert "residual" not in row["freeze_rule_shell"].lower()


def test_cosmology_source_grounding_gate_v1_is_not_derived() -> None:
    with (ROOT / "data/source_manifest/cosmology_source_grounding_gate_v1.csv").open(
        newline=""
    ) as f:
        rows = list(csv.DictReader(f))
    channels = {row["channel_id"] for row in rows}
    assert {
        "W_VOID_MATURITY",
        "W_WEB_ANISOTROPY",
        "W_PATH_PROJECTION",
        "W_TIME_READOUT",
    } <= channels
    assert {row["endpoint_scoring_allowed"] for row in rows} == {"false"}
    assert {row["current_gate_status"] for row in rows} == {
        "SOURCE_GROUNDING_GATE_DECLARED_NOT_DERIVED"
    }
    forbidden = ";".join(row["forbidden_inputs"] for row in rows)
    for marker in [
        "distance_residuals",
        "growth_residuals",
        "lensing_residuals",
        "fit_improvement_flags",
    ]:
        assert marker in forbidden
    for row in rows:
        assert row["activation_candidate"]
        assert row["quotient_survival_test"]
        assert row["closure_stability_test"]
        assert row["readout_survival_test"]
        assert row["required_future_artifact"].endswith(".csv")
        assert row["null_control"]


def test_cosmology_flrw_consistency_channel_audit_v1_is_not_scoring() -> None:
    subprocess.run(
        ["python", "scripts/validate_cosmology_flrw_consistency_channel_audit_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with (ROOT / "data/source_manifest/cosmology_flrw_consistency_channel_audit_v1.csv").open(
        newline=""
    ) as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 4
    channels = {row["channel_id"] for row in rows}
    assert channels == {
        "W_VOID_MATURITY",
        "W_WEB_ANISOTROPY",
        "W_PATH_PROJECTION",
        "W_TIME_READOUT",
    }
    assert {row["current_status"] for row in rows} == {"FLRW_AXIS_DECLARED_NOT_SCORED"}
    assert {row["endpoint_scoring_allowed"] for row in rows} == {"false"}
    assert {row["physical_validation_claimed"] for row in rows} == {"false"}
    primary_axes = {row["primary_flrw_consistency_axis"] for row in rows}
    assert {
        "density_reconstruction",
        "distance_optical_readout",
        "expansion_time_readout",
    } <= primary_axes
    all_axes = set()
    all_baselines = set()
    forbidden = []
    for row in rows:
        all_axes.add(row["primary_flrw_consistency_axis"])
        all_axes.update(part for part in row["secondary_flrw_consistency_axes"].split(";") if part)
        all_baselines.update(part for part in row["required_baseline_or_null_controls"].split(";") if part)
        forbidden.extend(part for part in row["forbidden_endpoint_fields"].split(";") if part)
    assert "single_flrw_geometry_assumption" in all_axes
    for baseline in [
        "flrw_curvature",
        "backreaction",
        "dark_energy",
        "flrw_distance_expansion_consistency",
    ]:
        assert baseline in all_baselines
    for marker in [
        "distance_residuals",
        "growth_residuals",
        "lensing_residuals",
        "fit_improvement_flags",
    ]:
        assert marker in forbidden


def test_void_web_endpoint_readiness_after_flrw_audit_v1_is_not_endpoint() -> None:
    subprocess.run(
        ["python", "scripts/build_void_web_endpoint_readiness_after_flrw_audit_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/validate_void_web_endpoint_readiness_after_flrw_audit_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with (
        ROOT / "data/derived/void_web_endpoint_readiness_after_flrw_audit_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    with (
        ROOT / "data/derived/void_web_endpoint_readiness_after_flrw_audit_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert len(rows) == 4
    assert summary["endpoint_ready_count"] == "0"
    assert summary["support_ready_count"] == "1"
    assert summary["endpoint_scoring_allowed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    statuses = {row["readiness_status"] for row in rows}
    assert "SAFETY_SUPPORT_PASS_NOT_ENDPOINT_SCORE" in statuses
    assert "PILOT_SIGNAL_NOT_ENDPOINT_READY" in statuses
    assert "GROWTH_STRESS_TEST_NOT_ENDPOINT_READY" in statuses
    assert "SEMI_NEGATIVE_CONTROL_NOT_ENDPOINT_READY" in statuses
    blockers = {row["endpoint_blocker"] for row in rows}
    assert "aic_loss_and_shuffled_control_not_beaten" in blockers
    assert "diagonal_covariance_and_wrong_sign_degeneracy" in blockers
    assert "near_zero_signal_and_wrong_sign_degeneracy" in blockers


def test_void_web_combined_multiblock_endpoint_protocol_v1_is_frozen_not_run() -> None:
    subprocess.run(
        ["python", "scripts/validate_void_web_combined_multiblock_endpoint_protocol_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with (
        ROOT / "data/source_manifest/void_web_combined_multiblock_endpoint_protocol_v1.csv"
    ).open(newline="") as f:
        protocol = list(csv.DictReader(f))[0]
    assert protocol["status"] == "COMBINED_MULTIBLOCK_ENDPOINT_PROTOCOL_FROZEN_NOT_RUN"
    assert protocol["scoring_allowed"] == "false"
    assert protocol["physical_validation_claimed"] == "false"
    assert "W_VOID_MATURITY" in protocol["included_channel_families"]
    assert "W_WEB_ANISOTROPY" in protocol["included_channel_families"]
    assert "W_PATH_PROJECTION" in protocol["disabled_channel_families"]
    assert "W_TIME_READOUT" in protocol["disabled_channel_families"]
    assert "AIC_total" in protocol["unified_information_criterion"]
    assert "deterministic_shuffled_void_web" in protocol["joint_null_controls"]
    assert "block_drop_distance" in protocol["joint_null_controls"]
    assert "block_drop_growth" in protocol["joint_null_controls"]
    assert "block_drop_multitracer" in protocol["joint_null_controls"]
    for marker in [
        "posthoc_block_weights",
        "posthoc_covariance_reweighting",
        "endpoint_score_claims",
    ]:
        assert marker in protocol["forbidden_inputs"]


def test_void_web_combined_multiblock_authorization_template_v1_is_not_completed() -> None:
    subprocess.run(
        ["python", "scripts/build_void_web_combined_multiblock_endpoint_authorization_review_template_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/validate_void_web_combined_multiblock_endpoint_authorization_review_template_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with (
        ROOT / "data/derived/void_web_combined_multiblock_endpoint_authorization_review_response_template_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    with (
        ROOT / "data/derived/void_web_combined_multiblock_endpoint_authorization_review_template_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert len(rows) == 4
    assert summary["review_completed"] == "false"
    assert summary["endpoint_run_allowed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert {row["review_completed"] for row in rows} == {"false"}
    assert {row["endpoint_run_allowed"] for row in rows} == {"false"}
    assert {row["physical_validation_claimed"] for row in rows} == {"false"}
    assert {row["forbidden_inputs_used"] for row in rows} == {"false"}
    assert {row["claim_boundary"] for row in rows} == {
        "combined_multiblock_endpoint_authorization_review_not_validation"
    }


def test_void_web_combined_multiblock_authorization_package_v1_is_clean_handoff() -> None:
    subprocess.run(
        ["python", "scripts/build_void_web_combined_multiblock_endpoint_authorization_review_package_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/validate_void_web_combined_multiblock_endpoint_authorization_review_package_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with (
        ROOT / "data/derived/void_web_combined_multiblock_endpoint_authorization_review_package_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/void_web_combined_multiblock_endpoint_authorization_review_package_v1_manifest.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert summary["status"] == "AUTHORIZATION_REVIEW_PACKAGE_BUILT_NOT_COMPLETED"
    assert summary["package_file_count"] == "15"
    assert summary["review_completed"] == "false"
    assert summary["endpoint_run_allowed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert summary["contains_endpoint_residuals"] == "false"
    assert summary["contains_endpoint_scores"] == "false"
    assert summary["contains_fit_statistics"] == "false"
    assert {row["contains_endpoint_residuals"] for row in rows} == {"false"}
    assert {row["contains_endpoint_scores"] for row in rows} == {"false"}
    assert {row["contains_fit_statistics"] for row in rows} == {"false"}
    assert "REVIEWER_README_VOID_WEB_COMBINED_ENDPOINT_AUTHORIZATION.md" in {
        row["package_path"] for row in rows
    }


def test_void_web_combined_multiblock_authorization_response_v1_grants_permission_only() -> None:
    subprocess.run(
        ["python", "scripts/validate_void_web_combined_multiblock_endpoint_authorization_review_response_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with (
        ROOT / "data/derived/void_web_combined_multiblock_endpoint_authorization_review_response_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/void_web_combined_multiblock_endpoint_authorization_review_response_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert summary["status"] == "AUTHORIZATION_REVIEW_COMPLETED"
    assert summary["decision"] == "GO_COMBINED_VOID_WEB_ENDPOINT_PERMISSION_ONLY"
    assert summary["review_completed"] == "true"
    assert summary["forbidden_inputs_used"] == "false"
    assert summary["endpoint_run_allowed"] == "true"
    assert summary["physical_validation_claimed"] == "false"
    assert summary["authorization_scope"] == (
        "single_predeclared_combined_void_web_endpoint_run_permission_only_not_validation"
    )
    assert summary["claim_boundary"] == "combined_multiblock_endpoint_authorization_review_not_validation"
    assert {row["review_completed"] for row in rows} == {"true"}
    assert {row["forbidden_inputs_used"] for row in rows} == {"false"}
    assert {row["endpoint_run_allowed"] for row in rows} == {"true"}
    assert {row["physical_validation_claimed"] for row in rows} == {"false"}


def test_void_web_combined_multiblock_authorized_endpoint_v1_preserves_weak_negative_result() -> None:
    subprocess.run(
        ["python", "scripts/run_void_web_combined_multiblock_authorized_endpoint_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/validate_void_web_combined_multiblock_authorized_endpoint_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with (ROOT / "data/derived/void_web_combined_multiblock_authorized_endpoint_v1_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    with (ROOT / "data/derived/void_web_combined_multiblock_authorized_endpoint_v1_grid.csv").open(
        newline=""
    ) as f:
        rows = list(csv.DictReader(f))
    assert summary["status"] == "AUTHORIZED_COMBINED_VOID_WEB_ENDPOINT_COMPLETE_PERMISSION_ONLY"
    assert summary["physical_validation_claimed"] == "false"
    assert summary["claim_boundary"] == "combined_void_web_endpoint_permission_only_not_validation"
    assert float(summary["candidate_delta_chi2_vs_baseline"]) < 0.0
    assert float(summary["candidate_delta_aic_vs_baseline"]) > 0.0
    assert float(summary["candidate_delta_bic_vs_baseline"]) > 0.0
    assert summary["candidate_beats_best_wrong_by_chi2"] == "false"
    assert summary["candidate_beats_best_wrong_by_aic"] == "false"
    assert summary["best_wrong_branch"] == "deterministic_shuffled_void_web"
    assert {row["physical_validation_claimed"] for row in rows} == {"false"}


def test_void_web_combined_endpoint_diagnostics_v1_identifies_void_inactive_failure_mode() -> None:
    subprocess.run(
        ["python", "scripts/build_void_web_combined_endpoint_diagnostics_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/validate_void_web_combined_endpoint_diagnostics_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with (ROOT / "data/derived/void_web_combined_endpoint_diagnostics_v1_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    with (ROOT / "data/derived/void_web_combined_endpoint_diagnostics_v1_branch_summary.csv").open(
        newline=""
    ) as f:
        rows = {row["combined_branch"]: row for row in csv.DictReader(f)}
    assert summary["status"] == "DIAGNOSTIC_COMPLETE_NOT_VALIDATION"
    assert summary["dominant_failure_mode"] == "void_channel_inactive_and_shuffled_control_marginally_better"
    assert summary["candidate_void_channel_active_at_best"] == "false"
    assert summary["candidate_web_channel_active_at_best"] == "true"
    assert summary["candidate_equals_web_only_chi2"] == "true"
    assert summary["physical_validation_claimed"] == "false"
    assert rows["source_native_void_web"]["void_channel_active_at_best"] == "false"
    assert rows["source_native_void_web"]["web_channel_active_at_best"] == "true"
    assert float(summary["shuffled_minus_candidate_chi2"]) < 0.0


def test_void_channel_inactivity_diagnostic_v1_preserves_void_mapping_blocker() -> None:
    subprocess.run(
        ["python", "scripts/build_void_channel_inactivity_diagnostic_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/validate_void_channel_inactivity_diagnostic_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with (ROOT / "data/derived/void_channel_inactivity_diagnostic_v1_summary.csv").open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (ROOT / "data/derived/void_channel_inactivity_diagnostic_v1_profile.csv").open(newline="") as f:
        profile = list(csv.DictReader(f))
    assert summary["status"] == "DIAGNOSTIC_COMPLETE_NOT_VALIDATION"
    assert summary["combined_candidate_void_channel_active_at_best"] == "false"
    assert summary["combined_candidate_equals_web_only_chi2"] == "true"
    assert float(summary["void_nonzero_fraction"]) < float(summary["web_nonzero_fraction"])
    assert float(summary["best_nonzero_void_delta_chi2_vs_zero"]) > 0.0
    assert summary["diagnostic_verdict"] == (
        "void_basis_has_limited_support_and_nonzero_void_amplitudes_do_not_improve_frozen_profiles"
    )
    assert summary["physical_validation_claimed"] == "false"
    assert {row["physical_validation_claimed"] for row in profile} == {"false"}


def test_void_source_basis_audit_v1_freezes_low_z_support_blocker() -> None:
    subprocess.run(
        ["python", "scripts/build_void_source_basis_audit_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/validate_void_source_basis_audit_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with (ROOT / "data/derived/void_source_basis_audit_v1_summary.csv").open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (ROOT / "data/derived/void_source_basis_audit_v1_redshift_bins.csv").open(newline="") as f:
        bins = list(csv.DictReader(f))
    assert summary["status"] == "SOURCE_BASIS_AUDIT_COMPLETE_NOT_VALIDATION"
    assert summary["source_basis_limitation"] == (
        "low_z_volume_limited_void_catalog_mapped_to_full_pantheon_distance_block"
    )
    assert summary["endpoint_scoring_allowed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert float(summary["void_catalog_z_support_max_proxy"]) < 0.2
    assert float(summary["pantheon_z_max"]) > 2.0
    assert float(summary["void_active_fraction"]) < 0.5
    assert {row["physical_validation_claimed"] for row in bins} == {"false"}
    assert all(float(row["void_active_fraction"]) == 0.0 for row in bins if float(row["z_bin_lo"]) >= 0.2)


def test_void_channel_remediation_gate_v1_blocks_endpoint_reopen() -> None:
    subprocess.run(
        ["python", "scripts/build_void_channel_remediation_gate_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/validate_void_channel_remediation_gate_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with (ROOT / "data/derived/void_channel_remediation_gate_v1.csv").open(newline="") as f:
        gate = list(csv.DictReader(f))[0]
    assert gate["route_status"] == "ENDPOINT_REOPEN_BLOCKED"
    assert gate["full_pantheon_void_endpoint_reopen_allowed"] == "false"
    assert gate["low_z_scope_endpoint_allowed_now"] == "false"
    assert gate["source_basis_rebuild_required_for_full_scope"] == "true"
    assert gate["void_channel_quarantined_from_full_distance_endpoint"] == "true"
    assert gate["endpoint_scoring_allowed"] == "false"
    assert gate["physical_validation_claimed"] == "false"
    assert gate["selected_route"] == "NO_ROUTE_SELECTED_NO_ENDPOINT_REOPEN"
    assert gate["claim_boundary"] == "void_channel_remediation_gate_not_scoring_not_validation"


def test_low_z_pantheon_void_scope_candidate_v1_is_not_endpoint_scoring() -> None:
    subprocess.run(
        ["python", "scripts/build_low_z_pantheon_void_scope_candidate_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/validate_low_z_pantheon_void_scope_candidate_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with (ROOT / "data/derived/low_z_pantheon_void_scope_candidate_v1_summary.csv").open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (ROOT / "data/derived/low_z_pantheon_void_scope_candidate_v1_row_mask.csv").open(newline="") as f:
        rows = list(csv.DictReader(f))
    included = [row for row in rows if row["included"] == "true"]
    assert summary["scope_status"] == "SCOPE_CANDIDATE_FROZEN_NOT_ENDPOINT"
    assert summary["endpoint_scoring_allowed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert summary["candidate_endpoint_run_allowed_now"] == "false"
    assert summary["requires_separate_authorization_before_scoring"] == "true"
    assert summary["claim_boundary"] == "low_z_void_scope_candidate_not_scoring_not_validation"
    assert 0 < len(included) < len(rows)
    assert int(summary["included_rows"]) == len(included)
    assert all(float(row["zHD"]) <= float(summary["z_support_max"]) for row in included)
    assert all(float(row["W_void_source_native_basis"]) > 0.0 for row in included)


def test_low_z_void_scope_replay_authorization_package_v1_is_handoff_only() -> None:
    subprocess.run(
        ["python", "scripts/build_low_z_pantheon_void_scope_replay_authorization_review_template_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/validate_low_z_pantheon_void_scope_replay_authorization_review_template_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/build_low_z_pantheon_void_scope_replay_authorization_review_package_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/validate_low_z_pantheon_void_scope_replay_authorization_review_package_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with (
        ROOT / "data/derived/low_z_pantheon_void_scope_replay_authorization_review_package_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "AUTHORIZATION_REVIEW_PACKAGE_BUILT_NOT_COMPLETED"
    assert summary["review_completed"] == "false"
    assert summary["endpoint_run_allowed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert summary["contains_endpoint_residuals"] == "false"
    assert summary["contains_endpoint_scores"] == "false"
    assert summary["contains_fit_statistics"] == "false"
    assert summary["claim_boundary"] == "low_z_void_scope_replay_authorization_review_not_validation"


def _low_z_void_replay_authorization_response_rows() -> list[dict[str, str]]:
    with (
        ROOT / "data/derived/low_z_pantheon_void_scope_replay_authorization_review_response_template_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        row["review_completed"] = "true"
        row["reviewer_id_or_role"] = "independent_low_z_void_scope_reviewer"
        row["reviewer_response"] = "yes"
        row["reviewer_rationale"] = "Reviewed source-side handoff only; no endpoint residuals, scores, or fits used."
        row["forbidden_inputs_used"] = "false"
        row["endpoint_run_allowed"] = "true"
        row["physical_validation_claimed"] = "false"
        if row["question_id"] == "Q2_low_z_rationale":
            row["reviewer_response"] = "caveated_yes"
        if row["question_id"] == "Q4_authorization":
            row["reviewer_response"] = "GO_LOW_Z_VOID_REPLAY_PERMISSION_ONLY"
    return rows


def _write_low_z_void_replay_authorization_response(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _low_z_void_replay_authorization_validator_cmd(response: Path, summary: Path) -> list[str]:
    return [
        "python",
        str(ROOT / "scripts/validate_low_z_pantheon_void_scope_replay_authorization_review_response_v1.py"),
        str(response),
        "--summary-out",
        str(summary),
    ]


def test_low_z_void_replay_authorization_response_validator_accepts_permission_only(
    tmp_path: Path,
) -> None:
    rows = _low_z_void_replay_authorization_response_rows()
    response = tmp_path / "low_z_void_replay_authorization_response.csv"
    summary = tmp_path / "summary.csv"
    _write_low_z_void_replay_authorization_response(response, rows)
    subprocess.run(
        _low_z_void_replay_authorization_validator_cmd(response, summary),
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with summary.open(newline="") as f:
        accepted = list(csv.DictReader(f))[0]
    assert accepted["status"] == "LOW_Z_VOID_SCOPE_REPLAY_AUTHORIZATION_ACCEPTED_PERMISSION_ONLY"
    assert accepted["review_completed"] == "true"
    assert accepted["forbidden_inputs_used"] == "false"
    assert accepted["endpoint_run_allowed"] == "true"
    assert accepted["physical_validation_claimed"] == "false"
    assert accepted["verdict"] == "low_z_void_replay_authorized_permission_only_not_validation"
    assert accepted["claim_boundary"] == "low_z_void_scope_replay_authorization_review_not_validation"


def test_low_z_void_replay_authorization_response_validator_rejects_forbidden_inputs(
    tmp_path: Path,
) -> None:
    rows = _low_z_void_replay_authorization_response_rows()
    rows[0]["forbidden_inputs_used"] = "true"
    response = tmp_path / "low_z_void_replay_authorization_forbidden.csv"
    summary = tmp_path / "summary.csv"
    _write_low_z_void_replay_authorization_response(response, rows)
    result = subprocess.run(
        _low_z_void_replay_authorization_validator_cmd(response, summary),
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert result.returncode != 0
    assert "forbidden_inputs_used=false" in result.stderr
    assert not summary.exists()


def test_low_z_void_replay_authorization_response_validator_rejects_validation_claim(
    tmp_path: Path,
) -> None:
    rows = _low_z_void_replay_authorization_response_rows()
    rows[1]["physical_validation_claimed"] = "true"
    response = tmp_path / "low_z_void_replay_authorization_validation_claim.csv"
    summary = tmp_path / "summary.csv"
    _write_low_z_void_replay_authorization_response(response, rows)
    result = subprocess.run(
        _low_z_void_replay_authorization_validator_cmd(response, summary),
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert result.returncode != 0
    assert "must not claim validation" in result.stderr
    assert not summary.exists()


def test_low_z_pantheon_void_replay_protocol_v1_is_frozen_not_run() -> None:
    subprocess.run(
        ["python", "scripts/validate_low_z_pantheon_void_replay_protocol_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with (ROOT / "data/source_manifest/low_z_pantheon_void_replay_protocol_v1.csv").open(newline="") as f:
        protocol = list(csv.DictReader(f))[0]
    assert protocol["status"] == "LOW_Z_VOID_REPLAY_PROTOCOL_FROZEN_NOT_RUN"
    assert protocol["scoring_allowed"] == "false"
    assert protocol["physical_validation_claimed"] == "false"
    assert protocol["included_channel_families"] == "W_VOID_MATURITY"
    for channel in ["W_WEB_ANISOTROPY", "W_PATH_PROJECTION", "W_TIME_READOUT"]:
        assert channel in protocol["disabled_channel_families"]
    for forbidden in [
        "distance_residual_driven_activation",
        "posthoc_row_selection",
        "posthoc_amplitude_tuning",
        "endpoint_score_claims",
        "physical_validation_claims",
    ]:
        assert forbidden in protocol["forbidden_inputs"]
    score_artifacts = [
        ROOT / "data/derived/low_z_pantheon_void_replay_v1_results.csv",
        ROOT / "data/derived/low_z_pantheon_void_replay_v1_residuals.csv",
        ROOT / "data/derived/low_z_pantheon_void_replay_v1_grid.csv",
        ROOT / "data/derived/low_z_pantheon_void_replay_v1_summary.csv",
    ]
    if any(path.exists() for path in score_artifacts):
        with (
            ROOT
            / "data/derived/low_z_pantheon_void_scope_replay_authorization_review_response_v1_summary.csv"
        ).open(newline="") as f:
            auth = list(csv.DictReader(f))[0]
        assert auth["verdict"] == "low_z_void_replay_authorized_permission_only_not_validation"
        assert auth["physical_validation_claimed"] == "false"


def test_low_z_pantheon_void_replay_v1_is_permission_only() -> None:
    response = ROOT / "data/derived/low_z_pantheon_void_scope_replay_authorization_review_response_v1.csv"
    if not response.exists():
        pytest.skip("completed low-z void authorization response not present")
    subprocess.run(
        [
            "python",
            "scripts/validate_low_z_pantheon_void_scope_replay_authorization_review_response_v1.py",
            str(response),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/run_low_z_pantheon_void_replay_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/validate_low_z_pantheon_void_replay_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with (ROOT / "data/derived/low_z_pantheon_void_replay_v1_summary.csv").open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["authorization_verdict"] == "low_z_void_replay_authorized_permission_only_not_validation"
    assert summary["n_rows"] == "424"
    assert summary["physical_validation_claimed"] == "false"
    assert summary["claim_boundary"] == "low_z_void_replay_permission_only_not_validation"
    assert "W_VOID_MATURITY" in summary["active_channels"]
    for channel in ["W_WEB_ANISOTROPY", "W_PATH_PROJECTION", "W_TIME_READOUT"]:
        assert channel in summary["disabled_channels"]
    assert abs(float(summary["delta_chi2_void_minus_baseline"]) + 0.37847238) < 1e-8
    assert abs(float(summary["delta_aic_void_minus_baseline"]) - 1.62152762) < 1e-8
    assert summary["candidate_rank_by_chi2_among_void_and_controls"] == "2"
    assert summary["controls_better_than_candidate_chi2"] == "1"


def test_low_z_void_replay_diagnostics_v1_preserves_weak_mixed_verdict() -> None:
    response = ROOT / "data/derived/low_z_pantheon_void_scope_replay_authorization_review_response_v1.csv"
    if not response.exists():
        pytest.skip("completed low-z void authorization response not present")
    subprocess.run(
        ["python", "scripts/run_low_z_pantheon_void_replay_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/build_low_z_void_replay_diagnostics_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/validate_low_z_void_replay_diagnostics_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with (ROOT / "data/derived/low_z_void_replay_diagnostics_v1_summary.csv").open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["diagnosis"] == "grid_edge_pressure_and_shuffled_control_beats_candidate"
    assert float(summary["shuffled_minus_candidate_chi2"]) < 0.0
    assert summary["candidate_omega_m_at_grid_edge"] == "true"
    assert summary["candidate_omega_void_at_grid_edge"] == "true"
    assert summary["physical_validation_claimed"] == "false"


def test_void_source_basis_refinement_gate_v1_blocks_new_void_endpoint() -> None:
    response = ROOT / "data/derived/low_z_pantheon_void_scope_replay_authorization_review_response_v1.csv"
    if not response.exists():
        pytest.skip("completed low-z void authorization response not present")
    subprocess.run(
        ["python", "scripts/run_low_z_pantheon_void_replay_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/build_low_z_void_replay_diagnostics_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/build_void_source_basis_refinement_gate_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/validate_void_source_basis_refinement_gate_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with (ROOT / "data/derived/void_source_basis_refinement_gate_v1.csv").open(newline="") as f:
        gate = list(csv.DictReader(f))[0]
    assert gate["current_basis_status"] == "current_W_void_not_endpoint_ready_redshift_degenerate_not_control_unique"
    assert gate["source_unique_ready"] == "false"
    assert gate["endpoint_scoring_allowed"] == "false"
    assert gate["physical_validation_claimed"] == "false"


def test_void_source_basis_refinement_acquisition_manifest_v1_freezes_next_routes() -> None:
    response = ROOT / "data/derived/low_z_pantheon_void_scope_replay_authorization_review_response_v1.csv"
    if not response.exists():
        pytest.skip("completed low-z void authorization response not present")
    subprocess.run(
        ["python", "scripts/run_low_z_pantheon_void_replay_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/build_low_z_void_replay_diagnostics_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/build_void_source_basis_refinement_gate_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/build_void_source_basis_refinement_acquisition_manifest_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/validate_void_source_basis_refinement_acquisition_manifest_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with (ROOT / "data/derived/void_source_basis_refinement_acquisition_manifest_v1_summary.csv").open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["required_routes"] == "6"
    assert summary["attached_routes"] == "0"
    assert summary["source_unique_ready"] == "false"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["physical_validation_claimed"] == "false"


def test_void_source_basis_refinement_r1_r3_source_attachment_v1_attaches_sources_without_replay() -> None:
    response = ROOT / "data/derived/low_z_pantheon_void_scope_replay_authorization_review_response_v1.csv"
    if not response.exists():
        pytest.skip("completed low-z void authorization response not present")
    for command in [
        ["python", "scripts/run_low_z_pantheon_void_replay_v1.py"],
        ["python", "scripts/build_low_z_void_replay_diagnostics_v1.py"],
        ["python", "scripts/build_void_source_basis_refinement_gate_v1.py"],
        ["python", "scripts/build_void_source_basis_refinement_acquisition_manifest_v1.py"],
        ["python", "scripts/build_void_source_basis_refinement_r1_r3_source_attachment_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_r1_r3_source_attachment_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/void_source_basis_refinement_r1_r3_source_attachment_v1_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["attached_routes"] == "3"
    assert summary["required_routes"] == "6"
    assert int(summary["low_z_rows"]) == 424
    assert int(summary["host_to_void_geometry_rows"]) == 424
    assert int(summary["los_environment_nonempty_rows"]) > 0
    assert summary["redshift_independence_preflight_complete"] == "false"
    assert summary["control_resistance_preflight_complete"] == "false"
    assert summary["leakage_review_complete"] == "false"
    assert summary["source_unique_ready"] == "false"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["physical_validation_claimed"] == "false"


def test_void_source_basis_refinement_r4_independence_preflight_v1_preserves_replay_block() -> None:
    response = ROOT / "data/derived/low_z_pantheon_void_scope_replay_authorization_review_response_v1.csv"
    if not response.exists():
        pytest.skip("completed low-z void authorization response not present")
    for command in [
        ["python", "scripts/run_low_z_pantheon_void_replay_v1.py"],
        ["python", "scripts/build_low_z_void_replay_diagnostics_v1.py"],
        ["python", "scripts/build_void_source_basis_refinement_gate_v1.py"],
        ["python", "scripts/build_void_source_basis_refinement_acquisition_manifest_v1.py"],
        ["python", "scripts/build_void_source_basis_refinement_r1_r3_source_attachment_v1.py"],
        ["python", "scripts/build_void_source_basis_refinement_r4_independence_preflight_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_r4_independence_preflight_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/void_source_basis_refinement_r4_independence_preflight_v1_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["redshift_independence_preflight_complete"] == "true"
    assert int(summary["features_tested"]) == 7
    assert int(summary["features_passing_low_correlation"]) >= 1
    assert summary["control_resistance_preflight_complete"] == "false"
    assert summary["leakage_review_complete"] == "false"
    assert summary["source_unique_ready"] == "false"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["physical_validation_claimed"] == "false"


def test_void_source_basis_refinement_r5_control_resistance_preflight_v1_freezes_controls_without_replay() -> None:
    response = ROOT / "data/derived/low_z_pantheon_void_scope_replay_authorization_review_response_v1.csv"
    if not response.exists():
        pytest.skip("completed low-z void authorization response not present")
    for command in [
        ["python", "scripts/run_low_z_pantheon_void_replay_v1.py"],
        ["python", "scripts/build_low_z_void_replay_diagnostics_v1.py"],
        ["python", "scripts/build_void_source_basis_refinement_gate_v1.py"],
        ["python", "scripts/build_void_source_basis_refinement_acquisition_manifest_v1.py"],
        ["python", "scripts/build_void_source_basis_refinement_r1_r3_source_attachment_v1.py"],
        ["python", "scripts/build_void_source_basis_refinement_r4_independence_preflight_v1.py"],
        ["python", "scripts/build_void_source_basis_refinement_r5_control_resistance_preflight_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_r5_control_resistance_preflight_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/void_source_basis_refinement_r5_control_resistance_preflight_v1_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["control_resistance_preflight_complete"] == "true"
    assert int(summary["features_admitted_from_R4"]) >= 1
    assert int(summary["control_families_per_feature"]) == 5
    assert int(summary["control_manifest_rows"]) == int(summary["features_admitted_from_R4"]) * 5
    assert int(summary["control_vector_rows"]) > 0
    assert summary["leakage_review_complete"] == "false"
    assert summary["source_unique_ready"] == "false"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["computes_new_scores"] == "false"
    assert summary["physical_validation_claimed"] == "false"


def test_void_source_basis_refinement_r6_reviewer_handoff_package_v1_keeps_review_open() -> None:
    response = ROOT / "data/derived/low_z_pantheon_void_scope_replay_authorization_review_response_v1.csv"
    if not response.exists():
        pytest.skip("completed low-z void authorization response not present")
    for command in [
        ["python", "scripts/run_low_z_pantheon_void_replay_v1.py"],
        ["python", "scripts/build_low_z_void_replay_diagnostics_v1.py"],
        ["python", "scripts/build_void_source_basis_refinement_gate_v1.py"],
        ["python", "scripts/build_void_source_basis_refinement_acquisition_manifest_v1.py"],
        ["python", "scripts/build_void_source_basis_refinement_r1_r3_source_attachment_v1.py"],
        ["python", "scripts/build_void_source_basis_refinement_r4_independence_preflight_v1.py"],
        ["python", "scripts/build_void_source_basis_refinement_r5_control_resistance_preflight_v1.py"],
        ["python", "scripts/build_void_source_basis_refinement_r6_reviewer_template_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_r6_reviewer_template_v1.py"],
        ["python", "scripts/build_void_source_basis_refinement_r6_reviewer_handoff_package_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_r6_reviewer_handoff_package_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/void_source_basis_refinement_r6_reviewer_template_v1_summary.csv").open(
        newline=""
    ) as f:
        template_summary = list(csv.DictReader(f))[0]
    with (ROOT / "data/derived/void_source_basis_refinement_r6_reviewer_handoff_package_v1_summary.csv").open(
        newline=""
    ) as f:
        package_summary = list(csv.DictReader(f))[0]
    assert template_summary["review_completed"] == "false"
    assert template_summary["leakage_review_complete"] == "false"
    assert package_summary["review_completed"] == "false"
    assert package_summary["leakage_review_complete"] == "false"
    assert package_summary["source_unique_ready"] == "false"
    assert package_summary["endpoint_replay_allowed"] == "false"
    assert package_summary["endpoint_validation_claimed"] == "false"
    assert int(package_summary["package_file_count"]) > 10


def test_void_source_basis_refinement_r6_completed_response_v1_closes_source_side_only() -> None:
    response = ROOT / "data/derived/void_source_basis_refinement_r6_completed_reviewer_response_v1.csv"
    if not response.exists():
        pytest.skip("completed R6 void reviewer response not present")
    for command in [
        ["python", "scripts/run_low_z_pantheon_void_replay_v1.py"],
        ["python", "scripts/build_low_z_void_replay_diagnostics_v1.py"],
        ["python", "scripts/build_void_source_basis_refinement_gate_v1.py"],
        ["python", "scripts/build_void_source_basis_refinement_acquisition_manifest_v1.py"],
        ["python", "scripts/build_void_source_basis_refinement_r1_r3_source_attachment_v1.py"],
        ["python", "scripts/build_void_source_basis_refinement_r4_independence_preflight_v1.py"],
        ["python", "scripts/build_void_source_basis_refinement_r5_control_resistance_preflight_v1.py"],
        ["python", "scripts/build_void_source_basis_refinement_r6_reviewer_template_v1.py"],
        ["python", "scripts/build_void_source_basis_refinement_r6_reviewer_handoff_package_v1.py"],
        [
            "python",
            "scripts/validate_void_source_basis_refinement_r6_completed_reviewer_response_v1.py",
            str(response),
            "--summary-out",
            "data/derived/void_source_basis_refinement_r6_completed_reviewer_response_v1_summary.csv",
        ],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/void_source_basis_refinement_r6_completed_reviewer_response_v1_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["review_completed"] == "true"
    assert summary["leakage_review_complete"] == "true"
    assert summary["source_unique_ready"] == "true"
    assert summary["computes_new_scores"] == "false"
    assert summary["contains_endpoint_data"] == "false"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"


def test_void_source_basis_refinement_endpoint_replay_authorization_package_v1_is_handoff_only() -> None:
    r6_response = ROOT / "data/derived/void_source_basis_refinement_r6_completed_reviewer_response_v1.csv"
    if not r6_response.exists():
        pytest.skip("completed R6 void reviewer response not present")
    for command in [
        [
            "python",
            "scripts/validate_void_source_basis_refinement_r6_completed_reviewer_response_v1.py",
            str(r6_response),
            "--summary-out",
            "data/derived/void_source_basis_refinement_r6_completed_reviewer_response_v1_summary.csv",
        ],
        ["python", "scripts/build_void_source_basis_refinement_endpoint_replay_authorization_review_template_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_endpoint_replay_authorization_review_template_v1.py"],
        ["python", "scripts/build_void_source_basis_refinement_endpoint_replay_authorization_review_package_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_endpoint_replay_authorization_review_package_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (
        ROOT
        / "data/derived/void_source_basis_refinement_endpoint_replay_authorization_review_package_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["review_completed"] == "false"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["contains_endpoint_residuals"] == "false"
    assert summary["contains_endpoint_scores"] == "false"
    assert summary["contains_fit_statistics"] == "false"
    assert int(summary["package_file_count"]) > 5


def test_void_source_basis_refinement_endpoint_replay_authorization_response_v1_grants_permission_only(
    tmp_path: Path,
) -> None:
    r6_response = ROOT / "data/derived/void_source_basis_refinement_r6_completed_reviewer_response_v1.csv"
    if not r6_response.exists():
        pytest.skip("completed R6 void reviewer response not present")
    for command in [
        [
            "python",
            "scripts/validate_void_source_basis_refinement_r6_completed_reviewer_response_v1.py",
            str(r6_response),
            "--summary-out",
            "data/derived/void_source_basis_refinement_r6_completed_reviewer_response_v1_summary.csv",
        ],
        ["python", "scripts/build_void_source_basis_refinement_endpoint_replay_authorization_review_template_v1.py"],
        ["python", "scripts/build_void_source_basis_refinement_endpoint_replay_authorization_review_package_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_endpoint_replay_authorization_review_package_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)

    template = ROOT / "data/derived/void_source_basis_refinement_endpoint_replay_authorization_review_response_template_v1.csv"
    response = tmp_path / "completed_refined_void_authorization_response.csv"
    with template.open(newline="") as f:
        rows = list(csv.DictReader(f))

    responses = {
        "Q1_r6_source_side_closure": "yes",
        "Q2_refined_replay_scope": "caveated_yes",
        "Q3_no_leakage": "yes",
        "Q4_authorization": "GO_REFINED_VOID_REPLAY_PERMISSION_ONLY",
    }
    for row in rows:
        row["review_completed"] = "true"
        row["reviewer_id_or_role"] = "unit_test_permission_only_reviewer"
        row["reviewer_response"] = responses[row["question_id"]]
        row["reviewer_rationale"] = "Synthetic permission-only response for validator coverage; no endpoint data used."
        row["forbidden_inputs_used"] = "false"
        row["endpoint_replay_allowed"] = "true"
        row["endpoint_validation_claimed"] = "false"

    with response.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    summary_out = tmp_path / "completed_refined_void_authorization_summary.csv"
    subprocess.run(
        [
            "python",
            "scripts/validate_void_source_basis_refinement_endpoint_replay_authorization_review_response_v1.py",
            str(response),
            "--summary-out",
            str(summary_out),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with summary_out.open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["review_completed"] == "true"
    assert summary["forbidden_inputs_used"] == "false"
    assert summary["endpoint_replay_allowed"] == "true"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["verdict"] == "refined_void_replay_authorized_permission_only_not_validation"


def test_void_source_basis_refinement_endpoint_replay_authorization_completed_response_v1_is_permission_only() -> None:
    response = ROOT / "data/derived/void_source_basis_refinement_endpoint_replay_authorization_review_response_v1.csv"
    if not response.exists():
        pytest.skip("completed refined void authorization response not present")
    summary_out = ROOT / "data/derived/void_source_basis_refinement_endpoint_replay_authorization_review_response_v1_summary.csv"
    subprocess.run(
        [
            "python",
            "scripts/validate_void_source_basis_refinement_endpoint_replay_authorization_review_response_v1.py",
            str(response),
            "--summary-out",
            str(summary_out),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with summary_out.open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["review_completed"] == "true"
    assert summary["forbidden_inputs_used"] == "false"
    assert summary["endpoint_replay_allowed"] == "true"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["authorization_scope"] == (
        "single_predeclared_refined_low_z_void_source_basis_replay_permission_only_not_validation"
    )
    assert summary["verdict"] == "refined_void_replay_authorized_permission_only_not_validation"


def test_void_source_basis_refinement_authorized_replay_v1_is_permission_only_diagnostic() -> None:
    response = ROOT / "data/derived/void_source_basis_refinement_endpoint_replay_authorization_review_response_v1.csv"
    if not response.exists():
        pytest.skip("completed refined void authorization response not present")
    for command in [
        [
            "python",
            "scripts/validate_void_source_basis_refinement_endpoint_replay_authorization_review_response_v1.py",
            str(response),
            "--summary-out",
            "data/derived/void_source_basis_refinement_endpoint_replay_authorization_review_response_v1_summary.csv",
        ],
        ["python", "scripts/run_void_source_basis_refinement_authorized_replay_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_authorized_replay_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/void_source_basis_refinement_authorized_replay_v1_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["endpoint_replay_allowed"] == "true"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["claim_boundary"] == "void_source_basis_refinement_authorized_replay_permission_only_not_validation"
    assert summary["best_candidate_feature_id"]
    assert float(summary["delta_chi2_candidate_minus_baseline"]) < 0.0
    assert float(summary["delta_aic_candidate_minus_baseline"]) > 0.0
    assert int(summary["controls_better_than_candidate_chi2"]) > 0


def test_void_source_basis_refinement_control_dominance_audit_v1_explains_weak_negative() -> None:
    response = ROOT / "data/derived/void_source_basis_refinement_endpoint_replay_authorization_review_response_v1.csv"
    if not response.exists():
        pytest.skip("completed refined void authorization response not present")
    for command in [
        ["python", "scripts/run_void_source_basis_refinement_authorized_replay_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_authorized_replay_v1.py"],
        ["python", "scripts/build_void_source_basis_refinement_control_dominance_audit_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_control_dominance_audit_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/void_source_basis_refinement_control_dominance_audit_v1_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["candidate_improves_chi2_over_baseline"] == "true"
    assert summary["candidate_loses_aic_to_baseline"] == "true"
    assert summary["best_control_beats_candidate_chi2"] == "true"
    assert summary["best_control_is_row_shuffle"] == "true"
    assert summary["best_control_low_redshift_row_leakage"] == "true"
    assert summary["uses_endpoint_residuals_for_new_source_selection"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["verdict"] == (
        "candidate_signal_not_source_specific_shuffled_control_dominates_without_redshift_leak"
    )


def test_void_source_basis_refinement_v2_void_morphology_values_v1_preserve_weak_negative() -> None:
    for command in [
        ["python", "scripts/build_void_source_basis_refinement_v2_void_morphology_values_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_v2_void_morphology_values_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/void_source_basis_refinement_v2_void_morphology_values_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    with (ROOT / "data/derived/void_source_basis_refinement_v2_void_morphology_values.csv").open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert summary["status"] == "V2_VOID_MORPHOLOGY_VALUES_FROZEN_WEAK_NEGATIVE_NOT_ENDPOINT_READY"
    assert summary["n_rows"] == "424"
    assert summary["weak_negative_status_inherited"] == "true"
    assert summary["best_control_beats_candidate_chi2"] == "true"
    assert summary["best_control_is_row_shuffle"] == "true"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["verdict"] == "void_morphology_values_frozen_but_weak_negative_preserved"
    assert rows
    assert {row["weak_negative_status_inherited"] for row in rows} == {"true"}
    assert {row["contains_distance_residuals"] for row in rows} == {"false"}
    assert {row["endpoint_replay_allowed"] for row in rows} == {"false"}


def test_void_source_basis_refinement_v2_web_morphology_values_v1_are_source_frozen() -> None:
    for command in [
        ["python", "scripts/build_void_source_basis_refinement_v2_web_morphology_values_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_v2_web_morphology_values_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/void_source_basis_refinement_v2_web_morphology_values_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    with (ROOT / "data/derived/void_source_basis_refinement_v2_web_morphology_values.csv").open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert summary["status"] == "V2_WEB_MORPHOLOGY_VALUES_FROZEN_NOT_ENDPOINT_READY"
    assert summary["n_rows"] == "424"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["contains_endpoint_scores"] == "false"
    assert summary["contains_distance_residuals"] == "false"
    assert summary["contains_fit_statistics"] == "false"
    assert summary["verdict"] == "web_morphology_values_frozen_not_endpoint_ready"
    assert rows
    assert {row["endpoint_replay_allowed"] for row in rows} == {"false"}
    assert {row["contains_distance_residuals"] for row in rows} == {"false"}
    assert {row["contains_fit_statistics"] for row in rows} == {"false"}


def test_void_source_basis_refinement_v2_cmb_safety_values_v1_are_source_frozen() -> None:
    for command in [
        ["python", "scripts/build_void_source_basis_refinement_v2_cmb_safety_values_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_v2_cmb_safety_values_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/void_source_basis_refinement_v2_cmb_safety_values_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    with (ROOT / "data/derived/void_source_basis_refinement_v2_cmb_safety_values.csv").open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert summary["status"] == "V2_CMB_SAFETY_VALUES_FROZEN_NOT_ENDPOINT_READY"
    assert summary["n_rows"] == "424"
    assert summary["rows_below_safety_floor"] == "424"
    assert summary["cmb_lowz_support_passed"] == "true"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["contains_cmb_map_data"] == "false"
    assert summary["contains_cmb_likelihood"] == "false"
    assert summary["verdict"] == "cmb_safety_values_frozen_not_endpoint_ready"
    assert rows
    assert {row["low_z_below_safety_floor"] for row in rows} == {"true"}
    assert {row["endpoint_replay_allowed"] for row in rows} == {"false"}
    assert {row["contains_distance_residuals"] for row in rows} == {"false"}


def test_void_source_basis_refinement_v2_path_projection_route_ledger_v1_preserves_blocker() -> None:
    for command in [
        ["python", "scripts/build_void_source_basis_refinement_v2_path_projection_crossmap_audit_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_v2_path_projection_crossmap_audit_v1.py"],
        ["python", "scripts/build_void_source_basis_refinement_v2_path_partial_scope_policy_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_v2_path_partial_scope_policy_v1.py"],
        ["python", "scripts/build_void_source_basis_refinement_v2_path_partial_scope_values_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_v2_path_partial_scope_values_v1.py"],
        ["python", "scripts/build_void_source_basis_refinement_v2_path_projection_route_ledger_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_v2_path_projection_route_ledger_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/void_source_basis_refinement_v2_path_projection_route_ledger_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    with (ROOT / "data/derived/void_source_basis_refinement_v2_path_projection_route_ledger.csv").open(
        newline=""
    ) as f:
        rows = list(csv.DictReader(f))
    assert summary["status"] == "V2_PATH_PROJECTION_ROUTE_LEDGER_FROZEN_VALUES_BLOCKED"
    assert summary["n_rows"] == "424"
    assert summary["kids_lensing_route_available"] == "true"
    assert summary["pantheon_lowz_ra_dec_available"] == "true"
    assert summary["lowz_to_kids_path_crossmap_candidate_available"] == "true"
    assert summary["lowz_to_kids_path_crossmap_available"] == "false"
    assert summary["partial_path_values_computed"] == "true"
    assert summary["full_lowz_path_values_computed"] == "false"
    assert summary["partial_path_candidate_count"] == "12"
    assert summary["path_values_computed"] == "false"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["verdict"] == "partial_path_values_available_but_full_lowz_path_channel_blocked"
    assert rows
    assert {row["pantheon_lowz_ra_dec_available"] for row in rows} == {"true"}
    assert {row["lowz_to_kids_path_crossmap_candidate_available"] for row in rows} == {"true"}
    assert {row["lowz_to_kids_path_crossmap_available"] for row in rows} == {"false"}
    assert {row["partial_path_values_computed"] for row in rows} == {"true"}
    assert {row["full_lowz_path_values_computed"] for row in rows} == {"false"}
    assert {row["W_path_value_status"] for row in rows} == {"BLOCKED_PATH_WEIGHT_RULE_NOT_FROZEN_FOR_PANTHEON_ROWS"}
    assert {row["W_path_source_value"] for row in rows} == {"NA"}
    assert {row["contains_lensing_residuals"] for row in rows} == {"false"}


def test_void_source_basis_refinement_v2_path_projection_crossmap_audit_v1_is_not_values() -> None:
    for command in [
        ["python", "scripts/build_void_source_basis_refinement_v2_path_projection_crossmap_audit_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_v2_path_projection_crossmap_audit_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/void_source_basis_refinement_v2_path_projection_crossmap_audit_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    with (ROOT / "data/derived/void_source_basis_refinement_v2_path_projection_crossmap_audit.csv").open(
        newline=""
    ) as f:
        rows = list(csv.DictReader(f))
    assert summary["status"] == "V2_PATH_PROJECTION_CROSSMAP_AUDIT_BUILT_VALUES_NOT_COMPUTED"
    assert summary["n_rows"] == "424"
    assert summary["lowz_ra_dec_available"] == "true"
    assert summary["kids_tile_coordinate_inventory_available"] == "true"
    assert summary["crossmap_candidate_available"] == "true"
    assert summary["crossmap_complete_for_lowz_scope"] == "false"
    assert summary["path_values_computed"] == "false"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["verdict"] == "lowz_coordinates_available_but_path_values_not_computed"
    assert int(summary["rows_inside_kids_dec_filename_envelope"]) > 0
    assert int(summary["rows_nearest_tile_within_1_deg"]) > 0
    assert rows
    assert {row["W_path_source_value"] for row in rows} == {"NA"}
    assert {row["contains_lensing_residuals"] for row in rows} == {"false"}


def test_void_source_basis_refinement_v2_path_partial_scope_policy_v1_is_not_full_channel() -> None:
    for command in [
        ["python", "scripts/build_void_source_basis_refinement_v2_path_projection_crossmap_audit_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_v2_path_projection_crossmap_audit_v1.py"],
        ["python", "scripts/build_void_source_basis_refinement_v2_path_partial_scope_policy_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_v2_path_partial_scope_policy_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/void_source_basis_refinement_v2_path_partial_scope_policy_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    with (ROOT / "data/derived/void_source_basis_refinement_v2_path_partial_scope_policy.csv").open(
        newline=""
    ) as f:
        rows = list(csv.DictReader(f))
    assert summary["status"] == "V2_PATH_PARTIAL_SCOPE_POLICY_FROZEN_VALUES_NOT_COMPUTED"
    assert summary["n_rows"] == "424"
    assert summary["strict_path_scope_candidate_count"] == "5"
    assert summary["caveated_path_scope_candidate_count"] == "7"
    assert summary["total_path_scope_candidate_count"] == "12"
    assert summary["full_lowz_scope_path_ready"] == "false"
    assert summary["path_values_computed"] == "false"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["verdict"] == "W_path_is_partial_scope_candidate_only_not_full_lowz_channel"
    assert rows
    assert {row["W_path_source_value"] for row in rows} == {"NA"}
    assert {row["contains_lensing_residuals"] for row in rows} == {"false"}


def test_void_source_basis_refinement_v2_path_partial_scope_values_v1_are_source_only_control() -> None:
    for command in [
        ["python", "scripts/build_void_source_basis_refinement_v2_path_projection_crossmap_audit_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_v2_path_projection_crossmap_audit_v1.py"],
        ["python", "scripts/build_void_source_basis_refinement_v2_path_partial_scope_policy_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_v2_path_partial_scope_policy_v1.py"],
        ["python", "scripts/build_void_source_basis_refinement_v2_path_partial_scope_values_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_v2_path_partial_scope_values_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/void_source_basis_refinement_v2_path_partial_scope_values_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    with (ROOT / "data/derived/void_source_basis_refinement_v2_path_partial_scope_values.csv").open(
        newline=""
    ) as f:
        rows = list(csv.DictReader(f))
    assert summary["status"] == "V2_PATH_PARTIAL_SCOPE_VALUES_FROZEN_NOT_ENDPOINT_READY"
    assert summary["total_path_scope_candidate_count"] == "12"
    assert summary["partial_path_values_computed"] == "true"
    assert summary["full_lowz_path_values_computed"] == "false"
    assert summary["nonzero_partial_path_value_count"] == "12"
    assert summary["rule_status"] == "SOURCE_ONLY_TILE_PROXIMITY_CONTROL_NOT_PHYSICAL_LENSING_WEIGHT"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["verdict"] == "partial_scope_W_path_values_available_only_as_source_side_control"
    assert rows
    nonzero = [row for row in rows if float(row["W_path_source_value"]) > 0.0]
    assert len(nonzero) == 12
    assert {row["contains_lensing_residuals"] for row in rows} == {"false"}
    assert {row["uses_kids_data_vector_values"] for row in rows} == {"false"}


def test_void_source_basis_refinement_v2_path_partial_scope_reviewer_package_v1_is_source_side_only() -> None:
    for command in [
        ["python", "scripts/build_void_source_basis_refinement_v2_path_projection_crossmap_audit_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_v2_path_projection_crossmap_audit_v1.py"],
        ["python", "scripts/build_void_source_basis_refinement_v2_path_partial_scope_policy_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_v2_path_partial_scope_policy_v1.py"],
        ["python", "scripts/build_void_source_basis_refinement_v2_path_partial_scope_values_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_v2_path_partial_scope_values_v1.py"],
        ["python", "scripts/build_void_source_basis_refinement_v2_path_projection_route_ledger_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_v2_path_projection_route_ledger_v1.py"],
        ["python", "scripts/build_void_source_basis_refinement_v2_multichannel_coupling_ledger_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_v2_multichannel_coupling_ledger_v1.py"],
        ["python", "scripts/build_void_source_basis_refinement_v2_path_partial_scope_reviewer_package_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_v2_path_partial_scope_reviewer_package_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (
        ROOT / "data/derived/void_source_basis_refinement_v2_path_partial_scope_reviewer_package_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/void_source_basis_refinement_v2_path_partial_scope_reviewer_package_v1_manifest.csv"
    ).open(newline="") as f:
        manifest = list(csv.DictReader(f))
    zip_path = ROOT / summary["zip_path"]
    zip_sha256_path = ROOT / summary["zip_sha256_path"]
    assert summary["status"] == "V2_PATH_PARTIAL_SCOPE_REVIEWER_PACKAGE_BUILT_NOT_COMPLETED"
    assert summary["verdict"] == "partial_path_scope_reviewer_package_ready_not_completed"
    assert summary["review_completed"] == "false"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["contains_endpoint_residuals"] == "false"
    assert summary["contains_endpoint_scores"] == "false"
    assert summary["contains_fit_statistics"] == "false"
    assert zip_path.exists()
    assert zip_sha256_path.exists()
    assert zip_sha256_path.read_text().strip().endswith(f"  {zip_path.name}")
    assert "data/derived/void_source_basis_refinement_v2_path_partial_scope_reviewer_response_template_v1.csv" in {
        row["package_path"] for row in manifest
    }
    assert {row["endpoint_replay_allowed"] for row in manifest} == {"false"}
    assert {row["endpoint_validation_claimed"] for row in manifest} == {"false"}
    assert {row["contains_endpoint_residuals"] for row in manifest} == {"false"}
    assert {row["contains_endpoint_scores"] for row in manifest} == {"false"}
    assert {row["contains_fit_statistics"] for row in manifest} == {"false"}


def test_void_source_basis_refinement_v2_path_partial_scope_completed_review_response_v1_is_caveated_source_side_only() -> None:
    for command in [
        ["python", "scripts/build_void_source_basis_refinement_v2_path_projection_crossmap_audit_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_v2_path_projection_crossmap_audit_v1.py"],
        ["python", "scripts/build_void_source_basis_refinement_v2_path_partial_scope_policy_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_v2_path_partial_scope_policy_v1.py"],
        ["python", "scripts/build_void_source_basis_refinement_v2_path_partial_scope_values_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_v2_path_partial_scope_values_v1.py"],
        ["python", "scripts/build_void_source_basis_refinement_v2_path_partial_scope_reviewer_package_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_v2_path_partial_scope_reviewer_package_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_v2_path_partial_scope_completed_review_response_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (
        ROOT
        / "data/derived/void_source_basis_refinement_v2_path_partial_scope_completed_review_response_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["review_completed"] == "true"
    assert summary["final_verdict"] == "ACCEPT_PARTIAL_PATH_CONTROL_AS_CAVEATED_SOURCE_SIDE"
    assert summary["acceptance_scope"] == "partial_scope_12_row_W_path_source_side_control_only"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["forbidden_inputs_used"] == "false"
    assert summary["physical_lensing_path_weight_claimed"] == "false"
    assert (
        summary["future_action_allowed"]
        == "prepare_separate_partial_scope_replay_authorization_package_only"
    )
    assert summary["verdict"] == "partial_path_scope_control_accepted_as_caveated_source_side_only"


def test_void_source_basis_refinement_v2_path_partial_scope_replay_authorization_package_v1_is_permission_request_only() -> None:
    for command in [
        ["python", "scripts/validate_void_source_basis_refinement_v2_path_partial_scope_completed_review_response_v1.py"],
        ["python", "scripts/build_void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_template_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_template_v1.py"],
        ["python", "scripts/build_void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_package_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_package_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (
        ROOT
        / "data/derived/void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_package_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (
        ROOT
        / "data/derived/void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_package_v1_manifest.csv"
    ).open(newline="") as f:
        manifest = list(csv.DictReader(f))
    zip_path = ROOT / summary["zip_path"]
    assert summary["status"] == "V2_PATH_PARTIAL_SCOPE_REPLAY_AUTHORIZATION_PACKAGE_BUILT_NOT_COMPLETED"
    assert summary["review_completed"] == "false"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["contains_endpoint_residuals"] == "false"
    assert summary["contains_endpoint_scores"] == "false"
    assert summary["contains_fit_statistics"] == "false"
    assert summary["physical_lensing_path_weight_claimed"] == "false"
    assert summary["verdict"] == "partial_path_scope_replay_authorization_package_ready_not_completed"
    assert zip_path.exists()
    assert {
        "data/derived/void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_response_template_v1.csv",
        "data/derived/void_source_basis_refinement_v2_path_partial_scope_completed_review_response_v1_summary.csv",
    }.issubset({row["package_path"] for row in manifest})
    assert {row["endpoint_replay_allowed"] for row in manifest} == {"false"}
    assert {row["endpoint_validation_claimed"] for row in manifest} == {"false"}
    assert {row["physical_lensing_path_weight_claimed"] for row in manifest} == {"false"}


def test_void_source_basis_refinement_v2_path_partial_scope_replay_authorization_response_v1_grants_permission_only() -> None:
    for command in [
        ["python", "scripts/validate_void_source_basis_refinement_v2_path_partial_scope_completed_review_response_v1.py"],
        ["python", "scripts/build_void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_template_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_template_v1.py"],
        ["python", "scripts/build_void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_package_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_package_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_response_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (
        ROOT
        / "data/derived/void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_response_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "V2_PATH_PARTIAL_SCOPE_REPLAY_AUTHORIZATION_ACCEPTED_PERMISSION_ONLY"
    assert summary["decision"] == "GO_PARTIAL_PATH_REPLAY_PERMISSION_ONLY"
    assert summary["review_completed"] == "true"
    assert summary["forbidden_inputs_used"] == "false"
    assert summary["endpoint_replay_allowed"] == "true"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_lensing_path_weight_claimed"] == "false"
    assert summary["authorization_scope"] == "single_permission_only_12_row_partial_W_path_replay_not_validation"
    assert summary["total_path_scope_candidate_count"] == "12"
    assert summary["remaining_lowz_rows_full_W_path_disabled"] == "412"
    assert summary["full_lowz_path_values_computed"] == "false"


def test_void_source_basis_refinement_v2_path_partial_scope_authorized_replay_v1_preserves_caveated_control_result() -> None:
    for command in [
        ["python", "scripts/validate_void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_response_v1.py"],
        ["python", "scripts/run_void_source_basis_refinement_v2_path_partial_scope_authorized_replay_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_v2_path_partial_scope_authorized_replay_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (
        ROOT / "data/derived/void_source_basis_refinement_v2_path_partial_scope_authorized_replay_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "V2_PATH_PARTIAL_SCOPE_REPLAY_AUTHORIZED_PERMISSION_ONLY_NOT_VALIDATION"
    assert summary["authorization_decision"] == "GO_PARTIAL_PATH_REPLAY_PERMISSION_ONLY"
    assert summary["n_rows"] == "12"
    assert summary["endpoint_replay_allowed"] == "true"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_lensing_path_weight_claimed"] == "false"
    assert summary["active_channel_family"] == "W_PATH_PROJECTION_PARTIAL_SCOPE_CONTROL"
    assert "FULL_LOWZ_W_PATH_CHANNEL" in summary["disabled_channels"]
    assert float(summary["delta_chi2_candidate_minus_baseline"]) < 0.0
    assert float(summary["delta_aic_candidate_minus_baseline"]) > 0.0
    assert int(summary["controls_better_than_candidate_chi2"]) == 2
    assert summary["candidate_rank_by_chi2_among_candidate_and_controls"] == "3"
    assert summary["best_control_branch"] == "rank_reverse_path_control"
    assert summary["claim_boundary"] == "v2_path_partial_scope_authorized_replay_permission_only_not_validation"


def test_void_source_basis_refinement_v2_path_coupled_projection_screen_v1_is_not_endpoint_validation() -> None:
    for command in [
        ["python", "scripts/run_void_source_basis_refinement_v2_path_coupled_projection_screen_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_v2_path_coupled_projection_screen_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (
        ROOT / "data/derived/void_source_basis_refinement_v2_path_coupled_projection_screen_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "V2_PATH_COUPLED_PROJECTION_SCREEN_PREAUTH_DIAGNOSTIC_NOT_ENDPOINT"
    assert summary["screen_status"] == "preauthorization_diagnostic_not_endpoint"
    assert summary["n_rows"] == "12"
    assert summary["normalization_rule"] == "max_abs_on_12_row_source_scope"
    assert summary["diagnostic_screen_executed"] == "true"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_lensing_path_weight_claimed"] == "false"
    assert summary["best_candidate_family"] in {
        "W_path",
        "W_path_x_W_void_centered",
        "W_path_x_W_web_centered",
        "W_path_x_W_void_centered_x_W_web_centered",
    }
    assert float(summary["delta_chi2_candidate_minus_baseline"]) < 0.0
    assert int(summary["candidate_rank_by_chi2_among_candidate_and_controls"]) >= 1
    assert int(summary["controls_better_than_candidate_chi2"]) >= 0
    assert summary["verdict"] in {
        "coupled_candidate_survives_fast_screen_requires_authorization",
        "coupled_candidate_not_control_resistant_in_fast_screen",
    }
    assert summary["claim_boundary"] == "v2_path_coupled_projection_screen_not_endpoint_not_validation"


def test_void_source_basis_refinement_v2_path_transform_bank_screen_v1_is_not_endpoint_validation() -> None:
    for command in [
        ["python", "scripts/run_void_source_basis_refinement_v2_path_transform_bank_screen_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_v2_path_transform_bank_screen_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (
        ROOT / "data/derived/void_source_basis_refinement_v2_path_transform_bank_screen_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/void_source_basis_refinement_v2_path_transform_bank_screen_v1_family_summary.csv"
    ).open(newline="") as f:
        families = list(csv.DictReader(f))
    assert summary["status"] == "V2_PATH_TRANSFORM_BANK_SCREEN_PREAUTH_DIAGNOSTIC_NOT_ENDPOINT"
    assert summary["screen_status"] == "preauthorization_diagnostic_not_endpoint"
    assert summary["n_rows"] == "12"
    assert summary["normalization_rule"] == "max_abs_on_12_row_source_scope"
    assert summary["diagnostic_screen_executed"] == "true"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_lensing_path_weight_claimed"] == "false"
    assert summary["best_candidate_family"]
    assert float(summary["delta_chi2_candidate_minus_baseline"]) < 0.0
    assert int(summary["candidate_rank_by_chi2_among_candidate_and_controls"]) >= 1
    assert int(summary["controls_better_than_candidate_chi2"]) >= 0
    assert len(families) == 40
    assert summary["verdict"] in {
        "path_transform_candidate_survives_fast_screen_requires_authorization",
        "path_transform_candidate_not_control_resistant_in_fast_screen",
    }
    assert summary["claim_boundary"] == "v2_path_transform_bank_screen_not_endpoint_not_validation"


def test_void_source_basis_refinement_v2_path_sky_environment_screen_v1_is_not_endpoint_validation() -> None:
    for command in [
        ["python", "scripts/run_void_source_basis_refinement_v2_path_sky_environment_screen_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_v2_path_sky_environment_screen_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (
        ROOT / "data/derived/void_source_basis_refinement_v2_path_sky_environment_screen_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/void_source_basis_refinement_v2_path_sky_environment_screen_v1_family_summary.csv"
    ).open(newline="") as f:
        families = list(csv.DictReader(f))
    assert summary["status"] == "V2_PATH_SKY_ENVIRONMENT_SCREEN_PREAUTH_DIAGNOSTIC_NOT_ENDPOINT"
    assert summary["screen_status"] == "preauthorization_diagnostic_not_endpoint"
    assert summary["n_rows"] == "12"
    assert summary["normalization_rule"] == "max_abs_on_12_row_source_scope"
    assert summary["diagnostic_screen_executed"] == "true"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_lensing_path_weight_claimed"] == "false"
    assert summary["best_candidate_family"]
    assert float(summary["delta_chi2_candidate_minus_baseline"]) < 0.0
    assert int(summary["candidate_rank_by_chi2_among_candidate_and_controls"]) >= 1
    assert int(summary["controls_better_than_candidate_chi2"]) >= 0
    assert len(families) == 14
    assert any(row["family_id"] == "W_path_x_sky_z" for row in families)
    assert summary["verdict"] in {
        "path_sky_environment_candidate_survives_fast_screen_requires_authorization",
        "path_sky_environment_candidate_not_control_resistant_in_fast_screen",
    }
    assert summary["claim_boundary"] == "v2_path_sky_environment_screen_not_endpoint_not_validation"


def test_void_source_basis_refinement_v2_observer_dependence_followup_package_v1_is_not_endpoint_validation() -> None:
    for command in [
        ["python", "scripts/build_void_source_basis_refinement_v2_observer_dependence_followup_template_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_v2_observer_dependence_followup_template_v1.py"],
        ["python", "scripts/build_void_source_basis_refinement_v2_observer_dependence_followup_package_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_v2_observer_dependence_followup_package_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (
        ROOT / "data/derived/void_source_basis_refinement_v2_observer_dependence_followup_template_v1_summary.csv"
    ).open(newline="") as f:
        template = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/void_source_basis_refinement_v2_observer_dependence_followup_package_v1_summary.csv"
    ).open(newline="") as f:
        package = list(csv.DictReader(f))[0]
    assert template["status"] == "V2_OBSERVER_DEPENDENCE_FOLLOWUP_TEMPLATE_READY_NOT_COMPLETED"
    assert template["followup_family"] == "W_path_x_sky_z"
    assert template["family_survives_controls"] == "true"
    assert template["review_completed"] == "false"
    assert template["endpoint_replay_allowed"] == "false"
    assert template["endpoint_validation_claimed"] == "false"
    assert template["physical_lensing_path_weight_claimed"] == "false"
    assert package["status"] == "V2_OBSERVER_DEPENDENCE_FOLLOWUP_PACKAGE_BUILT_NOT_COMPLETED"
    assert package["followup_family"] == "W_path_x_sky_z"
    assert package["review_completed"] == "false"
    assert package["endpoint_replay_allowed"] == "false"
    assert package["endpoint_validation_claimed"] == "false"
    assert package["contains_endpoint_residuals"] == "false"
    assert package["contains_endpoint_scores"] == "false"
    assert package["contains_fit_statistics"] == "false"
    assert package["physical_lensing_path_weight_claimed"] == "false"
    assert package["verdict"] == "observer_dependence_followup_package_ready_not_completed"
    assert package["claim_boundary"] == "v2_observer_dependence_followup_not_endpoint_not_validation"


def test_void_source_basis_refinement_v2_sky_z_replay_authorization_package_v1_is_permission_request_only() -> None:
    for command in [
        ["python", "scripts/build_void_source_basis_refinement_v2_sky_z_replay_authorization_review_template_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_v2_sky_z_replay_authorization_review_template_v1.py"],
        ["python", "scripts/build_void_source_basis_refinement_v2_sky_z_replay_authorization_review_package_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_v2_sky_z_replay_authorization_review_package_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (
        ROOT / "data/derived/void_source_basis_refinement_v2_sky_z_replay_authorization_review_template_v1_summary.csv"
    ).open(newline="") as f:
        template = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/void_source_basis_refinement_v2_sky_z_replay_authorization_review_package_v1_summary.csv"
    ).open(newline="") as f:
        package = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/void_source_basis_refinement_v2_sky_z_replay_authorization_review_package_v1_manifest.csv"
    ).open(newline="") as f:
        manifest = list(csv.DictReader(f))
    assert template["status"] == "V2_SKY_Z_REPLAY_AUTHORIZATION_TEMPLATE_READY_NOT_COMPLETED"
    assert template["followup_family"] == "W_path_x_sky_z"
    assert template["family_survives_controls"] == "true"
    assert template["controls_better_than_candidate_chi2"] == "0"
    assert template["review_completed"] == "false"
    assert template["endpoint_replay_allowed"] == "false"
    assert template["endpoint_validation_claimed"] == "false"
    assert package["status"] == "V2_SKY_Z_REPLAY_AUTHORIZATION_PACKAGE_BUILT_NOT_COMPLETED"
    assert package["followup_family"] == "W_path_x_sky_z"
    assert package["review_completed"] == "false"
    assert package["endpoint_replay_allowed"] == "false"
    assert package["endpoint_validation_claimed"] == "false"
    assert package["contains_endpoint_residuals"] == "false"
    assert package["contains_endpoint_scores"] == "false"
    assert package["contains_fit_statistics"] == "false"
    assert package["physical_lensing_path_weight_claimed"] == "false"
    assert package["verdict"] == "sky_z_replay_authorization_package_ready_not_completed"
    assert package["claim_boundary"] == "v2_sky_z_replay_authorization_review_not_validation"
    assert "data/derived/void_source_basis_refinement_v2_sky_z_replay_authorization_review_response_template_v1.csv" in {
        row["package_path"] for row in manifest
    }


def test_void_source_basis_refinement_v2_sky_z_authorized_replay_v1_is_permission_only_not_validation() -> None:
    for command in [
        ["python", "scripts/validate_void_source_basis_refinement_v2_sky_z_replay_authorization_review_response_v1.py"],
        ["python", "scripts/run_void_source_basis_refinement_v2_sky_z_authorized_replay_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_v2_sky_z_authorized_replay_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (
        ROOT / "data/derived/void_source_basis_refinement_v2_sky_z_replay_authorization_review_response_v1_summary.csv"
    ).open(newline="") as f:
        auth = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/void_source_basis_refinement_v2_sky_z_authorized_replay_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert auth["decision"] == "GO_SKY_Z_REPLAY_PERMISSION_ONLY"
    assert auth["endpoint_replay_allowed"] == "true"
    assert auth["endpoint_validation_claimed"] == "false"
    assert summary["status"] == "V2_SKY_Z_REPLAY_AUTHORIZED_PERMISSION_ONLY_NOT_VALIDATION"
    assert summary["active_family"] == "W_path_x_sky_z"
    assert summary["n_rows"] == "12"
    assert summary["family_survives_controls"] == "true"
    assert summary["controls_better_than_candidate_chi2"] == "0"
    assert float(summary["delta_chi2_candidate_minus_baseline"]) < 0.0
    assert float(summary["delta_chi2_candidate_minus_best_control"]) < 0.0
    assert summary["endpoint_replay_allowed"] == "true"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_lensing_path_weight_claimed"] == "false"
    assert summary["verdict"] == "sky_z_permission_replay_family_control_survives_not_validation"
    assert summary["claim_boundary"] == "v2_sky_z_authorized_replay_permission_only_not_validation"


def test_void_source_basis_refinement_v2_sky_z_source_audit_v1_is_not_scoring() -> None:
    for command in [
        ["python", "scripts/build_void_source_basis_refinement_v2_sky_z_source_audit_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_v2_sky_z_source_audit_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/void_source_basis_refinement_v2_sky_z_source_audit_v1.csv").open(
        newline=""
    ) as f:
        rows = list(csv.DictReader(f))
    with (ROOT / "data/derived/void_source_basis_refinement_v2_sky_z_source_audit_v1_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "V2_SKY_Z_SOURCE_AUDIT_BUILT_NOT_SCORING"
    assert summary["n_rows"] == "12"
    assert summary["positive_raw_count"] == "5"
    assert summary["negative_raw_count"] == "7"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_lensing_path_weight_claimed"] == "false"
    assert summary["claim_boundary"] == "v2_sky_z_source_audit_not_scoring_not_validation"
    assert len(rows) == 12
    assert all(row["contains_distance_residuals"] == "false" for row in rows)
    assert all(row["contains_fit_statistics"] == "false" for row in rows)
    assert all(row["endpoint_validation_claimed"] == "false" for row in rows)
    assert abs(max(abs(float(row["W_path_x_sky_z_normalized"])) for row in rows) - 1.0) < 1e-9


def test_void_source_basis_refinement_v2_observer_orientation_kernel_v2_is_source_side_only() -> None:
    for command in [
        ["python", "scripts/build_void_source_basis_refinement_v2_observer_orientation_kernel_v2.py"],
        ["python", "scripts/validate_void_source_basis_refinement_v2_observer_orientation_kernel_v2.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (
        ROOT / "data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    with (
        ROOT / "data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "OBSERVER_ORIENTATION_KERNEL_V2_BUILT_NOT_SCORING"
    assert summary["n_rows"] == "12"
    assert summary["primary_kernel"] == "W_path_times_centered_sky_z"
    assert summary["reference_kernel"] == "W_path_times_raw_sky_z"
    assert summary["primary_positive_count"] == "10"
    assert summary["primary_negative_count"] == "2"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_lensing_path_weight_claimed"] == "false"
    assert summary["claim_boundary"] == "v2_observer_orientation_kernel_v2_source_side_not_scoring"
    assert len(rows) == 12
    assert abs(sum(float(row["centered_sky_z"]) for row in rows)) < 1e-10
    assert abs(max(abs(float(row["K_primary_normalized"])) for row in rows) - 1.0) < 1e-9
    assert all(row["contains_distance_residuals"] == "false" for row in rows)
    assert all(row["contains_fit_statistics"] == "false" for row in rows)
    assert all(row["endpoint_validation_claimed"] == "false" for row in rows)


def test_void_source_basis_refinement_v2_observer_orientation_kernel_v2_authorization_package_is_not_replay() -> None:
    for command in [
        ["python", "scripts/build_void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_template.py"],
        ["python", "scripts/validate_void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_template.py"],
        ["python", "scripts/build_void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_package.py"],
        ["python", "scripts/validate_void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_package.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (
        ROOT / "data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_template_summary.csv"
    ).open(newline="") as f:
        template = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_package_summary.csv"
    ).open(newline="") as f:
        package = list(csv.DictReader(f))[0]
    assert template["status"] == "OBSERVER_ORIENTATION_KERNEL_V2_REPLAY_AUTHORIZATION_TEMPLATE_READY_NOT_COMPLETED"
    assert template["primary_kernel"] == "W_path_times_centered_sky_z"
    assert template["review_completed"] == "false"
    assert template["endpoint_replay_allowed"] == "false"
    assert template["endpoint_validation_claimed"] == "false"
    assert package["status"] == "OBSERVER_ORIENTATION_KERNEL_V2_REPLAY_AUTHORIZATION_PACKAGE_BUILT_NOT_COMPLETED"
    assert package["review_completed"] == "false"
    assert package["endpoint_replay_allowed"] == "false"
    assert package["endpoint_validation_claimed"] == "false"
    assert package["contains_endpoint_scores"] == "false"
    assert package["contains_fit_statistics"] == "false"
    assert package["physical_lensing_path_weight_claimed"] == "false"
    assert package["verdict"] == "observer_orientation_kernel_v2_replay_authorization_package_ready_not_completed"
    assert package["claim_boundary"] == "v2_observer_orientation_kernel_v2_replay_authorization_not_validation"


def test_void_source_basis_refinement_v2_observer_orientation_kernel_v2_authorized_replay_is_diagnostic_negative() -> None:
    for command in [
        ["python", "scripts/validate_void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_response.py"],
        ["python", "scripts/run_void_source_basis_refinement_v2_observer_orientation_kernel_v2_authorized_replay.py"],
        ["python", "scripts/validate_void_source_basis_refinement_v2_observer_orientation_kernel_v2_authorized_replay.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (
        ROOT
        / "data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_response_v1_summary.csv"
    ).open(newline="") as f:
        auth = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2_authorized_replay_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert auth["decision"] == "GO_OBSERVER_ORIENTATION_V2_REPLAY_PERMISSION_ONLY"
    assert auth["endpoint_replay_allowed"] == "true"
    assert auth["endpoint_validation_claimed"] == "false"
    assert summary["status"] == "V2_OBSERVER_ORIENTATION_KERNEL_V2_REPLAY_AUTHORIZED_PERMISSION_ONLY_NOT_VALIDATION"
    assert summary["active_family"] == "W_path_times_centered_sky_z"
    assert summary["n_rows"] == "12"
    assert summary["family_survives_controls"] == "false"
    assert summary["controls_better_than_candidate_chi2"] == "1"
    assert summary["candidate_rank_by_chi2_among_candidate_and_controls"] == "2"
    assert float(summary["delta_chi2_candidate_minus_baseline"]) < 0.0
    assert float(summary["delta_chi2_candidate_minus_best_control"]) > 0.0
    assert summary["endpoint_replay_allowed"] == "true"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_lensing_path_weight_claimed"] == "false"
    assert (
        summary["verdict"]
        == "observer_orientation_v2_permission_replay_not_control_resistant_not_validation"
    )
    assert (
        summary["claim_boundary"]
        == "v2_observer_orientation_kernel_v2_authorized_replay_permission_only_not_validation"
    )


def test_void_source_basis_refinement_v2_observer_basis_fast_screen_finds_review_candidate() -> None:
    for command in [
        ["python", "scripts/run_void_source_basis_refinement_v2_observer_basis_fast_screen_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_v2_observer_basis_fast_screen_v1.py"],
        ["python", "scripts/build_void_source_basis_refinement_v2_observer_basis_candidate_review_package_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_v2_observer_basis_candidate_review_package_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (
        ROOT / "data/derived/void_source_basis_refinement_v2_observer_basis_fast_screen_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/void_source_basis_refinement_v2_observer_basis_candidate_review_package_v1_summary.csv"
    ).open(newline="") as f:
        package = list(csv.DictReader(f))[0]
    assert summary["status"] == "V2_OBSERVER_BASIS_FAST_SCREEN_PREAUTH_DIAGNOSTIC_NOT_ENDPOINT"
    assert summary["best_candidate_family"] == "W_path_x_sky_x_x_zcenter"
    assert summary["surviving_family_count"] == "4"
    assert float(summary["best_candidate_delta_chi2_minus_baseline"]) < 0.0
    assert float(summary["best_candidate_delta_chi2_minus_best_global_control"]) < 0.0
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["claim_boundary"] == "v2_observer_basis_fast_screen_not_endpoint_not_validation"
    assert package["candidate_family"] == "W_path_x_sky_x_x_zcenter"
    assert package["review_completed"] == "false"
    assert package["endpoint_replay_allowed"] == "false"
    assert package["endpoint_validation_claimed"] == "false"
    assert package["verdict"] == "observer_basis_candidate_review_package_ready_not_completed"


def test_void_source_basis_refinement_v2_observer_basis_candidate_review_response_builds_replay_auth_package() -> None:
    for command in [
        ["python", "scripts/validate_void_source_basis_refinement_v2_observer_basis_candidate_review_response_v1.py"],
        ["python", "scripts/build_void_source_basis_refinement_v2_observer_basis_replay_authorization_package_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_v2_observer_basis_replay_authorization_package_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (
        ROOT / "data/derived/void_source_basis_refinement_v2_observer_basis_candidate_review_response_v1_summary.csv"
    ).open(newline="") as f:
        response = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/void_source_basis_refinement_v2_observer_basis_replay_authorization_package_v1_summary.csv"
    ).open(newline="") as f:
        package = list(csv.DictReader(f))[0]
    assert response["decision"] == "ACCEPT_OBSERVER_BASIS_CANDIDATE_FOR_SEPARATE_PERMISSION_ONLY_REPLAY_AUTHORIZATION_PACKAGE"
    assert response["endpoint_replay_allowed"] == "false"
    assert response["endpoint_validation_claimed"] == "false"
    assert response["recommended_next_action"] == "build_separate_permission_only_replay_authorization_package_for_W_path_x_sky_x_x_zcenter"
    assert package["candidate_family"] == "W_path_x_sky_x_x_zcenter"
    assert package["review_completed"] == "false"
    assert package["endpoint_replay_allowed"] == "false"
    assert package["endpoint_validation_claimed"] == "false"
    assert package["physical_lensing_path_weight_claimed"] == "false"
    assert package["verdict"] == "observer_basis_replay_authorization_package_ready_not_completed"


def test_void_source_basis_refinement_v2_observer_basis_authorized_replay_survives_controls() -> None:
    for command in [
        ["python", "scripts/validate_void_source_basis_refinement_v2_observer_basis_replay_authorization_response_v1.py"],
        ["python", "scripts/run_void_source_basis_refinement_v2_observer_basis_authorized_replay_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_v2_observer_basis_authorized_replay_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (
        ROOT / "data/derived/void_source_basis_refinement_v2_observer_basis_replay_authorization_response_v1_summary.csv"
    ).open(newline="") as f:
        auth = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/void_source_basis_refinement_v2_observer_basis_authorized_replay_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert auth["decision"] == "GO_OBSERVER_BASIS_REPLAY_PERMISSION_ONLY"
    assert auth["endpoint_replay_allowed"] == "true"
    assert auth["endpoint_validation_claimed"] == "false"
    assert summary["status"] == "V2_OBSERVER_BASIS_REPLAY_AUTHORIZED_PERMISSION_ONLY_NOT_VALIDATION"
    assert summary["active_family"] == "W_path_x_sky_x_x_zcenter"
    assert summary["n_rows"] == "12"
    assert summary["family_survives_controls"] == "true"
    assert summary["controls_better_than_candidate_chi2"] == "0"
    assert summary["candidate_rank_by_chi2_among_candidate_and_controls"] == "1"
    assert float(summary["delta_chi2_candidate_minus_baseline"]) < 0.0
    assert float(summary["delta_chi2_candidate_minus_best_control"]) < 0.0
    assert summary["endpoint_replay_allowed"] == "true"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_lensing_path_weight_claimed"] == "false"
    assert summary["verdict"] == "observer_basis_permission_replay_family_control_survives_not_validation"


def test_void_source_basis_refinement_v2_full_kernel_proxy_fast_screen_preserves_claim_boundary() -> None:
    for command in [
        ["python", "scripts/run_void_source_basis_refinement_v2_full_kernel_proxy_fast_screen_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_v2_full_kernel_proxy_fast_screen_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (
        ROOT / "data/derived/void_source_basis_refinement_v2_full_kernel_proxy_fast_screen_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/void_source_basis_refinement_v2_full_kernel_proxy_fast_screen_v1_family_summary.csv"
    ).open(newline="") as f:
        families = list(csv.DictReader(f))
    assert summary["status"] == "V2_FULL_KERNEL_PROXY_FAST_SCREEN_PREAUTH_DIAGNOSTIC_NOT_ENDPOINT"
    assert summary["n_rows"] == "12"
    assert summary["best_candidate_family"] == "W_path_x_sky_x_x_zcenter"
    assert summary["surviving_family_count"] == "2"
    assert "W_path_x_sky_x_x_zcenter_x_web_centered_x_los_density_mean" in summary["surviving_families"]
    assert float(summary["best_candidate_delta_chi2_minus_baseline"]) < 0.0
    assert float(summary["best_candidate_delta_chi2_minus_best_global_control"]) > 0.0
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_lensing_path_weight_claimed"] == "false"
    assert summary["claim_boundary"] == "v2_full_kernel_proxy_fast_screen_not_endpoint_not_validation"
    enriched = {
        row["family_id"]: row
        for row in families
        if row["family_id"] == "W_path_x_sky_x_x_zcenter_x_web_centered_x_los_density_mean"
    }
    assert enriched
    assert enriched["W_path_x_sky_x_x_zcenter_x_web_centered_x_los_density_mean"][
        "survives_family_controls"
    ] == "true"


def test_void_source_basis_refinement_v2_full_kernel_proxy_component_audit_preserves_negative_constraint() -> None:
    for command in [
        ["python", "scripts/build_void_source_basis_refinement_v2_full_kernel_proxy_component_audit_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_v2_full_kernel_proxy_component_audit_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (
        ROOT / "data/derived/void_source_basis_refinement_v2_full_kernel_proxy_component_audit_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/void_source_basis_refinement_v2_full_kernel_proxy_component_audit_v1.csv"
    ).open(newline="") as f:
        audit = list(csv.DictReader(f))
    assert summary["base_family"] == "W_path_x_sky_x_x_zcenter"
    assert summary["families_stronger_than_base"] == "0"
    assert "W_path_x_sky_x_x_zcenter_x_web_centered_x_los_density_mean" in summary[
        "control_surviving_enriched_families"
    ]
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_lensing_path_weight_claimed"] == "false"
    assert summary["claim_boundary"] == "v2_full_kernel_proxy_component_audit_not_endpoint_not_validation"
    assert summary["verdict"] == "extra_proxy_factors_do_not_outperform_base_observer_basis"
    base_rows = [row for row in audit if row["family_id"] == "W_path_x_sky_x_x_zcenter"]
    assert len(base_rows) == 1
    assert base_rows[0]["interpretation"] == "reference_observer_basis_carrier"


def test_full_observer_path_kernel_source_requirements_remain_non_scoring() -> None:
    subprocess.run(
        ["python", "scripts/validate_full_observer_path_kernel_source_requirements_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with (ROOT / "data/source_manifest/full_observer_path_kernel_source_requirements_v1.csv").open(
        newline=""
    ) as f:
        rows = list(csv.DictReader(f))
    assert {row["requirement_id"] for row in rows} == {"R1", "R2", "R3", "R4", "R5", "R6"}
    assert all(row["endpoint_replay_allowed"] == "false" for row in rows)
    assert all(row["endpoint_validation_claimed"] == "false" for row in rows)
    assert all(row["physical_lensing_path_weight_claimed"] == "false" for row in rows)
    assert any(row["channel"] == "metric_lensing_path" for row in rows)
    assert any(row["channel"] == "time_readout_phase" for row in rows)


def test_low_z_pantheon_los_radial_profile_is_source_side_partial_observable() -> None:
    for command in [
        ["python", "scripts/build_low_z_pantheon_los_radial_profile_v1.py"],
        ["python", "scripts/validate_low_z_pantheon_los_radial_profile_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/low_z_pantheon_los_radial_profile_v1_summary.csv").open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "LOS_RADIAL_PROFILE_BUILT_SOURCE_SIDE_NOT_SCORING"
    assert summary["rows"] == "424"
    assert summary["shell_count"] == "5"
    assert summary["complete_profile_rows"] == "153"
    assert summary["partial_path_scope_rows"] == "12"
    assert summary["partial_path_scope_complete_profile_rows"] == "7"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_lensing_path_weight_claimed"] == "false"
    assert summary["verdict"] == "los_radial_profile_available_as_partial_source_observable_not_full_path_integral"


def test_low_z_pantheon_path_aware_void_geometry_is_source_side_partial_observable() -> None:
    for command in [
        ["python", "scripts/build_low_z_pantheon_path_aware_void_geometry_v1.py"],
        ["python", "scripts/validate_low_z_pantheon_path_aware_void_geometry_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/low_z_pantheon_path_aware_void_geometry_v1_summary.csv").open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "PATH_AWARE_VOID_GEOMETRY_BUILT_SOURCE_SIDE_NOT_SCORING"
    assert summary["rows"] == "424"
    assert summary["path_intersection_rows"] == "180"
    assert summary["partial_path_scope_rows"] == "12"
    assert summary["partial_path_scope_intersection_rows"] == "10"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_lensing_path_weight_claimed"] == "false"
    assert summary["verdict"] == "path_aware_void_geometry_available_as_source_observable_not_full_metric_path"


def test_low_z_pantheon_directional_web_anisotropy_is_source_side_partial_observable() -> None:
    for command in [
        ["python", "scripts/build_low_z_pantheon_directional_web_anisotropy_v1.py"],
        ["python", "scripts/validate_low_z_pantheon_directional_web_anisotropy_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/low_z_pantheon_directional_web_anisotropy_v1_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "DIRECTIONAL_WEB_ANISOTROPY_BUILT_SOURCE_SIDE_NOT_SCORING"
    assert summary["rows"] == "424"
    assert summary["nonempty_web_cone_rows"] == "260"
    assert summary["quadrupole_ready_rows"] == "238"
    assert summary["partial_path_scope_rows"] == "12"
    assert summary["partial_path_scope_quadrupole_ready_rows"] == "9"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_lensing_path_weight_claimed"] == "false"
    assert summary["verdict"] == "directional_web_anisotropy_available_as_partial_source_observable_not_full_path_tensor"


def test_low_z_pantheon_metric_lensing_path_route_audit_preserves_r5_blocker() -> None:
    for command in [
        ["python", "scripts/build_low_z_pantheon_metric_lensing_path_route_audit_v1.py"],
        ["python", "scripts/validate_low_z_pantheon_metric_lensing_path_route_audit_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/low_z_pantheon_metric_lensing_path_route_audit_v1_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "METRIC_LENSING_PATH_ROUTE_AUDIT_BUILT_SOURCE_SIDE_NOT_SCORING"
    assert summary["rows"] == "424"
    assert summary["rows_nearest_kids_tile_within_1_deg"] == "5"
    assert summary["partial_path_scope_rows"] == "12"
    assert summary["partial_path_scope_nearest_kids_tile_within_1_deg"] == "5"
    assert summary["metric_lensing_numeric_product_available_for_source"] == "false"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_lensing_path_weight_claimed"] == "false"
    assert summary["verdict"] == "metric_lensing_routes_available_but_source_aligned_path_weight_missing"


def test_low_z_pantheon_time_readout_source_audit_preserves_r6_activation_blocker() -> None:
    for command in [
        ["python", "scripts/build_low_z_pantheon_time_readout_source_audit_v1.py"],
        ["python", "scripts/validate_low_z_pantheon_time_readout_source_audit_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/low_z_pantheon_time_readout_source_audit_v1_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "TIME_READOUT_SOURCE_AUDIT_BUILT_SOURCE_SIDE_NOT_SCORING"
    assert summary["rows"] == "424"
    assert summary["cc_hz_row_count"] == "32"
    assert summary["low_z_rows_with_cc_hz_support_delta_z_le_0p05"] == "424"
    assert summary["partial_path_scope_rows"] == "12"
    assert summary["partial_path_scope_cc_hz_support_delta_z_le_0p05"] == "12"
    assert summary["cc_hz_product_fetched_frozen"] == "true"
    assert summary["sdss_bao_rsd_products_fetched_frozen"] == "true"
    assert summary["cmb_route_cache_available"] == "true"
    assert summary["delta_clock_scale_frozen"] == "false"
    assert summary["time_readout_numeric_rule_available"] == "false"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["verdict"] == "time_readout_sources_partially_available_but_delta_clock_rule_missing"


def test_low_z_pantheon_time_readout_clock_scale_candidate_does_not_activate_w_time() -> None:
    for command in [
        ["python", "scripts/build_low_z_pantheon_time_readout_clock_scale_candidate_v1.py"],
        ["python", "scripts/validate_low_z_pantheon_time_readout_clock_scale_candidate_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (
        ROOT / "data/derived/low_z_pantheon_time_readout_clock_scale_candidate_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "TIME_READOUT_CLOCK_SCALE_CANDIDATE_BUILT_SOURCE_SIDE_NOT_SCORING"
    assert summary["cc_hz_row_count"] == "32"
    assert summary["delta_clock_star_candidate_rule"] == "median_errHz_over_Hz_from_CC_table"
    assert summary["delta_clock_star_candidate"] == "0.16581626506"
    assert summary["delta_clock_values_computed"] == "false"
    assert summary["W_time_values_computed"] == "false"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["verdict"] == "delta_clock_star_candidate_frozen_but_delta_clock_and_w_time_missing"


def test_low_z_pantheon_time_readout_redshift_bin_policy_candidate_does_not_activate_w_time() -> None:
    for command in [
        ["python", "scripts/build_low_z_pantheon_time_readout_redshift_bin_policy_candidate_v1.py"],
        ["python", "scripts/validate_low_z_pantheon_time_readout_redshift_bin_policy_candidate_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (
        ROOT / "data/derived/low_z_pantheon_time_readout_redshift_bin_policy_candidate_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "TIME_READOUT_REDSHIFT_BIN_POLICY_CANDIDATE_BUILT_SOURCE_SIDE_NOT_SCORING"
    assert summary["rows"] == "424"
    assert summary["cc_hz_row_count"] == "32"
    assert summary["used_cc_bin_count"] == "3"
    assert summary["low_z_rows_with_cc_hz_support_delta_z_le_0p05"] == "424"
    assert summary["delta_clock_star_candidate"] == "0.16581626506"
    assert summary["delta_clock_values_computed"] == "false"
    assert summary["W_time_values_computed"] == "false"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["verdict"] == "redshift_bin_policy_candidate_frozen_but_delta_clock_and_w_time_missing"


def test_low_z_pantheon_time_readout_delta_clock_uncertainty_candidate_does_not_activate_w_time() -> None:
    for command in [
        ["python", "scripts/build_low_z_pantheon_time_readout_delta_clock_uncertainty_candidate_v1.py"],
        ["python", "scripts/validate_low_z_pantheon_time_readout_delta_clock_uncertainty_candidate_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (
        ROOT / "data/derived/low_z_pantheon_time_readout_delta_clock_uncertainty_candidate_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "TIME_READOUT_DELTA_CLOCK_UNCERTAINTY_CANDIDATE_BUILT_SOURCE_SIDE_NOT_SCORING"
    assert summary["rows"] == "424"
    assert summary["cc_hz_row_count"] == "32"
    assert summary["used_cc_bin_count"] == "3"
    assert summary["delta_clock_star_candidate"] == "0.16581626506"
    assert summary["delta_clock_min"] == "0.0476000829881"
    assert summary["delta_clock_max"] == "0.834341816646"
    assert summary["W_time_values_computed"] == "false"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["verdict"] == "delta_clock_uncertainty_candidate_frozen_but_w_time_missing"


def test_low_z_pantheon_w_time_uncertainty_basis_candidate_is_not_endpoint_authorized() -> None:
    for command in [
        ["python", "scripts/build_low_z_pantheon_w_time_uncertainty_basis_candidate_v1.py"],
        ["python", "scripts/validate_low_z_pantheon_w_time_uncertainty_basis_candidate_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (
        ROOT / "data/derived/low_z_pantheon_w_time_uncertainty_basis_candidate_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "W_TIME_UNCERTAINTY_BASIS_CANDIDATE_BUILT_SOURCE_SIDE_NOT_SCORING"
    assert summary["rows"] == "424"
    assert summary["W_time_min"] == "-4.23048519997"
    assert summary["W_time_max"] == "2.81443932804"
    assert summary["W_time_values_computed"] == "true"
    assert summary["W_time_values_status"] == "SOURCE_SIDE_BASIS_CANDIDATE_ONLY_NOT_ENDPOINT"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["verdict"] == "w_time_uncertainty_basis_candidate_frozen_not_endpoint_authorized"


def test_low_z_pantheon_w_time_uncertainty_basis_replay_authorization_package_is_not_completed() -> None:
    for command in [
        ["python", "scripts/build_low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_template_v1.py"],
        ["python", "scripts/validate_low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_template_v1.py"],
        ["python", "scripts/build_low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_package_v1.py"],
        ["python", "scripts/validate_low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_package_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (
        ROOT / "data/derived/low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_package_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "W_TIME_UNCERTAINTY_BASIS_REPLAY_AUTHORIZATION_PACKAGE_BUILT_NOT_COMPLETED"
    assert summary["zip_sha256"] == "2067b221b0309bb8fcc3a294fcebf5c8fddd6123d7d7d7a151615c992a2fd69f"
    assert summary["package_file_count"] == "16"
    assert summary["review_completed"] == "false"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["contains_endpoint_residuals"] == "false"
    assert summary["contains_endpoint_scores"] == "false"
    assert summary["verdict"] == "w_time_uncertainty_basis_replay_authorization_package_ready_not_completed"


def test_low_z_pantheon_w_time_uncertainty_basis_completed_review_is_permission_only() -> None:
    completed_summary = (
        ROOT
        / "data/derived/low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_response_v1_summary.csv"
    )
    assert completed_summary.exists()
    with completed_summary.open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["decision"] == "GO_W_TIME_UNCERTAINTY_BASIS_REPLAY_PERMISSION_ONLY"
    assert summary["endpoint_replay_allowed"] == "true"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"


def test_low_z_pantheon_w_time_uncertainty_basis_authorized_replay_is_not_control_resistant() -> None:
    for command in [
        ["python", "scripts/run_low_z_pantheon_w_time_uncertainty_basis_authorized_replay_v1.py"],
        ["python", "scripts/validate_low_z_pantheon_w_time_uncertainty_basis_authorized_replay_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (
        ROOT / "data/derived/low_z_pantheon_w_time_uncertainty_basis_authorized_replay_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["verdict"] == "w_time_permission_replay_not_control_resistant_not_validation"
    assert summary["delta_chi2_candidate_minus_baseline"] == "-0.652452012"
    assert summary["controls_better_than_candidate_chi2"] == "3"
    assert summary["best_control_branch"] == "rank_reverse"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"


def test_low_z_pantheon_w_time_uncertainty_basis_gate_status_is_permission_only_ready() -> None:
    for command in [
        ["python", "scripts/build_low_z_pantheon_w_time_uncertainty_basis_gate_status_ledger_v1.py"],
        ["python", "scripts/validate_low_z_pantheon_w_time_uncertainty_basis_gate_status_ledger_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (
        ROOT / "data/derived/low_z_pantheon_w_time_uncertainty_basis_gate_status_ledger_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "SCORING_READY_PERMISSION_ONLY"
    assert summary["passed_gate_count"] == "4"
    assert summary["blocked_gate_count"] == "0"
    assert summary["completed_review_response_exists"] == "true"
    assert summary["endpoint_replay_allowed"] == "true"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert summary["recommended_next_action"] == "run_authorized_replay"


def test_low_z_pantheon_observer_time_combined_fast_screen_preserves_observer_only_lead() -> None:
    for command in [
        ["python", "scripts/run_low_z_pantheon_observer_time_combined_fast_screen_v1.py"],
        ["python", "scripts/validate_low_z_pantheon_observer_time_combined_fast_screen_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (
        ROOT / "data/derived/low_z_pantheon_observer_time_combined_fast_screen_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/low_z_pantheon_observer_time_combined_fast_screen_v1_family_summary.csv"
    ).open(newline="") as f:
        family_rows = {row["family_id"]: row for row in csv.DictReader(f)}
    assert summary["status"] == "PREAUTH_FAST_SCREEN_COMPLETE_NOT_REPLAY_NOT_VALIDATION"
    assert summary["best_candidate_family"] == "observer_only"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert summary["delta_chi2_candidate_minus_baseline"] == "-0.58072431813"
    assert family_rows["observer_times_time"]["delta_chi2_candidate_minus_baseline"] == "-0.47793496041"
    assert family_rows["observer_plus_time"]["delta_chi2_candidate_minus_baseline"] == "-0.42374598383"
    assert family_rows["time_on_observer_scope"]["delta_chi2_candidate_minus_baseline"] == "-0.03049277409"


def test_low_z_pantheon_clock_rate_phase_fast_screen_is_not_control_resistant() -> None:
    for command in [
        ["python", "scripts/build_low_z_pantheon_time_readout_clock_rate_phase_candidate_v1.py"],
        ["python", "scripts/validate_low_z_pantheon_time_readout_clock_rate_phase_candidate_v1.py"],
        ["python", "scripts/run_low_z_pantheon_clock_rate_phase_fast_screen_v1.py"],
        ["python", "scripts/validate_low_z_pantheon_clock_rate_phase_fast_screen_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (
        ROOT / "data/derived/low_z_pantheon_time_readout_clock_rate_phase_candidate_v1_summary.csv"
    ).open(newline="") as f:
        candidate_summary = list(csv.DictReader(f))[0]
    with (ROOT / "data/derived/low_z_pantheon_clock_rate_phase_fast_screen_v1_summary.csv").open(
        newline=""
    ) as f:
        screen_summary = list(csv.DictReader(f))[0]
    assert candidate_summary["verdict"] == "clock_rate_phase_candidate_frozen_source_side_not_endpoint_authorized"
    assert candidate_summary["endpoint_replay_allowed"] == "false"
    assert screen_summary["verdict"] == "clock_rate_phase_fast_screen_not_control_resistant"
    assert screen_summary["best_candidate_family"] == "clock_phase"
    assert screen_summary["delta_chi2_candidate_minus_baseline"] == "-0.523771964"
    assert screen_summary["best_global_control_branch"] == "rank_reverse"
    assert screen_summary["best_global_control_family"] == "clock_level"
    assert screen_summary["endpoint_replay_allowed"] == "false"
    assert screen_summary["endpoint_validation_claimed"] == "false"
    assert screen_summary["physical_validation_claimed"] == "false"


def test_low_z_pantheon_clock_rate_phase_rank_control_audit_explains_blocker() -> None:
    for command in [
        ["python", "scripts/build_low_z_pantheon_clock_rate_phase_rank_control_audit_v1.py"],
        ["python", "scripts/validate_low_z_pantheon_clock_rate_phase_rank_control_audit_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (
        ROOT / "data/derived/low_z_pantheon_clock_rate_phase_rank_control_audit_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["verdict"] == "low_cc_bin_count_rank_control_dominance_confirmed_not_validation"
    assert summary["assigned_cc_bin_count"] == "3"
    assert summary["all_families_rank_control_dominated"] == "true"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"


def test_pantheon_clock_rate_phase_cc_support_fast_screen_improves_but_fails_global_control() -> None:
    for command in [
        ["python", "scripts/build_pantheon_time_readout_clock_rate_phase_cc_support_candidate_v1.py"],
        ["python", "scripts/validate_pantheon_time_readout_clock_rate_phase_cc_support_candidate_v1.py"],
        ["python", "scripts/run_pantheon_clock_rate_phase_cc_support_fast_screen_v1.py"],
        ["python", "scripts/validate_pantheon_clock_rate_phase_cc_support_fast_screen_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (
        ROOT / "data/derived/pantheon_time_readout_clock_rate_phase_cc_support_candidate_v1_summary.csv"
    ).open(newline="") as f:
        candidate_summary = list(csv.DictReader(f))[0]
    with (ROOT / "data/derived/pantheon_clock_rate_phase_cc_support_fast_screen_v1_summary.csv").open(
        newline=""
    ) as f:
        screen_summary = list(csv.DictReader(f))[0]
    family_rows = {
        row["family_id"]: row
        for row in csv.DictReader(
            (ROOT / "data/derived/pantheon_clock_rate_phase_cc_support_fast_screen_v1_family_summary.csv").open(
                newline=""
            )
        )
    }
    assert candidate_summary["included_rows"] == "1370"
    assert candidate_summary["used_cc_bin_count"] == "31"
    assert screen_summary["verdict"] == "clock_rate_phase_cc_support_fast_screen_not_control_resistant"
    assert screen_summary["best_candidate_family"] == "clock_slope"
    assert screen_summary["delta_chi2_candidate_minus_baseline"] == "-1.14287181"
    assert screen_summary["best_global_control_branch"] == "rank_reverse"
    assert screen_summary["best_global_control_family"] == "clock_level"
    assert screen_summary["controls_better_than_candidate_chi2"] == "1"
    assert family_rows["clock_slope"]["family_survives_local_controls"] == "true"
    assert screen_summary["endpoint_replay_allowed"] == "false"
    assert screen_summary["endpoint_validation_claimed"] == "false"
    assert screen_summary["physical_validation_claimed"] == "false"


def test_pantheon_clock_slope_route_gate_freezes_review_candidate_status() -> None:
    for command in [
        ["python", "scripts/build_pantheon_clock_slope_route_gate_v1.py"],
        ["python", "scripts/validate_pantheon_clock_slope_route_gate_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/pantheon_clock_slope_route_gate_v1.csv").open(newline="") as f:
        gate = list(csv.DictReader(f))[0]
    assert gate["selected_route_candidate_family"] == "clock_slope"
    assert gate["local_controls_pass"] == "true"
    assert gate["global_controls_pass"] == "false"
    assert gate["baseline_improves"] == "true"
    assert gate["endpoint_replay_allowed"] == "false"
    assert gate["route_status"] == "CLOCK_SLOPE_REVIEW_CANDIDATE_ENDPOINT_BLOCKED_BY_GLOBAL_CONTROL"


def test_pantheon_clock_slope_route_replay_authorization_package_is_not_completed() -> None:
    for command in [
        ["python", "scripts/build_pantheon_clock_slope_route_replay_authorization_review_template_v1.py"],
        ["python", "scripts/validate_pantheon_clock_slope_route_replay_authorization_review_template_v1.py"],
        ["python", "scripts/build_pantheon_clock_slope_route_replay_authorization_review_package_v1.py"],
        ["python", "scripts/validate_pantheon_clock_slope_route_replay_authorization_review_package_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (
        ROOT / "data/derived/pantheon_clock_slope_route_replay_authorization_review_package_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["verdict"] == "clock_slope_route_replay_authorization_package_ready_not_completed"
    assert summary["review_completed"] == "false"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["contains_endpoint_residuals"] == "false"
    assert summary["contains_endpoint_scores"] == "false"
    assert summary["contains_fit_statistics"] == "false"


def test_sdss_bao_time_readout_observable_route_audit_is_underresolved_nonreplay() -> None:
    for command in [
        ["python", "scripts/build_sdss_bao_time_readout_observable_route_audit_v1.py"],
        ["python", "scripts/validate_sdss_bao_time_readout_observable_route_audit_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/sdss_bao_time_readout_observable_route_audit_v1_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    with (ROOT / "data/derived/sdss_bao_time_readout_observable_route_audit_v1.csv").open(
        newline=""
    ) as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 2
    assert summary["verdict"] == "independent_radial_bao_time_observable_present_but_underresolved_not_replay"
    assert summary["radial_bao_rows"] == "2"
    assert summary["redshift_bin_count"] == "2"
    assert summary["independent_from_pantheon_distance_residuals"] == "true"
    assert summary["independent_from_cc_clock_level_route"] == "true"
    assert summary["rd_nuisance_unresolved"] == "true"
    assert summary["underresolved_for_endpoint_route"] == "true"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert {row["observable"] for row in rows} == {"DH_over_rd"}
    assert {row["contains_endpoint_scores"] for row in rows} == {"false"}
    assert {row["contains_residuals"] for row in rows} == {"false"}


def test_paper10_joint_cc_bao_time_route_consistency_audit_identifies_level_not_slope() -> None:
    for command in [
        ["python", "scripts/build_paper10_joint_cc_bao_time_route_consistency_audit_v1.py"],
        ["python", "scripts/validate_paper10_joint_cc_bao_time_route_consistency_audit_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/paper10_joint_cc_bao_time_route_consistency_audit_v1_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    with (ROOT / "data/derived/paper10_joint_cc_bao_time_route_consistency_audit_v1.csv").open(
        newline=""
    ) as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 2
    assert summary["verdict"] == "radial_bao_aligns_with_cc_level_not_cc_slope_underresolved_not_replay"
    assert summary["radial_bao_rows"] == "2"
    assert summary["nearest_cc_rows_used"] == "2"
    assert summary["bao_cc_level_two_point_alignment"] == "1"
    assert summary["bao_cc_slope_two_point_alignment"] == "-1"
    assert summary["rd_nuisance_unresolved"] == "true"
    assert summary["two_point_underresolved"] == "true"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert {row["contains_endpoint_scores"] for row in rows} == {"false"}
    assert {row["contains_residuals"] for row in rows} == {"false"}


def test_paper10_time_readout_route_synthesis_gate_preserves_blockers() -> None:
    for command in [
        ["python", "scripts/build_paper10_joint_cc_bao_time_route_consistency_audit_v1.py"],
        ["python", "scripts/validate_paper10_joint_cc_bao_time_route_consistency_audit_v1.py"],
        ["python", "scripts/build_paper10_time_readout_route_synthesis_gate_v1.py"],
        ["python", "scripts/validate_paper10_time_readout_route_synthesis_gate_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/paper10_time_readout_route_synthesis_gate_v1.csv").open(newline="") as f:
        gate = list(csv.DictReader(f))[0]
    assert gate["cc_selected_route"] == "clock_slope"
    assert gate["cc_local_controls_pass"] == "true"
    assert gate["cc_global_controls_pass"] == "false"
    assert gate["radial_bao_rows"] == "2"
    assert gate["radial_bao_independent_from_cc_clock_level_route"] == "true"
    assert gate["radial_bao_rd_nuisance_unresolved"] == "true"
    assert gate["radial_bao_underresolved_for_endpoint_route"] == "true"
    assert (
        gate["joint_cc_bao_time_route_verdict"]
        == "radial_bao_aligns_with_cc_level_not_cc_slope_underresolved_not_replay"
    )
    assert gate["joint_cc_bao_level_alignment"] == "1"
    assert gate["joint_cc_bao_slope_alignment"] == "-1"
    assert (
        gate["synthesis_status"]
        == "clock_slope_review_candidate_plus_independent_bao_level_route_underresolved_not_endpoint"
    )
    assert gate["endpoint_replay_allowed"] == "false"
    assert gate["endpoint_validation_claimed"] == "false"
    assert gate["physical_validation_claimed"] == "false"


def test_paper10_time_readout_level_slope_route_split_ledger_preserves_route_boundaries() -> None:
    for command in [
        ["python", "scripts/build_paper10_time_readout_level_slope_route_split_ledger_v1.py"],
        ["python", "scripts/validate_paper10_time_readout_level_slope_route_split_ledger_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/paper10_time_readout_level_slope_route_split_ledger_v1.csv").open(
        newline=""
    ) as f:
        rows = list(csv.DictReader(f))
    with (ROOT / "data/derived/paper10_time_readout_level_slope_route_split_ledger_v1_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    by_route = {row["route_id"]: row for row in rows}
    assert set(by_route) == {"time_level_route", "time_slope_route"}
    assert by_route["time_level_route"]["joint_route_alignment"] == "1"
    assert by_route["time_slope_route"]["joint_route_alignment"] == "-1"
    assert "rd_nuisance_unresolved" in by_route["time_level_route"]["main_blockers"]
    assert "two_point_underresolved" in by_route["time_level_route"]["main_blockers"]
    assert "global_rank_control_blocker" in by_route["time_slope_route"]["main_blockers"]
    assert "claiming_radial_BAO_as_clock_slope_support" in by_route["time_slope_route"]["forbidden_route"]
    assert summary["verdict"] == "level_and_slope_time_routes_split_source_side_not_endpoint"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"


def test_paper10_time_level_route_nuisance_interface_freeze_plan_blocks_rd_leakage() -> None:
    subprocess.run(
        ["python", "scripts/validate_paper10_time_level_route_nuisance_interface_freeze_plan_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with (ROOT / "data/derived/paper10_time_level_route_nuisance_interface_freeze_plan_v1_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["route_id"] == "time_level_route"
    assert summary["nuisance_parameter"] == "rd"
    assert summary["verdict"] == "time_level_route_rd_policy_required_before_endpoint"
    assert "two_point_directional_level_alignment_only" in summary["allowed_current_use"]
    assert "no_absolute_H_scale_claim" in summary["allowed_current_use"]
    assert "freeze_external_rd_prior_or_rd_marginalization_policy" in summary["next_required_source_gate"]
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"


def test_paper10_bao_rd_cancelled_time_level_difference_audit_remains_directional_only() -> None:
    for command in [
        ["python", "scripts/build_paper10_bao_rd_cancelled_time_level_difference_audit_v1.py"],
        ["python", "scripts/validate_paper10_bao_rd_cancelled_time_level_difference_audit_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/paper10_bao_rd_cancelled_time_level_difference_audit_v1_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    with (ROOT / "data/derived/paper10_bao_rd_cancelled_time_level_difference_audit_v1.csv").open(
        newline=""
    ) as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 2
    assert summary["rd_cancels_in_difference"] == "true"
    assert summary["differential_direction_sign_agreement"] == "true"
    assert float(summary["delta_bao_snr"]) < 1.0
    assert summary["amplitude_interpretation_allowed"] == "false"
    assert summary["verdict"] == "rd_cancels_direction_agrees_but_bao_delta_low_significance_not_endpoint"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert {row["contains_endpoint_scores"] for row in rows} == {"false"}
    assert {row["contains_residuals"] for row in rows} == {"false"}


def test_paper10_time_level_rd_policy_selection_gate_forbids_residual_rd_fit() -> None:
    subprocess.run(
        ["python", "scripts/validate_paper10_time_level_rd_policy_selection_gate_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with (ROOT / "data/source_manifest/paper10_time_level_rd_policy_selection_gate_v1.csv").open(
        newline=""
    ) as f:
        rows = list(csv.DictReader(f))
    with (ROOT / "data/derived/paper10_time_level_rd_policy_selection_gate_v1_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    by_option = {row["policy_option"]: row for row in rows}
    assert by_option["rd_cancelled_differential_direction"]["policy_status"] == "ACCEPT_CURRENT_SOURCE_SIDE_ONLY"
    assert by_option["rd_cancelled_differential_direction"]["endpoint_replay_allowed"] == "false"
    assert by_option["external_rd_prior"]["policy_status"] == "FUTURE_ROUTE_PENDING_SOURCE_FREEZE"
    assert by_option["analytic_rd_marginalization"]["policy_status"] == "FUTURE_ROUTE_PENDING_PROTOCOL_FREEZE"
    assert by_option["fit_rd_from_pantheon_residuals"]["policy_status"] == "FORBIDDEN"
    assert "fitted_rd_from_pantheon" in by_option["fit_rd_from_pantheon_residuals"]["forbidden_inputs"]
    assert summary["accepted_current_policy"] == "rd_cancelled_differential_direction"
    assert summary["current_endpoint_replay_allowed"] == "false"
    assert summary["verdict"] == "rd_cancelled_direction_only_currently_allowed_external_or_marginalized_rd_pending"


def test_paper10_external_rd_prior_freeze_protocol_is_template_only() -> None:
    subprocess.run(
        ["python", "scripts/validate_paper10_external_rd_prior_freeze_protocol_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with (ROOT / "data/derived/paper10_external_rd_prior_freeze_protocol_v1_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    with (ROOT / "data/derived/paper10_external_rd_prior_freeze_response_template_v1.csv").open(
        newline=""
    ) as f:
        template = list(csv.DictReader(f))[0]
    assert summary["verdict"] == "external_rd_prior_protocol_ready_but_no_numeric_prior_frozen"
    assert summary["template_ready"] == "true"
    assert summary["completed_response_present"] == "false"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert template["uses_pantheon_residuals"] == "false"
    assert template["uses_endpoint_scores"] == "false"
    assert template["uses_late_time_fit_parameters"] == "false"


def test_paper10_external_rd_prior_freeze_response_is_source_side_only() -> None:
    subprocess.run(
        ["python", "scripts/validate_paper10_external_rd_prior_freeze_response_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with (ROOT / "data/derived/paper10_external_rd_prior_freeze_response_v1_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["prior_source_id"] == "Planck2018_base_LCDM_TTTEEE_lowE_lensing_rdrag"
    assert summary["rd_mpc"] == "147.09"
    assert summary["sigma_rd_mpc"] == "0.26"
    assert summary["uses_pantheon_residuals"] == "false"
    assert summary["uses_endpoint_scores"] == "false"
    assert summary["uses_late_time_fit_parameters"] == "false"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert summary["verdict"] == "planck2018_rd_prior_frozen_as_caveated_external_source_not_endpoint"


def test_paper10_bao_rd_marginalization_protocol_is_source_side_only() -> None:
    subprocess.run(
        ["python", "scripts/validate_paper10_bao_rd_marginalization_protocol_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with (ROOT / "data/derived/paper10_bao_rd_marginalization_protocol_v1_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "RD_MARGINALIZATION_PROTOCOL_READY_NOT_REPLAY_NOT_VALIDATION"
    assert summary["route_id"] == "time_level_route"
    assert summary["nuisance_parameter"] == "beta_rd"
    assert summary["protocol_blocker_closed"] == "joint_rd_marginalization_protocol_definition"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert summary["verdict"] == "rd_marginalization_protocol_frozen_but_endpoint_still_blocked"


def test_paper10_time_level_endpoint_control_suite_protocol_is_declaration_only() -> None:
    subprocess.run(
        ["python", "scripts/validate_paper10_time_level_endpoint_control_suite_protocol_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with (ROOT / "data/derived/paper10_time_level_endpoint_control_suite_protocol_v1_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "TIME_LEVEL_ENDPOINT_CONTROL_SUITE_PROTOCOL_READY_NOT_REPLAY_NOT_VALIDATION"
    assert summary["route_id"] == "time_level_route"
    assert summary["control_family_count"] == "7"
    assert summary["protocol_blocker_closed"] == "endpoint_control_suite_definition"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert summary["verdict"] == "time_level_endpoint_control_suite_declared_but_not_replayed"


def test_paper10_time_level_bao_support_expansion_manifest_declares_routes_only() -> None:
    subprocess.run(
        ["python", "scripts/validate_paper10_time_level_bao_support_expansion_manifest_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with (ROOT / "data/derived/paper10_time_level_bao_support_expansion_manifest_v1_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "BAO_SUPPORT_EXPANSION_MANIFEST_DECLARED_NOT_REPLAY_NOT_VALIDATION"
    assert summary["current_radial_bao_rows"] == "2"
    assert summary["candidate_expansion_route_count"] == "3"
    assert summary["protocol_target_min_independent_radial_bins"] == "4"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert (
        summary["verdict"]
        == "bao_support_expansion_routes_declared_but_current_endpoint_still_two_point_blocked"
    )


def test_paper10_desi_dr2_bao_source_inventory_is_source_freeze_only() -> None:
    for command in [
        ["python", "scripts/build_paper10_desi_dr2_bao_source_inventory_v1.py"],
        ["python", "scripts/validate_paper10_desi_dr2_bao_source_inventory_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/paper10_desi_dr2_bao_source_inventory_v1_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    with (ROOT / "data/derived/paper10_desi_dr2_bao_source_inventory_v1.csv").open(
        newline=""
    ) as f:
        rows = list(csv.DictReader(f))
    assert summary["status"] == "DESI_DR2_BAO_SOURCE_INVENTORY_FROZEN_NOT_REPLAY_NOT_VALIDATION"
    assert summary["mean_row_count"] == "13"
    assert summary["covariance_dimension"] == "13"
    assert summary["radial_dh_over_rd_rows"] == "6"
    assert summary["candidate_bao_support_blocker_status"] == "source_frozen_but_not_integrated_into_endpoint"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert summary["verdict"] == "desi_dr2_public_bao_source_frozen_but_time_level_endpoint_not_replayed"
    assert len(rows) == 13
    assert len([row for row in rows if row["quantity"] == "DH_over_rs"]) == 6
    assert {row["endpoint_replay_allowed"] for row in rows} == {"false"}
    assert {row["endpoint_validation_claimed"] for row in rows} == {"false"}
    assert {row["physical_validation_claimed"] for row in rows} == {"false"}


def test_paper10_desi_dr2_radial_bao_time_interface_is_source_side_only() -> None:
    for command in [
        ["python", "scripts/build_paper10_desi_dr2_radial_bao_time_interface_v1.py"],
        ["python", "scripts/validate_paper10_desi_dr2_radial_bao_time_interface_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/paper10_desi_dr2_radial_bao_time_interface_v1_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    with (ROOT / "data/derived/paper10_desi_dr2_radial_bao_time_interface_v1.csv").open(
        newline=""
    ) as f:
        rows = list(csv.DictReader(f))
    with (ROOT / "data/derived/paper10_desi_dr2_radial_bao_time_interface_covariance_v1.csv").open(
        newline=""
    ) as f:
        cov_rows = list(csv.DictReader(f))
    assert summary["status"] == "DESI_DR2_RADIAL_BAO_TIME_INTERFACE_FROZEN_NOT_REPLAY_NOT_VALIDATION"
    assert summary["radial_row_count"] == "6"
    assert summary["covariance_dimension"] == "6"
    assert summary["z_min"] == "0.51"
    assert summary["z_max"] == "2.33"
    assert summary["beta_rd_nuisance_required"] == "true"
    assert summary["matched_cc_support_required_before_replay"] == "true"
    assert summary["control_seed_manifest_required_before_replay"] == "true"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert summary["verdict"] == "desi_radial_bao_time_interface_frozen_but_endpoint_replay_still_blocked"
    assert len(rows) == 6
    assert len(cov_rows) == 36
    assert {row["endpoint_replay_allowed"] for row in rows} == {"false"}
    assert {row["endpoint_replay_allowed"] for row in cov_rows} == {"false"}


def test_paper10_desi_dr2_radial_bao_cc_match_is_partial_source_ledger_only() -> None:
    for command in [
        ["python", "scripts/build_paper10_desi_dr2_radial_bao_cc_match_v1.py"],
        ["python", "scripts/validate_paper10_desi_dr2_radial_bao_cc_match_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/paper10_desi_dr2_radial_bao_cc_match_v1_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    with (ROOT / "data/derived/paper10_desi_dr2_radial_bao_cc_match_v1.csv").open(
        newline=""
    ) as f:
        rows = list(csv.DictReader(f))
    assert summary["status"] == "DESI_DR2_RADIAL_BAO_CC_MATCH_LEDGER_FROZEN_NOT_REPLAY_NOT_VALIDATION"
    assert summary["input_radial_rows"] == "6"
    assert summary["matched_within_cc_range_rows"] == "5"
    assert summary["blocked_outside_cc_range_rows"] == "1"
    assert summary["blocked_z_eff"] == "2.33"
    assert summary["cc_extrapolation_used"] == "false"
    assert summary["control_seed_manifest_required_before_replay"] == "true"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert summary["verdict"] == "desi_bao_cc_support_partially_matched_high_z_row_blocked_no_replay"
    assert len(rows) == 6
    assert len([row for row in rows if row["cc_support_status"] == "MATCHED_WITHIN_CC_RANGE"]) == 5
    assert len([row for row in rows if row["cc_support_status"] == "BLOCKED_OUTSIDE_CC_RANGE_NO_EXTRAPOLATION"]) == 1
    assert {row["cc_extrapolation_used"] for row in rows} == {"false"}
    assert {row["endpoint_replay_allowed"] for row in rows} == {"false"}


def test_paper10_desi_time_level_control_seed_manifest_is_frozen_not_replay() -> None:
    subprocess.run(
        ["python", "scripts/validate_paper10_desi_time_level_control_seed_manifest_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with (ROOT / "data/derived/paper10_desi_time_level_control_seed_manifest_v1_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    with (ROOT / "data/source_manifest/paper10_desi_time_level_control_seed_manifest_v1.csv").open(
        newline=""
    ) as f:
        rows = list(csv.DictReader(f))
    assert summary["status"] == "DESI_TIME_LEVEL_CONTROL_SEED_MANIFEST_FROZEN_NOT_REPLAY_NOT_VALIDATION"
    assert summary["control_family_count"] == "7"
    assert summary["deterministic_seed_min"] == "41001"
    assert summary["deterministic_seed_max"] == "41007"
    assert summary["transform_scope"] == "first_CC_matched_DESI_5row_scope"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert summary["verdict"] == "desi_time_level_control_seed_manifest_frozen_not_replayed"
    assert len(rows) == 7
    assert len({row["seed"] for row in rows}) == 7
    assert {row["endpoint_replay_allowed"] for row in rows} == {"false"}
    assert {row["endpoint_validation_claimed"] for row in rows} == {"false"}
    assert {row["physical_validation_claimed"] for row in rows} == {"false"}


def test_paper10_time_level_route_external_rd_readiness_gate_closes_only_source_side_blockers() -> None:
    for command in [
        ["python", "scripts/build_paper10_time_level_route_external_rd_readiness_gate_v1.py"],
        ["python", "scripts/validate_paper10_time_level_route_external_rd_readiness_gate_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/paper10_time_level_route_external_rd_readiness_gate_v1_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    with (ROOT / "data/derived/paper10_time_level_route_external_rd_readiness_gate_v1.csv").open(
        newline=""
    ) as f:
        rows = list(csv.DictReader(f))
    by_item = {row["item"]: row for row in rows}
    assert len(rows) == 11
    assert (
        summary["verdict"]
        == "desi_time_cc_matched_scope_and_controls_frozen_but_endpoint_authorization_missing"
    )
    assert summary["rd_prior_source_id"] == "Planck2018_base_LCDM_TTTEEE_lowE_lensing_rdrag"
    assert summary["rd_mpc"] == "147.09"
    assert summary["sigma_rd_mpc"] == "0.26"
    assert summary["desi_dr2_radial_dh_over_rd_rows"] == "6"
    assert summary["desi_dr2_covariance_dimension"] == "13"
    assert summary["desi_dr2_time_interface_z_range"] == "0.51;2.33"
    assert summary["desi_dr2_cc_matched_rows"] == "5"
    assert summary["desi_dr2_cc_blocked_rows"] == "1"
    assert summary["desi_dr2_first_cc_matched_endpoint_rows"] == "5"
    assert summary["desi_time_level_control_family_count"] == "7"
    assert summary["desi_time_level_control_seed_range"] == "41001;41007"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert "external_rd_prior_source_freeze" in summary["closed_source_side_blockers"]
    assert "joint_rd_marginalization_protocol_definition" in summary["closed_source_side_blockers"]
    assert "endpoint_control_suite_definition" in summary["closed_source_side_blockers"]
    assert "bao_support_expansion_manifest_declared" in summary["closed_source_side_blockers"]
    assert "desi_dr2_public_bao_source_inventory_frozen" in summary["closed_source_side_blockers"]
    assert "desi_dr2_radial_bao_time_interface_frozen" in summary["closed_source_side_blockers"]
    assert "desi_dr2_radial_bao_cc_match_ledger_frozen" in summary["closed_source_side_blockers"]
    assert "desi_dr2_high_z_row_policy_frozen" in summary["closed_source_side_blockers"]
    assert "desi_time_level_control_seed_manifest_frozen" in summary["closed_source_side_blockers"]
    assert (
        "low_significance_current_sdss_bao_difference"
        in summary["closed_diagnostics_not_active_endpoint_blockers"]
    )
    assert summary["open_endpoint_blockers"] == "time_level_endpoint_authorization_review_missing"
    assert by_item["time_level_endpoint_authorization_review_missing"]["status"] == "BLOCKER_OPEN"
    assert by_item["low_significance_current_sdss_bao_difference"]["status"] == "CLOSED_DIAGNOSTIC_NOT_DESI_BLOCKER"
    assert by_item["external_rd_prior_source_freeze"]["status"] == "CLOSED_SOURCE_SIDE"
    assert by_item["joint_rd_marginalization_protocol_definition"]["status"] == "CLOSED_SOURCE_SIDE"
    assert by_item["endpoint_control_suite_definition"]["status"] == "CLOSED_SOURCE_SIDE"
    assert by_item["bao_support_expansion_manifest_declared"]["status"] == "CLOSED_SOURCE_SIDE"
    assert by_item["desi_dr2_public_bao_source_inventory_frozen"]["status"] == "CLOSED_SOURCE_SIDE"
    assert by_item["desi_dr2_radial_bao_time_interface_frozen"]["status"] == "CLOSED_SOURCE_SIDE"
    assert by_item["desi_dr2_radial_bao_cc_match_ledger_frozen"]["status"] == "CLOSED_SOURCE_SIDE"
    assert by_item["desi_dr2_high_z_row_policy_frozen"]["status"] == "CLOSED_SOURCE_SIDE"
    assert by_item["desi_time_level_control_seed_manifest_frozen"]["status"] == "CLOSED_SOURCE_SIDE"
    assert {row["endpoint_replay_allowed"] for row in rows} == {"false"}
    assert {row["endpoint_validation_claimed"] for row in rows} == {"false"}
    assert {row["physical_validation_claimed"] for row in rows} == {"false"}


def test_paper10_desi_time_level_endpoint_authorization_package_is_blank_not_replay() -> None:
    for command in [
        ["python", "scripts/build_paper10_desi_time_level_endpoint_authorization_review_template_v1.py"],
        ["python", "scripts/validate_paper10_desi_time_level_endpoint_authorization_review_template_v1.py"],
        ["python", "scripts/build_paper10_desi_time_level_endpoint_authorization_review_package_v1.py"],
        ["python", "scripts/validate_paper10_desi_time_level_endpoint_authorization_review_package_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (
        ROOT / "data/derived/paper10_desi_time_level_endpoint_authorization_review_template_v1_summary.csv"
    ).open(newline="") as f:
        template_summary = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/paper10_desi_time_level_endpoint_authorization_review_response_template_v1.csv"
    ).open(newline="") as f:
        template_rows = list(csv.DictReader(f))
    with (
        ROOT / "data/derived/paper10_desi_time_level_endpoint_authorization_review_package_v1_summary.csv"
    ).open(newline="") as f:
        package_summary = list(csv.DictReader(f))[0]
    assert template_summary["status"] == "DESI_TIME_LEVEL_ENDPOINT_AUTHORIZATION_TEMPLATE_READY_NOT_COMPLETED"
    assert template_summary["desi_first_endpoint_rows"] == "5"
    assert template_summary["desi_control_family_count"] == "7"
    assert template_summary["desi_control_seed_range"] == "41001;41007"
    assert template_summary["review_completed"] == "false"
    assert template_summary["endpoint_replay_allowed"] == "false"
    assert template_summary["endpoint_validation_claimed"] == "false"
    assert template_summary["physical_validation_claimed"] == "false"
    assert len(template_rows) == 5
    assert {row["review_completed"] for row in template_rows} == {"false"}
    assert {row["forbidden_inputs_used"] for row in template_rows} == {"false"}
    assert {row["endpoint_replay_allowed"] for row in template_rows} == {"false"}
    assert {row["endpoint_validation_claimed"] for row in template_rows} == {"false"}
    assert {row["physical_validation_claimed"] for row in template_rows} == {"false"}
    assert package_summary["status"] == "DESI_TIME_LEVEL_ENDPOINT_AUTHORIZATION_PACKAGE_BUILT_NOT_COMPLETED"
    assert package_summary["package_file_count"] == "36"
    assert package_summary["review_completed"] == "false"
    assert package_summary["endpoint_replay_allowed"] == "false"
    assert package_summary["endpoint_validation_claimed"] == "false"
    assert package_summary["contains_endpoint_residuals"] == "false"
    assert package_summary["contains_endpoint_scores"] == "false"
    assert package_summary["contains_fit_statistics"] == "false"
    assert package_summary["physical_validation_claimed"] == "false"
    assert package_summary["verdict"] == "desi_time_level_endpoint_authorization_package_ready_not_completed"


def test_paper10_desi_time_level_endpoint_authorization_response_validator_accepts_permission_only_probe(
    tmp_path: Path,
) -> None:
    template_path = ROOT / "data/derived/paper10_desi_time_level_endpoint_authorization_review_response_template_v1.csv"
    with template_path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        row["review_completed"] = "true"
        row["reviewer_id_or_role"] = "synthetic_test_reviewer_not_canonical"
        row["reviewer_response"] = "accept"
        row["reviewer_rationale"] = (
            "Synthetic validator probe: frozen five-row scope, controls, and no-leakage "
            "conditions are acknowledged."
        )
        row["endpoint_replay_allowed"] = "true"
    probe = tmp_path / "desi_time_level_endpoint_authorization_response_probe.csv"
    summary_out = tmp_path / "desi_time_level_endpoint_authorization_response_probe_summary.csv"
    with probe.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    subprocess.run(
        [
            "python",
            "scripts/validate_paper10_desi_time_level_endpoint_authorization_review_response_v1.py",
            str(probe),
            "--summary-out",
            str(summary_out),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with summary_out.open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "DESI_TIME_LEVEL_ENDPOINT_AUTHORIZATION_ACCEPTED_PERMISSION_ONLY"
    assert summary["decision"] == "GO_DESI_CC_5ROW_TIME_LEVEL_REPLAY_PERMISSION_ONLY"
    assert summary["review_completed"] == "true"
    assert summary["forbidden_inputs_used"] == "false"
    assert summary["endpoint_replay_allowed"] == "true"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert summary["desi_first_endpoint_rows"] == "5"
    assert summary["desi_control_family_count"] == "7"


def test_paper10_desi_time_level_endpoint_authorization_response_is_accepted_permission_only() -> None:
    subprocess.run(
        ["python", "scripts/validate_paper10_desi_time_level_endpoint_authorization_review_response_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with (
        ROOT / "data/derived/paper10_desi_time_level_endpoint_authorization_review_response_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "DESI_TIME_LEVEL_ENDPOINT_AUTHORIZATION_ACCEPTED_PERMISSION_ONLY"
    assert summary["decision"] == "GO_DESI_CC_5ROW_TIME_LEVEL_REPLAY_PERMISSION_ONLY"
    assert summary["response_path"] == "data/derived/paper10_desi_time_level_endpoint_authorization_review_response_v1.csv"
    assert summary["review_completed"] == "true"
    assert summary["forbidden_inputs_used"] == "false"
    assert summary["endpoint_replay_allowed"] == "true"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert summary["authorization_scope"] == "single_permission_only_desi_cc_5row_time_level_replay_not_validation"
    assert summary["desi_first_endpoint_rows"] == "5"
    assert summary["desi_control_family_count"] == "7"
    assert summary["desi_control_seed_range"] == "41001;41007"
    assert summary["claim_boundary"] == "paper10_desi_time_level_endpoint_authorization_review_not_validation"


def test_paper10_desi_time_level_endpoint_replay_run_template_is_auth_required_not_replay() -> None:
    subprocess.run(
        ["python", "scripts/validate_paper10_desi_time_level_endpoint_replay_run_template_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with (ROOT / "data/source_manifest/paper10_desi_time_level_endpoint_replay_run_template_v1.csv").open(
        newline=""
    ) as f:
        row = list(csv.DictReader(f))[0]
    assert row["status"] == "DESI_TIME_LEVEL_ENDPOINT_REPLAY_PREPARED_AUTH_REQUIRED_NOT_VALIDATION"
    assert row["active_route_family"] == "DESI_CC_MATCHED_RADIAL_BAO_TIME_LEVEL"
    assert row["endpoint_scope"] == "first_CC_matched_DESI_5row_scope"
    assert row["radial_rows_allowed"] == "0;1;2;3;4"
    assert row["radial_rows_excluded"] == "5"
    assert row["endpoint_replay_allowed"] == "false"
    assert row["endpoint_validation_claimed"] == "false"
    assert row["physical_validation_claimed"] == "false"
    assert row["claim_boundary"] == "paper10_desi_time_level_endpoint_replay_template_not_validation"
    for marker in [
        "endpoint_scores_before_authorization",
        "fit_statistics_before_authorization",
        "posthoc_row_selection",
        "posthoc_control_selection",
        "posthoc_cc_extrapolation",
        "physical_validation_claims",
    ]:
        assert marker in row["forbidden_inputs"]


def test_paper10_desi_time_level_endpoint_authorized_replay_preserves_negative_control_result() -> None:
    for command in [
        ["python", "scripts/run_paper10_desi_time_level_endpoint_authorized_replay_v1.py"],
        ["python", "scripts/validate_paper10_desi_time_level_endpoint_authorized_replay_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/paper10_desi_time_level_endpoint_authorized_replay_v1_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    with (ROOT / "data/derived/paper10_desi_time_level_endpoint_authorized_replay_v1_grid.csv").open(
        newline=""
    ) as f:
        rows = list(csv.DictReader(f))
    assert summary["status"] == "DESI_TIME_LEVEL_ENDPOINT_AUTHORIZED_REPLAY_PERMISSION_ONLY_NOT_VALIDATION"
    assert summary["authorization_decision"] == "GO_DESI_CC_5ROW_TIME_LEVEL_REPLAY_PERMISSION_ONLY"
    assert summary["n_rows"] == "5"
    assert summary["excluded_radial_rows"] == "5"
    assert summary["branch_count"] == "8"
    assert summary["endpoint_replay_allowed"] == "true"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert summary["family_survives_controls"] == "false"
    assert summary["verdict"] == "desi_time_level_permission_replay_not_control_resistant_not_validation"
    assert summary["best_control_branch"] == "redshift_order_shuffle_control"
    assert float(summary["candidate_chi2"]) > float(summary["best_control_chi2"])
    assert {row["endpoint_validation_claimed"] for row in rows} == {"false"}
    assert {row["physical_validation_claimed"] for row in rows} == {"false"}
    assert {row["claim_boundary"] for row in rows} == {
        "paper10_desi_time_level_endpoint_authorized_replay_permission_only_not_validation"
    }


def test_paper10_desi_time_level_negative_control_diagnostic_explains_failure_mode() -> None:
    for command in [
        ["python", "scripts/run_paper10_desi_time_level_endpoint_authorized_replay_v1.py"],
        ["python", "scripts/validate_paper10_desi_time_level_endpoint_authorized_replay_v1.py"],
        ["python", "scripts/build_paper10_desi_time_level_negative_control_diagnostic_v1.py"],
        ["python", "scripts/validate_paper10_desi_time_level_negative_control_diagnostic_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/paper10_desi_time_level_negative_control_diagnostic_v1_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    with (ROOT / "data/derived/paper10_desi_time_level_negative_control_diagnostic_v1_branches.csv").open(
        newline=""
    ) as f:
        branches = list(csv.DictReader(f))
    assert summary["status"] == "DESI_TIME_LEVEL_NEGATIVE_CONTROL_DIAGNOSTIC_BUILT_NOT_VALIDATION"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert summary["failure_mode"] == "five_row_time_level_constant_beta_endpoint_is_ordering_fragile"
    assert summary["largest_candidate_diag_pull_radial_index"] == "3"
    assert int(summary["controls_better_than_candidate_chi2"]) == 4
    assert summary["verdict"] == (
        "desi_time_level_negative_control_diagnostic_explains_non_control_resistance_not_validation"
    )
    best = min(branches, key=lambda row: float(row["chi2"]))
    assert best["branch"] == "redshift_order_shuffle_control"
    assert best["branch_role"] == "control_beats_candidate"


def test_paper10_desi_time_level_negative_response_blocks_replay_until_source_expansion() -> None:
    for command in [
        ["python", "scripts/build_paper10_desi_time_level_negative_control_diagnostic_v1.py"],
        ["python", "scripts/validate_paper10_desi_time_level_negative_control_diagnostic_v1.py"],
        ["python", "scripts/build_paper10_desi_time_level_negative_control_response_gate_v1.py"],
        ["python", "scripts/validate_paper10_desi_time_level_negative_control_response_gate_v1.py"],
        ["python", "scripts/validate_paper10_desi_time_readout_expansion_manifest_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/paper10_desi_time_level_negative_control_response_gate_v1_summary.csv").open(
        newline=""
    ) as f:
        response = list(csv.DictReader(f))[0]
    with (ROOT / "data/derived/paper10_desi_time_readout_expansion_manifest_v1_summary.csv").open(
        newline=""
    ) as f:
        expansion = list(csv.DictReader(f))[0]
    assert response["status"] == "DESI_TIME_LEVEL_NEGATIVE_CONTROL_RESPONSE_GATE_BUILT_NOT_VALIDATION"
    assert response["endpoint_replay_allowed"] == "false"
    assert response["next_allowed_action"] == "build_source_side_time_readout_expansion_manifest_only"
    assert response["verdict"] == (
        "desi_time_level_negative_control_response_gate_blocks_replay_until_richer_clock_readout_support"
    )
    assert expansion["status"] == "DESI_TIME_READOUT_EXPANSION_MANIFEST_VALIDATED_NOT_REPLAY_NOT_VALIDATION"
    assert expansion["route_count"] == "5"
    assert expansion["endpoint_ready_route_count"] == "0"
    assert expansion["next_primary_source_gate"] == "HIGH_Z_INDEPENDENT_CLOCK_SUPPORT"
    assert expansion["next_parallel_source_gate"] == "TIME_READOUT_SHAPE_OBSERVABLE"
    assert expansion["endpoint_replay_allowed"] == "false"
    assert expansion["verdict"] == "desi_time_readout_expansion_manifest_frozen_but_no_replay_ready_route"


def test_paper10_desi_high_z_clock_support_keeps_lya_row_as_holdout() -> None:
    for command in [
        ["python", "scripts/build_paper10_desi_high_z_independent_clock_support_audit_v1.py"],
        ["python", "scripts/validate_paper10_desi_high_z_independent_clock_support_audit_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/paper10_desi_high_z_independent_clock_support_audit_v1_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "DESI_HIGH_Z_INDEPENDENT_CLOCK_SUPPORT_AUDIT_BUILT_NOT_REPLAY_NOT_VALIDATION"
    assert summary["target_radial_index"] == "5"
    assert summary["target_z_eff"] == "2.33"
    assert summary["cc_z_max"] == "1.965"
    assert summary["target_within_frozen_cc_support"] == "false"
    assert summary["target_bracketed_without_extrapolation"] == "false"
    assert summary["endpoint_ready_support_count"] == "0"
    assert summary["high_z_row_can_enter_replay"] == "false"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert summary["verdict"] == "desi_high_z_clock_support_missing_row_remains_holdout_not_validation"


def test_paper10_desi_time_readout_shape_gate_freezes_candidate_without_replay() -> None:
    for command in [
        ["python", "scripts/build_paper10_desi_time_readout_shape_observable_gate_v1.py"],
        ["python", "scripts/validate_paper10_desi_time_readout_shape_observable_gate_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/paper10_desi_time_readout_shape_observable_gate_v1_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    with (ROOT / "data/derived/paper10_desi_time_readout_shape_observable_gate_v1.csv").open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert summary["status"] == "DESI_TIME_READOUT_SHAPE_OBSERVABLE_GATE_BUILT_NOT_REPLAY_NOT_VALIDATION"
    assert summary["input_cc_matched_rows"] == "5"
    assert summary["high_z_row_included"] == "false"
    assert summary["constant_beta_nuisance_removed"] == "true"
    assert summary["first_difference_rows"] == "4"
    assert summary["second_difference_rows"] == "3"
    assert summary["shape_observable_candidate_available"] == "true"
    assert summary["endpoint_ready_shape_observable"] == "false"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert summary["verdict"] == "desi_time_readout_shape_candidate_frozen_but_not_endpoint_ready"
    assert len(rows) == 7
    assert {row["constant_beta_nuisance_removed"] for row in rows} == {"true"}
    assert {row["high_z_row_included"] for row in rows} == {"false"}
    assert {row["endpoint_replay_allowed"] for row in rows} == {"false"}


def test_paper10_desi_time_readout_shape_projection_induction_maps_to_tau_channels() -> None:
    for command in [
        ["python", "scripts/build_paper10_desi_time_readout_shape_observable_gate_v1.py"],
        ["python", "scripts/build_paper10_desi_row5_high_z_source_route_scout_v1.py"],
        ["python", "scripts/build_paper10_desi_row5_holdout_confirmation_v1.py"],
        ["python", "scripts/build_paper10_desi_post_review_time_route_priority_v1.py"],
        ["python", "scripts/build_paper10_desi_time_readout_shape_projection_induction_v1.py"],
        ["python", "scripts/validate_paper10_desi_time_readout_shape_projection_induction_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/paper10_desi_time_readout_shape_projection_induction_v1_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    with (ROOT / "data/derived/paper10_desi_time_readout_shape_projection_induction_v1.csv").open(
        newline=""
    ) as f:
        rows = list(csv.DictReader(f))
    by_candidate = {row["candidate_id"]: row for row in rows}
    assert summary["status"] == "DESI_TIME_READOUT_SHAPE_PROJECTION_INDUCTION_MAPPED_NOT_REPLAY_NOT_VALIDATION"
    assert summary["primary_candidate"] == "CLOCK_SLOPE_SHAPE"
    assert summary["active_tau_channels"] == "K_time;K_closure;K_null"
    assert summary["projection_induction_complete"] == "false"
    assert summary["quotient_survival_gate_status"] == "not_proven_ordering_null_unresolved"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert summary["verdict"] == "time_shape_maps_to_K_time_candidate_but_projection_induction_incomplete"
    assert by_candidate["CLOCK_SLOPE_SHAPE"]["tau_readout_channel"] == "K_time"
    assert by_candidate["BAO_LEVEL_CONTEXT"]["tau_readout_channel"] == "K_closure"
    assert by_candidate["ORDERING_NULL_CONTROL"]["tau_readout_channel"] == "K_null"


def test_paper10_desi_ordering_control_suite_declares_k_null_blocker() -> None:
    for command in [
        ["python", "scripts/build_paper10_desi_time_readout_shape_projection_induction_v1.py"],
        ["python", "scripts/build_paper10_desi_ordering_control_suite_v1.py"],
        ["python", "scripts/validate_paper10_desi_ordering_control_suite_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/paper10_desi_ordering_control_suite_v1_summary.csv").open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (ROOT / "data/derived/paper10_desi_ordering_control_suite_v1.csv").open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert summary["status"] == "DESI_ORDERING_CONTROL_SUITE_DECLARED_NOT_REPLAY_NOT_VALIDATION"
    assert summary["required_control_count"] == "5"
    assert summary["available_control_count"] == "1"
    assert summary["shape_bound_control_count"] == "0"
    assert summary["primary_k_null_blocker"] == "redshift_order_shuffle"
    assert summary["ordering_control_suite_ready_for_replay"] == "false"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert summary["verdict"] == "k_null_ordering_controls_declared_but_not_shape_bound"
    assert {row["control_channel"] for row in rows} == {"K_null"}


def test_paper10_desi_cc_window_stress_binding_closes_unbound_control_without_replay() -> None:
    for command in [
        ["python", "scripts/build_paper10_desi_cc_window_stress_binding_v1.py"],
        ["python", "scripts/validate_paper10_desi_cc_window_stress_binding_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/paper10_desi_cc_window_stress_binding_v1_summary.csv").open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "DESI_CC_WINDOW_STRESS_BOUND_CAVEATED_NOT_REPLAY_NOT_VALIDATION"
    assert summary["cc_window_stress_bound_to_shape_route"] == "true"
    assert summary["cc_window_stress_release_policy"] == "SOURCE_REOPEN_ONLY_NO_REPLAY"
    assert summary["row_can_enter_replay"] == "false"
    assert summary["shape_route_replay_ready_after_cc_window_stress"] == "false"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert summary["verdict"] == "cc_window_stress_bound_as_caveated_source_control_not_replay_release"


def test_paper10_desi_shape_bound_control_vectors_bind_all_controls_without_replay() -> None:
    for command in [
        ["python", "scripts/build_paper10_desi_time_readout_shape_projection_induction_v1.py"],
        ["python", "scripts/build_paper10_desi_ordering_control_suite_v1.py"],
        ["python", "scripts/build_paper10_desi_cc_window_stress_binding_v1.py"],
        ["python", "scripts/build_paper10_desi_shape_bound_control_vectors_v1.py"],
        ["python", "scripts/validate_paper10_desi_shape_bound_control_vectors_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/paper10_desi_shape_bound_control_vectors_v1_summary.csv").open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (ROOT / "data/derived/paper10_desi_shape_bound_control_vectors_v1.csv").open(newline="") as f:
        rows = list(csv.DictReader(f))
    by_family = {row["control_family"]: row for row in rows}
    assert summary["status"] == "DESI_SHAPE_BOUND_CONTROL_VECTORS_BUILT_NOT_REPLAY_NOT_VALIDATION"
    assert summary["required_control_count"] == "5"
    assert summary["shape_bound_control_count"] == "5"
    assert summary["unbound_control_families"] == "none"
    assert summary["ordering_control_suite_shape_bound"] == "true"
    assert summary["ordering_control_suite_ready_for_replay"] == "false"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert summary["verdict"] == "shape_route_controls_bound_but_replay_not_authorized"
    assert by_family["redshift_order_shuffle"]["control_binding_status"] == "bound_source_vector"
    assert by_family["cc_window_stress"]["control_binding_status"] == "bound_caveated_source_window_stress"
    assert {row["uses_endpoint_scores"] for row in rows} == {"false"}
    assert {row["uses_endpoint_residuals"] for row in rows} == {"false"}


def test_paper10_desi_multi_clock_support_audit_blocks_endpoint() -> None:
    for command in [
        ["python", "scripts/build_paper10_desi_multi_clock_support_per_bao_row_audit_v1.py"],
        ["python", "scripts/validate_paper10_desi_multi_clock_support_per_bao_row_audit_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/paper10_desi_multi_clock_support_per_bao_row_audit_v1_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    with (ROOT / "data/derived/paper10_desi_multi_clock_support_per_bao_row_audit_v1.csv").open(
        newline=""
    ) as f:
        rows = list(csv.DictReader(f))
    assert summary["status"] == "DESI_MULTI_CLOCK_SUPPORT_PER_BAO_ROW_AUDIT_BUILT_NOT_REPLAY_NOT_VALIDATION"
    assert summary["authorized_row_count"] == "5"
    assert summary["strict_multi_clock_pass_count"] == "3"
    assert summary["relaxed_multi_clock_pass_count"] == "4"
    assert summary["relaxed_multi_clock_failed_radial_indices"] == "4"
    assert summary["multi_clock_support_endpoint_ready"] == "false"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert summary["verdict"] == "desi_multi_clock_support_incomplete_not_endpoint_ready"
    assert len(rows) == 5
    by_index = {row["radial_index"]: row for row in rows}
    assert by_index["4"]["relaxed_independent_reference_count"] == "1"
    assert {row["endpoint_replay_allowed"] for row in rows} == {"false"}


def test_paper10_desi_shape_independent_review_package_is_not_replay() -> None:
    for command in [
        ["python", "scripts/build_paper10_desi_time_readout_shape_projection_induction_v1.py"],
        ["python", "scripts/build_paper10_desi_ordering_control_suite_v1.py"],
        ["python", "scripts/build_paper10_desi_cc_window_stress_binding_v1.py"],
        ["python", "scripts/build_paper10_desi_shape_bound_control_vectors_v1.py"],
        ["python", "scripts/build_paper10_desi_time_readout_shape_independent_review_package_v1.py"],
        ["python", "scripts/validate_paper10_desi_time_readout_shape_independent_review_package_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (
        ROOT / "data/derived/paper10_desi_time_readout_shape_independent_review_package_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/paper10_desi_time_readout_shape_independent_review_response_template_v1.csv"
    ).open(newline="") as f:
        template = list(csv.DictReader(f))
    assert summary["status"] == "DESI_TIME_READOUT_SHAPE_INDEPENDENT_REVIEW_PACKAGE_BUILT_NOT_COMPLETED"
    assert summary["review_completed"] == "false"
    assert summary["shape_observable_candidate_available"] == "true"
    assert summary["endpoint_ready_shape_observable"] == "false"
    assert summary["multi_clock_support_endpoint_ready"] == "false"
    assert summary["high_z_row_can_enter_replay"] == "false"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert summary["contains_endpoint_residuals"] == "false"
    assert summary["contains_endpoint_scores"] == "false"
    assert summary["contains_fit_statistics"] == "false"
    assert summary["verdict"] == "desi_shape_independent_review_package_ready_not_completed_not_replay"
    assert len(template) == 4
    assert {row["review_completed"] for row in template} == {"false"}
    assert {row["forbidden_inputs_used"] for row in template} == {"false"}
    assert {row["endpoint_replay_allowed"] for row in template} == {"false"}


def test_paper10_desi_shape_route_replay_authorization_package_is_permission_request_only() -> None:
    for command in [
        ["python", "scripts/build_paper10_desi_time_readout_shape_projection_induction_v1.py"],
        ["python", "scripts/build_paper10_desi_ordering_control_suite_v1.py"],
        ["python", "scripts/build_paper10_desi_cc_window_stress_binding_v1.py"],
        ["python", "scripts/build_paper10_desi_shape_bound_control_vectors_v1.py"],
        ["python", "scripts/build_paper10_desi_shape_route_replay_authorization_review_package_v1.py"],
        ["python", "scripts/validate_paper10_desi_shape_route_replay_authorization_review_package_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (
        ROOT / "data/derived/paper10_desi_shape_route_replay_authorization_review_package_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/paper10_desi_shape_route_replay_authorization_review_response_template_v1.csv"
    ).open(newline="") as f:
        template = list(csv.DictReader(f))
    assert summary["status"] == "DESI_SHAPE_ROUTE_REPLAY_AUTHORIZATION_PACKAGE_BUILT_NOT_COMPLETED"
    assert summary["review_completed"] == "false"
    assert summary["shape_observable_candidate_available"] == "true"
    assert summary["primary_candidate"] == "CLOCK_SLOPE_SHAPE"
    assert summary["shape_bound_control_count"] == "5"
    assert summary["unbound_control_families"] == "none"
    assert summary["cc_window_stress_release_policy"] == "SOURCE_REOPEN_ONLY_NO_REPLAY"
    assert summary["multi_clock_support_endpoint_ready"] == "false"
    assert summary["high_z_row_can_enter_replay"] == "false"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert summary["contains_endpoint_residuals"] == "false"
    assert summary["contains_endpoint_scores"] == "false"
    assert summary["contains_fit_statistics"] == "false"
    assert summary["verdict"] == "desi_shape_route_replay_authorization_package_ready_not_completed"
    assert summary["claim_boundary"] == "paper10_desi_shape_route_replay_authorization_review_not_validation"
    assert len(template) == 4
    assert {row["review_completed"] for row in template} == {"false"}
    assert {row["forbidden_inputs_used"] for row in template} == {"false"}
    assert {row["endpoint_replay_allowed"] for row in template} == {"false"}


def _desi_shape_route_authorization_template_rows() -> list[dict[str, str]]:
    with (
        ROOT / "data/derived/paper10_desi_shape_route_replay_authorization_review_response_template_v1.csv"
    ).open(newline="") as f:
        return list(csv.DictReader(f))


def _write_desi_shape_route_authorization_response(
    path: Path, rows: list[dict[str, str]], decision: str, forbidden: str = "false"
) -> None:
    completed = []
    responses = {
        "Q1_shape_route_scope": "yes",
        "Q2_control_binding": "caveated_yes",
        "Q3_no_leakage": "yes",
        "Q4_authorization": decision,
    }
    for row in rows:
        out = dict(row)
        out["review_completed"] = "true"
        out["reviewer_id_or_role"] = "external_protocol_reviewer"
        out["reviewer_response"] = responses[out["question_id"]]
        out["reviewer_rationale"] = "Reviewer confirms the protocol state under source-side leakage rules."
        out["forbidden_inputs_used"] = forbidden
        out["endpoint_replay_allowed"] = (
            "true"
            if row["question_id"] == "Q4_authorization"
            and decision == "GO_DESI_SHAPE_ROUTE_REPLAY_PERMISSION_ONLY"
            else "false"
        )
        out["endpoint_validation_claimed"] = "false"
        out["physical_validation_claimed"] = "false"
        completed.append(out)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(completed[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(completed)


def test_paper10_desi_shape_route_replay_authorization_response_accepts_permission_only(
    tmp_path: Path,
) -> None:
    for command in [
        ["python", "scripts/build_paper10_desi_time_readout_shape_projection_induction_v1.py"],
        ["python", "scripts/build_paper10_desi_ordering_control_suite_v1.py"],
        ["python", "scripts/build_paper10_desi_cc_window_stress_binding_v1.py"],
        ["python", "scripts/build_paper10_desi_shape_bound_control_vectors_v1.py"],
        ["python", "scripts/build_paper10_desi_shape_route_replay_authorization_review_package_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    response = tmp_path / "shape_route_go.csv"
    summary = tmp_path / "shape_route_go_summary.csv"
    _write_desi_shape_route_authorization_response(
        response,
        _desi_shape_route_authorization_template_rows(),
        "GO_DESI_SHAPE_ROUTE_REPLAY_PERMISSION_ONLY",
    )
    subprocess.run(
        [
            "python",
            "scripts/validate_paper10_desi_shape_route_replay_authorization_review_response_v1.py",
            str(response),
            "--summary-out",
            str(summary),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with summary.open(newline="") as f:
        out = list(csv.DictReader(f))[0]
    assert out["status"] == "DESI_SHAPE_ROUTE_REPLAY_AUTHORIZATION_ACCEPTED_PERMISSION_ONLY"
    assert out["decision"] == "GO_DESI_SHAPE_ROUTE_REPLAY_PERMISSION_ONLY"
    assert out["endpoint_replay_allowed"] == "true"
    assert out["endpoint_validation_claimed"] == "false"
    assert out["physical_validation_claimed"] == "false"
    assert out["recommended_next_action"] == "run_one_separate_predeclared_DESI_shape_route_replay_without_validation_claim"


def test_paper10_desi_shape_route_replay_authorization_completed_response_is_imported() -> None:
    response = ROOT / "data/derived/paper10_desi_shape_route_replay_authorization_review_response_v1.csv"
    summary = ROOT / "data/derived/paper10_desi_shape_route_replay_authorization_review_response_v1_summary.csv"
    subprocess.run(
        [
            "python",
            "scripts/validate_paper10_desi_shape_route_replay_authorization_review_response_v1.py",
            str(response),
            "--summary-out",
            str(summary),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with summary.open(newline="") as f:
        out = list(csv.DictReader(f))[0]
    assert out["status"] == "DESI_SHAPE_ROUTE_REPLAY_AUTHORIZATION_ACCEPTED_PERMISSION_ONLY"
    assert out["decision"] == "GO_DESI_SHAPE_ROUTE_REPLAY_PERMISSION_ONLY"
    assert out["forbidden_inputs_used"] == "false"
    assert out["endpoint_replay_allowed"] == "true"
    assert out["endpoint_validation_claimed"] == "false"
    assert out["physical_validation_claimed"] == "false"


def test_paper10_desi_shape_route_replay_authorization_response_rejects_leakage(
    tmp_path: Path,
) -> None:
    subprocess.run(
        ["python", "scripts/build_paper10_desi_shape_route_replay_authorization_review_package_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    response = tmp_path / "shape_route_leakage.csv"
    summary = tmp_path / "shape_route_leakage_summary.csv"
    _write_desi_shape_route_authorization_response(
        response,
        _desi_shape_route_authorization_template_rows(),
        "GO_DESI_SHAPE_ROUTE_REPLAY_PERMISSION_ONLY",
        forbidden="true",
    )
    result = subprocess.run(
        [
            "python",
            "scripts/validate_paper10_desi_shape_route_replay_authorization_review_response_v1.py",
            str(response),
            "--summary-out",
            str(summary),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert not summary.exists()


def test_paper10_desi_shape_route_replay_run_template_is_auth_required_not_replay() -> None:
    for command in [
        ["python", "scripts/build_paper10_desi_time_readout_shape_observable_gate_v1.py"],
        ["python", "scripts/build_paper10_desi_time_readout_shape_projection_induction_v1.py"],
        ["python", "scripts/build_paper10_desi_cc_window_stress_binding_v1.py"],
        ["python", "scripts/build_paper10_desi_shape_bound_control_vectors_v1.py"],
        ["python", "scripts/validate_paper10_desi_shape_route_replay_run_template_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/source_manifest/paper10_desi_shape_route_replay_run_template_v1.csv").open(
        newline=""
    ) as f:
        row = list(csv.DictReader(f))[0]
    assert row["status"] == "DESI_SHAPE_ROUTE_REPLAY_PREPARED_AUTH_REQUIRED_NOT_VALIDATION"
    assert row["active_route_family"] == "DESI_CC_MATCHED_RADIAL_BAO_TIME_SHAPE"
    assert row["shape_rows_allowed"] == "0;1;2;3"
    assert row["curvature_rows_available"] == "0;1;2"
    assert row["radial_rows_allowed"] == "0;1;2;3;4"
    assert row["radial_rows_excluded"] == "5"
    assert row["endpoint_replay_allowed"] == "false"
    assert row["endpoint_validation_claimed"] == "false"
    assert row["physical_validation_claimed"] == "false"
    assert row["claim_boundary"] == "paper10_desi_shape_route_replay_template_not_validation"


def test_paper10_desi_shape_route_authorized_replay_runs_permission_only() -> None:
    for command in [
        ["python", "scripts/run_paper10_desi_shape_route_authorized_replay_v1.py"],
        ["python", "scripts/validate_paper10_desi_shape_route_authorized_replay_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/paper10_desi_shape_route_authorized_replay_v1_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    with (ROOT / "data/derived/paper10_desi_shape_route_authorized_replay_v1_grid.csv").open(
        newline=""
    ) as f:
        grid = list(csv.DictReader(f))
    assert summary["status"] == "DESI_SHAPE_ROUTE_AUTHORIZED_REPLAY_PERMISSION_ONLY_NOT_VALIDATION"
    assert summary["authorization_decision"] == "GO_DESI_SHAPE_ROUTE_REPLAY_PERMISSION_ONLY"
    assert summary["active_route_family"] == "DESI_CC_MATCHED_RADIAL_BAO_TIME_SHAPE"
    assert summary["family_survives_controls"] == "true"
    assert summary["controls_ge_candidate_score"] == "0"
    assert summary["endpoint_replay_allowed"] == "true"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert summary["verdict"] == "desi_shape_route_permission_replay_candidate_exceeds_all_controls_not_validation"
    assert {row["endpoint_validation_claimed"] for row in grid} == {"false"}
    assert {row["physical_validation_claimed"] for row in grid} == {"false"}


def test_paper10_desi_shape_route_robustness_stress_preserves_claim_boundary() -> None:
    for command in [
        ["python", "scripts/build_paper10_desi_shape_route_robustness_stress_v1.py"],
        ["python", "scripts/validate_paper10_desi_shape_route_robustness_stress_v1.py"],
        ["python", "scripts/build_paper10_desi_shape_route_robustness_figure_v1.py"],
        ["python", "scripts/validate_paper10_desi_shape_route_robustness_figure_v1.py"],
        ["python", "scripts/build_paper10_desi_shape_row_sensitivity_source_audit_v1.py"],
        ["python", "scripts/validate_paper10_desi_shape_row_sensitivity_source_audit_v1.py"],
        ["python", "scripts/build_paper10_desi_shape_core_source_acquisition_manifest_v1.py"],
        ["python", "scripts/validate_paper10_desi_shape_core_source_acquisition_manifest_v1.py"],
        ["python", "scripts/build_paper10_desi_shape_core_source_support_scan_v1.py"],
        ["python", "scripts/validate_paper10_desi_shape_core_source_support_scan_v1.py"],
        ["python", "scripts/build_paper10_desi_shape_row1_confirmatory_source_attachment_v1.py"],
        ["python", "scripts/validate_paper10_desi_shape_row1_confirmatory_source_attachment_v1.py"],
        ["python", "scripts/build_paper10_desi_shape_row1_confirmatory_source_review_package_v1.py"],
        ["python", "scripts/validate_paper10_desi_shape_row1_confirmatory_source_review_package_v1.py"],
        ["python", "scripts/validate_paper10_desi_shape_row1_confirmatory_source_review_response_v1.py"],
        ["python", "scripts/build_paper10_desi_shape_row2_moresco2012_source_attachment_v1.py"],
        ["python", "scripts/validate_paper10_desi_shape_row2_moresco2012_source_attachment_v1.py"],
        ["python", "scripts/build_paper10_desi_shape_row2_moresco2012_source_attachment_review_package_v1.py"],
        ["python", "scripts/validate_paper10_desi_shape_row2_moresco2012_source_attachment_review_package_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/paper10_desi_shape_route_robustness_stress_v1_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    with (ROOT / "data/derived/paper10_desi_shape_route_robustness_stress_v1.csv").open(
        newline=""
    ) as f:
        rows = list(csv.DictReader(f))
    assert summary["status"] == "DESI_SHAPE_ROUTE_ROBUSTNESS_STRESS_BUILT_PERMISSION_REPLAY_NOT_VALIDATION"
    assert summary["candidate_score_rank_among_replay_branches"] == "1"
    assert summary["best_control_branch"] == "control_leave_shape_row_max"
    assert summary["verdict"] == "positive_but_narrow_margin_and_row_sensitive_not_validation"
    assert summary["endpoint_replay_allowed"] == "true"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert len([row for row in rows if row["test_family"] == "leave_one"]) == 4
    assert len([row for row in rows if row["test_family"] == "leave_two"]) == 6
    assert {row["endpoint_validation_claimed"] for row in rows} == {"false"}
    assert {row["physical_validation_claimed"] for row in rows} == {"false"}
    assert (
        ROOT / "paper10_submission_source/figures/fig_desi_shape_route_robustness_stress.pdf"
    ).stat().st_size > 0
    with (ROOT / "data/derived/paper10_desi_shape_row_sensitivity_source_audit_v1_summary.csv").open(
        newline=""
    ) as f:
        source_summary = list(csv.DictReader(f))[0]
    assert source_summary["core_sensitive_rows"] == "1;2"
    assert source_summary["caveated_core_sensitive_rows"] == "2"
    assert source_summary["most_dispensable_row"] == "0"
    assert source_summary["most_required_row"] == "1"
    assert source_summary["endpoint_validation_claimed"] == "false"
    with (
        ROOT / "data/derived/paper10_desi_shape_core_source_acquisition_manifest_v1_summary.csv"
    ).open(newline="") as f:
        acquisition_summary = list(csv.DictReader(f))[0]
    assert acquisition_summary["p0_targets"] == "DESI_SHAPE_ROW_2_CORE_SUPPORT"
    assert acquisition_summary["p1_targets"] == "DESI_SHAPE_ROW_1_CORE_SUPPORT"
    assert acquisition_summary["source_fetch_completed"] == "false"
    assert acquisition_summary["endpoint_replay_allowed"] == "false"
    assert acquisition_summary["endpoint_validation_claimed"] == "false"
    with (ROOT / "data/derived/paper10_desi_shape_core_source_support_scan_v1_summary.csv").open(
        newline=""
    ) as f:
        support_summary = list(csv.DictReader(f))[0]
    assert support_summary["row2_moresco2012_support_found"] == "true"
    assert support_summary["row2_support_status"] == "partial_strengthening_in_interval_not_endpoint_pair_replacement"
    assert support_summary["endpoint_replay_allowed"] == "false"
    assert support_summary["endpoint_validation_claimed"] == "false"
    with (
        ROOT / "data/derived/paper10_desi_shape_row1_confirmatory_source_attachment_v1_summary.csv"
    ).open(newline="") as f:
        row1_summary = list(csv.DictReader(f))[0]
    assert row1_summary["row1_confirmatory_source_count"] == "2"
    assert row1_summary["row1_endpoint_ready"] == "false"
    assert row1_summary["endpoint_replay_allowed"] == "false"
    assert row1_summary["endpoint_validation_claimed"] == "false"
    with (
        ROOT / "data/derived/paper10_desi_shape_row1_confirmatory_source_review_package_v1_summary.csv"
    ).open(newline="") as f:
        row1_review_summary = list(csv.DictReader(f))[0]
    assert row1_review_summary["review_completed"] == "false"
    assert row1_review_summary["row1_confirmatory_source_count"] == "2"
    assert row1_review_summary["contains_endpoint_residuals"] == "false"
    assert row1_review_summary["contains_endpoint_scores"] == "false"
    assert row1_review_summary["endpoint_replay_allowed"] == "false"
    assert row1_review_summary["endpoint_validation_claimed"] == "false"
    with (
        ROOT / "data/derived/paper10_desi_shape_row1_confirmatory_source_review_response_v1_summary.csv"
    ).open(newline="") as f:
        row1_response_summary = list(csv.DictReader(f))[0]
    assert row1_response_summary["row1_confirmatory_source_accepted"] == "true"
    assert row1_response_summary["row1_endpoint_ready"] == "false"
    assert row1_response_summary["endpoint_replay_allowed"] == "false"
    assert row1_response_summary["endpoint_validation_claimed"] == "false"
    with (
        ROOT / "data/derived/paper10_desi_shape_row2_moresco2012_source_attachment_v1_summary.csv"
    ).open(newline="") as f:
        attachment_summary = list(csv.DictReader(f))[0]
    assert attachment_summary["attached_source_key"] == "Moresco2012ExpansionRate"
    assert attachment_summary["row2_source_caveat_reduced"] == "true"
    assert attachment_summary["endpoint_pair_replacement"] == "false"
    assert attachment_summary["row2_endpoint_ready"] == "false"
    assert attachment_summary["endpoint_replay_allowed"] == "false"
    assert attachment_summary["endpoint_validation_claimed"] == "false"
    with (
        ROOT
        / "data/derived/paper10_desi_shape_row2_moresco2012_source_attachment_review_package_v1_summary.csv"
    ).open(newline="") as f:
        review_summary = list(csv.DictReader(f))[0]
    assert review_summary["review_completed"] == "false"
    assert review_summary["attached_source_key"] == "Moresco2012ExpansionRate"
    assert review_summary["endpoint_pair_replacement"] == "false"
    assert review_summary["row2_endpoint_ready"] == "false"
    assert review_summary["endpoint_replay_allowed"] == "false"
    assert review_summary["endpoint_validation_claimed"] == "false"
    assert (
        ROOT / "data/derived/paper10_desi_shape_row2_moresco2012_source_attachment_review_package_v1.zip"
    ).stat().st_size > 0


def test_paper10_desi_shape_core_support_synthesis_gate_is_not_validation() -> None:
    for command in [
        ["python", "scripts/run_paper10_desi_shape_row2_authorized_replay_v1.py"],
        ["python", "scripts/validate_paper10_desi_shape_row2_authorized_replay_v1.py"],
        ["python", "scripts/build_paper10_desi_shape_row1_confirmatory_source_attachment_v1.py"],
        ["python", "scripts/validate_paper10_desi_shape_row1_confirmatory_source_attachment_v1.py"],
        ["python", "scripts/build_paper10_desi_shape_core_support_synthesis_gate_v1.py"],
        ["python", "scripts/validate_paper10_desi_shape_core_support_synthesis_gate_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (
        ROOT / "data/derived/paper10_desi_shape_core_support_synthesis_gate_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (ROOT / "data/derived/paper10_desi_shape_core_support_synthesis_gate_v1.csv").open(
        newline=""
    ) as f:
        rows = list(csv.DictReader(f))
    assert summary["status"] == "DESI_SHAPE_CORE_SUPPORT_SYNTHESIS_BUILT_SOURCE_STRENGTHENED_NOT_VALIDATION"
    assert summary["core_rows"] == "1;2"
    assert summary["most_required_row"] == "1"
    assert summary["row2_removed_retained_fraction"] == "0.749151602906"
    assert summary["row2_only_candidate_score"] == "0.415519707291"
    assert summary["row2_only_best_control_score"] == "1.62654904473"
    assert summary["route_interpretation"] == "multi_row_narrow_margin_source_sensitive_signal_not_row2_only"
    assert summary["validation_status"] == "not_endpoint_validation_not_physical_validation_not_falsification"
    assert summary["endpoint_replay_allowed_by_this_gate"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert summary["claim_boundary"] == "paper10_desi_shape_core_support_synthesis_gate_not_validation"
    assert {row["component_id"] for row in rows} == {
        "ROUTE_WIDE_REPLAY",
        "ROW_SENSITIVITY",
        "CORE_SOURCE_SUPPORT_SCAN",
        "ROW1_CONFIRMATORY_SOURCE_ATTACHMENT",
        "ROW2_CAVEAT_REDUCTION",
        "ROW2_ONLY_PERMISSION_REPLAY",
    }
    assert {row["endpoint_replay_allowed_by_this_gate"] for row in rows} == {"false"}
    assert {row["endpoint_validation_claimed"] for row in rows} == {"false"}
    assert {row["physical_validation_claimed"] for row in rows} == {"false"}


def test_paper10_desi_shape_route_source_synthesis_review_package_is_not_replay() -> None:
    for command in [
        ["python", "scripts/run_paper10_desi_shape_row2_authorized_replay_v1.py"],
        ["python", "scripts/validate_paper10_desi_shape_row2_authorized_replay_v1.py"],
        ["python", "scripts/build_paper10_desi_shape_core_support_synthesis_gate_v1.py"],
        ["python", "scripts/validate_paper10_desi_shape_core_support_synthesis_gate_v1.py"],
        ["python", "scripts/build_paper10_desi_shape_route_source_synthesis_review_package_v1.py"],
        ["python", "scripts/validate_paper10_desi_shape_route_source_synthesis_review_package_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (
        ROOT / "data/derived/paper10_desi_shape_route_source_synthesis_review_package_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/paper10_desi_shape_route_source_synthesis_review_response_template_v1.csv"
    ).open(newline="") as f:
        template = list(csv.DictReader(f))
    assert summary["status"] == "DESI_SHAPE_ROUTE_SOURCE_SYNTHESIS_REVIEW_PACKAGE_BUILT_NOT_COMPLETED"
    assert summary["core_rows"] == "1;2"
    assert summary["most_required_row"] == "1"
    assert summary["row1_status"] == "most_required_confirmatory_independent_support_review_accepted_not_endpoint_ready"
    assert summary["row2_status"] == "caveat_reduced_but_permission_replay_not_control_resistant_not_promotion_ready"
    assert summary["route_interpretation"] == "multi_row_narrow_margin_source_sensitive_signal_not_row2_only"
    assert summary["shape_route_promotion_allowed"] == "false"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert summary["contains_endpoint_residuals"] == "false"
    assert summary["contains_fit_statistics"] == "false"
    assert summary["claim_boundary"] == "paper10_desi_shape_route_source_synthesis_review_not_replay_not_validation"
    assert len(template) == 4
    assert {row["review_completed"] for row in template} == {"false"}
    assert {row["endpoint_replay_allowed"] for row in template} == {"false"}
    assert {row["endpoint_validation_claimed"] for row in template} == {"false"}
    assert {row["physical_validation_claimed"] for row in template} == {"false"}
    assert {row["shape_route_promotion_allowed"] for row in template} == {"false"}


def test_paper10_desi_shape_route_source_synthesis_review_response_allows_future_gate_only() -> None:
    subprocess.run(
        ["python", "scripts/validate_paper10_desi_shape_route_source_synthesis_review_response_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with (
        ROOT / "data/derived/paper10_desi_shape_route_source_synthesis_review_response_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert (
        summary["status"]
        == "DESI_SHAPE_ROUTE_SOURCE_SYNTHESIS_REVIEW_ACCEPTED_FOR_FUTURE_GATE_PREPARATION_NOT_REPLAY_NOT_VALIDATION"
    )
    assert summary["decision"] == "ACCEPT_AS_SOURCE_SYNTHESIS_SUPPORT_FOR_FUTURE_GATE_PREPARATION_NOT_REPLAY_NOT_VALIDATION"
    assert summary["accepted_question_count"] == "4"
    assert summary["future_gate_preparation_allowed"] == "true"
    assert summary["shape_route_promotion_allowed"] == "false"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert summary["forbidden_inputs_used"] == "false"
    assert summary["claim_boundary"] == "paper10_desi_shape_route_source_synthesis_review_not_replay_not_validation"
    assert summary["verdict"] == "source_synthesis_supports_future_gate_preparation_not_replay_not_validation"


def test_paper10_desi_shape_post_synthesis_gate_authorization_package_is_not_replay() -> None:
    for command in [
        ["python", "scripts/build_paper10_desi_shape_post_synthesis_gate_authorization_review_package_v1.py"],
        ["python", "scripts/validate_paper10_desi_shape_post_synthesis_gate_authorization_review_package_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (
        ROOT / "data/derived/paper10_desi_shape_post_synthesis_gate_authorization_review_package_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/paper10_desi_shape_post_synthesis_gate_authorization_review_response_template_v1.csv"
    ).open(newline="") as f:
        template = list(csv.DictReader(f))
    assert summary["status"] == "DESI_SHAPE_POST_SYNTHESIS_GATE_AUTHORIZATION_PACKAGE_BUILT_NOT_COMPLETED"
    assert summary["source_synthesis_future_gate_preparation_allowed"] == "true"
    assert summary["route_margin"] == "0.01485705264"
    assert summary["robustness_verdict"] == "positive_but_narrow_margin_and_row_sensitive_not_validation"
    assert summary["prepare_later_authorization_package_allowed"] == "false"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert summary["contains_endpoint_residuals"] == "false"
    assert summary["contains_fit_statistics"] == "false"
    assert summary["claim_boundary"] == "paper10_desi_shape_post_synthesis_gate_authorization_review_not_replay_not_validation"
    assert summary["verdict"] == "post_synthesis_gate_authorization_package_ready_not_completed_not_replay"
    assert len(template) == 4
    assert {row["review_completed"] for row in template} == {"false"}
    assert {row["prepare_later_authorization_package_allowed"] for row in template} == {"false"}
    assert {row["endpoint_replay_allowed"] for row in template} == {"false"}
    assert {row["endpoint_validation_claimed"] for row in template} == {"false"}
    assert {row["physical_validation_claimed"] for row in template} == {"false"}


def test_paper10_desi_shape_post_synthesis_gate_authorization_response_allows_package_only() -> None:
    subprocess.run(
        ["python", "scripts/validate_paper10_desi_shape_post_synthesis_gate_authorization_review_response_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with (
        ROOT / "data/derived/paper10_desi_shape_post_synthesis_gate_authorization_review_response_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert (
        summary["status"]
        == "DESI_SHAPE_POST_SYNTHESIS_GATE_AUTHORIZATION_REVIEW_ACCEPTED_FOR_SEPARATE_GATE_PREPARATION_NOT_REPLAY_NOT_VALIDATION"
    )
    assert summary["decision"] == "ACCEPT_PREPARE_SEPARATE_VALIDATION_ORIENTED_GATE_PACKAGE_NOT_REPLAY_NOT_VALIDATION"
    assert summary["accepted_question_count"] == "4"
    assert summary["source_synthesis_future_gate_preparation_allowed"] == "true"
    assert summary["prepare_later_authorization_package_allowed"] == "true"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert summary["forbidden_inputs_used"] == "false"
    assert summary["verdict"] == "gate_preparation_authorized_only_current_route_not_validated"


def test_paper10_desi_shape_validation_oriented_gate_review_package_is_not_replay() -> None:
    for command in [
        ["python", "scripts/build_paper10_desi_shape_validation_oriented_gate_review_package_v1.py"],
        ["python", "scripts/validate_paper10_desi_shape_validation_oriented_gate_review_package_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (
        ROOT / "data/derived/paper10_desi_shape_validation_oriented_gate_review_package_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/paper10_desi_shape_validation_oriented_gate_review_response_template_v1.csv"
    ).open(newline="") as f:
        template = list(csv.DictReader(f))
    assert summary["status"] == "DESI_SHAPE_VALIDATION_ORIENTED_GATE_REVIEW_PACKAGE_BUILT_NOT_COMPLETED"
    assert summary["post_synthesis_prepare_later_authorization_package_allowed"] == "true"
    assert summary["route_margin"] == "0.01485705264"
    assert summary["robustness_verdict"] == "positive_but_narrow_margin_and_row_sensitive_not_validation"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert summary["contains_endpoint_residuals"] == "false"
    assert summary["contains_fit_statistics"] == "false"
    assert summary["claim_boundary"] == "paper10_desi_shape_validation_oriented_gate_review_not_replay_not_validation"
    assert summary["verdict"] == "validation_oriented_gate_review_package_ready_not_completed_not_replay"
    assert len(template) == 4
    assert {row["review_completed"] for row in template} == {"false"}
    assert {row["endpoint_replay_allowed"] for row in template} == {"false"}
    assert {row["endpoint_validation_claimed"] for row in template} == {"false"}
    assert {row["physical_validation_claimed"] for row in template} == {"false"}


def test_paper10_desi_shape_validation_oriented_gate_response_prepares_only_future_replay() -> None:
    subprocess.run(
        ["python", "scripts/validate_paper10_desi_shape_validation_oriented_gate_review_response_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with (
        ROOT / "data/derived/paper10_desi_shape_validation_oriented_gate_review_response_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert (
        summary["status"]
        == "DESI_SHAPE_VALIDATION_ORIENTED_GATE_REVIEW_ACCEPTED_FOR_FUTURE_PERMISSION_ONLY_DIAGNOSTIC_NOT_REPLAY_NOT_VALIDATION"
    )
    assert summary["decision"] == "GO_DESI_SHAPE_VALIDATION_ORIENTED_PERMISSION_REPLAY_ONLY"
    assert summary["accepted_question_count"] == "4"
    assert summary["future_permission_only_replay_preparation_allowed"] == "true"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert summary["forbidden_inputs_used"] == "false"
    assert summary["narrow_margin_caveat_retained"] == "true"
    assert summary["row_sensitive_caveat_retained"] == "true"
    assert summary["row2_negative_diagnostic_retained"] == "true"
    assert (
        summary["recommended_next_action"]
        == "prepare_separate_completed_permission_only_replay_authorization_response_before_any_run_keep_endpoint_validation_false"
    )


def test_paper10_desi_shape_validation_permission_replay_authorization_package_is_blank() -> None:
    for command in [
        ["python", "scripts/build_paper10_desi_shape_validation_permission_replay_authorization_review_package_v1.py"],
        ["python", "scripts/validate_paper10_desi_shape_validation_permission_replay_authorization_review_package_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (
        ROOT
        / "data/derived/paper10_desi_shape_validation_permission_replay_authorization_review_package_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (
        ROOT
        / "data/derived/paper10_desi_shape_validation_permission_replay_authorization_review_response_template_v1.csv"
    ).open(newline="") as f:
        template = list(csv.DictReader(f))
    assert summary["status"] == "DESI_SHAPE_VALIDATION_PERMISSION_REPLAY_AUTHORIZATION_PACKAGE_BUILT_NOT_COMPLETED"
    assert summary["route_margin"] == "0.01485705264"
    assert summary["robustness_verdict"] == "positive_but_narrow_margin_and_row_sensitive_not_validation"
    assert summary["narrow_margin_caveat_retained"] == "true"
    assert summary["row_sensitive_caveat_retained"] == "true"
    assert summary["row2_negative_diagnostic_retained"] == "true"
    assert summary["future_permission_only_replay_preparation_allowed"] == "true"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert summary["contains_endpoint_residuals"] == "false"
    assert summary["contains_new_endpoint_scores"] == "false"
    assert summary["contains_fit_statistics"] == "false"
    assert summary["verdict"] == "validation_permission_replay_authorization_package_ready_not_completed_not_replay"
    assert len(template) == 4
    assert {row["review_completed"] for row in template} == {"false"}
    assert {row["forbidden_inputs_used"] for row in template} == {"false"}
    assert {row["endpoint_replay_allowed"] for row in template} == {"false"}
    assert {row["endpoint_validation_claimed"] for row in template} == {"false"}
    assert {row["physical_validation_claimed"] for row in template} == {"false"}


def test_paper10_desi_shape_validation_permission_response_and_replay_are_permission_only() -> None:
    for command in [
        ["python", "scripts/validate_paper10_desi_shape_validation_permission_replay_authorization_review_response_v1.py"],
        ["python", "scripts/run_paper10_desi_shape_validation_permission_authorized_replay_v1.py"],
        ["python", "scripts/validate_paper10_desi_shape_validation_permission_authorized_replay_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (
        ROOT
        / "data/derived/paper10_desi_shape_validation_permission_replay_authorization_review_response_v1_summary.csv"
    ).open(newline="") as f:
        auth = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/paper10_desi_shape_validation_permission_authorized_replay_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert auth["decision"] == "GO_DESI_SHAPE_VALIDATION_PERMISSION_REPLAY_ONLY"
    assert auth["permission_only_replay_authorized"] == "true"
    assert auth["endpoint_validation_claimed"] == "false"
    assert auth["physical_validation_claimed"] == "false"
    assert summary["status"] == "DESI_SHAPE_VALIDATION_PERMISSION_AUTHORIZED_REPLAY_PERMISSION_ONLY_NOT_VALIDATION"
    assert summary["candidate_shape_quadratic_score"] == "5.52425578108"
    assert summary["best_control_branch"] == "control_leave_shape_row_max"
    assert summary["best_control_shape_quadratic_score"] == "5.50939872844"
    assert summary["delta_candidate_minus_best_control_score"] == "0.01485705264"
    assert summary["controls_ge_candidate_score"] == "0"
    assert summary["family_survives_controls"] == "true"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert (
        summary["verdict"]
        == "desi_shape_validation_permission_replay_candidate_exceeds_all_controls_not_validation"
    )


def test_joint_existing_artifact_meta_score_is_prevalidation_only() -> None:
    for command in [
        ["python", "scripts/build_joint_existing_artifact_meta_score_v1.py"],
        ["python", "scripts/validate_joint_existing_artifact_meta_score_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/joint_existing_artifact_meta_score_v1_summary.csv").open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (ROOT / "data/derived/joint_existing_artifact_meta_score_v1.csv").open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert summary["verdict"] == "MULTI_CHANNEL_VIABILITY_PATTERN_PRESENT_NOT_VALIDATION"
    assert summary["channels_audited"] == "7"
    assert summary["net_meta_weight"] == "2.500"
    assert summary["joint_endpoint_claimed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["cosmological_validation_claimed"] == "false"
    assert summary["dark_sector_verdict_allowed"] == "false"
    assert len(rows) == 7
    assert {row["claim_boundary"] for row in rows} == {
        "joint_existing_artifact_meta_score_prevalidation_not_cosmological_validation"
    }


def test_joint_multichannel_endpoint_candidate_is_not_validation() -> None:
    for command in [
        ["python", "scripts/run_joint_multichannel_endpoint_candidate_v1.py"],
        ["python", "scripts/validate_joint_multichannel_endpoint_candidate_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/joint_multichannel_endpoint_candidate_v1_summary.csv").open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (ROOT / "data/derived/joint_multichannel_endpoint_candidate_v1.csv").open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert summary["verdict"] == "JOINT_ENDPOINT_CANDIDATE_INCONCLUSIVE_PREVALIDATION"
    assert summary["channels_scored"] == "7"
    assert summary["normalized_joint_score"] == "0.200059110"
    assert summary["joint_endpoint_claimed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["cosmological_validation_claimed"] == "false"
    assert len(rows) == 7
    assert sum(1 for row in rows if float(row["weighted_channel_score"]) > 0) == 3
    assert sum(1 for row in rows if float(row["weighted_channel_score"]) < 0) == 2
    assert {row["claim_boundary"] for row in rows} == {
        "joint_multichannel_endpoint_candidate_preflight_not_validation"
    }


def test_joint_multichannel_block_score_records_fragility() -> None:
    for command in [
        ["python", "scripts/run_joint_multichannel_block_score_v1.py"],
        ["python", "scripts/validate_joint_multichannel_block_score_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/joint_multichannel_block_score_v1_summary.csv").open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (ROOT / "data/derived/joint_multichannel_block_score_v1_leave_one_channel.csv").open(newline="") as f:
        loo = list(csv.DictReader(f))
    assert summary["verdict"] == "JOINT_BLOCK_SCORE_FRAGILE_OR_INCONCLUSIVE_PREVALIDATION"
    assert summary["block_normalized_score"] == "0.413070369"
    assert summary["exact_sign_flip_one_sided_p_ge_observed"] == "0.375000000"
    assert summary["leave_one_positive_count"] == "4"
    assert summary["joint_likelihood_claimed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["cosmological_validation_claimed"] == "false"
    dropped = {row["dropped_channel_id"]: row["retains_positive_score"] for row in loo}
    assert dropped["kids_lensing_cosebis_low_mode"] == "false"
    assert all(
        row["claim_boundary"] == "joint_multichannel_block_score_prevalidation_not_joint_likelihood"
        for row in loo
    )


def test_joint_best_justified_kernel_score_is_prevalidation_only() -> None:
    for command in [
        ["python", "scripts/run_joint_best_justified_kernel_score_v1.py"],
        ["python", "scripts/validate_joint_best_justified_kernel_score_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/joint_best_justified_kernel_score_v1_summary.csv").open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (ROOT / "data/source_manifest/joint_best_justified_kernel_manifest_v1.csv").open(newline="") as f:
        manifest = list(csv.DictReader(f))
    with (ROOT / "data/derived/joint_best_justified_kernel_score_v1_leave_one_channel.csv").open(newline="") as f:
        loo = list(csv.DictReader(f))

    assert summary["verdict"] == "BEST_JUSTIFIED_JOINT_KERNEL_POSITIVE_PREFLIGHT_NOT_VALIDATION"
    assert summary["positive_support_channels"] == "3"
    assert summary["positive_support_channel_order"] == (
        "kids_lensing_cosebis_low_mode;observer_path_basis_low_z;desi_shape_time_readout"
    )
    assert summary["normalized_score"] == "0.713515777"
    assert summary["exact_sign_flip_one_sided_p_ge_observed"] == "0.125000000"
    assert summary["leave_one_positive_count"] == "3"
    assert summary["joint_likelihood_claimed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["cosmological_validation_claimed"] == "false"

    by_channel = {row["channel_id"]: row for row in manifest}
    assert by_channel["act_kpath_lensing_path"]["positive_support_allowed"] == "false"
    assert by_channel["act_kpath_lensing_path"]["kernel_role"] == "k_null_diagnostic"
    assert by_channel["act_kpath_lensing_path"]["Q_i"] == "0.000000000"
    assert all(row["retains_positive_score"] == "true" for row in loo)


def test_joint_best_justified_kernel_robustness_is_prevalidation_only() -> None:
    for command in [
        ["python", "scripts/run_joint_best_justified_kernel_robustness_v1.py"],
        ["python", "scripts/validate_joint_best_justified_kernel_robustness_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/joint_best_justified_kernel_robustness_v1_summary.csv").open(newline="") as f:
        rows = list(csv.DictReader(f))

    scheme_rows = [row for row in rows if row["scheme_id"]]
    aggregate = next(
        row for row in rows
        if row["robustness_id"] == "JOINT_BEST_JUSTIFIED_KERNEL_ROBUSTNESS_V1"
    )

    assert len(scheme_rows) == 5
    assert all(row["positive_score"] == "true" for row in scheme_rows)
    assert all(row["endpoint_validation_claimed"] == "false" for row in scheme_rows)
    assert all(row["cosmological_validation_claimed"] == "false" for row in scheme_rows)
    assert all(
        row["active_channel_order"] == (
            "kids_lensing_cosebis_low_mode;observer_path_basis_low_z;desi_shape_time_readout"
        )
        for row in scheme_rows
    )

    by_scheme = {row["scheme_id"]: row for row in scheme_rows}
    assert by_scheme["equal_geometric"]["normalized_score"] == "0.713515777"
    assert by_scheme["conservative_min_gate"]["normalized_score"] == "0.703534932"
    assert by_scheme["conservative_min_gate"]["combined_control_one_sided_p_ge_observed"] == "0.993055556"

    assert aggregate["schemes_tested"] == "5"
    assert aggregate["positive_scheme_count"] == "5"
    assert aggregate["min_normalized_score"] == "0.703534932"
    assert aggregate["max_exact_sign_flip_p"] == "0.125000000"
    assert aggregate["verdict"] == "BEST_JUSTIFIED_KERNEL_ROBUST_POSITIVE_PREFLIGHT_NOT_VALIDATION"
    assert aggregate["joint_likelihood_claimed"] == "false"
    assert aggregate["endpoint_validation_claimed"] == "false"
    assert aggregate["cosmological_validation_claimed"] == "false"


def test_joint_best_justified_kernel_figure_is_source_backed() -> None:
    subprocess.run(
        ["python", "scripts/build_joint_best_justified_kernel_figure_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    figure = ROOT / "paper10_submission_source/figures/fig_joint_best_justified_kernel_v1.pdf"
    assert figure.exists()
    assert figure.stat().st_size > 10_000


def test_joint_best_justified_qi_review_package_is_source_side_only() -> None:
    subprocess.run(
        ["python", "scripts/validate_joint_best_justified_qi_review_package_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with (
        ROOT / "data/source_manifest/joint_best_justified_qi_review_requirements_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert {row["endpoint_scoring_allowed"] for row in rows} == {"false"}
    assert {row["endpoint_validation_claimed"] for row in rows} == {"false"}
    assert {row["cosmological_validation_claimed"] for row in rows} == {"false"}
    assert {row["claim_boundary"] for row in rows} == {"qi_review_source_side_only_not_scoring"}
    assert {row["requirement_id"] for row in rows} == {
        "QI_REVIEW_01_SOURCE_GATES",
        "QI_REVIEW_02_KIDS_COSEBIS",
        "QI_REVIEW_03_OBSERVER_PATH",
        "QI_REVIEW_04_DESI_SHAPE",
        "QI_REVIEW_05_ZERO_SUPPORT_BRANCHES",
        "QI_REVIEW_06_EXPONENT_POLICY",
        "QI_REVIEW_07_PROMOTION_RULE",
    }
    package = ROOT / "data/derived/joint_best_justified_qi_review_package_v1.zip"
    with zipfile.ZipFile(package) as zf:
        names = set(zf.namelist())
    required = {
        "q_i_review_package_v1/README_FOR_REVIEWER.md",
        "q_i_review_package_v1/REVIEW_INSTRUCTIONS.md",
        "q_i_review_package_v1/joint_best_justified_qi_review_requirements_v1.csv",
        "q_i_review_package_v1/joint_best_justified_qi_review_response_template_v1.csv",
        "q_i_review_package_v1/joint_best_justified_kernel_manifest_v1.csv",
        "q_i_review_package_v1/joint_best_justified_kernel_score_v1_summary.csv",
        "q_i_review_package_v1/joint_best_justified_kernel_robustness_v1_summary.csv",
    }
    assert required.issubset(names)


def test_joint_non_lensing_lift_diagnostic_identifies_next_channel() -> None:
    for command in [
        ["python", "scripts/build_joint_non_lensing_lift_diagnostic_v1.py"],
        ["python", "scripts/validate_joint_non_lensing_lift_diagnostic_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/joint_non_lensing_lift_diagnostic_v1_summary.csv").open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (ROOT / "data/derived/joint_non_lensing_lift_diagnostic_v1.csv").open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert summary["non_lensing_weighted_sum"] == "-0.363118958"
    assert summary["required_lift_to_zero"] == "0.363118958"
    assert summary["highest_lift_priority_channel"] == "observer_path_basis_low_z"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["cosmological_validation_claimed"] == "false"
    assert len(rows) == 4
    assert {row["claim_boundary"] for row in rows} == {
        "joint_non_lensing_lift_diagnostic_not_validation"
    }


def test_observer_path_strengthening_gate_blocks_full_metric_path() -> None:
    for command in [
        ["python", "scripts/build_observer_path_strengthening_gate_v1.py"],
        ["python", "scripts/validate_observer_path_strengthening_gate_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/observer_path_strengthening_gate_v1_summary.csv").open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (ROOT / "data/derived/observer_path_strengthening_gate_v1.csv").open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert summary["current_observer_family"] == "W_path_x_sky_x_x_zcenter"
    assert summary["current_family_survives_controls"] == "true"
    assert summary["metric_path_source_aligned_numeric_count"] == "0"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    route_status = {row["route_id"]: row["route_status"] for row in rows}
    assert route_status["metric_lensing_path_weight"] == (
        "BLOCKED_FOR_ENDPOINT_UNTIL_SOURCE_ALIGNED_NUMERIC_PRODUCT"
    )
    assert {row["claim_boundary"] for row in rows} == {
        "observer_path_strengthening_gate_source_side_not_endpoint"
    }


def test_observer_path_metric_product_requirements_package_is_requirements_only() -> None:
    for command in [
        ["python", "scripts/build_observer_path_metric_product_requirements_package_v1.py"],
        ["python", "scripts/validate_observer_path_metric_product_requirements_package_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (
        ROOT / "data/derived/observer_path_metric_product_requirements_package_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/observer_path_metric_product_requirements_review_response_template_v1.csv"
    ).open(newline="") as f:
        template = list(csv.DictReader(f))
    assert summary["observer_path_scope_rows"] == "12"
    assert summary["route_audit_rows"] == "424"
    assert summary["metric_path_source_aligned_numeric_count"] == "0"
    assert summary["route_audit_numeric_product_count"] == "0"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_lensing_path_weight_claimed"] == "false"
    assert summary["verdict"] == "METRIC_PATH_PRODUCT_REQUIREMENTS_READY_FOR_EXTERNAL_REVIEW_NOT_ENDPOINT"
    assert {row["question_id"] for row in template} == {
        "Q1_product_specificity",
        "Q2_source_alignment",
        "Q3_leakage_barrier",
        "Q4_replay_boundary",
    }
    assert {row["claim_boundary"] for row in template} == {
        "observer_path_metric_product_requirements_not_endpoint_not_validation"
    }


def test_observer_path_metric_product_requirements_review_response_is_requirements_only() -> None:
    subprocess.run(
        ["python", "scripts/validate_observer_path_metric_product_requirements_review_response_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with (
        ROOT / "data/derived/observer_path_metric_product_requirements_review_completed_summary_v1.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["decision"] == "ACCEPT_REQUIREMENTS_ONLY"
    assert summary["accepted_requirements_only_rows"] == "4"
    assert summary["source_aligned_metric_product_count"] == "0"
    assert summary["endpoint_replay_allowed"].lower() == "false"
    assert summary["endpoint_validation_claimed"].lower() == "false"
    assert summary["physical_lensing_path_weight_claimed"].lower() == "false"
    assert summary["completion_check"] == "pass"


def test_observer_path_metric_environment_product_is_caveated_not_physical_lensing() -> None:
    for command in [
        ["python", "scripts/build_observer_path_metric_environment_product_v1.py"],
        ["python", "scripts/validate_observer_path_metric_environment_product_v1.py"],
        ["python", "scripts/build_observer_path_metric_product_acquisition_status_v1.py"],
        ["python", "scripts/validate_observer_path_metric_product_acquisition_status_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/observer_path_metric_environment_product_v1_summary.csv").open(
        newline=""
    ) as f:
        product = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/observer_path_metric_product_acquisition_status_v1_summary.csv"
    ).open(newline="") as f:
        status = list(csv.DictReader(f))[0]
    assert product["observer_path_scope_rows"] == "12"
    assert product["metric_environment_product_available_count"] == "12"
    assert product["nonzero_metric_environment_path_weight_count"] == "12"
    assert product["physical_lensing_path_weight_claimed"] == "false"
    assert status["caveated_metric_environment_product_count"] == "12"
    assert status["physical_kappa_shear_mass_map_product_count"] == "0"
    assert status["endpoint_replay_allowed"] == "false"
    assert status["verdict"] == (
        "CAVEATED_METRIC_ENVIRONMENT_DATA_ACQUIRED_BUT_PHYSICAL_LENSING_PATH_STILL_BLOCKED"
    )


def test_observer_path_metric_environment_fast_screen_preserves_negative_control_result() -> None:
    for command in [
        ["python", "scripts/run_observer_path_metric_environment_fast_screen_v1.py"],
        ["python", "scripts/validate_observer_path_metric_environment_fast_screen_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/observer_path_metric_environment_fast_screen_v1_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["best_candidate_family"] == "metric_environment_path"
    assert summary["best_candidate_delta_chi2_minus_baseline"] == "-0.55793885392"
    assert summary["best_candidate_survives_controls"] == "false"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["verdict"] == "METRIC_ENVIRONMENT_PREAUTH_SIGNAL_NOT_CONTROL_RESISTANT_NOT_ENDPOINT"


def test_observer_path_metric_environment_ordering_diagnostic_preserves_control_failure() -> None:
    for command in [
        ["python", "scripts/run_observer_path_metric_environment_fast_screen_v1.py"],
        ["python", "scripts/build_observer_path_metric_environment_ordering_diagnostic_v1.py"],
        ["python", "scripts/validate_observer_path_metric_environment_ordering_diagnostic_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (
        ROOT / "data/derived/observer_path_metric_environment_ordering_diagnostic_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["best_candidate_family"] == "metric_environment_path"
    assert summary["best_control_branch"] == "rank_reverse"
    assert summary["delta_chi2_candidate_minus_best_control"] == "0.12520399356"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["contains_distance_residuals"] == "false"
    assert summary["verdict"] == (
        "SOURCE_ORDER_NOT_CONTROL_RESISTANT_REQUIRES_SOURCE_NATIVE_REORDERING_NOT_ENDPOINT"
    )


def test_observer_path_source_native_ordering_bank_remains_preauthorization_only() -> None:
    for command in [
        ["python", "scripts/build_observer_path_source_native_ordering_kernel_v1.py"],
        ["python", "scripts/validate_observer_path_source_native_ordering_kernel_v1.py"],
        ["python", "scripts/run_observer_path_source_native_ordering_fast_screen_v1.py"],
        ["python", "scripts/validate_observer_path_source_native_ordering_fast_screen_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (
        ROOT / "data/derived/observer_path_source_native_ordering_fast_screen_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["best_candidate_family"] == "K_order_void_web_los_balanced"
    assert summary["best_candidate_delta_chi2_minus_baseline"] == "-0.16922377119"
    assert summary["best_candidate_delta_chi2_minus_best_control"] == "0.07467294067"
    assert summary["best_candidate_survives_controls"] == "false"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["verdict"] == "SOURCE_NATIVE_ORDERING_PREAUTH_SIGNAL_NOT_CONTROL_RESISTANT_NOT_ENDPOINT"


def test_observer_path_metric_lensing_next_gate_blocks_endpoint_replay() -> None:
    for command in [
        ["python", "scripts/build_observer_path_metric_lensing_next_gate_v1.py"],
        ["python", "scripts/validate_observer_path_metric_lensing_next_gate_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/observer_path_metric_lensing_next_gate_v1_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["caveated_metric_environment_proxy_available"] == "true"
    assert summary["act_dr6_source_side_kappa_sampling_available"] == "true"
    assert summary["act_dr6_source_frozen_path_weight_candidate_available"] == "true"
    assert summary["act_dr6_low_z_source_rows"] == "424"
    assert summary["act_dr6_mask_positive_rows"] == "168"
    assert summary["physical_metric_lensing_path_product_available"] == "false"
    assert summary["metric_environment_screen_survives_controls"] == "false"
    assert summary["source_native_ordering_screen_survives_controls"] == "false"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["next_required_action"] == "external_review_and_replay_authorization_for_act_path_weight_candidate"
    assert summary["verdict"] == "ACT_DR6_PATH_WEIGHT_CANDIDATE_READY_BUT_REVIEW_BLOCKS_REPLAY"


def test_paper10_desi_shape_row2_attachment_review_response_validator_blocks_replay_leakage(
    tmp_path: Path,
) -> None:
    for command in [
        ["python", "scripts/build_paper10_desi_shape_core_source_support_scan_v1.py"],
        ["python", "scripts/build_paper10_desi_shape_row2_moresco2012_source_attachment_v1.py"],
        ["python", "scripts/build_paper10_desi_shape_row2_moresco2012_source_attachment_review_package_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)

    template = (
        ROOT
        / "data/derived/paper10_desi_shape_row2_moresco2012_source_attachment_review_response_template_v1.csv"
    )
    with template.open(newline="") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        row["review_completed"] = "true"
        row["reviewer_id_or_role"] = "test_external_source_reviewer"
        row["reviewer_response"] = "accept"
        row["reviewer_rationale"] = "Accepted as caveat-reducing source-side support only."

    accepted = tmp_path / "accepted.csv"
    with accepted.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    accepted_summary = tmp_path / "accepted_summary.csv"
    subprocess.run(
        [
            "python",
            "scripts/validate_paper10_desi_shape_row2_moresco2012_source_attachment_review_response_v1.py",
            str(accepted),
            "--summary-out",
            str(accepted_summary),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with accepted_summary.open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["row2_source_caveat_reduced"] == "true"
    assert summary["endpoint_pair_replacement"] == "false"
    assert summary["row2_endpoint_ready"] == "false"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"

    rows[0]["endpoint_replay_allowed"] = "true"
    bad = tmp_path / "bad.csv"
    with bad.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    bad_run = subprocess.run(
        [
            "python",
            "scripts/validate_paper10_desi_shape_row2_moresco2012_source_attachment_review_response_v1.py",
            str(bad),
            "--summary-out",
            str(tmp_path / "bad_summary.csv"),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert bad_run.returncode != 0

    canonical_response = (
        ROOT / "data/derived/paper10_desi_shape_row2_moresco2012_source_attachment_review_response_v1.csv"
    )
    if canonical_response.exists():
        subprocess.run(
            [
                "python",
                "scripts/validate_paper10_desi_shape_row2_moresco2012_source_attachment_review_response_v1.py",
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        with (
            ROOT
            / "data/derived/paper10_desi_shape_row2_moresco2012_source_attachment_review_response_v1_summary.csv"
        ).open(newline="") as f:
            canonical_summary = list(csv.DictReader(f))[0]
        assert canonical_summary["verdict"] == (
            "row2_moresco2012_attachment_accepted_as_caveat_reducing_not_endpoint_ready"
        )
        assert canonical_summary["endpoint_replay_allowed"] == "false"
        assert canonical_summary["endpoint_validation_claimed"] == "false"
        subprocess.run(
            [
                "python",
                "scripts/build_paper10_desi_shape_row2_promotion_readiness_gate_v1.py",
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        subprocess.run(
            [
                "python",
                "scripts/validate_paper10_desi_shape_row2_promotion_readiness_gate_v1.py",
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        subprocess.run(
            [
                "python",
                "scripts/build_paper10_desi_shape_row2_endpoint_pair_independence_scout_v1.py",
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        subprocess.run(
            [
                "python",
                "scripts/validate_paper10_desi_shape_row2_endpoint_pair_independence_scout_v1.py",
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        with (
            ROOT / "data/derived/paper10_desi_shape_row2_promotion_readiness_gate_v1_summary.csv"
        ).open(newline="") as f:
            promotion_summary = list(csv.DictReader(f))[0]
        assert promotion_summary["row2_source_caveat_reduced"] == "true"
        assert promotion_summary["endpoint_pair_independence_satisfied"] == "false"
        assert promotion_summary["row2_promotion_ready"] == "false"
        assert promotion_summary["shape_route_promotion_allowed"] == "false"
        assert promotion_summary["endpoint_replay_allowed"] == "false"
        with (
            ROOT
            / "data/derived/paper10_desi_shape_row2_endpoint_pair_independence_scout_v1_summary.csv"
        ).open(newline="") as f:
            scout_summary = list(csv.DictReader(f))[0]
        assert scout_summary["left_strict_independent_count"] == "0"
        assert scout_summary["right_strict_independent_count"] == "1"
        assert scout_summary["left_best_independent_candidate"] == "none"
        assert scout_summary["right_best_independent_candidate"] == "Moresco (2015)"
        assert scout_summary["endpoint_pair_independence_satisfied"] == "false"
        assert scout_summary["row2_promotion_ready"] == "false"
        assert scout_summary["shape_route_promotion_allowed"] == "false"
        assert scout_summary["endpoint_replay_allowed"] == "false"
        assert scout_summary["endpoint_validation_claimed"] == "false"
        subprocess.run(
            [
                "python",
                "scripts/build_paper10_desi_shape_row2_left_endpoint_nearmiss_freeze_v1.py",
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        subprocess.run(
            [
                "python",
                "scripts/validate_paper10_desi_shape_row2_left_endpoint_nearmiss_freeze_v1.py",
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        with (
            ROOT
            / "data/derived/paper10_desi_shape_row2_left_endpoint_nearmiss_freeze_v1_summary.csv"
        ).open(newline="") as f:
            near_summary = list(csv.DictReader(f))[0]
        assert near_summary["relaxed_independent_left_candidate_count"] == "2"
        assert near_summary["strict_independent_left_support_count"] == "0"
        assert near_summary["closest_relaxed_independent_candidate"] == "Stern et al. (2010)"
        assert near_summary["closest_relaxed_independent_delta_z"] == "0.054"
        assert near_summary["left_endpoint_release_allowed"] == "false"
        assert near_summary["row2_promotion_ready"] == "false"
        assert near_summary["endpoint_replay_allowed"] == "false"
        assert near_summary["endpoint_validation_claimed"] == "false"
        subprocess.run(
            [
                "python",
                "scripts/build_paper10_desi_shape_row2_left_endpoint_window_review_package_v1.py",
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        subprocess.run(
            [
                "python",
                "scripts/validate_paper10_desi_shape_row2_left_endpoint_window_review_package_v1.py",
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        with (
            ROOT
            / "data/derived/paper10_desi_shape_row2_left_endpoint_window_review_package_v1_summary.csv"
        ).open(newline="") as f:
            review_package_summary = list(csv.DictReader(f))[0]
        assert review_package_summary["review_completed"] == "false"
        assert review_package_summary["left_endpoint_release_allowed"] == "false"
        assert review_package_summary["row2_promotion_ready"] == "false"
        assert review_package_summary["endpoint_replay_allowed"] == "false"
        assert review_package_summary["endpoint_validation_claimed"] == "false"
        assert review_package_summary["contains_endpoint_residuals"] == "false"
        assert review_package_summary["contains_endpoint_scores"] == "false"

        left_template = (
            ROOT
            / "data/derived/paper10_desi_shape_row2_left_endpoint_window_review_response_template_v1.csv"
        )
        with left_template.open(newline="") as f:
            left_rows = list(csv.DictReader(f))
        for row in left_rows:
            row["review_completed"] = "true"
            row["reviewer_id_or_role"] = "test_external_source_reviewer"
            row["reviewer_rationale"] = "Caveated source-window context only; no endpoint residuals used."
        by_question = {row["question_id"]: row for row in left_rows}
        by_question["Q1_STRICT_WINDOW_STATUS"]["reviewer_response"] = "ALLOW_CAVEATED_WINDOW_REVIEW_ROUTE"
        by_question["Q2_NEARMISS_ELIGIBILITY"]["reviewer_response"] = "ACCEPT_AS_CAVEATED_NEAR_WINDOW_SOURCE"
        by_question["Q2_NEARMISS_ELIGIBILITY"]["source_reference_or_url"] = "Stern et al. (2010); Moresco et al. (2012)"
        by_question["Q3_RELEASE_POLICY"]["reviewer_response"] = "SOURCE_REOPEN_ONLY_NO_REPLAY"
        accepted_left = tmp_path / "accepted_left_endpoint_window.csv"
        with accepted_left.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(left_rows[0].keys()), lineterminator="\n")
            writer.writeheader()
            writer.writerows(left_rows)
        accepted_left_summary = tmp_path / "accepted_left_endpoint_window_summary.csv"
        subprocess.run(
            [
                "python",
                "scripts/validate_paper10_desi_shape_row2_left_endpoint_window_review_response_v1.py",
                str(accepted_left),
                "--summary-out",
                str(accepted_left_summary),
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        with accepted_left_summary.open(newline="") as f:
            accepted_left_summary_row = list(csv.DictReader(f))[0]
        assert accepted_left_summary_row["source_reopen_caveated"] == "true"
        assert accepted_left_summary_row["left_endpoint_release_allowed"] == "false"
        assert accepted_left_summary_row["row2_promotion_ready"] == "false"
        assert accepted_left_summary_row["endpoint_replay_allowed"] == "false"

        left_rows[0]["endpoint_replay_allowed"] = "true"
        bad_left = tmp_path / "bad_left_endpoint_window.csv"
        with bad_left.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(left_rows[0].keys()), lineterminator="\n")
            writer.writeheader()
            writer.writerows(left_rows)
        bad_left_run = subprocess.run(
            [
                "python",
                "scripts/validate_paper10_desi_shape_row2_left_endpoint_window_review_response_v1.py",
                str(bad_left),
                "--summary-out",
                str(tmp_path / "bad_left_endpoint_window_summary.csv"),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        assert bad_left_run.returncode != 0
        subprocess.run(
            [
                "python",
                "scripts/build_paper10_desi_shape_row2_left_endpoint_window_decision_gate_v1.py",
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        subprocess.run(
            [
                "python",
                "scripts/validate_paper10_desi_shape_row2_left_endpoint_window_decision_gate_v1.py",
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        with (
            ROOT
            / "data/derived/paper10_desi_shape_row2_left_endpoint_window_decision_gate_v1_summary.csv"
        ).open(newline="") as f:
            decision_summary = list(csv.DictReader(f))[0]
        assert decision_summary["gate_status"] == "ROW2_LEFT_SOURCE_REOPEN_CAVEATED_NO_REPLAY"
        assert decision_summary["review_completed"] == "true"
        assert decision_summary["source_reopen_caveated"] == "true"
        assert decision_summary["left_endpoint_release_allowed"] == "false"
        assert decision_summary["row2_promotion_ready"] == "false"
        assert decision_summary["endpoint_replay_allowed"] == "false"
        assert decision_summary["endpoint_validation_claimed"] == "false"
        subprocess.run(
            [
                "python",
                "scripts/build_paper10_desi_shape_row2_post_window_review_source_plan_v1.py",
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        subprocess.run(
            [
                "python",
                "scripts/validate_paper10_desi_shape_row2_post_window_review_source_plan_v1.py",
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        with (
            ROOT
            / "data/derived/paper10_desi_shape_row2_post_window_review_source_plan_v1_summary.csv"
        ).open(newline="") as f:
            source_plan_summary = list(csv.DictReader(f))[0]
        assert (
            source_plan_summary["source_plan_status"]
            == "ROW2_SOURCE_REOPENED_CAVEATED_LEFT_ENDPOINT_STILL_NOT_RELEASED"
        )
        assert source_plan_summary["source_reopen_caveated"] == "true"
        assert source_plan_summary["strict_left_endpoint_support_count"] == "0"
        assert source_plan_summary["p0_source_target_count"] == "2"
        assert source_plan_summary["row2_promotion_ready"] == "false"
        assert source_plan_summary["endpoint_replay_allowed"] == "false"
        assert source_plan_summary["endpoint_validation_claimed"] == "false"
        subprocess.run(
            [
                "python",
                "scripts/build_paper10_desi_shape_row2_left_strict_support_scout_v1.py",
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        subprocess.run(
            [
                "python",
                "scripts/validate_paper10_desi_shape_row2_left_strict_support_scout_v1.py",
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        with (
            ROOT
            / "data/derived/paper10_desi_shape_row2_left_strict_support_scout_v1_summary.csv"
        ).open(newline="") as f:
            strict_scout_summary = list(csv.DictReader(f))[0]
        assert strict_scout_summary["strict_independent_support_count"] == "0"
        assert strict_scout_summary["nearest_candidate_reference"] == "Simon et al. (2005)"
        assert strict_scout_summary["nearest_independent_candidate_reference"] == "Stern et al. (2010)"
        assert strict_scout_summary["row2_promotion_ready"] == "false"
        assert strict_scout_summary["endpoint_replay_allowed"] == "false"
        assert strict_scout_summary["endpoint_validation_claimed"] == "false"
        subprocess.run(
            [
                "python",
                "scripts/build_paper10_desi_shape_row2_source_native_shape_support_scout_v1.py",
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        subprocess.run(
            [
                "python",
                "scripts/validate_paper10_desi_shape_row2_source_native_shape_support_scout_v1.py",
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        with (
            ROOT
            / "data/derived/paper10_desi_shape_row2_source_native_shape_support_scout_v1_summary.csv"
        ).open(newline="") as f:
            source_native_summary = list(csv.DictReader(f))[0]
        assert source_native_summary["source_native_row_count"] == "4"
        assert source_native_summary["row2_covariance_positive_definite"] == "true"
        assert source_native_summary["uses_endpoint_scores"] == "false"
        assert source_native_summary["uses_endpoint_residuals"] == "false"
        assert source_native_summary["row2_promotion_ready"] == "false"
        assert source_native_summary["endpoint_replay_allowed"] == "false"
        assert source_native_summary["endpoint_validation_claimed"] == "false"
        subprocess.run(
            [
                "python",
                "scripts/build_paper10_desi_shape_row2_source_native_shape_support_review_package_v1.py",
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        subprocess.run(
            [
                "python",
                "scripts/validate_paper10_desi_shape_row2_source_native_shape_support_review_package_v1.py",
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        with (
            ROOT
            / "data/derived/paper10_desi_shape_row2_source_native_shape_support_review_package_v1_summary.csv"
        ).open(newline="") as f:
            source_native_package_summary = list(csv.DictReader(f))[0]
        assert source_native_package_summary["review_completed"] == "false"
        assert source_native_package_summary["source_native_row_count"] == "4"
        assert source_native_package_summary["row2_covariance_positive_definite"] == "true"
        assert source_native_package_summary["row2_promotion_ready"] == "false"
        assert source_native_package_summary["endpoint_replay_allowed"] == "false"
        assert source_native_package_summary["contains_endpoint_scores"] == "false"


def test_paper10_desi_shape_independent_review_response_validator_accepts_caveated_non_replay(
    tmp_path: Path,
) -> None:
    subprocess.run(
        ["python", "scripts/build_paper10_desi_time_readout_shape_projection_induction_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/build_paper10_desi_ordering_control_suite_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/build_paper10_desi_cc_window_stress_binding_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/build_paper10_desi_shape_bound_control_vectors_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/build_paper10_desi_time_readout_shape_independent_review_package_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    template_path = ROOT / "data/derived/paper10_desi_time_readout_shape_independent_review_response_template_v1.csv"
    with template_path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    completed = []
    for row in rows:
        new_row = dict(row)
        new_row["review_completed"] = "true"
        new_row["reviewer_id_or_role"] = "independent_source_side_reviewer"
        new_row["reviewer_response"] = "caveated_yes" if row["question_id"] in {"Q3_caveat_acceptance", "Q4_next_action_limit"} else "yes"
        new_row["reviewer_rationale"] = "Source-side fields and blockers reviewed; no endpoint replay or validation is authorized."
        completed.append(new_row)
    response = tmp_path / "completed_shape_review.csv"
    with response.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(completed[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(completed)
    summary = tmp_path / "shape_review_summary.csv"
    subprocess.run(
        [
            "python",
            "scripts/validate_paper10_desi_time_readout_shape_independent_review_response_v1.py",
            str(response),
            "--summary-out",
            str(summary),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with summary.open(newline="") as f:
        result = list(csv.DictReader(f))[0]
    assert result["status"] == "DESI_TIME_READOUT_SHAPE_INDEPENDENT_REVIEW_ACCEPTED_CAVEATED_SOURCE_SIDE_NOT_REPLAY"
    assert result["decision"] == "RETAIN_CAVEATED_SOURCE_SIDE_SHAPE_CANDIDATE_ONLY"
    assert result["review_completed"] == "true"
    assert result["endpoint_replay_allowed"] == "false"
    assert result["endpoint_validation_claimed"] == "false"
    assert result["physical_validation_claimed"] == "false"


def test_paper10_desi_clock_support_acquisition_manifest_freezes_missing_targets() -> None:
    for command in [
        ["python", "scripts/build_paper10_desi_clock_support_acquisition_manifest_v1.py"],
        ["python", "scripts/validate_paper10_desi_clock_support_acquisition_manifest_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/paper10_desi_clock_support_acquisition_manifest_v1_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    with (ROOT / "data/derived/paper10_desi_clock_support_acquisition_manifest_v1.csv").open(
        newline=""
    ) as f:
        rows = list(csv.DictReader(f))
    assert summary["status"] == "DESI_CLOCK_SUPPORT_ACQUISITION_MANIFEST_FROZEN_NOT_FETCHED_NOT_REPLAY_NOT_VALIDATION"
    assert summary["target_count"] == "2"
    assert summary["source_fetch_completed"] == "false"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert summary["verdict"] == "desi_clock_support_acquisition_targets_frozen_sources_not_attached"
    by_target = {row["target_id"]: row for row in rows}
    assert set(by_target) == {
        "DESI_RADIAL_ROW_4_MULTI_CLOCK_REDUNDANCY",
        "DESI_RADIAL_ROW_5_HIGH_Z_CLOCK_SUPPORT",
    }
    assert by_target["DESI_RADIAL_ROW_4_MULTI_CLOCK_REDUNDANCY"]["radial_index"] == "4"
    assert by_target["DESI_RADIAL_ROW_4_MULTI_CLOCK_REDUNDANCY"]["target_z_eff"] == "1.484"
    assert by_target["DESI_RADIAL_ROW_5_HIGH_Z_CLOCK_SUPPORT"]["radial_index"] == "5"
    assert by_target["DESI_RADIAL_ROW_5_HIGH_Z_CLOCK_SUPPORT"]["target_z_eff"] == "2.33"
    assert {row["source_fetch_status"] for row in rows} == {"not_fetched"}
    assert {row["endpoint_replay_allowed"] for row in rows} == {"false"}


def test_paper10_desi_clock_support_candidate_scan_does_not_close_gate() -> None:
    for command in [
        ["python", "scripts/build_paper10_desi_clock_support_source_candidate_scan_v1.py"],
        ["python", "scripts/validate_paper10_desi_clock_support_source_candidate_scan_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/paper10_desi_clock_support_source_candidate_scan_v1_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    with (ROOT / "data/derived/paper10_desi_clock_support_source_candidate_scan_v1.csv").open(
        newline=""
    ) as f:
        rows = list(csv.DictReader(f))
    assert summary["status"] == "DESI_CLOCK_SUPPORT_SOURCE_CANDIDATE_SCAN_BUILT_NOT_REPLAY_NOT_VALIDATION"
    assert summary["candidate_count"] == "6"
    assert summary["accepted_for_acquisition_target_count"] == "0"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert summary["verdict"] == "desi_clock_support_candidate_scan_found_cross_probe_context_but_no_gate_closing_clock_support"
    assert {row["accepted_for_acquisition_target"] for row in rows} == {"false"}
    assert {row["control_or_context_only"] for row in rows} == {"true"}
    by_candidate = {row["candidate_id"]: row for row in rows}
    assert by_candidate["EBOSS_DR16_QSO_BAO_RSD_Z1P48"]["gate_result"] == "RETAIN_AS_ROW4_CROSS_PROBE_CONTROL_ONLY_NOT_CLOCK_SUPPORT"
    assert by_candidate["TOMASETTI_2023_VANDELS_CC_Z1P26"]["gate_result"] == "REJECT_FOR_ROW4_OUTSIDE_FROZEN_Z_WINDOW"
    assert by_candidate["EBOSS_DR16_LYA_BAO_Z2P33"]["gate_result"] == "RETAIN_AS_CROSS_PROBE_CONTROL_ONLY_NOT_CLOCK_SUPPORT"


def test_paper10_desi_clock_support_blocker_verdict_keeps_route_blocked() -> None:
    for command in [
        ["python", "scripts/build_paper10_desi_clock_support_blocker_verdict_v1.py"],
        ["python", "scripts/validate_paper10_desi_clock_support_blocker_verdict_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/paper10_desi_clock_support_blocker_verdict_v1_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    with (ROOT / "data/derived/paper10_desi_clock_support_blocker_verdict_v1.csv").open(
        newline=""
    ) as f:
        rows = list(csv.DictReader(f))
    assert summary["status"] == "DESI_CLOCK_SUPPORT_ROUTE_BLOCKED_AFTER_SOURCE_SCAN_NOT_REPLAY_NOT_VALIDATION"
    assert summary["active_blocker_count"] == "2"
    assert summary["candidate_scan_accepted_count"] == "0"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert summary["verdict"] == "desi_clock_support_route_remains_blocked_pending_independent_clock_sources"
    by_blocker = {row["blocker_id"]: row for row in rows}
    assert set(by_blocker) == {
        "ROW4_INDEPENDENT_CLOCK_REDUNDANCY_MISSING",
        "ROW5_HIGH_Z_CLOCK_SUPPORT_MISSING",
    }
    assert {row["blocker_status"] for row in rows} == {"ACTIVE_BLOCKER"}
    assert {row["endpoint_replay_allowed"] for row in rows} == {"false"}
    assert "BAO_RSD_as_clock_support" in by_blocker["ROW4_INDEPENDENT_CLOCK_REDUNDANCY_MISSING"][
        "disallowed_next_action"
    ]
    assert "LyA_BAO_as_clock_support" in by_blocker["ROW5_HIGH_Z_CLOCK_SUPPORT_MISSING"][
        "disallowed_next_action"
    ]


def test_paper10_desi_row4_cc_bracket_source_freeze_preserves_independence_blocker() -> None:
    for command in [
        ["python", "scripts/build_paper10_desi_row4_clock_reopen_manifest_v1.py"],
        ["python", "scripts/validate_paper10_desi_row4_clock_reopen_manifest_v1.py"],
        ["python", "scripts/build_paper10_desi_row4_cc_bracket_source_freeze_v1.py"],
        ["python", "scripts/validate_paper10_desi_row4_cc_bracket_source_freeze_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/paper10_desi_row4_cc_bracket_source_freeze_v1_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    with (ROOT / "data/derived/paper10_desi_row4_cc_bracket_source_freeze_v1.csv").open(
        newline=""
    ) as f:
        rows = list(csv.DictReader(f))
    assert summary["status"] == "ROW4_CC_BRACKET_SOURCE_VALUES_FROZEN_REFERENCE_FAMILY_NOT_INDEPENDENT_NOT_REPLAY"
    assert summary["frozen_entry_count"] == "2"
    assert summary["source_values_frozen"] == "true"
    assert summary["reference_family"] == "Simon_2005"
    assert summary["independent_reference_family_redundancy_satisfied"] == "false"
    assert summary["row4_can_enter_replay"] == "false"
    assert summary["row5_remains_blocked"] == "true"
    by_entry = {row["entry_id"]: row for row in rows}
    assert by_entry["SIMON_2005_CC_Z1P43"]["H_z_km_s_Mpc"] == "177"
    assert by_entry["SIMON_2005_CC_Z1P43"]["sigma_H_km_s_Mpc"] == "18"
    assert by_entry["SIMON_2005_CC_Z1P53"]["H_z_km_s_Mpc"] == "140"
    assert by_entry["SIMON_2005_CC_Z1P53"]["sigma_H_km_s_Mpc"] == "14"
    assert {row["independent_of_current_blocker_reference_family"] for row in rows} == {"false"}
    assert {row["endpoint_replay_allowed"] for row in rows} == {"false"}


def test_paper10_desi_row4_non_simon_clock_search_keeps_blocker() -> None:
    for command in [
        ["python", "scripts/build_paper10_desi_row4_cc_bracket_source_freeze_v1.py"],
        ["python", "scripts/build_paper10_desi_row4_non_simon_clock_search_v1.py"],
        ["python", "scripts/validate_paper10_desi_row4_non_simon_clock_search_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/paper10_desi_row4_non_simon_clock_search_v1_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    with (ROOT / "data/derived/paper10_desi_row4_non_simon_clock_search_v1.csv").open(
        newline=""
    ) as f:
        rows = list(csv.DictReader(f))
    assert summary["status"] == "ROW4_NON_SIMON_STRICT_WINDOW_SEARCH_NEGATIVE_NOT_REPLAY"
    assert summary["non_simon_inside_strict_window_count"] == "0"
    assert summary["accepted_for_row4_release_count"] == "0"
    assert summary["closest_non_simon_candidate"] == "MORESCO_2015_CC_Z1P363"
    assert summary["closest_non_simon_delta_z"] == "0.121"
    assert summary["row4_can_enter_replay"] == "false"
    assert summary["verdict"] == "row4_non_simon_strict_window_search_negative_blocker_remains"
    by_candidate = {row["candidate_id"]: row for row in rows}
    assert by_candidate["MORESCO_2015_CC_Z1P363"]["inside_strict_window"] == "false"
    assert by_candidate["MORESCO_2015_CC_Z1P363"]["independent_of_current_blocker_reference_family"] == "true"
    assert by_candidate["SIMON_2005_CC_Z1P43"]["inside_strict_window"] == "true"
    assert by_candidate["SIMON_2005_CC_Z1P43"]["independent_of_current_blocker_reference_family"] == "false"
    assert {row["accepted_for_row4_release"] for row in rows} == {"false"}
    assert {row["endpoint_replay_allowed"] for row in rows} == {"false"}


def test_paper10_desi_row4_window_review_package_is_blank_non_replay_handoff() -> None:
    for command in [
        ["python", "scripts/build_paper10_desi_row4_non_simon_clock_search_v1.py"],
        ["python", "scripts/build_paper10_desi_row4_window_review_package_v1.py"],
        ["python", "scripts/validate_paper10_desi_row4_window_review_package_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/paper10_desi_row4_window_review_package_v1_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    with (ROOT / "data/derived/paper10_desi_row4_window_review_response_template_v1.csv").open(
        newline=""
    ) as f:
        template = list(csv.DictReader(f))
    assert summary["status"] == "DESI_ROW4_WINDOW_REVIEW_PACKAGE_BUILT_NOT_COMPLETED"
    assert summary["review_completed"] == "false"
    assert summary["strict_search_verdict"] == "row4_non_simon_strict_window_search_negative_blocker_remains"
    assert summary["row4_can_enter_replay"] == "false"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert summary["contains_endpoint_residuals"] == "false"
    assert summary["contains_endpoint_scores"] == "false"
    assert summary["contains_fit_statistics"] == "false"
    assert len(template) == 3
    assert {row["review_completed"] for row in template} == {"false"}
    assert {row["forbidden_inputs_used"] for row in template} == {"false"}
    assert {row["endpoint_replay_allowed"] for row in template} == {"false"}


def test_paper10_desi_row4_window_review_response_positive_still_requires_replay_review(tmp_path: Path) -> None:
    response = tmp_path / "paper10_desi_row4_window_review_response_v1.csv"
    summary = tmp_path / "summary.csv"
    rows = [
        {
            "policy_id": "PAPER10_DESI_ROW4_WINDOW_REVIEW_POLICY_V1",
            "question_id": "Q1_STRICT_WINDOW_STATUS",
            "question_text": "Should the frozen strict row-4 clock-support window remain |Delta z|<=0.10 after the non-Simon near-miss search?",
            "required_response": "KEEP_STRICT_WINDOW or ALLOW_CAVEATED_WINDOW_EXTENSION or REJECT_REOPEN",
            "acceptance_condition": "If KEEP_STRICT_WINDOW, row4 remains blocked. If ALLOW_CAVEATED_WINDOW_EXTENSION, reviewer must justify source-side use of Moresco2015 z=1.363 as caveated row4 support. If REJECT_REOPEN, close row4 source acquisition for this paper version.",
            "review_completed": "true",
            "reviewer_id_or_role": "external_source_reviewer",
            "reviewer_response": "ALLOW_CAVEATED_WINDOW_EXTENSION",
            "reviewer_rationale": "Near-window source can be carried only as caveated source-side context; no endpoint scores were used.",
            "source_reference_or_url": "https://doi.org/10.1093/mnrasl/slv037",
            "forbidden_inputs_used": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": "paper10_desi_row4_window_review_not_validation",
        },
        {
            "policy_id": "PAPER10_DESI_ROW4_WINDOW_REVIEW_POLICY_V1",
            "question_id": "Q2_MORESCO_2015_ELIGIBILITY",
            "question_text": "Can Moresco 2015 z=1.363, H=160+/-33.6, be treated as independent source-side row4 clock context despite |Delta z|=0.121?",
            "required_response": "ACCEPT_AS_CAVEATED_NEAR_WINDOW_SOURCE or RETAIN_AS_CONTEXT_ONLY or REJECT_SOURCE",
            "acceptance_condition": "ACCEPT_AS_CAVEATED_NEAR_WINDOW_SOURCE requires explicit reviewer rationale that the redshift separation is source-side acceptable and does not use endpoint residuals. RETAIN_AS_CONTEXT_ONLY keeps blocker active.",
            "review_completed": "true",
            "reviewer_id_or_role": "external_source_reviewer",
            "reviewer_response": "ACCEPT_AS_CAVEATED_NEAR_WINDOW_SOURCE",
            "reviewer_rationale": "The source is independent of Simon and close enough to reopen only a caveated source ledger.",
            "source_reference_or_url": "https://doi.org/10.1093/mnrasl/slv037",
            "forbidden_inputs_used": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": "paper10_desi_row4_window_review_not_validation",
        },
        {
            "policy_id": "PAPER10_DESI_ROW4_WINDOW_REVIEW_POLICY_V1",
            "question_id": "Q3_RELEASE_POLICY",
            "question_text": "If Q2 is accepted, what is the maximum allowed consequence?",
            "required_response": "SOURCE_REOPEN_ONLY_NO_REPLAY or AUTHORIZE_REPLAY_REVIEW_REQUIRED or NO_RELEASE",
            "acceptance_condition": "Default accepted consequence is SOURCE_REOPEN_ONLY_NO_REPLAY. Any endpoint replay still requires a separate replay-authorization package after the source window decision is frozen.",
            "review_completed": "true",
            "reviewer_id_or_role": "external_source_reviewer",
            "reviewer_response": "AUTHORIZE_REPLAY_REVIEW_REQUIRED",
            "reviewer_rationale": "A separate replay authorization is required before endpoint scoring.",
            "source_reference_or_url": "https://doi.org/10.1093/mnrasl/slv037",
            "forbidden_inputs_used": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": "paper10_desi_row4_window_review_not_validation",
        },
    ]
    with response.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    subprocess.run(
        [
            "python",
            "scripts/validate_paper10_desi_row4_window_review_response_v1.py",
            str(response),
            "--summary-out",
            str(summary),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with summary.open(newline="") as f:
        out = list(csv.DictReader(f))[0]
    assert out["status"] == "DESI_ROW4_WINDOW_REVIEW_IMPORTED_CAVEATED_SOURCE_REOPEN_NOT_REPLAY"
    assert out["source_reopen_caveated"] == "true"
    assert out["replay_review_required_before_endpoint"] == "true"
    assert out["row4_can_enter_replay"] == "false"
    assert out["endpoint_replay_allowed"] == "false"
    assert out["endpoint_validation_claimed"] == "false"
    assert out["physical_validation_claimed"] == "false"


def test_paper10_desi_row4_window_decision_gate_records_caveated_source_reopen_after_review() -> None:
    for command in [
        ["python", "scripts/build_paper10_desi_row4_window_review_package_v1.py"],
        ["python", "scripts/build_paper10_desi_row4_window_decision_gate_v1.py"],
        ["python", "scripts/validate_paper10_desi_row4_window_decision_gate_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/paper10_desi_row4_window_decision_gate_v1_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "DESI_ROW4_WINDOW_DECISION_GATE_BUILT_NOT_REPLAY_NOT_VALIDATION"
    assert summary["gate_status"] == "ROW4_SOURCE_REOPEN_CAVEATED_NO_REPLAY"
    assert summary["review_completed"] == "true"
    assert summary["source_reopen_caveated"] == "true"
    assert summary["row4_can_enter_replay"] == "false"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert summary["verdict"] == "row4_source_reopen_caveated_no_replay"


def test_paper10_desi_time_route_closure_status_blocks_replay_until_source_blockers_close() -> None:
    for command in [
        ["python", "scripts/build_paper10_desi_row4_window_decision_gate_v1.py"],
        ["python", "scripts/build_paper10_desi_row5_high_z_decision_gate_v1.py"],
        ["python", "scripts/build_paper10_desi_time_route_closure_status_v1.py"],
        ["python", "scripts/validate_paper10_desi_time_route_closure_status_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/paper10_desi_time_route_closure_status_v1_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "DESI_TIME_ROUTE_CLOSURE_STATUS_BUILT_NOT_REPLAY_NOT_VALIDATION"
    assert summary["closure_status"] == "DESI_TIME_ROUTE_CLOSED_PENDING_SOURCE_BLOCKERS_NOT_REPLAY"
    assert summary["row4_gate_status"] == "ROW4_SOURCE_REOPEN_CAVEATED_NO_REPLAY"
    assert summary["row4_status"] == "ROW4_CAVEATED_SOURCE_REOPENED_REPLAY_REVIEW_STILL_REQUIRED"
    assert summary["row5_gate_status"] == "ROW5_HIGH_Z_BLOCKER_REMAINS_NOT_REPLAY"
    assert summary["row5_status"] == "ROW5_HIGH_Z_CLOCK_SUPPORT_MISSING"
    assert summary["negative_control_blocks_replay"] == "true"
    assert summary["desi_time_route_endpoint_ready"] == "false"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert summary["verdict"] == "desi_time_route_closed_pending_row4_or_row5_or_richer_clock_readout_support"


def test_paper10_desi_time_route_closure_status_source_ready_still_requires_replay_review(tmp_path: Path) -> None:
    def copy_one(src: str, dst: Path, updates: dict[str, str]) -> Path:
        with (ROOT / src).open(newline="") as f:
            row = list(csv.DictReader(f))[0]
        row.update(updates)
        with dst.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(row.keys()), lineterminator="\n")
            writer.writeheader()
            writer.writerow(row)
        return dst

    row4 = copy_one(
        "data/derived/paper10_desi_row4_window_decision_gate_v1_summary.csv",
        tmp_path / "row4.csv",
        {
            "gate_status": "ROW4_SOURCE_REOPEN_CAVEATED_REPLAY_REVIEW_REQUIRED_NOT_REPLAY",
            "review_completed": "true",
            "source_reopen_caveated": "true",
            "replay_review_required_before_endpoint": "true",
            "verdict": "row4_source_reopen_caveated_prepare_replay_review_only",
        },
    )
    row5 = copy_one(
        "data/derived/paper10_desi_row5_high_z_decision_gate_v1_summary.csv",
        tmp_path / "row5.csv",
        {
            "gate_status": "ROW5_SOURCE_REOPEN_REPLAY_REVIEW_REQUIRED_NOT_REPLAY",
            "review_completed": "true",
            "source_reopen": "true",
            "replay_review_required_before_endpoint": "true",
            "verdict": "row5_source_reopen_prepare_replay_review_only",
        },
    )
    negative = copy_one(
        "data/derived/paper10_desi_time_level_negative_control_response_gate_v1_summary.csv",
        tmp_path / "negative.csv",
        {
            "route_status": "DESI_TIME_LEVEL_ROUTE_SOURCE_READY_REPLAY_REVIEW_REQUIRED",
            "verdict": "desi_time_level_negative_control_response_gate_source_ready_replay_review_required",
        },
    )
    out = tmp_path / "closure.csv"
    summary = tmp_path / "closure_summary.csv"
    subprocess.run(
        [
            "python",
            "scripts/build_paper10_desi_time_route_closure_status_v1.py",
            "--row4",
            str(row4),
            "--row5",
            str(row5),
            "--negative-control",
            str(negative),
            "--out",
            str(out),
            "--summary-out",
            str(summary),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with summary.open(newline="") as f:
        result = list(csv.DictReader(f))[0]
    assert result["closure_status"] == "DESI_TIME_ROUTE_SOURCE_READY_BUT_REPLAY_REVIEW_REQUIRED"
    assert result["row4_status"] == "ROW4_CAVEATED_SOURCE_REOPENED_REPLAY_REVIEW_STILL_REQUIRED"
    assert result["row5_status"] == "ROW5_SOURCE_REOPENED_REPLAY_REVIEW_STILL_REQUIRED"
    assert result["negative_control_blocks_replay"] == "false"
    assert result["desi_time_route_endpoint_ready"] == "false"
    assert result["endpoint_replay_allowed"] == "false"
    assert result["endpoint_validation_claimed"] == "false"
    assert result["physical_validation_claimed"] == "false"
    assert result["verdict"] == "desi_time_route_source_ready_replay_review_required_not_validation"


def test_paper10_desi_row5_high_z_decision_gate_records_blocker_after_review() -> None:
    for command in [
        ["python", "scripts/build_paper10_desi_row5_high_z_review_package_v1.py"],
        ["python", "scripts/build_paper10_desi_row5_high_z_decision_gate_v1.py"],
        ["python", "scripts/validate_paper10_desi_row5_high_z_decision_gate_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/paper10_desi_row5_high_z_decision_gate_v1_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "DESI_ROW5_HIGH_Z_DECISION_GATE_BUILT_NOT_REPLAY_NOT_VALIDATION"
    assert summary["gate_status"] == "ROW5_HIGH_Z_BLOCKER_REMAINS_NOT_REPLAY"
    assert summary["review_completed"] == "true"
    assert summary["source_reopen"] == "false"
    assert summary["row5_can_enter_replay"] == "false"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert summary["verdict"] == "row5_high_z_blocker_remains_no_replay"


def test_paper10_desi_row5_high_z_source_route_scout_records_no_gate_closing_source() -> None:
    for command in [
        ["python", "scripts/build_paper10_desi_row5_high_z_source_route_scout_v1.py"],
        ["python", "scripts/validate_paper10_desi_row5_high_z_source_route_scout_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/paper10_desi_row5_high_z_source_route_scout_v1_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "DESI_ROW5_HIGH_Z_SOURCE_ROUTE_SCOUT_BUILT_NOT_REPLAY_NOT_VALIDATION"
    assert summary["candidate_count"] == "4"
    assert summary["accepted_for_row5_count"] == "0"
    assert summary["context_only_count"] == "4"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert summary["verdict"] == "row5_high_z_scout_found_context_but_no_gate_closing_source"


def test_paper10_desi_row5_holdout_confirmation_records_predeclared_exclusion() -> None:
    for command in [
        ["python", "scripts/build_paper10_desi_row5_high_z_source_route_scout_v1.py"],
        ["python", "scripts/build_paper10_desi_row5_holdout_confirmation_v1.py"],
        ["python", "scripts/validate_paper10_desi_row5_holdout_confirmation_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/paper10_desi_row5_holdout_confirmation_v1_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "ROW5_HOLDOUT_CONFIRMED_NOT_REPLAY_NOT_VALIDATION"
    assert summary["heldout_radial_row"] == "5"
    assert summary["heldout_z"] == "2.33"
    assert summary["accepted_for_row5_count"] == "0"
    assert summary["allowed_radial_rows"] == "0;1;2;3;4"
    assert summary["excluded_radial_rows"] == "5"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert summary["verdict"] == "row5_holdout_confirmed_no_gate_closing_source_not_replay"


def test_paper10_desi_post_review_time_route_priority_selects_shape_gate() -> None:
    for command in [
        ["python", "scripts/build_paper10_desi_row5_high_z_source_route_scout_v1.py"],
        ["python", "scripts/build_paper10_desi_row5_holdout_confirmation_v1.py"],
        ["python", "scripts/build_paper10_desi_post_review_time_route_priority_v1.py"],
        ["python", "scripts/validate_paper10_desi_post_review_time_route_priority_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/paper10_desi_post_review_time_route_priority_v1_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "POST_REVIEW_TIME_ROUTE_PRIORITY_BUILT_NOT_REPLAY_NOT_VALIDATION"
    assert summary["primary_next_gate"] == "TIME_READOUT_SHAPE_OBSERVABLE"
    assert summary["secondary_required_gate"] == "ORDERING_CONTROL_SUITE"
    assert summary["row5_role"] == "HIGH_Z_HOLDOUT_FUTURE_REOPEN_ONLY"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert summary["verdict"] == "post_review_priority_is_shape_derivation_not_row5_replay"


def test_paper10_desi_row5_high_z_review_package_is_blank_non_replay_handoff() -> None:
    for command in [
        ["python", "scripts/build_paper10_desi_time_route_closure_status_v1.py"],
        ["python", "scripts/build_paper10_desi_row5_high_z_review_package_v1.py"],
        ["python", "scripts/validate_paper10_desi_row5_high_z_review_package_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/paper10_desi_row5_high_z_review_package_v1_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    with (ROOT / "data/derived/paper10_desi_row5_high_z_review_response_template_v1.csv").open(
        newline=""
    ) as f:
        template = list(csv.DictReader(f))
    assert summary["status"] == "DESI_ROW5_HIGH_Z_REVIEW_PACKAGE_BUILT_NOT_COMPLETED"
    assert summary["review_completed"] == "false"
    assert summary["row5_high_z_status"] == "desi_high_z_clock_support_missing_row_remains_holdout_not_validation"
    assert summary["desi_time_route_endpoint_ready"] == "false"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert summary["contains_endpoint_residuals"] == "false"
    assert summary["contains_endpoint_scores"] == "false"
    assert summary["contains_fit_statistics"] == "false"
    assert len(template) == 3
    assert {row["review_completed"] for row in template} == {"false"}
    assert {row["forbidden_inputs_used"] for row in template} == {"false"}
    assert {row["endpoint_replay_allowed"] for row in template} == {"false"}


def test_paper10_desi_row5_high_z_review_response_positive_still_requires_replay_review(tmp_path: Path) -> None:
    response = tmp_path / "paper10_desi_row5_high_z_review_response_v1.csv"
    summary = tmp_path / "summary.csv"
    rows = [
        {
            "policy_id": "PAPER10_DESI_ROW5_HIGH_Z_REVIEW_POLICY_V1",
            "question_id": "Q1_HIGH_Z_CLOCK_SOURCE",
            "question_text": "Can the reviewer identify an independent high-z cosmic-clock or chronometer source covering or bracketing z=2.33 without extrapolating the frozen CC table?",
            "required_response": "ACCEPT_HIGH_Z_CLOCK_SOURCE or NO_HIGH_Z_CLOCK_SOURCE or CAVEATED_CONTEXT_ONLY",
            "acceptance_condition": "ACCEPT requires a public/citable source-native clock or chronometer value/range at or bracketing z=2.33; BAO/r_d alone is not sufficient. NO or CAVEATED_CONTEXT keeps row5 blocked.",
            "review_completed": "true",
            "reviewer_id_or_role": "external_source_reviewer",
            "reviewer_response": "NO_HIGH_Z_CLOCK_SOURCE",
            "reviewer_rationale": "No independent high-z chronometer source is attached in this response.",
            "source_reference_or_url": "NA",
            "source_redshift_or_range": "NA",
            "forbidden_inputs_used": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": "paper10_desi_row5_high_z_review_not_validation",
        },
        {
            "policy_id": "PAPER10_DESI_ROW5_HIGH_Z_REVIEW_POLICY_V1",
            "question_id": "Q2_SOURCE_NATIVE_TIME_READOUT",
            "question_text": "If no clock source exists, can a source-native high-z time/readout observable be defined without treating Ly-alpha BAO alone as clock support?",
            "required_response": "ACCEPT_SOURCE_NATIVE_TIME_READOUT_CANDIDATE or RETAIN_AS_CROSS_PROBE_CONTEXT_ONLY or REJECT_ROUTE",
            "acceptance_condition": "ACCEPT requires an explicit source-side time/readout observable definition independent of endpoint scores; RETAIN_AS_CROSS_PROBE_CONTEXT_ONLY keeps row5 blocked but preserves Ly-alpha BAO as context.",
            "review_completed": "true",
            "reviewer_id_or_role": "external_source_reviewer",
            "reviewer_response": "ACCEPT_SOURCE_NATIVE_TIME_READOUT_CANDIDATE",
            "reviewer_rationale": "A source-native high-z time/readout candidate is accepted only as source-side route; Ly-alpha BAO alone is not treated as clock support.",
            "source_reference_or_url": "https://arxiv.org/abs/2007.08995",
            "source_redshift_or_range": "z=2.33",
            "forbidden_inputs_used": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": "paper10_desi_row5_high_z_review_not_validation",
        },
        {
            "policy_id": "PAPER10_DESI_ROW5_HIGH_Z_REVIEW_POLICY_V1",
            "question_id": "Q3_RELEASE_POLICY",
            "question_text": "If Q1 or Q2 is accepted, what is the maximum allowed consequence?",
            "required_response": "SOURCE_REOPEN_ONLY_NO_REPLAY or AUTHORIZE_REPLAY_REVIEW_REQUIRED or NO_RELEASE",
            "acceptance_condition": "Any accepted source route can at most reopen source acquisition or require a separate replay-authorization review; this package itself must not authorize endpoint replay.",
            "review_completed": "true",
            "reviewer_id_or_role": "external_source_reviewer",
            "reviewer_response": "AUTHORIZE_REPLAY_REVIEW_REQUIRED",
            "reviewer_rationale": "A separate replay authorization is required before endpoint scoring.",
            "source_reference_or_url": "https://arxiv.org/abs/2007.08995",
            "source_redshift_or_range": "z=2.33",
            "forbidden_inputs_used": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": "paper10_desi_row5_high_z_review_not_validation",
        },
    ]
    with response.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    subprocess.run(
        [
            "python",
            "scripts/validate_paper10_desi_row5_high_z_review_response_v1.py",
            str(response),
            "--summary-out",
            str(summary),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with summary.open(newline="") as f:
        out = list(csv.DictReader(f))[0]
    assert out["status"] == "DESI_ROW5_HIGH_Z_REVIEW_IMPORTED_SOURCE_REOPEN_NOT_REPLAY"
    assert out["source_reopen"] == "true"
    assert out["accepted_clock_source"] == "false"
    assert out["accepted_source_native_time_readout"] == "true"
    assert out["replay_review_required_before_endpoint"] == "true"
    assert out["row5_can_enter_replay"] == "false"
    assert out["endpoint_replay_allowed"] == "false"
    assert out["endpoint_validation_claimed"] == "false"
    assert out["physical_validation_claimed"] == "false"


def test_void_source_basis_refinement_v2_time_readout_route_ledger_v1_preserves_blocker() -> None:
    for command in [
        ["python", "scripts/build_void_source_basis_refinement_v2_time_readout_route_ledger_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_v2_time_readout_route_ledger_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/void_source_basis_refinement_v2_time_readout_route_ledger_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    with (ROOT / "data/derived/void_source_basis_refinement_v2_time_readout_route_ledger.csv").open(
        newline=""
    ) as f:
        rows = list(csv.DictReader(f))
    assert summary["status"] == "V2_TIME_READOUT_ROUTE_LEDGER_FROZEN_VALUES_BLOCKED"
    assert summary["n_rows"] == "424"
    assert summary["time_route_declared"] == "true"
    assert summary["time_values_computable"] == "false"
    assert summary["time_values_computed"] == "false"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["verdict"] == "time_route_declared_but_products_not_fetched_or_numeric_rule_missing"
    assert "CC_HZ_TABLE=PRODUCT_SELECTED_NOT_FETCHED" in summary["required_product_status"]
    assert rows
    assert {row["W_time_value_status"] for row in rows} == {"BLOCKED_TIME_PRODUCTS_NOT_FETCHED_OR_NOT_NUMERIC"}
    assert {row["W_time_source_value"] for row in rows} == {"NA"}
    assert {row["contains_late_time_fit_parameters"] for row in rows} == {"false"}


def test_void_source_basis_refinement_v2_projection_morphology_gate_v1_tracks_missing_channels() -> None:
    for command in [
        ["python", "scripts/build_void_source_basis_refinement_v2_projection_morphology_gate_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_v2_projection_morphology_gate_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/void_source_basis_refinement_v2_projection_morphology_gate_v1_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    with (ROOT / "data/derived/void_source_basis_refinement_v2_projection_morphology_gate_v1.csv").open(
        newline=""
    ) as f:
        rows = list(csv.DictReader(f))
    assert summary["all_components_tracked"] == "true"
    assert summary["components_required"] == "6"
    assert summary["components_tracked"] == "6"
    assert summary["components_ready"] == "0"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["verdict"] == "missing_projection_morphology_components_accounted_endpoint_still_blocked"
    component_ids = {row["component_id"] for row in rows}
    assert {
        "V2_VOID_MORPHOLOGY",
        "V2_WEB_MORPHOLOGY",
        "V2_OBSERVER_PATH_PROJECTION",
        "V2_TIME_READOUT_PROJECTION",
        "V2_CMB_SAFETY",
        "V2_MULTI_CHANNEL_COUPLING",
    } == component_ids


def test_void_source_basis_refinement_v2_multichannel_coupling_ledger_v1_blocks_endpoint() -> None:
    for command in [
        ["python", "scripts/build_void_source_basis_refinement_v2_multichannel_coupling_ledger_v1.py"],
        ["python", "scripts/validate_void_source_basis_refinement_v2_multichannel_coupling_ledger_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/void_source_basis_refinement_v2_multichannel_coupling_ledger_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    with (ROOT / "data/derived/void_source_basis_refinement_v2_multichannel_coupling_ledger.csv").open(
        newline=""
    ) as f:
        rows = list(csv.DictReader(f))
    assert summary["status"] == "V2_MULTI_CHANNEL_COUPLING_LEDGER_FROZEN_ENDPOINT_BLOCKED"
    assert summary["endpoint_ready_coupling_rule_count"] == "0"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["void_values_available"] == "true"
    assert summary["web_values_available"] == "true"
    assert summary["path_values_available"] == "false"
    assert summary["time_values_available"] == "false"
    assert summary["cmb_safety_passed"] == "true"
    assert summary["void_weak_negative_preserved"] == "true"
    assert summary["verdict"] == "multichannel_coupling_accounted_but_endpoint_blocked"
    assert {row["coupling_rule_id"] for row in rows} == {
        "VOID_WEB_VALUE_PAIR",
        "VOID_WEB_PATH",
        "VOID_WEB_TIME",
        "FULL_V2_PROJECTION_MORPHOLOGY",
    }
    assert {row["endpoint_ready"] for row in rows} == {"false"}
    assert {row["endpoint_replay_allowed"] for row in rows} == {"false"}
    void_web = next(row for row in rows if row["coupling_rule_id"] == "VOID_WEB_VALUE_PAIR")
    assert void_web["source_values_available"] == "true"
    assert void_web["coupling_values_computable"] == "true"
    assert void_web["blocking_reason"] == "void_branch_weak_negative_control_dominance_preserved"


def test_source_page_cache_is_hash_locked() -> None:
    with (ROOT / "data/source_manifest/source_page_cache_manifest.csv").open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) >= 10
    assert {row["status"] for row in rows} == {"CACHED"}
    for row in rows:
        cache_path = ROOT / row["cache_path"]
        assert cache_path.exists(), row["source_id"]
        assert row["sha256"]
        assert int(row["byte_count"]) > 0


def test_product_freeze_plan_covers_sources_without_endpoint_permission() -> None:
    with (ROOT / "data/source_manifest/paper10_source_freeze_manifest.csv").open(newline="") as f:
        source_rows = list(csv.DictReader(f))
    with (ROOT / "data/source_manifest/paper10_product_freeze_plan.csv").open(newline="") as f:
        product_rows = list(csv.DictReader(f))
    source_ids = {row["source_id"] for row in source_rows}
    product_source_ids = {row["source_id"] for row in product_rows}
    assert source_ids <= product_source_ids
    assert {row["endpoint_allowed"] for row in product_rows} == {"false"}
    assert "PRODUCT_FETCHED_FROZEN" not in {row["freeze_status"] for row in product_rows}
    for row in product_rows:
        assert row["transform_rule_id"].startswith("TR_")
        assert row["endpoint_forbidden_inputs"]


def test_void_web_source_native_freeze_plan_blocks_endpoint_leakage() -> None:
    with (
        ROOT / "data/source_manifest/void_web_source_native_freeze_plan_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert {row["channel_id"] for row in rows} == {
        "W_VOID_MATURITY",
        "W_WEB_ANISOTROPY",
    }
    assert {row["freeze_status"] for row in rows} == {
        "SOURCE_NATIVE_CANDIDATE_SELECTED_NOT_FETCHED"
    }
    assert {row["endpoint_scoring_allowed"] for row in rows} == {"false"}
    forbidden = ";".join(row["endpoint_forbidden_inputs"] for row in rows)
    for marker in [
        "distance_residuals",
        "growth_residuals",
        "lensing_residuals",
        "fit_improvement_flags",
        "posthoc_void_thresholds",
        "posthoc_environment_labels",
    ]:
        assert marker in forbidden
    for row in rows:
        assert row["planned_local_path"].startswith("data/raw/")
        assert row["required_transform_rule"].startswith("TR_")
        assert row["required_hash"] == "sha256"
        assert row["null_control"]


def test_void_web_source_native_products_are_frozen_not_endpoint_enabled() -> None:
    with (
        ROOT / "data/source_manifest/void_web_source_native_frozen_products_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    ids = {row["frozen_product_id"] for row in rows}
    assert {
        "VOIDFINDER_PLANCK2018_MAXIMAL_VOID_TABLE",
        "VOIDFINDER_PLANCK2018_MASK",
        "SDSS_DR17_MCPM_SLIMEMOLD_GALAXY_CATALOG",
        "SDSS_DR17_MCPM_SHA1SUM",
    } <= ids
    assert {row["status"] for row in rows} == {"SOURCE_NATIVE_PRODUCT_FETCHED_FROZEN"}
    assert {row["endpoint_allowed"] for row in rows} == {"false"}
    for row in rows:
        path = ROOT / row["local_path"]
        assert path.exists(), row["frozen_product_id"]
        assert int(row["byte_count"]) > 0
        assert row["sha256"]
        assert row["endpoint_blocker"]


def test_void_web_source_native_inventory_is_not_endpoint_scoring() -> None:
    with (ROOT / "data/derived/void_web_source_native_inventory_v1.csv").open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 4
    blob = " ".join(row["observable_summary"] for row in rows)
    assert "void_rows=1163" in blob
    assert "fits_bintable_rows=638820" in blob
    assert {row["endpoint_allowed"] for row in rows} == {"false"}
    assert {row["contains_endpoint_scores"] for row in rows} == {"false"}
    assert {row["contains_residuals"] for row in rows} == {"false"}


def test_void_web_source_native_design_matrix_is_not_endpoint_scoring() -> None:
    with (
        ROOT / "data/derived/pantheon_void_web_source_native_design_matrix_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "TRANSFORM_RULE_FROZEN_NOT_SCORED"
    assert summary["endpoint_scoring_allowed"] == "false"
    assert int(summary["rows"]) == 1371
    assert int(summary["void_nonzero_rows"]) == 426
    assert int(summary["web_nonzero_rows"]) == 1333
    assert summary["contains_model_predictions"] == "false"
    assert summary["contains_residuals"] == "false"
    assert summary["contains_fit_statistics"] == "false"
    with (ROOT / "data/derived/pantheon_void_web_source_native_design_matrix_v1.csv").open(
        newline=""
    ) as f:
        columns = set(csv.DictReader(f).fieldnames or [])
    assert "W_void_source_native_basis" in columns
    assert "W_web_source_native_basis" in columns
    assert "distance_residuals" not in columns
    assert "chi2" not in columns


def test_void_web_source_native_full_cov_pilot_is_nonvalidation() -> None:
    with (
        ROOT / "data/source_manifest/pantheon_void_web_source_native_full_cov_pilot_v1.csv"
    ).open(newline="") as f:
        manifest = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/pantheon_void_web_source_native_full_cov_pilot_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert manifest["status"] == "VOID_WEB_SOURCE_NATIVE_FULL_COV_PILOT_NOT_VALIDATION"
    assert summary["status"] == manifest["status"]
    assert summary["claim_boundary"] == "void_web_source_native_full_cov_pilot_not_validation"
    assert "W_PATH_PROJECTION" in summary["disabled_channels"]
    assert "W_TIME_READOUT" in summary["disabled_channels"]
    forbidden = manifest["forbidden_inputs"]
    assert "distance_residuals" in forbidden
    assert "posthoc_environment_labels" in forbidden
    for key in [
        "baseline_best_chi2",
        "source_native_void_web_best_chi2",
        "source_native_void_only_best_chi2",
        "source_native_web_only_best_chi2",
        "wrong_web_sign_best_chi2",
        "shuffled_best_chi2",
        "delta_aic_source_native_void_web_minus_baseline",
    ]:
        float(summary[key])


def test_growth_web_source_native_design_and_pilot_are_nonvalidation() -> None:
    with (ROOT / "data/source_manifest/sdss_final_bao_rsd_growth_summary_v1.csv").open(
        newline=""
    ) as f:
        growth_rows = list(csv.DictReader(f))
    assert len(growth_rows) == 6
    assert {row["endpoint_allowed"] for row in growth_rows} == {"false"}
    assert {row["covariance_status"] for row in growth_rows} == {"DIAGONAL_ERROR_ONLY"}
    with (ROOT / "data/derived/growth_web_source_native_design_matrix_v1_summary.csv").open(
        newline=""
    ) as f:
        design_summary = list(csv.DictReader(f))[0]
    assert design_summary["endpoint_scoring_allowed"] == "false"
    assert int(design_summary["rows"]) == 6
    assert int(design_summary["web_nonzero_rows"]) == 5
    assert design_summary["contains_residuals"] == "false"
    assert design_summary["contains_fit_statistics"] == "false"
    with (ROOT / "data/derived/growth_web_source_native_pilot_v1_summary.csv").open(
        newline=""
    ) as f:
        pilot_summary = list(csv.DictReader(f))[0]
    assert pilot_summary["status"] == "GROWTH_WEB_SOURCE_NATIVE_PILOT_NOT_VALIDATION"
    assert pilot_summary["claim_boundary"] == "growth_web_source_native_pilot_not_validation"
    assert pilot_summary["covariance_policy"] == "diagonal_summary_errors_only"
    assert "W_VOID_MATURITY" in pilot_summary["disabled_channels"]
    for key in [
        "baseline_best_chi2",
        "web_best_chi2",
        "wrong_web_sign_best_chi2",
        "shuffled_web_best_chi2",
        "delta_aic_web_minus_baseline",
    ]:
        float(pilot_summary[key])


def test_sdss_multitracer_bao_rsd_full_cov_pilot_is_nonvalidation() -> None:
    with (ROOT / "data/source_manifest/sdss_multitracer_bao_rsd_products_v1.csv").open(
        newline=""
    ) as f:
        product_rows = list(csv.DictReader(f))
    assert len(product_rows) == 2
    assert {row["status"] for row in product_rows} == {"SOURCE_NATIVE_PRODUCT_FETCHED_FROZEN"}
    assert {row["endpoint_allowed"] for row in product_rows} == {"false"}
    assert {row["measurement_space"] for row in product_rows} == {
        "configuration_space",
        "fourier_space",
    }
    for row in product_rows:
        assert (ROOT / row["zip_path"]).exists()
        assert (ROOT / row["data_path"]).exists()
        assert (ROOT / row["covariance_path"]).exists()
        assert row["sha256"]

    with (ROOT / "data/derived/sdss_multitracer_bao_rsd_design_matrix_v1.csv").open(
        newline=""
    ) as f:
        design_rows = list(csv.DictReader(f))
    assert len(design_rows) == 6
    assert [row["observable"] for row in design_rows] == [
        "DM_over_rd",
        "DH_over_rd",
        "fsigma8",
        "DM_over_rd",
        "DH_over_rd",
        "fsigma8",
    ]
    assert all(
        row["W_web_applies_to_observable"] == "false"
        for row in design_rows
        if row["observable"] != "fsigma8"
    )
    with (ROOT / "data/derived/sdss_multitracer_bao_rsd_design_matrix_v1_summary.csv").open(
        newline=""
    ) as f:
        design_summary = list(csv.DictReader(f))[0]
    assert design_summary["endpoint_scoring_allowed"] == "false"
    assert design_summary["contains_residuals"] == "false"
    assert design_summary["contains_fit_statistics"] == "false"
    assert design_summary["covariance_shape"] == "6x6"

    with (ROOT / "data/derived/sdss_multitracer_bao_rsd_full_cov_pilot_v1_summary.csv").open(
        newline=""
    ) as f:
        pilot_summary = list(csv.DictReader(f))[0]
    assert pilot_summary["status"] == "SDSS_MULTITRACER_BAO_RSD_FULL_COV_PILOT_NOT_VALIDATION"
    assert (
        pilot_summary["claim_boundary"]
        == "sdss_multitracer_bao_rsd_full_cov_pilot_not_validation"
    )
    assert pilot_summary["covariance_policy"] == "official_6x6_compressed_parameter_covariance"
    assert "W_VOID_MATURITY" in pilot_summary["disabled_channels"]
    for key in [
        "baseline_best_chi2",
        "web_best_chi2",
        "wrong_web_sign_best_chi2",
        "shuffled_web_best_chi2",
        "delta_aic_web_minus_baseline",
    ]:
        float(pilot_summary[key])


def test_cmb_safety_lowz_support_check_is_known_limit_only() -> None:
    with (ROOT / "data/source_manifest/cmb_safety_lowz_support_v1.csv").open(newline="") as f:
        run = list(csv.DictReader(f))[0]
    assert run["status"] == "CMB_SAFETY_SUPPORT_CHECK_NOT_VALIDATION"
    assert run["endpoint_scoring_allowed"] == "false"
    assert "posthoc_cmb_map_selection" in run["forbidden_inputs"]
    with (ROOT / "data/derived/cmb_safety_lowz_support_v1.csv").open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 2
    assert {row["probe_id"] for row in rows} == {"z_safety_floor", "z_recombination_proxy"}
    for row in rows:
        assert row["passes_zero_support"] == "true"
        assert float(row["W_void_source_native_basis"]) == 0.0
        assert float(row["W_web_source_native_basis"]) == 0.0
    with (ROOT / "data/derived/cmb_safety_lowz_support_v1_summary.csv").open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["passes_cmb_lowz_support_check"] == "true"
    assert summary["contains_cmb_map_data"] == "false"
    assert summary["contains_cmb_likelihood"] == "false"
    assert summary["contains_fit_statistics"] == "false"


def test_kids1000_lensing_route_is_provenance_only() -> None:
    with (ROOT / "data/source_manifest/kids1000_lensing_route_v1.csv").open(newline="") as f:
        route = list(csv.DictReader(f))[0]
    assert route["status"] == "KIDS1000_LENSING_ROUTE_DECLARED_NOT_FETCHED"
    assert route["endpoint_scoring_allowed"] == "false"
    assert "lensing_residuals" in route["forbidden_inputs"]
    assert "posthoc_tomographic_selection" in route["forbidden_inputs"]
    with (ROOT / "data/derived/kids1000_lensing_route_v1_head.csv").open(newline="") as f:
        head = list(csv.DictReader(f))[0]
    assert int(head["status_code"]) == 200
    assert int(head["content_length"]) > 0
    assert "gzip" in head["content_type"]
    assert head["contains_lensing_data_vectors"] == "false"
    assert head["contains_covariance_matrices"] == "false"
    assert head["contains_fit_statistics"] == "false"
    with (ROOT / "data/derived/kids1000_lensing_route_v1_summary.csv").open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["endpoint_scoring_allowed"] == "false"
    assert summary["contains_lensing_likelihood"] == "false"
    assert summary["contains_lensing_residuals"] == "false"
    for marker in [
        "tomographic_bin_policy",
        "statistic_choice_COSEBIs_or_2PCF_or_bandpowers",
        "covariance_block_policy",
    ]:
        assert marker in summary["future_freeze_items"]


def test_kids1000_lensing_tarball_inventory_and_cosebis_route_are_not_scored() -> None:
    with (ROOT / "data/source_manifest/kids1000_lensing_products_v1.csv").open(newline="") as f:
        product = list(csv.DictReader(f))[0]
    assert product["status"] == "SOURCE_NATIVE_PRODUCT_FETCHED_FROZEN"
    assert product["endpoint_allowed"] == "false"
    tarball = ROOT / product["local_path"]
    assert tarball.exists()
    assert int(product["byte_count"]) > 0
    assert product["sha256"]
    with (ROOT / "data/source_manifest/kids1000_cosebis_lensing_route_v1.csv").open(
        newline=""
    ) as f:
        route = list(csv.DictReader(f))[0]
    assert route["selected_statistic"] == "COSEBIs"
    assert route["endpoint_scoring_allowed"] == "false"
    assert "lensing_residuals" in route["forbidden_inputs"]
    assert "kids_chain_posterior_reweighting" in route["forbidden_inputs"]
    with (ROOT / "data/derived/kids1000_lensing_inventory_v1_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "KIDS1000_LENSING_INVENTORY_BUILT_NOT_SCORED"
    assert summary["endpoint_scoring_allowed"] == "false"
    assert summary["contains_residuals"] == "false"
    assert summary["contains_fit_statistics"] == "false"
    assert int(summary["n_fits_products"]) == 3
    assert int(summary["n_selected_cosebis_members"]) == 1
    with (ROOT / "data/derived/kids1000_lensing_inventory_v1.csv").open(newline="") as f:
        rows = list(csv.DictReader(f))
    selected = [row for row in rows if row["selected_for_cosebis_route"] == "true"]
    assert len(selected) == 1
    assert selected[0]["member_kind"] == "fits_product"
    assert "cosebis_" in selected[0]["member_name"]


def test_kids1000_cosebis_hdu_policy_freezes_roles_without_scoring() -> None:
    with (ROOT / "data/source_manifest/kids1000_cosebis_hdu_policy_v1.csv").open(
        newline=""
    ) as f:
        policy = list(csv.DictReader(f))[0]
    assert policy["status"] == "KIDS1000_COSEBIS_HDU_POLICY_FROZEN_NOT_SCORED"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert policy["selected_hdu_data_vector"] == "En"
    assert policy["selected_hdu_covariance"] == "COVMAT"
    assert policy["selected_hdu_redshift_distribution"] == "NZ_SOURCE"
    assert "lensing_residuals" in policy["forbidden_inputs"]
    assert "posthoc_mode_cuts" in policy["forbidden_inputs"]
    with (ROOT / "data/derived/kids1000_cosebis_hdu_inventory_v1_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "KIDS1000_COSEBIS_HDU_INVENTORY_BUILT_NOT_SCORED"
    assert summary["endpoint_scoring_allowed"] == "false"
    assert summary["contains_predictions"] == "false"
    assert summary["contains_residuals"] == "false"
    assert summary["contains_fit_statistics"] == "false"
    assert summary["data_vector_rows"] == "300"
    assert summary["covariance_shape"] == "300x300"
    assert summary["redshift_distribution_rows"] == "119"
    assert summary["covariance_positive_definite"] == "true"
    with (ROOT / "data/derived/kids1000_cosebis_hdu_inventory_v1.csv").open(
        newline=""
    ) as f:
        rows = list(csv.DictReader(f))
    roles = {row["role"] for row in rows}
    assert {"data_vector", "covariance", "redshift_distribution"} <= roles


def test_kids1000_cosebis_tomographic_mode_policy_freezes_structure_without_scoring() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_tomographic_mode_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert policy["status"] == "KIDS1000_COSEBIS_TOMOGRAPHIC_MODE_POLICY_FROZEN_NOT_SCORED"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert policy["expected_tomographic_bins"] == "5"
    assert policy["expected_tomographic_pairs"] == "15"
    assert policy["expected_modes_per_pair"] == "20"
    assert "lensing_residuals" in policy["forbidden_inputs"]
    assert "posthoc_mode_cuts" in policy["forbidden_inputs"]
    with (
        ROOT / "data/derived/kids1000_cosebis_tomographic_mode_inventory_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "KIDS1000_COSEBIS_TOMOGRAPHIC_MODE_INVENTORY_BUILT_NOT_SCORED"
    assert summary["endpoint_scoring_allowed"] == "false"
    assert summary["contains_predictions"] == "false"
    assert summary["contains_residuals"] == "false"
    assert summary["contains_fit_statistics"] == "false"
    assert summary["n_tomographic_bins"] == "5"
    assert summary["n_tomographic_pairs"] == "15"
    assert summary["n_modes_per_pair"] == "20"
    assert summary["data_vector_rows"] == "300"
    assert summary["all_pairs_upper_triangular"] == "true"
    assert summary["all_pairs_complete"] == "true"
    with (
        ROOT / "data/derived/kids1000_cosebis_tomographic_mode_inventory_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 15
    assert {(row["bin1"], row["bin2"]) for row in rows} == {
        ("1", "1"),
        ("1", "2"),
        ("1", "3"),
        ("1", "4"),
        ("1", "5"),
        ("2", "2"),
        ("2", "3"),
        ("2", "4"),
        ("2", "5"),
        ("3", "3"),
        ("3", "4"),
        ("3", "5"),
        ("4", "4"),
        ("4", "5"),
        ("5", "5"),
    }
    assert {row["rows_for_pair"] for row in rows} == {"20"}
    assert {row["modes"] for row in rows} == {";".join(str(value) for value in range(1, 21))}
    assert {row["endpoint_scoring_allowed"] for row in rows} == {"false"}


def test_kids1000_cosebis_covariance_readiness_is_not_an_inverse_likelihood() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_covariance_readiness_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert policy["status"] == "KIDS1000_COSEBIS_COVARIANCE_READINESS_POLICY_FROZEN_NOT_SCORED"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert policy["current_inversion_allowed"] == "false"
    assert policy["selected_hdu_covariance"] == "COVMAT"
    assert "lensing_residuals" in policy["forbidden_inputs"]
    assert "posthoc_mode_cuts" in policy["forbidden_inputs"]
    with (
        ROOT / "data/derived/kids1000_cosebis_covariance_readiness_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "KIDS1000_COSEBIS_COVARIANCE_READINESS_BUILT_NOT_SCORED"
    assert summary["endpoint_scoring_allowed"] == "false"
    assert summary["current_inversion_allowed"] == "false"
    assert summary["inverse_saved"] == "false"
    assert summary["contains_predictions"] == "false"
    assert summary["contains_residuals"] == "false"
    assert summary["contains_fit_statistics"] == "false"
    assert summary["covariance_shape"] == "300x300"
    assert summary["positive_diagonal"] == "true"
    assert summary["positive_definite"] == "true"
    assert summary["cholesky_ready"] == "true"
    assert float(summary["min_eigenvalue"]) > 0.0
    assert float(summary["condition_number"]) > 1.0
    with (
        ROOT / "data/derived/kids1000_cosebis_covariance_readiness_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 1
    assert rows[0]["inverse_saved"] == "false"


def test_kids1000_cosebis_mask_modecut_policy_keeps_all_rows_without_leakage() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_mask_modecut_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert policy["status"] == "KIDS1000_COSEBIS_MASK_MODECUT_POLICY_FROZEN_NOT_SCORED"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert policy["mask_policy"] == "retain_all_source_rows"
    assert policy["mode_cut_policy"] == "retain_modes_1_through_20"
    assert policy["expected_input_rows"] == "300"
    assert policy["expected_retained_rows"] == "300"
    assert "lensing_residuals" in policy["forbidden_inputs"]
    assert "kids_data_vector_outlier_removal" in policy["forbidden_inputs"]
    with (
        ROOT / "data/derived/kids1000_cosebis_mask_modecut_inventory_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "KIDS1000_COSEBIS_MASK_MODECUT_INVENTORY_BUILT_NOT_SCORED"
    assert summary["endpoint_scoring_allowed"] == "false"
    assert summary["contains_predictions"] == "false"
    assert summary["contains_residuals"] == "false"
    assert summary["contains_fit_statistics"] == "false"
    assert summary["uses_residuals"] == "false"
    assert summary["uses_fit_statistics"] == "false"
    assert summary["input_rows"] == "300"
    assert summary["retained_rows"] == "300"
    assert summary["dropped_rows"] == "0"
    assert summary["n_retained_tomographic_pairs"] == "15"
    with (
        ROOT / "data/derived/kids1000_cosebis_mask_modecut_inventory_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 15
    assert {row["retained_rows_for_pair"] for row in rows} == {"20"}
    assert {row["dropped_rows_for_pair"] for row in rows} == {"0"}
    assert {row["dropped_modes"] for row in rows} == {""}
    assert {row["uses_residuals"] for row in rows} == {"false"}


def test_kids1000_cosebis_tomographic_weight_policy_is_unit_retention_only() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_tomographic_weight_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert policy["status"] == "KIDS1000_COSEBIS_TOMOGRAPHIC_WEIGHT_POLICY_FROZEN_NOT_SCORED"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert policy["statistical_likelihood_weighting_allowed"] == "false"
    assert policy["weight_policy"] == "unit_retention_weight_all_pairs"
    assert "posthoc_pair_weighting" in policy["forbidden_inputs"]
    with (
        ROOT / "data/derived/kids1000_cosebis_tomographic_weight_inventory_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "KIDS1000_COSEBIS_TOMOGRAPHIC_WEIGHT_INVENTORY_BUILT_NOT_SCORED"
    assert summary["endpoint_scoring_allowed"] == "false"
    assert summary["statistical_likelihood_weighting_allowed"] == "false"
    assert summary["contains_predictions"] == "false"
    assert summary["contains_residuals"] == "false"
    assert summary["contains_fit_statistics"] == "false"
    assert summary["uses_residuals"] == "false"
    assert summary["uses_fit_statistics"] == "false"
    assert summary["uses_posterior_chains"] == "false"
    assert summary["n_tomographic_pairs"] == "15"
    assert summary["rows_per_pair"] == "20"
    assert summary["all_pairs_unit_weight"] == "true"
    assert summary["min_retention_weight"] == "1.000000"
    assert summary["max_retention_weight"] == "1.000000"
    with (
        ROOT / "data/derived/kids1000_cosebis_tomographic_weight_inventory_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 15
    assert {row["retention_weight"] for row in rows} == {"1.000000"}
    assert {row["statistical_likelihood_weighting_allowed"] for row in rows} == {"false"}
    assert {row["uses_residuals"] for row in rows} == {"false"}
    assert {row["uses_posterior_chains"] for row in rows} == {"false"}


def test_kids1000_cosebis_covariance_subselection_keeps_full_covariance() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_covariance_subselection_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert policy["status"] == "KIDS1000_COSEBIS_COVARIANCE_SUBSELECTION_POLICY_FROZEN_NOT_SCORED"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert policy["current_inversion_allowed"] == "false"
    assert policy["expected_full_covariance_shape"] == "300x300"
    assert policy["expected_retained_covariance_shape"] == "300x300"
    assert "posthoc_covariance_subselection" in policy["forbidden_inputs"]
    with (
        ROOT / "data/derived/kids1000_cosebis_covariance_subselection_inventory_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "KIDS1000_COSEBIS_COVARIANCE_SUBSELECTION_INVENTORY_BUILT_NOT_SCORED"
    assert summary["endpoint_scoring_allowed"] == "false"
    assert summary["current_inversion_allowed"] == "false"
    assert summary["inverse_saved"] == "false"
    assert summary["contains_predictions"] == "false"
    assert summary["contains_residuals"] == "false"
    assert summary["contains_fit_statistics"] == "false"
    assert summary["uses_residuals"] == "false"
    assert summary["uses_fit_statistics"] == "false"
    assert summary["uses_posterior_chains"] == "false"
    assert summary["full_covariance_shape"] == "300x300"
    assert summary["retained_covariance_shape"] == "300x300"
    assert summary["retained_rows"] == "300"
    assert summary["full_covariance_retained"] == "true"
    assert summary["dropped_covariance_rows"] == "0"
    assert summary["dropped_covariance_cols"] == "0"
    with (
        ROOT / "data/derived/kids1000_cosebis_covariance_subselection_inventory_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 15
    assert {row["retained_rows_for_pair"] for row in rows} == {"20"}
    assert {row["dropped_covariance_rows"] for row in rows} == {"0"}
    assert {row["dropped_covariance_cols"] for row in rows} == {"0"}
    assert [int(row["covariance_row_start_zero_based"]) for row in rows] == list(range(0, 300, 20))
    assert [int(row["covariance_row_end_zero_based"]) for row in rows] == list(range(19, 300, 20))


def test_kids1000_cosebis_covariance_inversion_policy_is_readiness_only() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_covariance_inversion_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert policy["status"] == "KIDS1000_COSEBIS_COVARIANCE_INVERSION_POLICY_FROZEN_NOT_SCORED"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert policy["current_inversion_executed"] == "false"
    assert policy["requires_frozen_theory_vector"] == "true"
    assert policy["expected_covariance_shape"] == "300x300"
    assert "cholesky_solve" in policy["inversion_policy"]
    assert "do_not_materialize" in policy["inverse_materialization_policy"]
    assert "posthoc_covariance_inversion_choice" in policy["forbidden_inputs"]
    with (
        ROOT / "data/derived/kids1000_cosebis_covariance_inversion_readiness_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "KIDS1000_COSEBIS_COVARIANCE_INVERSION_READINESS_BUILT_NOT_SCORED"
    assert summary["endpoint_scoring_allowed"] == "false"
    assert summary["current_inversion_executed"] == "false"
    assert summary["inverse_saved"] == "false"
    assert summary["contains_theory_vector"] == "false"
    assert summary["contains_predictions"] == "false"
    assert summary["contains_residuals"] == "false"
    assert summary["contains_fit_statistics"] == "false"
    assert summary["covariance_shape"] == "300x300"
    assert summary["cholesky_ready"] == "true"
    assert summary["requires_frozen_theory_vector"] == "true"
    assert float(summary["min_eigenvalue"]) > 0.0
    assert float(summary["condition_number"]) > 1.0
    with (
        ROOT / "data/derived/kids1000_cosebis_covariance_inversion_readiness_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 1
    assert rows[0]["current_inversion_executed"] == "false"
    assert rows[0]["inverse_saved"] == "false"


def test_kids1000_cosebis_theory_vector_policy_is_declared_not_computed() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_theory_vector_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert policy["status"] == "KIDS1000_COSEBIS_THEORY_VECTOR_POLICY_DECLARED_NOT_COMPUTED"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert policy["current_theory_vector_computed"] == "false"
    assert policy["expected_theory_vector_rows"] == "300"
    assert "W_WEB_ANISOTROPY" in policy["active_channels"]
    assert "W_PATH_PROJECTION" in policy["active_channels"]
    assert "W_TIME_READOUT" in policy["disabled_channels"]
    assert "kids_data_vector_values" in policy["forbidden_inputs"]
    assert "posthoc_theory_vector_choice" in policy["forbidden_inputs"]
    with (
        ROOT / "data/derived/kids1000_cosebis_theory_vector_readiness_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "KIDS1000_COSEBIS_THEORY_VECTOR_READINESS_BUILT_SOURCE_FROZEN_NOT_SCORED"
    assert summary["endpoint_scoring_allowed"] == "false"
    assert summary["current_theory_vector_computed"] == "true"
    assert summary["contains_theory_vector"] == "true"
    assert summary["contains_predictions"] == "false"
    assert summary["contains_residuals"] == "false"
    assert summary["contains_fit_statistics"] == "false"
    assert summary["uses_kids_data_vector_values"] == "false"
    assert summary["uses_posterior_chains"] == "false"
    assert summary["expected_theory_vector_rows"] == "300"
    assert summary["retained_data_vector_rows"] == "300"
    assert summary["n_tomographic_pairs"] == "15"
    assert summary["n_modes_per_pair"] == "20"
    with (
        ROOT / "data/derived/kids1000_cosebis_theory_vector_readiness_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 1
    assert rows[0]["contains_theory_vector"] == "true"
    assert rows[0]["source_frozen_theory_vector_artifact"] == (
        "data/derived/kids1000_cosebis_source_frozen_theory_vector_v1_summary.csv"
    )
    assert rows[0]["uses_kids_data_vector_values"] == "false"


def test_kids1000_cosebis_source_frozen_theory_vector_is_not_scoring() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_source_frozen_theory_vector_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert policy["status"] == "KIDS1000_COSEBIS_SOURCE_FROZEN_THEORY_VECTOR_POLICY_FROZEN_NOT_SCORED"
    assert policy["current_theory_vector_computed"] == "true"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert policy["expected_rows"] == "300"
    assert "mode^(-1/2)" in policy["mode_shape_rule"]
    assert policy["amplitude_policy"] == "unit_amplitude_no_fit_no_residual_calibration"
    for marker in [
        "kids_data_vector_values",
        "lensing_residuals",
        "posthoc_mode_shape_choice",
        "posthoc_amplitude_fit",
    ]:
        assert marker in policy["forbidden_inputs"]

    with (
        ROOT / "data/derived/kids1000_cosebis_source_frozen_theory_vector_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "KIDS1000_COSEBIS_SOURCE_FROZEN_THEORY_VECTOR_BUILT_NOT_SCORED"
    assert summary["theory_rows"] == "300"
    assert summary["theory_vector_computed"] == "true"
    assert summary["contains_theory_vector"] == "true"
    assert summary["contains_predictions"] == "false"
    assert summary["contains_residuals"] == "false"
    assert summary["contains_fit_statistics"] == "false"
    assert summary["uses_kids_data_vector_values"] == "false"
    assert summary["uses_posterior_chains"] == "false"
    assert summary["uses_posthoc_selection"] == "false"
    assert summary["endpoint_scoring_allowed"] == "false"
    assert summary["positive_theory_support"] == "true"
    assert summary["positive_web_claim_allowed"] == "false"
    assert abs(float(summary["mean_mode_shape_weight"]) - 1.0) < 1e-12

    with (
        ROOT / "data/derived/kids1000_cosebis_source_frozen_theory_vector_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 300
    assert len({row["pair_id"] for row in rows}) == 15
    assert len({row["mode"] for row in rows}) == 20
    assert all(float(row["theory_value"]) > 0 for row in rows)
    assert all(row["contains_theory_vector"] == "true" for row in rows)
    assert all(row["contains_prediction"] == "false" for row in rows)
    assert all(row["contains_residual"] == "false" for row in rows)
    assert all(row["contains_fit_statistic"] == "false" for row in rows)
    assert all(row["uses_kids_data_vector_values"] == "false" for row in rows)
    assert all(row["uses_posterior_chains"] == "false" for row in rows)
    assert all(row["uses_posthoc_selection"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert all(float(row["w_web_contribution"]) == 0 for row in rows)


def test_kids1000_cosebis_theory_vector_template_is_row_index_only() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_theory_vector_template_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert policy["status"] == "KIDS1000_COSEBIS_THEORY_VECTOR_TEMPLATE_POLICY_FROZEN_NOT_COMPUTED"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert policy["current_theory_values_computed"] == "false"
    assert policy["expected_rows"] == "300"
    for marker in [
        "kids_data_vector_values",
        "posterior_chains",
        "lensing_residuals",
        "posthoc_theory_vector_choice",
        "posthoc_channel_activation",
    ]:
        assert marker in policy["forbidden_inputs"]
    with (
        ROOT / "data/derived/kids1000_cosebis_theory_vector_template_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "KIDS1000_COSEBIS_THEORY_VECTOR_TEMPLATE_BUILT_NOT_COMPUTED"
    assert summary["template_rows"] == "300"
    assert summary["tomographic_pair_count"] == "15"
    assert summary["modes_per_pair"] == "20"
    assert summary["theory_values_computed"] == "false"
    assert summary["contains_theory_vector"] == "false"
    assert summary["contains_predictions"] == "false"
    assert summary["contains_residuals"] == "false"
    assert summary["contains_fit_statistics"] == "false"
    assert summary["uses_kids_data_vector_values"] == "false"
    assert summary["uses_posterior_chains"] == "false"
    assert summary["endpoint_scoring_allowed"] == "false"
    with (ROOT / "data/derived/kids1000_cosebis_theory_vector_template_v1.csv").open(
        newline=""
    ) as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 300
    assert [row["row_index_zero_based"] for row in rows] == [str(i) for i in range(300)]
    assert [row["row_index_one_based"] for row in rows] == [str(i) for i in range(1, 301)]
    assert len({row["pair_id"] for row in rows}) == 15
    assert all(row["theory_value_status"] == "template_pending_source_frozen_mapping" for row in rows)
    assert all(row["theory_value"] == "" for row in rows)
    assert all(row["w_web_contribution"] == "" for row in rows)
    assert all(row["w_path_contribution"] == "" for row in rows)
    assert all(row["baseline_contribution"] == "" for row in rows)
    assert all(row["template_row_only"] == "true" for row in rows)
    assert all(row["contains_theory_value"] == "false" for row in rows)
    assert all(row["contains_prediction"] == "false" for row in rows)
    assert all(row["contains_residual"] == "false" for row in rows)
    assert all(row["uses_kids_data_vector_values"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)


def test_kids1000_cosebis_mapping_template_join_contract_is_schema_only() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_mapping_template_join_contract_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert policy["status"] == "KIDS1000_COSEBIS_MAPPING_TEMPLATE_JOIN_CONTRACT_POLICY_FROZEN_NOT_COMPUTED"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert policy["current_join_values_computed"] == "false"
    assert policy["current_theory_values_computed"] == "false"
    assert policy["current_mapping_vector_computed"] == "false"
    assert policy["expected_rows"] == "300"
    assert policy["join_key"] == "row_index_zero_based"
    for marker in [
        "kids_data_vector_values",
        "posterior_chains",
        "lensing_residuals",
        "fit_improvement_flags",
        "posthoc_mapping_row_selection",
        "posthoc_channel_activation",
        "posthoc_sky_direction_selection",
        "posthoc_web_environment_labels",
        "posthoc_path_projection_labels",
    ]:
        assert marker in policy["forbidden_inputs"]
    with (
        ROOT / "data/derived/kids1000_cosebis_mapping_template_join_contract_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "KIDS1000_COSEBIS_MAPPING_TEMPLATE_JOIN_CONTRACT_BUILT_NOT_COMPUTED"
    assert summary["join_rows"] == "300"
    assert summary["join_key"] == "row_index_zero_based"
    assert summary["join_contract_built"] == "true"
    assert summary["join_values_computed"] == "false"
    assert summary["mapping_vector_computed"] == "false"
    assert summary["theory_values_computed"] == "false"
    assert summary["contains_theory_vector"] == "false"
    assert summary["contains_predictions"] == "false"
    assert summary["contains_residuals"] == "false"
    assert summary["contains_fit_statistics"] == "false"
    assert summary["uses_kids_data_vector_values"] == "false"
    assert summary["uses_posterior_chains"] == "false"
    assert summary["uses_posthoc_selection"] == "false"
    assert summary["endpoint_scoring_allowed"] == "false"
    with (
        ROOT / "data/derived/kids1000_cosebis_mapping_template_join_contract_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 300
    assert [row["row_index_zero_based"] for row in rows] == [str(i) for i in range(300)]
    assert len({row["pair_id"] for row in rows}) == 15
    assert all(row["join_key"] == "row_index_zero_based" for row in rows)
    assert all(row["join_contract_row_only"] == "true" for row in rows)
    for field in [
        "source_frozen_w_web_basis",
        "source_frozen_w_path_basis",
        "source_frozen_baseline_basis",
        "source_frozen_channel_activation",
        "source_frozen_mapping_provenance",
    ]:
        assert all(row[field] == "" for row in rows)
    assert all(row["join_values_computed"] == "false" for row in rows)
    assert all(row["mapping_vector_computed"] == "false" for row in rows)
    assert all(row["theory_values_computed"] == "false" for row in rows)
    assert all(row["contains_theory_vector"] == "false" for row in rows)
    assert all(row["contains_prediction"] == "false" for row in rows)
    assert all(row["contains_residual"] == "false" for row in rows)
    assert all(row["uses_posthoc_selection"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)


def test_kids1000_cosebis_source_frozen_mapping_vector_is_source_side_only() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_source_frozen_mapping_vector_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert policy["status"] == "KIDS1000_COSEBIS_SOURCE_FROZEN_MAPPING_VECTOR_POLICY_FROZEN_NOT_SCORED"
    assert policy["current_mapping_vector_computed"] == "true"
    assert policy["current_theory_vector_computed"] == "false"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert policy["expected_target_rows"] == "300"
    assert policy["expected_domain_rows"] == "58800"
    assert (
        policy["mapping_rule"]
        == "source_frozen_row_tile_average_of_unit_mean_fde_times_unit_mean_redshift_pair_factor"
    )
    for marker in [
        "kids_data_vector_values",
        "posterior_chains",
        "lensing_residuals",
        "fit_improvement_flags",
        "posthoc_mapping_rule_choice",
    ]:
        assert marker in policy["forbidden_inputs"]

    with (
        ROOT / "data/derived/kids1000_cosebis_source_frozen_mapping_vector_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "KIDS1000_COSEBIS_SOURCE_FROZEN_MAPPING_VECTOR_BUILT_NOT_THEORY_NOT_SCORED"
    assert summary["target_rows"] == "300"
    assert summary["domain_rows"] == "58800"
    assert summary["mapping_vector_computed"] == "true"
    assert summary["path_mapping_computed"] == "true"
    assert summary["contains_mapping_vector"] == "true"
    assert summary["contains_theory_vector"] == "false"
    assert summary["contains_predictions"] == "false"
    assert summary["contains_residuals"] == "false"
    assert summary["contains_fit_statistics"] == "false"
    assert summary["uses_kids_data_vector_values"] == "false"
    assert summary["uses_posterior_chains"] == "false"
    assert summary["uses_posthoc_weight_selection"] == "false"
    assert summary["uses_posthoc_tile_selection"] == "false"
    assert summary["uses_posthoc_sky_direction_selection"] == "false"
    assert summary["uses_posthoc_web_environment_labels"] == "false"
    assert summary["uses_posthoc_path_projection_labels"] == "false"
    assert summary["endpoint_scoring_allowed"] == "false"
    assert summary["unique_mapping_value_count_rounded_1e_minus_12"] == "15"
    assert summary["positive_mapping_support"] == "true"
    assert summary["positive_web_claim_allowed"] == "false"
    assert summary["mode_shape_generated"] == "false"
    assert summary["limitation"] == (
        "source_frozen_mapping_vector_has_pair_redshift_and_path_variation_but_no_mode_shape_or_theory_vector"
    )

    with (
        ROOT / "data/derived/kids1000_cosebis_source_frozen_mapping_vector_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 300
    assert len({row["source_frozen_mapping_value"] for row in rows}) == 15
    assert all(float(row["source_frozen_mapping_value"]) > 0 for row in rows)
    assert all(row["w_web_basis"] == "0.000000000000e+00" for row in rows)
    assert all(row["contains_mapping_vector"] == "true" for row in rows)
    assert all(row["contains_theory_vector"] == "false" for row in rows)
    assert all(row["contains_predictions"] == "false" for row in rows)
    assert all(row["contains_residuals"] == "false" for row in rows)
    assert all(row["contains_fit_statistics"] == "false" for row in rows)
    assert all(row["uses_kids_data_vector_values"] == "false" for row in rows)
    assert all(row["uses_posthoc_weight_selection"] == "false" for row in rows)
    assert all(row["uses_posthoc_tile_selection"] == "false" for row in rows)
    assert all(row["uses_posthoc_sky_direction_selection"] == "false" for row in rows)
    assert all(row["uses_posthoc_web_environment_labels"] == "false" for row in rows)
    assert all(row["uses_posthoc_path_projection_labels"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)

    with (
        ROOT / "data/derived/kids1000_cosebis_source_frozen_mapping_domain_weights_v1.csv"
    ).open(newline="") as f:
        domain = list(csv.DictReader(f))
    assert len(domain) == 58800
    assert len({row["tile_index_zero_based"] for row in domain}) == 196
    assert all(row["contains_mapping_vector"] == "true" for row in domain)
    assert all(row["contains_theory_vector"] == "false" for row in domain)
    assert all(row["contains_predictions"] == "false" for row in domain)
    assert all(row["contains_residuals"] == "false" for row in domain)
    assert all(row["uses_kids_data_vector_values"] == "false" for row in domain)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in domain)


def test_kids1000_cosebis_web_path_mapping_policy_is_source_mapping_available_not_scoring() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_web_path_mapping_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert policy["status"] == "KIDS1000_COSEBIS_WEB_PATH_MAPPING_POLICY_SOURCE_MAPPING_AVAILABLE_NOT_SCORED"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert policy["current_mapping_computed"] == "true"
    assert policy["expected_target_rows"] == "300"
    assert "W_WEB_ANISOTROPY" in policy["active_channels"]
    assert "W_PATH_PROJECTION" in policy["active_channels"]
    for marker in [
        "source_frozen_web_environment_catalog",
        "source_frozen_lensing_path_mask_or_depth_map",
        "source_frozen_redshift_kernel_mapping",
        "source_frozen_null_sky_rotation_or_pair_shuffle",
    ]:
        assert marker in policy["required_future_source_products"]
    for marker in [
        "kids_data_vector_values",
        "posthoc_sky_direction_selection",
        "posthoc_web_environment_labels",
    ]:
        assert marker in policy["forbidden_inputs"]
    with (
        ROOT / "data/derived/kids1000_cosebis_web_path_mapping_readiness_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "KIDS1000_COSEBIS_WEB_PATH_MAPPING_READINESS_BUILT_NOT_COMPUTED"
    assert summary["endpoint_scoring_allowed"] == "false"
    assert summary["current_mapping_computed"] == "true"
    assert summary["contains_mapping_vector"] == "true"
    assert summary["contains_theory_vector"] == "false"
    assert summary["contains_predictions"] == "false"
    assert summary["contains_residuals"] == "false"
    assert summary["contains_fit_statistics"] == "false"
    assert summary["uses_kids_data_vector_values"] == "false"
    assert summary["uses_posterior_chains"] == "false"
    assert summary["uses_posthoc_sky_direction_selection"] == "false"
    assert summary["target_rows"] == "300"
    assert summary["n_tomographic_pairs"] == "15"
    assert summary["n_modes_per_pair"] == "20"
    assert summary["required_future_source_product_count"] == "4"
    assert summary["mapping_vector_artifact"] == (
        "data/derived/kids1000_cosebis_source_frozen_mapping_vector_v1_summary.csv"
    )
    assert summary["mapping_unique_value_count"] == "15"
    with (
        ROOT / "data/derived/kids1000_cosebis_web_path_mapping_readiness_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 1
    assert rows[0]["contains_mapping_vector"] == "true"
    assert rows[0]["uses_posthoc_sky_direction_selection"] == "false"


def test_kids1000_cosebis_redshift_kernel_inventory_is_source_side_only() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_redshift_kernel_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert policy["status"] == "KIDS1000_COSEBIS_REDSHIFT_KERNEL_POLICY_FROZEN_NOT_SCORED"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert policy["selected_hdu_redshift_distribution"] == "NZ_SOURCE"
    assert policy["expected_nz_rows"] == "119"
    assert policy["expected_source_bins"] == "5"
    assert policy["current_kernel_mapping_computed"] == "true"
    for marker in [
        "kids_data_vector_values",
        "lensing_residuals",
        "posthoc_kernel_reweighting",
        "kids_posterior_parameter_selection",
    ]:
        assert marker in policy["forbidden_inputs"]
    with (
        ROOT / "data/derived/kids1000_cosebis_redshift_kernel_inventory_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "KIDS1000_COSEBIS_REDSHIFT_KERNEL_INVENTORY_BUILT_NOT_SCORED"
    assert summary["endpoint_scoring_allowed"] == "false"
    assert summary["kernel_mapping_computed"] == "true"
    assert summary["uses_kids_data_vector_values"] == "false"
    assert summary["uses_residuals"] == "false"
    assert summary["uses_fit_statistics"] == "false"
    assert summary["uses_posterior_chains"] == "false"
    assert summary["contains_predictions"] == "false"
    assert summary["contains_residuals"] == "false"
    assert summary["contains_fit_statistics"] == "false"
    assert summary["n_source_bins"] == "5"
    assert summary["nz_rows"] == "119"
    with (
        ROOT / "data/derived/kids1000_cosebis_redshift_kernel_inventory_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 5
    assert [row["source_bin"] for row in rows] == ["1", "2", "3", "4", "5"]
    mean_z = [float(row["mean_z"]) for row in rows]
    assert mean_z == sorted(mean_z)
    for row in rows:
        assert float(row["area_sum_nz_dz"]) > 0.0
        assert float(row["support_z_min_nonzero"]) >= 0.0
        assert float(row["support_z_max_nonzero"]) > float(row["support_z_min_nonzero"])
        assert row["endpoint_scoring_allowed"] == "false"
        assert row["uses_kids_data_vector_values"] == "false"
        assert row["contains_predictions"] == "false"
        assert row["contains_residuals"] == "false"
        assert row["contains_fit_statistics"] == "false"


def test_kids1000_cosebis_path_mask_depth_gap_keeps_path_route_blocked() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_path_mask_depth_gap_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert policy["status"] == "KIDS1000_COSEBIS_PATH_MASK_DEPTH_GAP_DECLARED_EXTERNAL_PRODUCT_REQUIRED"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert policy["current_path_mapping_computed"] == "false"
    assert policy["path_mask_depth_product_available"] == "false"
    assert policy["required_future_source_product"] == "source_frozen_lensing_path_mask_or_depth_map"
    for marker in [
        "posthoc_path_projection_labels",
        "posthoc_sky_direction_selection",
        "kids_data_vector_values",
    ]:
        assert marker in policy["forbidden_inputs"]
    with (
        ROOT / "data/derived/kids1000_cosebis_path_mask_depth_gap_inventory_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "KIDS1000_COSEBIS_PATH_MASK_DEPTH_GAP_BUILT_EXTERNAL_PRODUCT_REQUIRED"
    assert summary["endpoint_scoring_allowed"] == "false"
    assert summary["path_mask_depth_product_available"] == "false"
    assert summary["accepted_path_mask_depth_products"] == "0"
    assert summary["blocker"] == "external_source_frozen_lensing_path_mask_or_depth_map_required"
    assert summary["current_path_mapping_computed"] == "false"
    assert summary["contains_mapping_vector"] == "false"
    assert summary["contains_theory_vector"] == "false"
    assert summary["contains_predictions"] == "false"
    assert summary["contains_residuals"] == "false"
    assert summary["uses_kids_data_vector_values"] == "false"
    assert summary["uses_posthoc_path_selection"] == "false"
    with (
        ROOT / "data/derived/kids1000_cosebis_path_mask_depth_gap_inventory_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert rows
    assert {row["accepted_as_path_mask_depth_product"] for row in rows} == {"false"}
    assert any(row["member_name"].endswith("Read.me") for row in rows)
    assert any(
        row["classification_reason"] == "statistic_fits_filename_token_not_survey_path_map"
        for row in rows
    )
    for row in rows:
        assert row["endpoint_scoring_allowed"] == "false"
        assert row["contains_mapping_vector"] == "false"
        assert row["contains_predictions"] == "false"
        assert row["contains_residuals"] == "false"
        assert row["uses_kids_data_vector_values"] == "false"


def test_kids1000_dr4_path_mask_route_scripts_are_frozen_not_scored() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_dr4_path_mask_route_scripts_v1.csv"
    ).open(newline="") as f:
        manifest = list(csv.DictReader(f))
    assert len(manifest) == 3
    assert {row["endpoint_allowed"] for row in manifest} == {"false"}
    assert "KIDS_DR41_9BAND_MASK_WGET_SCRIPT" in {row["route_id"] for row in manifest}
    for row in manifest:
        for marker in [
            "posthoc_path_projection_labels",
            "posthoc_sky_direction_selection",
            "kids_data_vector_values",
        ]:
            assert marker in row["forbidden_inputs"]
    with (
        ROOT / "data/derived/kids1000_dr4_path_mask_route_scripts_inventory_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "KIDS_DR4_PATH_MASK_ROUTE_SCRIPTS_FETCHED_FROZEN_NOT_SCORED"
    assert summary["endpoint_scoring_allowed"] == "false"
    assert summary["preferred_route_id"] == "KIDS_DR41_9BAND_MASK_WGET_SCRIPT"
    assert summary["preferred_listed_mask_product_count"] == "196"
    assert summary["mask_products_fetched"] == "false"
    assert summary["path_mapping_computed"] == "false"
    assert summary["contains_mapping_vector"] == "false"
    assert summary["contains_theory_vector"] == "false"
    assert summary["contains_predictions"] == "false"
    assert summary["contains_residuals"] == "false"
    assert summary["uses_kids_data_vector_values"] == "false"
    with (
        ROOT / "data/derived/kids1000_dr4_path_mask_route_scripts_inventory_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 3
    assert {row["route_id"] for row in rows} == {row["route_id"] for row in manifest}
    for row in rows:
        assert row["status"] == "KIDS_DR4_PATH_MASK_ROUTE_SCRIPT_FETCHED_FROZEN"
        assert row["http_status"] == "200"
        assert len(row["sha256"]) == 64
        assert int(row["listed_mask_product_count"]) > 0
        assert row["mask_products_fetched"] == "false"
        assert row["path_mapping_computed"] == "false"
        assert row["contains_predictions"] == "false"
        assert row["contains_residuals"] == "false"
        assert row["uses_kids_data_vector_values"] == "false"
        assert (ROOT / row["local_path"]).exists()


def test_kids1000_dr4_path_mask_route_tile_inventory_is_not_mapping() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_dr4_path_mask_route_tile_inventory_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert policy["status"] == "KIDS_DR4_PATH_MASK_ROUTE_TILE_INVENTORY_POLICY_FROZEN_NOT_SCORED"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert policy["preferred_route_id"] == "KIDS_DR41_9BAND_MASK_WGET_SCRIPT"
    assert policy["expected_tile_count"] == "196"
    assert policy["current_tile_inventory_computed"] == "true"
    assert policy["current_mask_products_fetched"] == "false"
    assert policy["current_path_mapping_computed"] == "false"
    assert policy["current_theory_vector_computed"] == "false"
    for marker in [
        "kids_data_vector_values",
        "posterior_chains",
        "lensing_residuals",
        "fit_improvement_flags",
        "posthoc_path_projection_labels",
        "posthoc_sky_direction_selection",
        "posthoc_tile_selection",
    ]:
        assert marker in policy["forbidden_inputs"]
    with (
        ROOT / "data/derived/kids1000_dr4_path_mask_route_tile_inventory_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "KIDS_DR4_PATH_MASK_ROUTE_TILE_INVENTORY_BUILT_NOT_MAPPED"
    assert summary["tile_count"] == "196"
    assert summary["unique_tile_coordinate_count"] == "196"
    assert summary["duplicate_tile_coordinate_count"] == "0"
    assert summary["mask_products_fetched"] == "false"
    assert summary["mask_pixels_parsed"] == "false"
    assert summary["footprint_polygon_computed"] == "false"
    assert summary["path_mapping_computed"] == "false"
    assert summary["contains_mapping_vector"] == "false"
    assert summary["contains_theory_vector"] == "false"
    assert summary["contains_predictions"] == "false"
    assert summary["contains_residuals"] == "false"
    assert summary["uses_kids_data_vector_values"] == "false"
    with (
        ROOT / "data/derived/kids1000_dr4_path_mask_route_tile_inventory_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 196
    assert rows[0]["tile_ra_deg_filename_proxy"] == "0.0"
    assert rows[0]["tile_dec_deg_filename_proxy"] == "-28.2"
    assert rows[-1]["tile_ra_deg_filename_proxy"] == "5.6"
    assert rows[-1]["tile_dec_deg_filename_proxy"] == "-28.2"
    for row in rows:
        float(row["tile_ra_deg_filename_proxy"])
        float(row["tile_dec_deg_filename_proxy"])
        assert row["tile_coordinate_source"] == "KiDS_mask_filename_token"
        assert row["mask_product_fetched"] == "false"
        assert row["mask_pixels_parsed"] == "false"
        assert row["footprint_polygon_computed"] == "false"
        assert row["path_mapping_computed"] == "false"
        assert row["contains_mapping_vector"] == "false"
        assert row["contains_theory_vector"] == "false"
        assert row["uses_kids_data_vector_values"] == "false"


def test_kids1000_dr4_path_mask_head_sample_is_metadata_only() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_dr4_path_mask_head_sample_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert policy["status"] == "KIDS_DR4_PATH_MASK_HEAD_SAMPLE_POLICY_FROZEN_NOT_SCORED"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert policy["preferred_route_id"] == "KIDS_DR41_9BAND_MASK_WGET_SCRIPT"
    assert policy["sample_rule"] == "first_middle_last_from_preferred_route"
    assert policy["sample_indices_zero_based"] == "0;98;195"
    assert policy["current_mask_products_fetched"] == "false"
    for marker in [
        "posthoc_mask_subset_selection",
        "posthoc_path_projection_labels",
        "kids_data_vector_values",
    ]:
        assert marker in policy["forbidden_inputs"]
    with (
        ROOT / "data/derived/kids1000_dr4_path_mask_head_sample_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "KIDS_DR4_PATH_MASK_HEAD_SAMPLE_CHECKED_NOT_FETCHED"
    assert summary["endpoint_scoring_allowed"] == "false"
    assert summary["sample_count"] == "3"
    assert summary["http_200_count"] == "3"
    assert int(summary["min_content_length"]) > 0
    assert summary["mask_products_fetched"] == "false"
    assert summary["path_mapping_computed"] == "false"
    assert summary["contains_mapping_vector"] == "false"
    assert summary["contains_theory_vector"] == "false"
    assert summary["contains_predictions"] == "false"
    assert summary["contains_residuals"] == "false"
    assert summary["uses_kids_data_vector_values"] == "false"
    with (
        ROOT / "data/derived/kids1000_dr4_path_mask_head_sample_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert [row["sample_index_zero_based"] for row in rows] == ["0", "98", "195"]
    for row in rows:
        assert row["head_status"] == "HEAD_CHECKED_MASK_NOT_FETCHED"
        assert row["http_status"] == "200"
        assert int(row["content_length"]) > 0
        assert "fits" in row["content_type"].lower()
        assert row["mask_product_fetched"] == "false"
        assert row["path_mapping_computed"] == "false"
        assert row["contains_predictions"] == "false"
        assert row["contains_residuals"] == "false"
        assert row["uses_kids_data_vector_values"] == "false"


def test_kids1000_dr4_path_mask_subset_is_inventory_not_mapping() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_dr4_path_mask_subset_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert policy["status"] == "KIDS_DR4_PATH_MASK_SUBSET_POLICY_FROZEN_NOT_SCORED"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert policy["subset_rule"] == "promote_head_sample_first_middle_last_to_download_subset"
    assert policy["subset_indices_zero_based"] == "0;98;195"
    assert policy["expected_subset_count"] == "3"
    assert policy["current_mask_products_fetched"] == "true"
    assert policy["current_mask_pixels_parsed"] == "true"
    assert policy["current_path_mapping_computed"] == "false"
    for marker in [
        "posthoc_mask_subset_selection",
        "posthoc_path_projection_labels",
        "kids_data_vector_values",
    ]:
        assert marker in policy["forbidden_inputs"]
    with (
        ROOT / "data/derived/kids1000_dr4_path_mask_subset_inventory_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "KIDS_DR4_PATH_MASK_SUBSET_FETCHED_INVENTORIED_NOT_SCORED"
    assert summary["endpoint_scoring_allowed"] == "false"
    assert summary["subset_count"] == "3"
    assert int(summary["total_byte_count"]) > 0
    assert int(summary["total_pixels"]) == 1323000000
    assert summary["mask_products_fetched"] == "true"
    assert summary["mask_pixels_parsed"] == "true"
    assert summary["path_mapping_computed"] == "false"
    assert summary["contains_mapping_vector"] == "false"
    assert summary["contains_theory_vector"] == "false"
    assert summary["contains_predictions"] == "false"
    assert summary["contains_residuals"] == "false"
    assert summary["uses_kids_data_vector_values"] == "false"
    with (
        ROOT / "data/derived/kids1000_dr4_path_mask_subset_inventory_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert [row["sample_index_zero_based"] for row in rows] == ["0", "98", "195"]
    assert len(rows) == 3
    for row in rows:
        path = ROOT / row["local_path"]
        assert path.exists(), row["local_path"]
        assert row["http_status"] == "200"
        assert len(row["sha256"]) == 64
        assert int(row["byte_count"]) > 0
        assert row["primary_shape"] == "21000x21000"
        assert int(row["n_pixels"]) == 441000000
        assert row["mask_product_fetched"] == "true"
        assert row["mask_pixels_parsed"] == "true"
        assert row["path_mapping_computed"] == "false"
        assert row["contains_mapping_vector"] == "false"
        assert row["contains_predictions"] == "false"
        assert row["contains_residuals"] == "false"
        assert row["uses_kids_data_vector_values"] == "false"
        assert float(row["finite_fraction"]) > 0.0
        assert float(row["nonzero_finite_fraction"]) > 0.0


def test_kids1000_dr4_path_mask_observable_shell_is_source_only() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_dr4_path_mask_observable_shell_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert policy["status"] == "KIDS_DR4_PATH_MASK_OBSERVABLE_SHELL_POLICY_FROZEN_NOT_SCORED"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert policy["observable_rule"] == "filename_tile_coordinate_plus_centered_zero_fraction_shell"
    assert policy["expected_subset_count"] == "3"
    assert policy["current_source_observable_shell_computed"] == "true"
    assert policy["current_path_mapping_computed"] == "false"
    assert policy["current_theory_vector_computed"] == "false"
    assert policy["current_endpoint_scores_computed"] == "false"
    for marker in [
        "kids_data_vector_values",
        "posterior_chains",
        "lensing_residuals",
        "fit_improvement_flags",
        "posthoc_path_projection_labels",
        "posthoc_mask_subset_selection",
    ]:
        assert marker in policy["forbidden_inputs"]
    with (
        ROOT / "data/derived/kids1000_dr4_path_mask_observable_shell_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "KIDS_DR4_PATH_MASK_OBSERVABLE_SHELL_BUILT_SOURCE_ONLY_NOT_SCORED"
    assert summary["subset_count"] == "3"
    assert summary["endpoint_scoring_allowed"] == "false"
    assert summary["source_observable_shell_computed"] == "true"
    assert summary["path_mapping_computed"] == "false"
    assert summary["contains_mapping_vector"] == "false"
    assert summary["contains_theory_vector"] == "false"
    assert summary["contains_predictions"] == "false"
    assert summary["contains_residuals"] == "false"
    assert summary["uses_kids_data_vector_values"] == "false"
    assert float(summary["min_source_mask_shell_value"]) < 0.0
    assert float(summary["max_source_mask_shell_value"]) > 0.0
    with (
        ROOT / "data/derived/kids1000_dr4_path_mask_observable_shell_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert [row["sample_index_zero_based"] for row in rows] == ["0", "98", "195"]
    assert [(row["tile_ra_deg_filename_proxy"], row["tile_dec_deg_filename_proxy"]) for row in rows] == [
        ("0.0", "-28.2"),
        ("206.0", "1.5"),
        ("5.6", "-28.2"),
    ]
    shell_values = [float(row["source_mask_shell_value"]) for row in rows]
    assert min(shell_values) < 0.0
    assert max(shell_values) > 0.0
    assert all(abs(value) <= 1.0 for value in shell_values)
    for row in rows:
        assert row["source_shell_scope"] == "three_mask_subset_only"
        assert row["tile_coordinate_source"] == "KiDS_mask_filename_token"
        assert row["mask_value_semantics_interpreted"] == "false"
        assert row["source_observable_shell_computed"] == "true"
        assert row["path_mapping_computed"] == "false"
        assert row["contains_mapping_vector"] == "false"
        assert row["contains_theory_vector"] == "false"
        assert row["contains_predictions"] == "false"
        assert row["contains_residuals"] == "false"
        assert row["uses_kids_data_vector_values"] == "false"
        assert 0.0 <= float(row["mask_zero_finite_fraction_proxy"]) <= 1.0


def test_kids1000_cosebis_path_mapping_design_skeleton_is_not_mapping() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_path_mapping_design_skeleton_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert policy["status"] == "KIDS1000_COSEBIS_PATH_MAPPING_DESIGN_SKELETON_POLICY_FROZEN_NOT_SCORED"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert policy["expected_target_rows"] == "300"
    assert policy["route_tile_count"] == "196"
    assert policy["current_design_skeleton_computed"] == "true"
    assert policy["current_path_weights_computed"] == "false"
    assert policy["current_path_mapping_computed"] == "false"
    assert policy["current_theory_vector_computed"] == "false"
    for marker in [
        "kids_data_vector_values",
        "posterior_chains",
        "lensing_residuals",
        "fit_improvement_flags",
        "posthoc_path_projection_labels",
        "posthoc_sky_direction_selection",
        "posthoc_tile_selection",
    ]:
        assert marker in policy["forbidden_inputs"]
    with (
        ROOT / "data/derived/kids1000_cosebis_path_mapping_design_skeleton_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "KIDS1000_COSEBIS_PATH_MAPPING_DESIGN_SKELETON_BUILT_NOT_MAPPED"
    assert summary["target_rows"] == "300"
    assert summary["tomographic_pair_count"] == "15"
    assert summary["mode_count_per_pair"] == "20"
    assert summary["route_tile_count"] == "196"
    assert summary["endpoint_scoring_allowed"] == "false"
    assert summary["path_weights_computed"] == "false"
    assert summary["path_mapping_computed"] == "false"
    assert summary["contains_mapping_vector"] == "false"
    assert summary["contains_theory_vector"] == "false"
    assert summary["contains_predictions"] == "false"
    assert summary["contains_residuals"] == "false"
    assert summary["uses_kids_data_vector_values"] == "false"
    with (
        ROOT / "data/derived/kids1000_cosebis_path_mapping_design_skeleton_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 300
    assert [row["target_row_index_zero_based"] for row in rows] == [str(i) for i in range(300)]
    assert rows[0]["pair_id"] == "1-1"
    assert rows[0]["mode"] == "1"
    assert rows[-1]["pair_id"] == "5-5"
    assert rows[-1]["mode"] == "20"
    for row in rows:
        assert row["preferred_route_tile_count"] == "196"
        assert row["design_skeleton_computed"] == "true"
        assert row["path_weights_computed"] == "false"
        assert row["path_mapping_computed"] == "false"
        assert row["contains_mapping_vector"] == "false"
        assert row["contains_theory_vector"] == "false"
        assert row["uses_kids_data_vector_values"] == "false"
        float(row["bin1_mean_z"])
        float(row["bin2_mean_z"])


def test_kids1000_cosebis_path_mapping_domain_skeleton_is_not_mapping() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_path_mapping_domain_skeleton_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert policy["status"] == "KIDS1000_COSEBIS_PATH_MAPPING_DOMAIN_SKELETON_POLICY_FROZEN_NOT_SCORED"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert policy["expected_target_rows"] == "300"
    assert policy["expected_tile_count"] == "196"
    assert policy["expected_domain_rows"] == "58800"
    assert policy["current_domain_skeleton_computed"] == "true"
    assert policy["current_tile_weights_computed"] == "false"
    assert policy["current_path_mapping_computed"] == "false"
    assert policy["current_theory_vector_computed"] == "false"
    for marker in [
        "kids_data_vector_values",
        "posterior_chains",
        "lensing_residuals",
        "fit_improvement_flags",
        "posthoc_path_projection_labels",
        "posthoc_sky_direction_selection",
        "posthoc_tile_selection",
    ]:
        assert marker in policy["forbidden_inputs"]
    with (
        ROOT / "data/derived/kids1000_cosebis_path_mapping_domain_skeleton_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "KIDS1000_COSEBIS_PATH_MAPPING_DOMAIN_SKELETON_BUILT_NOT_MAPPED"
    assert summary["target_rows"] == "300"
    assert summary["tile_count"] == "196"
    assert summary["domain_rows"] == "58800"
    assert summary["endpoint_scoring_allowed"] == "false"
    assert summary["tile_weights_computed"] == "false"
    assert summary["footprint_overlap_computed"] == "false"
    assert summary["path_mapping_computed"] == "false"
    assert summary["contains_mapping_vector"] == "false"
    assert summary["contains_theory_vector"] == "false"
    assert summary["contains_predictions"] == "false"
    assert summary["contains_residuals"] == "false"
    assert summary["uses_kids_data_vector_values"] == "false"
    with (
        ROOT / "data/derived/kids1000_cosebis_path_mapping_domain_skeleton_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 58800
    assert rows[0]["target_row_index_zero_based"] == "0"
    assert rows[0]["tile_index_zero_based"] == "0"
    assert rows[-1]["target_row_index_zero_based"] == "299"
    assert rows[-1]["tile_index_zero_based"] == "195"
    assert len({row["target_row_index_zero_based"] for row in rows}) == 300
    assert len({row["tile_index_zero_based"] for row in rows}) == 196
    for row in (rows[0], rows[195], rows[196], rows[-1]):
        assert row["domain_skeleton_computed"] == "true"
        assert row["tile_weight_computed"] == "false"
        assert row["footprint_overlap_computed"] == "false"
        assert row["path_weight_computed"] == "false"
        assert row["web_environment_label_computed"] == "false"
        assert row["path_mapping_computed"] == "false"
        assert row["contains_mapping_vector"] == "false"
        assert row["contains_theory_vector"] == "false"
        assert row["uses_kids_data_vector_values"] == "false"
        float(row["tile_ra_deg_filename_proxy"])
        float(row["tile_dec_deg_filename_proxy"])


def test_kids1000_cosebis_path_weight_construction_rule_is_source_computable_not_mapping() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_path_weight_construction_rule_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert policy["status"] == "KIDS1000_COSEBIS_PATH_WEIGHT_CONSTRUCTION_RULE_DECLARED_NOT_COMPUTED"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert policy["current_weight_rule_declared"] == "true"
    assert policy["current_tile_weights_computed"] == "false"
    assert policy["current_path_mapping_computed"] == "false"
    assert policy["current_theory_vector_computed"] == "false"
    assert "N_pair" in policy["symbolic_factorization"]
    assert "E_web" in policy["symbolic_factorization"]
    for marker in [
        "kids_data_vector_values",
        "posterior_chains",
        "lensing_residuals",
        "fit_improvement_flags",
        "posthoc_path_projection_labels",
        "posthoc_sky_direction_selection",
        "posthoc_tile_selection",
        "posthoc_weight_selection",
    ]:
        assert marker in policy["forbidden_inputs"]
    with (
        ROOT / "data/derived/kids1000_cosebis_path_weight_construction_rule_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "KIDS1000_COSEBIS_PATH_WEIGHT_CONSTRUCTION_RULE_BUILT_NOT_COMPUTED"
    assert summary["factor_count"] == "7"
    assert summary["available_factor_count"] == "6"
    assert summary["available_uniform_not_promotable_factor_count"] == "1"
    assert summary["available_non_degenerate_factor_count"] == "2"
    assert summary["partial_available_factor_count"] == "0"
    assert summary["missing_factor_count"] == "0"
    assert summary["declared_not_computed_factor_count"] == "0"
    assert summary["declared_not_executed_factor_count"] == "1"
    assert summary["domain_rows"] == "58800"
    assert summary["path_weight_rule_computable"] == "true"
    assert summary["tile_weights_computed"] == "false"
    assert summary["path_mapping_computed"] == "false"
    assert summary["contains_mapping_vector"] == "false"
    assert summary["contains_theory_vector"] == "false"
    assert summary["contains_predictions"] == "false"
    assert summary["contains_residuals"] == "false"
    with (
        ROOT / "data/derived/kids1000_cosebis_path_weight_construction_rule_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    by_factor = {row["factor_id"]: row for row in rows}
    assert by_factor["N_pair"]["source_state"] == "available_for_future_rule"
    assert by_factor["T_tile"]["source_state"] == "available_for_future_rule"
    assert by_factor["F_overlap"]["source_state"] == "available_non_degenerate_full_route_pixel_fraction"
    assert by_factor["F_overlap"]["source_count"] == "196"
    assert by_factor["D_path"]["source_state"] == "available_non_degenerate_full_route_mask_load_proxy"
    assert by_factor["D_path"]["source_count"] == "196"
    assert by_factor["D_path"]["numeric_factor_computed"] == "true"
    assert by_factor["E_web"]["source_state"] == "available_uniform_null_web_control"
    assert by_factor["E_web"]["source_count"] == "196"
    assert by_factor["E_web"]["numeric_factor_computed"] == "true"
    assert by_factor["C_norm"]["source_state"] == "available_source_side_unit_mean_normalization"
    assert by_factor["C_norm"]["source_count"] == "58800"
    assert by_factor["C_norm"]["numeric_factor_computed"] == "true"
    assert by_factor["null_controls"]["source_state"] == "declared_not_executed"
    for row in rows:
        assert row["tile_weights_computed"] == "false"
        assert row["path_mapping_computed"] == "false"
        assert row["contains_mapping_vector"] == "false"
        assert row["contains_theory_vector"] == "false"
        assert row["uses_kids_data_vector_values"] == "false"
        assert row["endpoint_scoring_allowed"] == "false"


def test_kids1000_cosebis_path_factor_acquisition_plan_is_not_fetching_or_scoring() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_path_factor_acquisition_plan_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert policy["status"] == "KIDS1000_COSEBIS_PATH_FACTOR_ACQUISITION_PLAN_DECLARED_NOT_FETCHED"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert policy["current_plan_declared"] == "true"
    assert policy["current_external_products_fetched"] == "false"
    assert policy["current_path_mapping_computed"] == "false"
    assert policy["current_theory_vector_computed"] == "false"
    for marker in [
        "kids_data_vector_values",
        "posterior_chains",
        "lensing_residuals",
        "fit_improvement_flags",
        "posthoc_path_projection_labels",
        "posthoc_sky_direction_selection",
        "posthoc_tile_selection",
        "posthoc_weight_selection",
    ]:
        assert marker in policy["forbidden_inputs"]
    with (
        ROOT / "data/derived/kids1000_cosebis_path_factor_acquisition_plan_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "KIDS1000_COSEBIS_PATH_FACTOR_ACQUISITION_PLAN_BUILT_NOT_FETCHED"
    assert summary["requirement_count"] == "7"
    assert summary["blocking_requirement_count"] == "0"
    assert summary["nonblocking_requirement_count"] == "7"
    assert summary["external_products_fetched"] == "false"
    assert summary["numeric_factors_computed"] == "false"
    assert summary["path_mapping_computed"] == "false"
    assert summary["contains_mapping_vector"] == "false"
    assert summary["contains_theory_vector"] == "false"
    assert summary["contains_predictions"] == "false"
    assert summary["contains_residuals"] == "false"
    with (
        ROOT / "data/derived/kids1000_cosebis_path_factor_acquisition_plan_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    by_req = {row["requirement_id"]: row for row in rows}
    assert by_req["REQ_F_OVERLAP_SOURCE"]["blocks_weight_computation"] == "false"
    assert by_req["REQ_F_OVERLAP_SOURCE"]["current_state"] == "available_non_degenerate_full_route_pixel_fraction"
    assert by_req["REQ_D_PATH_SOURCE"]["blocks_weight_computation"] == "false"
    assert (
        by_req["REQ_D_PATH_SOURCE"]["current_state"]
        == "available_non_degenerate_full_route_mask_load_proxy"
    )
    assert by_req["REQ_E_WEB_SOURCE"]["blocks_weight_computation"] == "false"
    assert by_req["REQ_E_WEB_SOURCE"]["current_state"] == "available_uniform_null_web_control"
    assert by_req["REQ_C_NORM_RULE"]["blocks_weight_computation"] == "false"
    assert by_req["REQ_C_NORM_RULE"]["current_state"] == "available_source_side_unit_mean_normalization"
    assert by_req["REQ_N_PAIR_LOCK"]["blocks_weight_computation"] == "false"
    assert by_req["REQ_T_TILE_LOCK"]["blocks_weight_computation"] == "false"
    assert by_req["REQ_NULL_CONTROLS_EXECUTION"]["blocks_weight_computation"] == "false"
    for row in rows:
        assert row["external_products_fetched"] == "false"
        assert row["numeric_factor_computed"] == "false"
        assert row["path_mapping_computed"] == "false"
        assert row["contains_mapping_vector"] == "false"
        assert row["contains_theory_vector"] == "false"
        assert row["uses_kids_data_vector_values"] == "false"
        assert row["endpoint_scoring_allowed"] == "false"


def test_kids1000_cosebis_path_source_product_route_manifest_is_not_fetching_or_scoring() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_path_source_product_route_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert policy["status"] == "KIDS1000_COSEBIS_PATH_SOURCE_PRODUCT_ROUTE_POLICY_DECLARED_NOT_FETCHED"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert policy["current_route_manifest_declared"] == "true"
    assert policy["current_external_products_fetched"] == "false"
    assert policy["current_path_mapping_computed"] == "false"
    assert policy["current_theory_vector_computed"] == "false"
    for marker in [
        "kids_data_vector_values",
        "posterior_chains",
        "lensing_residuals",
        "fit_improvement_flags",
        "posthoc_path_projection_labels",
        "posthoc_sky_direction_selection",
        "posthoc_tile_selection",
        "posthoc_weight_selection",
    ]:
        assert marker in policy["forbidden_inputs"]
    with (
        ROOT / "data/derived/kids1000_cosebis_path_source_product_route_manifest_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "KIDS1000_COSEBIS_PATH_SOURCE_PRODUCT_ROUTE_MANIFEST_BUILT_NOT_FETCHED"
    assert summary["route_count"] == "10"
    assert summary["declared_not_acquired_route_count"] == "1"
    assert summary["already_supported_route_count"] == "6"
    assert summary["alternative_not_needed_route_count"] == "2"
    assert summary["declared_not_computed_route_count"] == "0"
    assert summary["declared_not_executed_route_count"] == "1"
    assert summary["blocker_resolving_candidate_count"] == "0"
    assert summary["control_or_lock_candidate_count"] == "10"
    assert summary["external_products_fetched"] == "false"
    assert summary["numeric_factors_computed"] == "false"
    assert summary["path_mapping_computed"] == "false"
    assert summary["contains_mapping_vector"] == "false"
    assert summary["contains_theory_vector"] == "false"
    assert summary["contains_predictions"] == "false"
    assert summary["contains_residuals"] == "false"
    with (
        ROOT / "data/derived/kids1000_cosebis_path_source_product_route_manifest_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    by_route = {row["route_id"]: row for row in rows}
    assert by_route["ROUTE_F_OVERLAP_OFFICIAL_FOOTPRINT_GEOMETRY"]["may_resolve_blocker"] == "false"
    assert by_route["ROUTE_F_OVERLAP_PIXEL_MASK_DERIVED"]["may_resolve_blocker"] == "false"
    assert by_route["ROUTE_D_PATH_FULL_MASK_DEPTH_PRODUCTS"]["may_resolve_blocker"] == "false"
    assert by_route["ROUTE_E_WEB_EXTERNAL_ENVIRONMENT_CATALOG"]["may_resolve_blocker"] == "false"
    assert by_route["ROUTE_C_NORM_SOURCE_NORMALIZATION_PROTOCOL"]["may_resolve_blocker"] == "false"
    assert by_route["ROUTE_C_NORM_SOURCE_NORMALIZATION_PROTOCOL"]["route_status"] == "already_source_supported_no_fetch"
    assert by_route["ROUTE_D_PATH_DOCUMENTED_SUBSET_CONTROL"]["may_resolve_blocker"] == "false"
    assert by_route["ROUTE_E_WEB_NULL_ABSENT_CONTROL"]["may_resolve_blocker"] == "false"
    assert by_route["ROUTE_NULL_CONTROLS_AFTER_MAPPING"]["may_resolve_blocker"] == "false"
    for row in rows:
        assert row["external_products_fetched"] == "false"
        assert row["numeric_factor_computed"] == "false"
        assert row["path_mapping_computed"] == "false"
        assert row["contains_mapping_vector"] == "false"
        assert row["contains_theory_vector"] == "false"
        assert row["uses_kids_data_vector_values"] == "false"
        assert row["endpoint_scoring_allowed"] == "false"


def test_kids1000_cosebis_path_blocker_resolution_order_is_mapping_available_not_scoring() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_path_blocker_resolution_order_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert policy["status"] == "KIDS1000_COSEBIS_PATH_BLOCKER_RESOLUTION_ORDER_POLICY_FROZEN_NOT_FETCHED"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert policy["current_order_declared"] == "true"
    assert policy["current_external_products_fetched"] == "false"
    assert policy["current_path_mapping_computed"] == "false"
    assert policy["current_theory_vector_computed"] == "false"
    with (
        ROOT / "data/derived/kids1000_cosebis_path_blocker_resolution_order_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "KIDS1000_COSEBIS_PATH_BLOCKER_RESOLUTION_ORDER_BUILT_NOT_FETCHED"
    assert summary["stage_count"] == "6"
    assert summary["resolved_source_supported_stage_count"] == "4"
    assert summary["resolved_control_supported_stage_count"] == "1"
    assert summary["blocking_unresolved_stage_count"] == "0"
    assert summary["not_allowed_stage_count"] == "0"
    assert summary["declared_not_computed_stage_count"] == "0"
    assert summary["declared_not_executed_stage_count"] == "0"
    assert summary["first_blocker"] == "none"
    assert summary["next_action"] == "resolve_non_degenerate_promotion_gate_before_endpoint_scoring"
    assert summary["external_products_fetched"] == "false"
    assert summary["numeric_factors_computed"] == "false"
    assert summary["path_mapping_computed"] == "true"
    assert summary["contains_mapping_vector"] == "true"
    assert summary["contains_theory_vector"] == "false"
    assert summary["contains_predictions"] == "false"
    assert summary["contains_residuals"] == "false"
    with (
        ROOT / "data/derived/kids1000_cosebis_path_blocker_resolution_order_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    observed = [(row["order_rank"], row["factor_id"], row["stage_status"]) for row in rows]
    assert observed == [
        ("1", "F_overlap", "resolved_source_supported"),
        ("2", "D_path", "resolved_source_supported"),
        ("3", "E_web", "resolved_control_supported"),
        ("4", "C_norm", "resolved_source_supported"),
        ("5", "mapping_vector", "resolved_source_supported"),
        ("6", "null_controls", "resolved_control_replay_supported"),
    ]
    for row in rows:
        assert row["external_products_fetched"] == "false"
        assert row["numeric_factor_computed"] == "false"
        assert row["path_mapping_computed"] == "true"
        assert row["contains_mapping_vector"] == "true"
        assert row["contains_theory_vector"] == "false"
        assert row["uses_kids_data_vector_values"] == "false"
        assert row["endpoint_scoring_allowed"] == "false"


def test_kids1000_cosebis_f_overlap_rule_shell_is_not_computed_or_mapping() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_f_overlap_rule_shell_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert policy["status"] == "KIDS1000_COSEBIS_F_OVERLAP_RULE_SHELL_DECLARED_NOT_COMPUTED"
    assert policy["first_blocker"] == "F_overlap"
    assert policy["factor_id"] == "F_overlap"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert policy["current_shell_declared"] == "true"
    assert policy["current_overlap_rule_computed"] == "false"
    assert policy["current_external_products_fetched"] == "false"
    assert policy["current_path_mapping_computed"] == "false"
    with (
        ROOT / "data/derived/kids1000_cosebis_f_overlap_rule_shell_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "KIDS1000_COSEBIS_F_OVERLAP_RULE_SHELL_BUILT_NOT_COMPUTED"
    assert summary["shell_item_count"] == "6"
    assert summary["candidate_route_count"] == "2"
    assert summary["target_rows"] == "300"
    assert summary["route_tiles"] == "196"
    assert summary["domain_rows"] == "58800"
    assert summary["first_blocker"] == "F_overlap"
    assert summary["overlap_rule_ready"] == "false"
    assert summary["mapping_allowed"] == "false"
    assert summary["external_products_fetched"] == "false"
    assert summary["overlap_rule_computed"] == "false"
    assert summary["path_mapping_computed"] == "false"
    assert summary["contains_mapping_vector"] == "false"
    assert summary["contains_theory_vector"] == "false"
    assert summary["contains_predictions"] == "false"
    assert summary["contains_residuals"] == "false"
    with (
        ROOT / "data/derived/kids1000_cosebis_f_overlap_rule_shell_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    by_item = {row["shell_item_id"]: row for row in rows}
    assert by_item["F_OVERLAP_INPUT_DOMAIN"]["blocks_overlap_computation"] == "false"
    assert by_item["F_OVERLAP_ROUTE_OFFICIAL_GEOMETRY"]["blocks_overlap_computation"] == "true"
    assert by_item["F_OVERLAP_ROUTE_PIXEL_MASK_DERIVED"]["blocks_overlap_computation"] == "true"
    assert by_item["F_OVERLAP_OUTPUT_SCHEMA"]["blocks_overlap_computation"] == "true"
    assert "one_row_per_target_row_tile_domain_entry" in by_item["F_OVERLAP_OUTPUT_SCHEMA"]["minimum_acceptance"]
    for row in rows:
        assert row["external_products_fetched"] == "false"
        assert row["overlap_rule_computed"] == "false"
        assert row["numeric_factor_computed"] == "false"
        assert row["path_mapping_computed"] == "false"
        assert row["contains_mapping_vector"] == "false"
        assert row["contains_theory_vector"] == "false"
        assert row["uses_kids_data_vector_values"] == "false"
        assert row["uses_posthoc_tile_selection"] == "false"
        assert row["endpoint_scoring_allowed"] == "false"


def test_kids1000_cosebis_f_overlap_source_availability_preserves_gap() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_f_overlap_source_availability_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert policy["status"] == "KIDS1000_COSEBIS_F_OVERLAP_SOURCE_AVAILABILITY_POLICY_DECLARED_NOT_FETCHED"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert policy["current_availability_checked"] == "true"
    assert policy["current_external_products_fetched"] == "false"
    assert policy["current_overlap_rule_computed"] == "false"
    assert policy["current_path_mapping_computed"] == "false"
    with (
        ROOT / "data/derived/kids1000_cosebis_f_overlap_source_availability_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "KIDS1000_COSEBIS_F_OVERLAP_SOURCE_AVAILABILITY_BUILT_NOT_FETCHED"
    assert summary["availability_item_count"] == "5"
    assert summary["expected_route_tile_count"] == "196"
    assert summary["partial_mask_subset_count"] == "3"
    assert summary["accepted_overlap_route_count"] == "0"
    assert summary["overlap_rule_ready"] == "false"
    assert summary["first_unresolved_source_gap"] == "official_geometry_or_full_196_mask_products"
    assert summary["external_products_fetched"] == "false"
    assert summary["overlap_rule_computed"] == "false"
    assert summary["path_mapping_computed"] == "false"
    assert summary["contains_mapping_vector"] == "false"
    assert summary["contains_theory_vector"] == "false"
    assert summary["contains_predictions"] == "false"
    assert summary["contains_residuals"] == "false"
    with (
        ROOT / "data/derived/kids1000_cosebis_f_overlap_source_availability_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    by_item = {row["availability_item_id"]: row for row in rows}
    assert by_item["F_OVERLAP_DOMAIN_SHELL"]["acceptance_status"] == "accepted_as_domain_shell_not_overlap_rule"
    assert by_item["F_OVERLAP_OFFICIAL_GEOMETRY_PRODUCT"]["availability_status"] == "missing"
    assert by_item["F_OVERLAP_PIXEL_MASK_ROUTE_SCRIPT"]["availability_status"] == "available_route_script_only"
    assert by_item["F_OVERLAP_PIXEL_MASK_ROUTE_SCRIPT"]["source_count"] == "196"
    assert by_item["F_OVERLAP_PIXEL_MASK_SUBSET"]["availability_status"] == "partial_available"
    assert by_item["F_OVERLAP_PIXEL_MASK_SUBSET"]["source_count"] == "3"
    assert by_item["F_OVERLAP_FULL_PIXEL_MASK_SET"]["acceptance_status"] == "not_accepted_full_196_mask_set_missing"
    for row in rows:
        assert row["external_products_fetched"] == "false"
        assert row["overlap_rule_computed"] == "false"
        assert row["numeric_factor_computed"] == "false"
        assert row["path_mapping_computed"] == "false"
        assert row["contains_mapping_vector"] == "false"
        assert row["contains_theory_vector"] == "false"
        assert row["uses_kids_data_vector_values"] == "false"
        assert row["endpoint_scoring_allowed"] == "false"


def test_kids1000_cosebis_f_overlap_full_mask_acquisition_manifest_preserves_missing_set() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_f_overlap_full_mask_acquisition_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert policy["status"] == "KIDS1000_COSEBIS_F_OVERLAP_FULL_MASK_ACQUISITION_POLICY_DECLARED_NOT_FETCHED"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert policy["current_manifest_declared"] == "true"
    assert policy["current_external_products_fetched"] == "false"
    assert policy["current_overlap_rule_computed"] == "false"
    assert policy["current_path_mapping_computed"] == "false"
    with (
        ROOT / "data/derived/kids1000_cosebis_f_overlap_full_mask_acquisition_manifest_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "KIDS1000_COSEBIS_F_OVERLAP_FULL_MASK_ACQUISITION_MANIFEST_BUILT_NOT_FETCHED"
    assert summary["expected_mask_count"] == "196"
    assert summary["local_present_count"] == "3"
    assert summary["missing_mask_count"] == "193"
    assert summary["full_mask_set_present"] == "false"
    assert summary["accepted_for_full_overlap_count"] == "0"
    assert summary["overlap_rule_ready"] == "false"
    assert summary["external_products_fetched"] == "false"
    assert summary["overlap_rule_computed"] == "false"
    assert summary["path_mapping_computed"] == "false"
    assert summary["contains_mapping_vector"] == "false"
    assert summary["contains_theory_vector"] == "false"
    assert summary["contains_predictions"] == "false"
    assert summary["contains_residuals"] == "false"
    with (
        ROOT / "data/derived/kids1000_cosebis_f_overlap_full_mask_acquisition_manifest_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 196
    assert sum(row["local_mask_present"] == "true" for row in rows) == 3
    assert sum(row["local_mask_present"] == "false" for row in rows) == 193
    assert all(row["accepted_for_full_overlap"] == "false" for row in rows)
    assert all(row["overlap_rule_computed"] == "false" for row in rows)
    assert all(row["path_mapping_computed"] == "false" for row in rows)
    assert all(row["uses_kids_data_vector_values"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)


def test_kids1000_cosebis_f_overlap_full_mask_batch_plan_is_unfetched_and_git_safe() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_f_overlap_full_mask_batch_plan_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert policy["status"] == "KIDS1000_COSEBIS_F_OVERLAP_FULL_MASK_BATCH_PLAN_DECLARED_NOT_FETCHED"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert policy["current_batch_plan_declared"] == "true"
    assert policy["current_external_products_fetched"] == "false"
    assert policy["current_overlap_rule_computed"] == "false"
    with (
        ROOT / "data/derived/kids1000_cosebis_f_overlap_full_mask_batch_plan_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "KIDS1000_COSEBIS_F_OVERLAP_FULL_MASK_BATCH_PLAN_BUILT_NOT_FETCHED"
    assert summary["expected_mask_count"] == "196"
    assert summary["local_present_count"] == "3"
    assert summary["missing_mask_count"] == "193"
    assert summary["batch_size_limit"] == "20"
    assert summary["batch_count"] == "10"
    assert summary["cache_git_policy"] == "large_fits_files_ignored_manifest_only_committed"
    assert summary["batch_fetches_executed"] == "false"
    assert summary["external_products_fetched"] == "false"
    assert summary["overlap_rule_computed"] == "false"
    assert summary["path_mapping_computed"] == "false"
    assert summary["contains_mapping_vector"] == "false"
    assert summary["contains_theory_vector"] == "false"
    assert "full_route_cache_v1/*.fits.gz" in (ROOT / ".gitignore").read_text()
    assert "data/local/" in (ROOT / ".gitignore").read_text()
    with (
        ROOT / "data/derived/kids1000_cosebis_f_overlap_full_mask_batch_plan_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    sizes = [int(row["batch_size"]) for row in rows]
    assert len(rows) == 10
    assert sum(sizes) == 193
    assert max(sizes) <= 20
    assert sizes[-1] == 13
    assert all(row["batch_fetch_executed"] == "false" for row in rows)
    assert all(row["external_products_fetched"] == "false" for row in rows)
    assert all(row["overlap_rule_computed"] == "false" for row in rows)
    assert all(row["path_mapping_computed"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)


def test_kids1000_cosebis_f_overlap_full_mask_batch_dry_run_is_unfetched() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_f_overlap_full_mask_batch_dry_run_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert policy["status"] == "KIDS1000_COSEBIS_F_OVERLAP_FULL_MASK_BATCH_DRY_RUN_DECLARED_NOT_FETCHED"
    assert policy["default_batch_index"] == "0"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert policy["current_external_products_fetched"] == "false"
    assert policy["current_overlap_rule_computed"] == "false"
    assert policy["current_path_mapping_computed"] == "false"
    with (
        ROOT / "data/derived/kids1000_cosebis_f_overlap_full_mask_batch_dry_run_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "KIDS1000_COSEBIS_F_OVERLAP_FULL_MASK_BATCH_DRY_RUN_BUILT_NOT_FETCHED"
    assert summary["batch_index_zero_based"] == "0"
    assert summary["batch_size"] == "20"
    assert summary["fetch_mode"] == "dry_run"
    assert summary["batch_fetch_executed"] == "false"
    assert summary["external_products_fetched"] == "false"
    assert summary["overlap_rule_computed"] == "false"
    assert summary["path_mapping_computed"] == "false"
    assert summary["contains_mapping_vector"] == "false"
    assert summary["contains_theory_vector"] == "false"
    assert summary["contains_predictions"] == "false"
    assert summary["contains_residuals"] == "false"
    assert summary["contains_fit_statistics"] == "false"
    assert summary["endpoint_scoring_allowed"] == "false"
    with (
        ROOT / "data/derived/kids1000_cosebis_f_overlap_full_mask_batch_dry_run_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 20
    assert all(row["fetch_mode"] == "dry_run" for row in rows)
    assert all(row["fetch_status"] == "dry_run_not_fetched" for row in rows)
    assert all(row["http_status"] == "" for row in rows)
    assert all(row["byte_count"] == "" for row in rows)
    assert all(row["sha256"] == "" for row in rows)
    assert all(row["external_products_fetched"] == "false" for row in rows)
    assert all(row["overlap_rule_computed"] == "false" for row in rows)
    assert all(row["numeric_factor_computed"] == "false" for row in rows)
    assert all(row["path_mapping_computed"] == "false" for row in rows)
    assert all(row["contains_mapping_vector"] == "false" for row in rows)
    assert all(row["contains_theory_vector"] == "false" for row in rows)
    assert all(row["contains_predictions"] == "false" for row in rows)
    assert all(row["contains_residuals"] == "false" for row in rows)
    assert all(row["contains_fit_statistics"] == "false" for row in rows)
    assert all(row["uses_kids_data_vector_values"] == "false" for row in rows)
    assert all(row["uses_posterior_chains"] == "false" for row in rows)
    assert all(row["uses_posthoc_tile_selection"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)


def test_kids1000_cosebis_f_overlap_batch_promotion_review_is_not_ready() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_f_overlap_batch_promotion_review_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert policy["status"] == "KIDS1000_COSEBIS_F_OVERLAP_BATCH_PROMOTION_REVIEW_DECLARED_NOT_READY"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert policy["current_execution_review_artifact_present"] == "false"
    assert policy["current_checksum_manifest_present"] == "false"
    assert policy["current_overlap_rule_computed"] == "false"
    with (
        ROOT / "data/derived/kids1000_cosebis_f_overlap_batch_promotion_review_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "KIDS1000_COSEBIS_F_OVERLAP_BATCH_PROMOTION_REVIEW_BUILT_NOT_READY"
    assert summary["dry_run_batch_id"] == "F_OVERLAP_FULL_MASK_BATCH_00"
    assert summary["dry_run_batch_size"] == "20"
    assert summary["planned_total_batch_count"] == "10"
    assert summary["planned_missing_mask_count"] == "193"
    assert summary["requirement_count"] == "6"
    assert summary["blocking_requirement_count"] == "4"
    assert summary["promotion_ready"] == "false"
    assert summary["first_blocker"] == "PROMOTE_01_EXECUTION_REVIEW_ARTIFACT"
    assert summary["execution_review_artifact_present"] == "false"
    assert summary["checksum_manifest_present"] == "false"
    assert summary["external_products_fetched"] == "false"
    assert summary["overlap_rule_computed"] == "false"
    assert summary["path_mapping_computed"] == "false"
    assert summary["contains_mapping_vector"] == "false"
    assert summary["contains_theory_vector"] == "false"
    assert summary["endpoint_scoring_allowed"] == "false"
    with (
        ROOT / "data/derived/kids1000_cosebis_f_overlap_batch_promotion_review_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 6
    by_id = {row["requirement_id"]: row for row in rows}
    assert set(by_id) == {
        "PROMOTE_01_EXECUTION_REVIEW_ARTIFACT",
        "PROMOTE_02_CHECKSUM_MANIFEST",
        "PROMOTE_03_BATCH_PRODUCT_COUNT",
        "PROMOTE_04_FORBIDDEN_INPUT_AUDIT",
        "PROMOTE_05_OVERLAP_DERIVATION_STILL_SEPARATE",
        "PROMOTE_06_FILLED_REVIEW_VALIDATOR_AVAILABLE",
    }
    assert by_id["PROMOTE_05_OVERLAP_DERIVATION_STILL_SEPARATE"]["blocks_promotion"] == "false"
    assert by_id["PROMOTE_06_FILLED_REVIEW_VALIDATOR_AVAILABLE"]["blocks_promotion"] == "false"
    assert by_id["PROMOTE_06_FILLED_REVIEW_VALIDATOR_AVAILABLE"]["status"] == "satisfied_not_executed"
    assert all(row["promotion_ready"] == "false" for row in rows)
    assert all(row["external_products_fetched"] == "false" for row in rows)
    assert all(row["overlap_rule_computed"] == "false" for row in rows)
    assert all(row["path_mapping_computed"] == "false" for row in rows)
    assert all(row["contains_mapping_vector"] == "false" for row in rows)
    assert all(row["contains_theory_vector"] == "false" for row in rows)
    assert all(row["contains_predictions"] == "false" for row in rows)
    assert all(row["contains_residuals"] == "false" for row in rows)
    assert all(row["contains_fit_statistics"] == "false" for row in rows)
    assert all(row["uses_kids_data_vector_values"] == "false" for row in rows)
    assert all(row["uses_posterior_chains"] == "false" for row in rows)
    assert all(row["uses_posthoc_tile_selection"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)


def test_kids1000_cosebis_f_overlap_resolution_decision_is_control_only() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_f_overlap_resolution_decision_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert policy["status"] == "KIDS1000_COSEBIS_F_OVERLAP_RESOLUTION_DECISION_POLICY_FROZEN_NOT_RESOLVED"
    assert policy["current_overlap_rule_computed"] == "false"
    assert policy["current_path_mapping_computed"] == "false"
    assert policy["current_endpoint_scoring_allowed"] == "false"
    with (
        ROOT / "data/derived/kids1000_cosebis_f_overlap_resolution_decision_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "KIDS1000_COSEBIS_F_OVERLAP_RESOLUTION_DECISION_BUILT_NOT_RESOLVED"
    assert summary["decision_item_count"] == "4"
    assert summary["endpoint_route_accepted_count"] == "1"
    assert summary["control_route_accepted_count"] == "1"
    assert summary["unresolved_route_count"] == "2"
    assert summary["f_overlap_endpoint_ready"] == "true"
    assert summary["f_overlap_control_ready"] == "true"
    assert summary["accepted_control_scope"] == "three_mask_subset_partial_path_control_only"
    assert summary["full_route_source_cache_complete"] == "true"
    assert summary["header_footprint_rule_available"] == "true"
    assert summary["header_footprint_rule_uniform"] == "true"
    assert summary["header_footprint_non_degenerate_support"] == "false"
    assert summary["pixel_fraction_subset_pilot_non_degenerate"] == "true"
    assert summary["pixel_fraction_subset_pilot_scope"] == "three_committed_mask_subset_only"
    assert float(summary["pixel_fraction_subset_min_f_overlap"]) < float(
        summary["pixel_fraction_subset_max_f_overlap"]
    )
    assert int(summary["pixel_fraction_subset_unique_value_count"]) == 3
    assert summary["first_required_next_action"] == "f_overlap_source_route_resolved_proceed_to_remaining_path_weight_factors"
    assert summary["overlap_rule_computed"] == "false"
    assert summary["path_mapping_computed"] == "false"
    assert summary["contains_mapping_vector"] == "false"
    assert summary["contains_theory_vector"] == "false"
    assert summary["contains_predictions"] == "false"
    assert summary["contains_residuals"] == "false"
    assert summary["contains_fit_statistics"] == "false"
    assert summary["uses_kids_data_vector_values"] == "false"
    assert summary["uses_posterior_chains"] == "false"
    assert summary["uses_posthoc_tile_selection"] == "false"
    assert summary["endpoint_scoring_allowed"] == "false"
    with (
        ROOT / "data/derived/kids1000_cosebis_f_overlap_resolution_decision_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 4
    by_item = {row["decision_item_id"]: row for row in rows}
    assert by_item["F_OVERLAP_THREE_MASK_SUBSET"]["decision_class"] == "accepted_caveated_control_only"
    assert by_item["F_OVERLAP_THREE_MASK_SUBSET"]["endpoint_route_accepted"] == "false"
    assert by_item["F_OVERLAP_THREE_MASK_SUBSET"]["control_route_accepted"] == "true"
    for item_id in [
        "F_OVERLAP_OFFICIAL_GEOMETRY_ROUTE",
        "F_OVERLAP_BATCH0_DRY_RUN",
    ]:
        assert by_item[item_id]["decision_class"] == "rejected_unresolved"
        assert by_item[item_id]["endpoint_route_accepted"] == "false"
        assert by_item[item_id]["control_route_accepted"] == "false"
    assert by_item["F_OVERLAP_FULL_PIXEL_MASK_ROUTE"]["decision_class"] == (
        "accepted_source_frozen_full_route_pixel_fraction"
    )
    assert by_item["F_OVERLAP_FULL_PIXEL_MASK_ROUTE"]["endpoint_route_accepted"] == "true"
    assert by_item["F_OVERLAP_FULL_PIXEL_MASK_ROUTE"]["control_route_accepted"] == "false"
    assert all(row["overlap_rule_computed"] == "false" for row in rows)
    assert all(row["path_mapping_computed"] == "false" for row in rows)
    assert all(row["contains_mapping_vector"] == "false" for row in rows)
    assert all(row["contains_theory_vector"] == "false" for row in rows)
    assert all(row["contains_predictions"] == "false" for row in rows)
    assert all(row["contains_residuals"] == "false" for row in rows)
    assert all(row["uses_kids_data_vector_values"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    for marker in [
        "kids_data_vector_values",
        "posterior_chains",
        "lensing_residuals",
        "posthoc_overlap_rule_choice",
        "posthoc_path_projection_labels",
    ]:
        assert marker in policy["forbidden_inputs"]


def test_kids1000_cosebis_f_overlap_full_route_cache_inventory_is_source_only() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_f_overlap_full_route_cache_inventory_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert policy["status"] == "KIDS1000_COSEBIS_F_OVERLAP_FULL_ROUTE_CACHE_INVENTORY_LOCAL_ONLY_NOT_SCORED"
    assert policy["endpoint_scoring_allowed"] == "false"
    with (
        ROOT / "data/derived/kids1000_cosebis_f_overlap_full_route_cache_inventory_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "KIDS1000_COSEBIS_F_OVERLAP_FULL_ROUTE_CACHE_INVENTORY_BUILT_LOCAL_ONLY_NOT_SCORED"
    assert summary["expected_mask_count"] == "196"
    assert summary["present_mask_count"] == "196"
    assert summary["missing_mask_count"] == "0"
    assert summary["local_full_route_cache_count"] == "193"
    assert summary["committed_subset_count"] == "3"
    assert summary["source_cache_complete"] == "true"
    assert summary["local_cache_required_for_public_reproduce"] == "false"
    assert summary["public_reproduce_uses_committed_inventory_only"] == "true"
    for key in [
        "overlap_rule_computed",
        "path_mapping_computed",
        "contains_mapping_vector",
        "contains_theory_vector",
        "contains_predictions",
        "contains_residuals",
        "contains_fit_statistics",
        "uses_kids_data_vector_values",
        "uses_posterior_chains",
        "uses_posthoc_tile_selection",
        "endpoint_scoring_allowed",
    ]:
        assert summary[key] == "false"
    with (
        ROOT / "data/derived/kids1000_cosebis_f_overlap_full_route_cache_inventory_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 196
    assert all(row["local_or_committed_mask_present"] == "true" for row in rows)
    assert all(row["accepted_for_source_cache_inventory"] == "true" for row in rows)
    assert all(row["sha256"] for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)


def test_kids1000_cosebis_f_overlap_header_footprint_rule_is_source_only_uniform() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_f_overlap_header_footprint_rule_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert policy["status"] == "KIDS1000_COSEBIS_F_OVERLAP_HEADER_FOOTPRINT_RULE_LOCAL_DERIVATION_NOT_SCORED"
    assert policy["endpoint_scoring_allowed"] == "false"
    with (
        ROOT / "data/derived/kids1000_cosebis_f_overlap_header_footprint_rule_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "KIDS1000_COSEBIS_F_OVERLAP_HEADER_FOOTPRINT_RULE_BUILT_NOT_MAPPED"
    assert summary["tile_count"] == "196"
    assert summary["target_rows"] == "300"
    assert summary["domain_rows"] == "58800"
    assert summary["header_footprint_rule_available"] == "true"
    assert summary["pixel_mask_values_read"] == "false"
    assert summary["pixel_mask_overlap_computed"] == "false"
    assert summary["overlap_rule_computed"] == "true"
    assert summary["path_mapping_computed"] == "false"
    assert summary["unique_f_overlap_value_count_rounded_1e_minus_12"] == "1"
    assert summary["min_f_overlap_value"] == "1.000000000000e+00"
    assert summary["max_f_overlap_value"] == "1.000000000000e+00"
    for key in [
        "contains_mapping_vector",
        "contains_theory_vector",
        "contains_predictions",
        "contains_residuals",
        "contains_fit_statistics",
        "uses_kids_data_vector_values",
        "uses_posterior_chains",
        "uses_posthoc_tile_selection",
        "endpoint_scoring_allowed",
    ]:
        assert summary[key] == "false"
    with (
        ROOT / "data/derived/kids1000_cosebis_f_overlap_header_footprint_rule_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 58800
    assert all(row["f_overlap_value"] == "1.000000000000e+00" for row in rows)
    assert all(row["pixel_mask_values_read"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)


def test_kids1000_cosebis_f_overlap_header_footprint_degeneracy_audit_blocks_promotion() -> None:
    with (
        ROOT
        / "data/source_manifest/kids1000_cosebis_f_overlap_header_footprint_degeneracy_audit_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert policy["status"] == "KIDS1000_COSEBIS_F_OVERLAP_HEADER_FOOTPRINT_DEGENERACY_AUDIT_DECLARED_NOT_SCORED"
    assert policy["endpoint_scoring_allowed"] == "false"
    with (
        ROOT / "data/derived/kids1000_cosebis_f_overlap_header_footprint_degeneracy_audit_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "KIDS1000_COSEBIS_F_OVERLAP_HEADER_FOOTPRINT_DEGENERACY_AUDIT_BUILT_UNIFORM_NOT_PROMOTABLE"
    assert summary["tile_count"] == "196"
    assert summary["blocking_item_count"] == "2"
    assert summary["unique_f_overlap_value_count_rounded_1e_minus_12"] == "1"
    assert summary["header_rule_uniform"] == "true"
    assert summary["non_degenerate_mapping_support"] == "false"
    assert summary["recommended_next_action"] == "derive_pixel_mask_or_subtile_overlap_rule"
    assert summary["path_mapping_computed"] == "false"
    assert summary["endpoint_scoring_allowed"] == "false"


def test_kids1000_cosebis_f_overlap_pixel_fraction_pilot_is_source_only_non_degenerate() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_f_overlap_pixel_fraction_pilot_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert policy["status"] == "KIDS1000_COSEBIS_F_OVERLAP_PIXEL_FRACTION_PILOT_SOURCE_ONLY_NOT_SCORED"
    assert policy["source_scope"] == "three_committed_mask_subset_only"
    assert policy["endpoint_scoring_allowed"] == "false"
    with (
        ROOT / "data/derived/kids1000_cosebis_f_overlap_pixel_fraction_pilot_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "KIDS1000_COSEBIS_F_OVERLAP_PIXEL_FRACTION_PILOT_BUILT_SOURCE_ONLY_NOT_MAPPED"
    assert summary["tile_count"] == "3"
    assert summary["pixel_fraction_pilot_non_degenerate"] == "true"
    assert summary["header_footprint_rule_uniformity_resolved_for_subset"] == "true"
    assert summary["full_route_pixel_rule_computed"] == "false"
    assert 0.0 < float(summary["min_f_overlap_pixel_fraction_value"])
    assert float(summary["min_f_overlap_pixel_fraction_value"]) < float(
        summary["max_f_overlap_pixel_fraction_value"]
    )
    assert summary["max_f_overlap_pixel_fraction_value"] == "1.000000000000e+00"
    assert summary["unique_f_overlap_value_count_rounded_1e_minus_12"] == "3"
    assert (
        summary["recommended_next_action"]
        == "promote_to_full_route_pixel_or_subtile_rule_with_streaming_cache_before_endpoint_scoring"
    )
    with (
        ROOT / "data/derived/kids1000_cosebis_f_overlap_pixel_fraction_pilot_tile_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 3
    values = [float(row["f_overlap_pixel_fraction_value"]) for row in rows]
    assert min(values) < max(values)
    assert all(row["mask_pixels_parsed_upstream"] == "true" for row in rows)
    assert all(row["source_scope"] == "three_committed_mask_subset_only" for row in rows)
    for key in [
        "path_mapping_computed",
        "contains_mapping_vector",
        "contains_theory_vector",
        "contains_predictions",
        "contains_residuals",
        "contains_fit_statistics",
        "uses_kids_data_vector_values",
        "uses_posterior_chains",
        "uses_posthoc_tile_selection",
        "uses_posthoc_path_projection_labels",
        "endpoint_scoring_allowed",
    ]:
        assert summary[key] == "false"
        assert all(row[key] == "false" for row in rows)
    for marker in [
        "kids_data_vector_values",
        "posterior_chains",
        "lensing_residuals",
        "posthoc_tile_selection",
        "posthoc_path_projection_labels",
    ]:
        assert marker in policy["forbidden_inputs"]


def test_kids1000_cosebis_f_overlap_full_route_pixel_fraction_rule_is_source_only_non_degenerate() -> None:
    with (
        ROOT
        / "data/source_manifest/kids1000_cosebis_f_overlap_full_route_pixel_fraction_rule_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert (
        policy["status"]
        == "KIDS1000_COSEBIS_F_OVERLAP_FULL_ROUTE_PIXEL_FRACTION_RULE_SOURCE_ONLY_NOT_SCORED"
    )
    assert policy["source_scope"] == "full_196_route_mask_set"
    assert policy["endpoint_scoring_allowed"] == "false"

    with (
        ROOT / "data/derived/kids1000_cosebis_f_overlap_full_route_pixel_fraction_rule_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert (
        summary["status"]
        == "KIDS1000_COSEBIS_F_OVERLAP_FULL_ROUTE_PIXEL_FRACTION_RULE_BUILT_SOURCE_ONLY_NOT_MAPPED"
    )
    assert summary["tile_count"] == "196"
    assert summary["target_rows"] == "300"
    assert summary["domain_rows"] == "58800"
    assert summary["full_route_pixel_fraction_non_degenerate"] == "true"
    assert summary["f_overlap_endpoint_route_support"] == "true"
    assert 0.0 < float(summary["min_f_overlap_value"]) < float(summary["max_f_overlap_value"]) <= 1.0
    assert int(summary["unique_f_overlap_value_count_rounded_1e_minus_12"]) > 1

    with (
        ROOT / "data/derived/kids1000_cosebis_f_overlap_full_route_pixel_fraction_tile_rule_v1.csv"
    ).open(newline="") as f:
        tile_rows = list(csv.DictReader(f))
    with (
        ROOT / "data/derived/kids1000_cosebis_f_overlap_full_route_pixel_fraction_rule_v1.csv"
    ).open(newline="") as f:
        domain_rows = list(csv.DictReader(f))
    assert len(tile_rows) == 196
    assert len(domain_rows) == 58800
    assert len({round(float(row["f_overlap_full_route_pixel_fraction_value"]), 12) for row in tile_rows}) > 1
    assert len({round(float(row["f_overlap_value"]), 12) for row in domain_rows}) > 1
    assert all(row["sha256"] for row in tile_rows)
    assert all(row["full_route_pixel_fraction_computed"] == "true" for row in tile_rows)
    assert all(row["full_route_pixel_fraction_computed"] == "true" for row in domain_rows)

    for key in [
        "path_mapping_computed",
        "contains_mapping_vector",
        "contains_theory_vector",
        "contains_predictions",
        "contains_residuals",
        "contains_fit_statistics",
        "uses_kids_data_vector_values",
        "uses_posterior_chains",
        "uses_posthoc_tile_selection",
        "uses_posthoc_path_projection_labels",
        "endpoint_scoring_allowed",
    ]:
        assert summary[key] == "false"
        assert all(row[key] == "false" for row in tile_rows)
        assert all(row[key] == "false" for row in domain_rows)
    for marker in [
        "kids_data_vector_values",
        "posterior_chains",
        "lensing_residuals",
        "posthoc_tile_selection",
        "posthoc_path_projection_labels",
        "posthoc_overlap_rule_choice",
    ]:
        assert marker in policy["forbidden_inputs"]


def test_kids1000_cosebis_d_path_full_route_mask_load_rule_is_source_only_non_degenerate() -> None:
    with (
        ROOT
        / "data/source_manifest/kids1000_cosebis_d_path_full_route_mask_load_rule_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert (
        policy["status"]
        == "KIDS1000_COSEBIS_D_PATH_FULL_ROUTE_MASK_LOAD_RULE_SOURCE_ONLY_NOT_SCORED"
    )
    assert policy["source_scope"] == "full_196_route_mask_set"
    assert policy["endpoint_scoring_allowed"] == "false"

    with (
        ROOT / "data/derived/kids1000_cosebis_d_path_full_route_mask_load_rule_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert (
        summary["status"]
        == "KIDS1000_COSEBIS_D_PATH_FULL_ROUTE_MASK_LOAD_RULE_BUILT_SOURCE_ONLY_NOT_MAPPED"
    )
    assert summary["tile_count"] == "196"
    assert summary["target_rows"] == "300"
    assert summary["domain_rows"] == "58800"
    assert summary["d_path_full_route_mask_load_non_degenerate"] == "true"
    assert summary["d_path_source_route_support"] == "true"
    assert summary["d_path_not_identical_to_f_overlap"] == "true"
    assert 0.0 < float(summary["min_d_path_value"]) < float(summary["max_d_path_value"]) <= 1.0
    assert int(summary["unique_d_path_value_count_rounded_1e_minus_12"]) > 1
    assert float(summary["max_abs_delta_from_f_overlap"]) > 1.0e-6

    with (
        ROOT / "data/derived/kids1000_cosebis_d_path_full_route_mask_load_tile_rule_v1.csv"
    ).open(newline="") as f:
        tile_rows = list(csv.DictReader(f))
    with (
        ROOT / "data/derived/kids1000_cosebis_d_path_full_route_mask_load_rule_v1.csv"
    ).open(newline="") as f:
        domain_rows = list(csv.DictReader(f))
    assert len(tile_rows) == 196
    assert len(domain_rows) == 58800
    assert len({round(float(row["d_path_full_route_mask_load_value"]), 12) for row in tile_rows}) > 1
    assert len({round(float(row["d_path_value"]), 12) for row in domain_rows}) > 1
    assert all(row["sha256"] for row in tile_rows)
    assert all(row["d_path_mask_load_computed"] == "true" for row in tile_rows)
    assert all(row["d_path_mask_load_computed"] == "true" for row in domain_rows)

    for key in [
        "path_mapping_computed",
        "contains_mapping_vector",
        "contains_theory_vector",
        "contains_predictions",
        "contains_residuals",
        "contains_fit_statistics",
        "uses_kids_data_vector_values",
        "uses_posterior_chains",
        "uses_posthoc_tile_selection",
        "uses_posthoc_path_projection_labels",
        "endpoint_scoring_allowed",
    ]:
        assert summary[key] == "false"
        assert all(row[key] == "false" for row in tile_rows)
        assert all(row[key] == "false" for row in domain_rows)
    for marker in [
        "kids_data_vector_values",
        "posterior_chains",
        "lensing_residuals",
        "posthoc_tile_selection",
        "posthoc_path_projection_labels",
        "posthoc_d_path_rule_choice",
    ]:
        assert marker in policy["forbidden_inputs"]


def test_kids1000_cosebis_e_web_null_control_rule_is_source_only_uniform_control() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_e_web_null_control_rule_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert policy["status"] == "KIDS1000_COSEBIS_E_WEB_NULL_CONTROL_RULE_SOURCE_ONLY_NOT_SCORED"
    assert policy["source_scope"] == "full_196_route_tile_domain"
    assert policy["positive_web_claim_allowed"] == "false"
    assert policy["endpoint_scoring_allowed"] == "false"

    with (
        ROOT / "data/derived/kids1000_cosebis_e_web_null_control_rule_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "KIDS1000_COSEBIS_E_WEB_NULL_CONTROL_RULE_BUILT_SOURCE_ONLY_NOT_MAPPED"
    assert summary["tile_count"] == "196"
    assert summary["target_rows"] == "300"
    assert summary["domain_rows"] == "58800"
    assert summary["e_web_null_control_uniform"] == "true"
    assert summary["e_web_source_route_support"] == "true"
    assert summary["positive_web_claim_allowed"] == "false"
    assert summary["unique_e_web_value_count_rounded_1e_minus_12"] == "1"
    assert float(summary["min_e_web_value"]) == float(summary["max_e_web_value"]) == 1.0

    with (ROOT / "data/derived/kids1000_cosebis_e_web_null_control_tile_rule_v1.csv").open(
        newline=""
    ) as f:
        tile_rows = list(csv.DictReader(f))
    with (ROOT / "data/derived/kids1000_cosebis_e_web_null_control_rule_v1.csv").open(
        newline=""
    ) as f:
        domain_rows = list(csv.DictReader(f))
    assert len(tile_rows) == 196
    assert len(domain_rows) == 58800
    assert {float(row["e_web_null_control_value"]) for row in tile_rows} == {1.0}
    assert {float(row["e_web_value"]) for row in domain_rows} == {1.0}
    assert all(row["e_web_null_control_computed"] == "true" for row in tile_rows)
    assert all(row["e_web_null_control_computed"] == "true" for row in domain_rows)
    assert all(row["positive_web_claim_allowed"] == "false" for row in tile_rows)
    assert all(row["positive_web_claim_allowed"] == "false" for row in domain_rows)

    for key in [
        "path_mapping_computed",
        "contains_mapping_vector",
        "contains_theory_vector",
        "contains_predictions",
        "contains_residuals",
        "contains_fit_statistics",
        "uses_kids_data_vector_values",
        "uses_posterior_chains",
        "uses_posthoc_tile_selection",
        "uses_posthoc_sky_direction_selection",
        "uses_posthoc_web_environment_labels",
        "uses_posthoc_path_projection_labels",
        "endpoint_scoring_allowed",
    ]:
        assert summary[key] == "false"
        assert all(row[key] == "false" for row in tile_rows)
        assert all(row[key] == "false" for row in domain_rows)
    for marker in [
        "kids_data_vector_values",
        "posterior_chains",
        "lensing_residuals",
        "posthoc_tile_selection",
        "posthoc_sky_direction_selection",
        "posthoc_web_environment_labels",
        "posthoc_path_projection_labels",
        "posthoc_e_web_rule_choice",
    ]:
        assert marker in policy["forbidden_inputs"]


def test_kids1000_cosebis_c_norm_source_side_rule_is_source_only_normalization() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_c_norm_source_side_rule_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert policy["status"] == "KIDS1000_COSEBIS_C_NORM_SOURCE_SIDE_RULE_SOURCE_ONLY_NOT_SCORED"
    assert policy["source_scope"] == "full_58800_domain_rows"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert policy["current_path_mapping_computed"] == "false"
    assert policy["current_theory_vector_computed"] == "false"

    with (
        ROOT / "data/derived/kids1000_cosebis_c_norm_source_side_rule_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "KIDS1000_COSEBIS_C_NORM_SOURCE_SIDE_RULE_BUILT_SOURCE_ONLY_NOT_MAPPED"
    assert summary["domain_rows"] == "58800"
    assert summary["c_norm_source_route_support"] == "true"
    assert summary["c_norm_positive_raw_support"] == "true"
    assert float(summary["min_raw_source_weight_fde"]) > 0.0
    assert float(summary["max_raw_source_weight_fde"]) > float(summary["min_raw_source_weight_fde"])
    assert float(summary["c_norm_value"]) > 0.0
    assert abs(float(summary["mean_normalized_source_weight_fde"]) - 1.0) < 1.0e-10

    with (
        ROOT / "data/derived/kids1000_cosebis_c_norm_source_side_domain_rule_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 58800
    raw_values = [float(row["raw_source_weight_fde"]) for row in rows]
    assert min(raw_values) > 0.0
    assert abs((1.0 / (sum(raw_values) / len(raw_values))) - float(summary["c_norm_value"])) < 1.0e-10

    for key in [
        "path_mapping_computed",
        "contains_mapping_vector",
        "contains_theory_vector",
        "contains_predictions",
        "contains_residuals",
        "contains_fit_statistics",
        "uses_kids_data_vector_values",
        "uses_posterior_chains",
        "uses_posthoc_weight_selection",
        "uses_posthoc_tile_selection",
        "uses_posthoc_sky_direction_selection",
        "uses_posthoc_web_environment_labels",
        "uses_posthoc_path_projection_labels",
        "endpoint_scoring_allowed",
    ]:
        assert summary[key] == "false"
        assert all(row[key] == "false" for row in rows)
    for marker in [
        "kids_data_vector_values",
        "posterior_chains",
        "lensing_residuals",
        "fit_statistics",
        "fit_improvement_flags",
        "posthoc_weight_selection",
        "posthoc_tile_selection",
        "posthoc_sky_direction_selection",
        "posthoc_web_environment_labels",
        "posthoc_path_projection_labels",
        "posthoc_c_norm_rule_choice",
    ]:
        assert marker in policy["forbidden_inputs"]


def test_kids1000_cosebis_partial_control_scoring_protocol_is_frozen_not_run() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_partial_control_scoring_protocol_v1.csv"
    ).open(newline="") as f:
        protocol = list(csv.DictReader(f))[0]
    assert protocol["status"] == "PARTIAL_CONTROL_SCORING_PROTOCOL_FROZEN_NOT_RUN"
    assert protocol["control_scope"] == "three_mask_subset_partial_path_control_only"
    assert protocol["partial_control_scoring_allowed"] == "false"
    assert protocol["endpoint_scoring_allowed"] == "false"
    assert "diagnostic_chi2_shell_only" in protocol["primary_score_shell"]
    assert "not_endpoint_scores" in protocol["allowed_outputs"]
    for marker in [
        "partial_control_baseline",
        "partial_control_candidate",
        "wrong_channel_controls",
        "fixed_seed_sign_flip_controls",
        "control_rank_only",
    ]:
        assert marker in protocol["allowed_comparison_outputs"]
    for marker in [
        "F_overlap endpoint route rejected",
        "F_overlap partial control accepted",
        "partial mapping vector source-frozen",
        "null controls declared",
        "no endpoint leakage flags",
    ]:
        assert marker in protocol["minimum_preconditions"]
    for marker in [
        "kids_data_vector_values_for_source_selection",
        "posterior_chains",
        "fit_improvement_flags",
        "lensing_residuals",
        "posthoc_mask_subset_selection",
    ]:
        assert marker in protocol["forbidden_inputs"]
    with (
        ROOT / "data/derived/kids1000_cosebis_f_overlap_resolution_decision_v1_summary.csv"
    ).open(newline="") as f:
        f_overlap = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_mapping_template_join_contract_v1_summary.csv"
    ).open(newline="") as f:
        join_contract = list(csv.DictReader(f))[0]
    assert protocol["parent_f_overlap_decision_policy"] == f_overlap["policy_id"]
    assert protocol["parent_join_contract_policy"] == join_contract["policy_id"]
    assert f_overlap["f_overlap_endpoint_ready"] == "true"
    assert f_overlap["f_overlap_control_ready"] == "true"
    assert join_contract["mapping_vector_computed"] == "false"
    forbidden_outputs = [
        "kids1000_cosebis_partial_control_scoring_v1_results.csv",
        "kids1000_cosebis_partial_control_scoring_v1_residuals.csv",
        "kids1000_cosebis_partial_control_scoring_v1_grid.csv",
        "kids1000_cosebis_partial_control_scoring_v1_null_controls.csv",
        "kids1000_cosebis_partial_control_scoring_v1_summary.csv",
    ]
    for filename in forbidden_outputs:
        assert not (ROOT / "data/derived" / filename).exists()


def test_kids1000_cosebis_partial_control_mapping_shell_is_not_mapping() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_partial_control_mapping_shell_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert policy["status"] == "KIDS1000_COSEBIS_PARTIAL_CONTROL_MAPPING_SHELL_POLICY_FROZEN_NOT_MAPPED"
    assert policy["control_scope"] == "three_mask_subset_partial_path_control_only"
    assert policy["expected_target_rows"] == "300"
    assert policy["expected_mask_control_rows"] == "3"
    assert policy["expected_shell_rows"] == "900"
    assert policy["current_partial_mapping_values_computed"] == "false"
    assert policy["current_partial_control_scoring_allowed"] == "false"
    assert policy["current_endpoint_scoring_allowed"] == "false"
    for marker in [
        "kids_data_vector_values",
        "posterior_chains",
        "lensing_residuals",
        "fit_improvement_flags",
        "posthoc_mask_subset_selection",
        "posthoc_weight_selection",
    ]:
        assert marker in policy["forbidden_inputs"]
    with (
        ROOT / "data/derived/kids1000_cosebis_partial_control_mapping_shell_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "KIDS1000_COSEBIS_PARTIAL_CONTROL_MAPPING_SHELL_BUILT_NOT_MAPPED"
    assert summary["target_rows"] == "300"
    assert summary["mask_control_rows"] == "3"
    assert summary["shell_rows"] == "900"
    assert summary["mapping_shell_built"] == "true"
    assert summary["partial_mapping_values_computed"] == "false"
    assert summary["contains_mapping_vector"] == "false"
    assert summary["contains_theory_vector"] == "false"
    assert summary["contains_predictions"] == "false"
    assert summary["contains_residuals"] == "false"
    assert summary["contains_fit_statistics"] == "false"
    assert summary["uses_kids_data_vector_values"] == "false"
    assert summary["uses_posterior_chains"] == "false"
    assert summary["uses_posthoc_selection"] == "false"
    assert summary["partial_control_scoring_allowed"] == "false"
    assert summary["endpoint_scoring_allowed"] == "false"
    with (
        ROOT / "data/derived/kids1000_cosebis_partial_control_mapping_shell_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 900
    assert [row["shell_row_index_zero_based"] for row in rows] == [str(i) for i in range(900)]
    assert len({row["target_row_index_zero_based"] for row in rows}) == 300
    assert len({row["mask_sample_index_zero_based"] for row in rows}) == 3
    assert all(row["mapping_shell_row_only"] == "true" for row in rows)
    assert all(row["partial_mapping_value"] == "" for row in rows)
    assert all(row["partial_mapping_values_computed"] == "false" for row in rows)
    assert all(row["contains_mapping_vector"] == "false" for row in rows)
    assert all(row["contains_theory_vector"] == "false" for row in rows)
    assert all(row["contains_prediction"] == "false" for row in rows)
    assert all(row["contains_residual"] == "false" for row in rows)
    assert all(row["partial_control_scoring_allowed"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)
    assert {row["source_shell_scope"] for row in rows} == {"three_mask_subset_only"}
    assert all(abs(float(row["source_mask_shell_value"])) <= 1.000000000001 for row in rows)


def test_kids1000_cosebis_partial_control_mapping_values_are_not_scores() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_partial_control_mapping_values_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert policy["status"] == "KIDS1000_COSEBIS_PARTIAL_CONTROL_MAPPING_VALUES_POLICY_FROZEN_SOURCE_ONLY"
    assert policy["formula_id"] == "PARTIAL_CONTROL_MASK_Z_MODE_DECAY_V1"
    assert policy["expected_shell_rows"] == "900"
    assert policy["current_contains_endpoint_mapping_vector"] == "false"
    assert policy["current_contains_theory_vector"] == "false"
    assert policy["current_contains_predictions"] == "false"
    assert policy["current_contains_residuals"] == "false"
    assert policy["current_contains_fit_statistics"] == "false"
    assert policy["current_uses_kids_data_vector_values"] == "false"
    assert policy["current_uses_posterior_chains"] == "false"
    assert policy["current_uses_posthoc_selection"] == "false"
    assert policy["current_partial_control_scoring_allowed"] == "false"
    assert policy["current_endpoint_scoring_allowed"] == "false"
    for marker in [
        "kids_data_vector_values_for_source_selection",
        "KiDS_En_data_vector_values",
        "posterior_chains",
        "lensing_residuals",
        "fit_improvement_flags",
        "posthoc_mask_subset_selection",
        "posthoc_weight_selection",
    ]:
        assert marker in policy["forbidden_inputs"]
    with (
        ROOT / "data/derived/kids1000_cosebis_partial_control_mapping_values_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "KIDS1000_COSEBIS_PARTIAL_CONTROL_MAPPING_VALUES_BUILT_SOURCE_ONLY_NOT_SCORED"
    assert summary["shell_rows"] == "900"
    assert summary["target_rows"] == "300"
    assert summary["mask_control_rows"] == "3"
    assert summary["partial_mapping_values_computed"] == "true"
    assert summary["contains_partial_mapping_values"] == "true"
    assert summary["contains_endpoint_mapping_vector"] == "false"
    assert summary["contains_theory_vector"] == "false"
    assert summary["contains_predictions"] == "false"
    assert summary["contains_residuals"] == "false"
    assert summary["contains_fit_statistics"] == "false"
    assert summary["uses_kids_data_vector_values"] == "false"
    assert summary["uses_posterior_chains"] == "false"
    assert summary["uses_posthoc_selection"] == "false"
    assert summary["partial_control_scoring_allowed"] == "false"
    assert summary["endpoint_scoring_allowed"] == "false"
    with (
        ROOT / "data/derived/kids1000_cosebis_partial_control_mapping_values_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 900
    assert [row["shell_row_index_zero_based"] for row in rows] == [str(i) for i in range(900)]
    assert len({row["target_row_index_zero_based"] for row in rows}) == 300
    assert len({row["mask_sample_index_zero_based"] for row in rows}) == 3
    for row in rows:
        assert row["mapping_values_policy_id"] == policy["policy_id"]
        assert row["formula_id"] == policy["formula_id"]
        assert row["partial_mapping_values_computed"] == "true"
        assert row["contains_partial_mapping_values"] == "true"
        assert row["contains_endpoint_mapping_vector"] == "false"
        assert row["contains_theory_vector"] == "false"
        assert row["contains_prediction"] == "false"
        assert row["contains_residual"] == "false"
        assert row["contains_fit_statistic"] == "false"
        assert row["uses_kids_data_vector_values"] == "false"
        assert row["uses_posterior_chains"] == "false"
        assert row["uses_posthoc_selection"] == "false"
        assert row["partial_control_scoring_allowed"] == "false"
        assert row["endpoint_scoring_allowed"] == "false"
        expected = (
            float(row["source_mask_shell_value"])
            * float(row["normalized_pair_mean_z_weight"])
            * float(row["mode_decay_weight"])
        )
        assert abs(float(row["partial_mapping_value"]) - expected) < 5e-11


def test_kids1000_cosebis_partial_control_design_matrix_is_not_scoring() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_partial_control_design_matrix_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert policy["status"] == "KIDS1000_COSEBIS_PARTIAL_CONTROL_DESIGN_MATRIX_POLICY_FROZEN_SOURCE_ONLY"
    branches = policy["branch_set"].split(";")
    assert branches == [
        "baseline_zero",
        "mask_sample_0",
        "mask_sample_98",
        "mask_sample_195",
        "positive_mask_mean",
        "sign_flip_positive_mean",
    ]
    assert policy["expected_target_rows"] == "300"
    assert policy["expected_branch_count"] == "6"
    assert policy["current_design_matrix_built"] == "false"
    assert policy["current_partial_control_scoring_allowed"] == "false"
    assert policy["current_endpoint_scoring_allowed"] == "false"
    with (
        ROOT / "data/derived/kids1000_cosebis_partial_control_design_matrix_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "KIDS1000_COSEBIS_PARTIAL_CONTROL_DESIGN_MATRIX_BUILT_SOURCE_ONLY_NOT_SCORED"
    assert summary["target_rows"] == "300"
    assert summary["branch_count"] == "6"
    assert summary["design_matrix_built"] == "true"
    assert summary["contains_partial_control_candidate_vectors"] == "true"
    assert summary["contains_endpoint_theory_vector"] == "false"
    assert summary["contains_predictions"] == "false"
    assert summary["contains_residuals"] == "false"
    assert summary["contains_fit_statistics"] == "false"
    assert summary["uses_kids_data_vector_values"] == "false"
    assert summary["uses_posterior_chains"] == "false"
    assert summary["uses_posthoc_selection"] == "false"
    assert summary["partial_control_scoring_allowed"] == "false"
    assert summary["endpoint_scoring_allowed"] == "false"
    with (
        ROOT / "data/derived/kids1000_cosebis_partial_control_design_matrix_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 300
    assert [row["target_row_index_zero_based"] for row in rows] == [str(i) for i in range(300)]
    for row in rows:
        assert row["contains_partial_control_candidate_vectors"] == "true"
        assert row["contains_endpoint_theory_vector"] == "false"
        assert row["contains_prediction"] == "false"
        assert row["contains_residual"] == "false"
        assert row["contains_fit_statistic"] == "false"
        assert row["uses_kids_data_vector_values"] == "false"
        assert row["uses_posterior_chains"] == "false"
        assert row["uses_posthoc_selection"] == "false"
        assert row["partial_control_scoring_allowed"] == "false"
        assert row["endpoint_scoring_allowed"] == "false"
        assert float(row["baseline_zero"]) == 0
        positive_mean = 0.5 * (float(row["mask_sample_98"]) + float(row["mask_sample_195"]))
        assert abs(float(row["positive_mask_mean"]) - positive_mean) < 5e-11
        assert abs(float(row["sign_flip_positive_mean"]) + positive_mean) < 5e-11


def test_kids1000_cosebis_partial_control_diagnostic_scoring_is_not_endpoint() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_partial_control_diagnostic_scoring_v1.csv"
    ).open(newline="") as f:
        manifest = list(csv.DictReader(f))[0]
    assert manifest["status"] == "PARTIAL_CONTROL_DIAGNOSTIC_SCORING_NOT_ENDPOINT_VALIDATION"
    assert manifest["partial_control_scoring_allowed"] == "true"
    assert manifest["endpoint_scoring_allowed"] == "false"
    assert "nonnegative_amplitude" in manifest["amplitude_policy"]
    for marker in [
        "kids_data_vector_values_for_source_selection",
        "posterior_chains",
        "lensing_residuals_for_source_or_branch_selection",
        "posthoc_mask_subset_selection",
        "posthoc_weight_selection",
    ]:
        assert marker in manifest["forbidden_inputs"]
    assert "retained_En_data_vector_values_for_scoring_only" in manifest["allowed_inputs"]
    assert "full_COVMAT_covariance_for_scoring_only" in manifest["allowed_inputs"]
    with (
        ROOT / "data/derived/kids1000_cosebis_partial_control_diagnostic_scoring_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == manifest["status"]
    assert summary["n_rows"] == "300"
    assert summary["branch_count"] == "6"
    assert summary["partial_control_scoring_executed"] == "true"
    assert summary["endpoint_scoring_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["uses_kids_data_vector_values_for_scoring"] == "true"
    assert summary["uses_kids_data_vector_values_for_source_selection"] == "false"
    assert summary["uses_posterior_chains"] == "false"
    assert summary["uses_posthoc_selection"] == "false"
    assert summary["claim_boundary"] == "partial_control_diagnostic_scoring_not_endpoint_not_validation"
    assert float(summary["covariance_min_eigenvalue"]) > 0
    assert float(summary["covariance_condition_number"]) > 0
    with (
        ROOT / "data/derived/kids1000_cosebis_partial_control_diagnostic_scoring_v1_grid.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    branches = {row["branch"] for row in rows}
    assert branches == {
        "baseline_zero",
        "mask_sample_0",
        "mask_sample_98",
        "mask_sample_195",
        "positive_mask_mean",
        "sign_flip_positive_mean",
    }
    assert len(rows) == 6
    baseline = next(row for row in rows if row["branch"] == "baseline_zero")
    assert float(baseline["best_nonnegative_amplitude"]) == 0
    baseline_chi2 = float(baseline["chi2"])
    assert abs(float(summary["baseline_chi2"]) - baseline_chi2) < 5e-8
    best = min(rows, key=lambda row: float(row["chi2"]))
    assert summary["best_branch"] == best["branch"]
    assert float(summary["best_delta_chi2_vs_baseline"]) <= 0
    for row in rows:
        assert row["claim_boundary"] == summary["claim_boundary"]
        assert row["endpoint_scoring_allowed"] == "false"
        assert row["uses_kids_data_vector_values_for_scoring"] == "true"
        assert row["uses_kids_data_vector_values_for_source_selection"] == "false"
        assert row["uses_posterior_chains"] == "false"
        assert row["uses_posthoc_selection"] == "false"
        assert float(row["best_nonnegative_amplitude"]) >= 0
        assert abs(float(row["delta_chi2_vs_baseline"]) - (float(row["chi2"]) - baseline_chi2)) < 5e-8


def test_kids1000_cosebis_partial_control_null_replay_is_not_endpoint() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_partial_control_null_replay_v1.csv"
    ).open(newline="") as f:
        manifest = list(csv.DictReader(f))[0]
    assert manifest["status"] == "PARTIAL_CONTROL_NULL_REPLAY_NOT_ENDPOINT_VALIDATION"
    assert manifest["partial_control_scoring_allowed"] == "true"
    assert manifest["endpoint_scoring_allowed"] == "false"
    assert "predeclared_null_control_seed_inventory" in manifest["allowed_inputs"]
    for marker in [
        "kids_data_vector_values_for_source_selection",
        "posterior_chains",
        "lensing_residuals_for_source_or_branch_selection",
        "posthoc_mask_subset_selection",
        "posthoc_weight_selection",
    ]:
        assert marker in manifest["forbidden_inputs"]
    with (
        ROOT / "data/derived/kids1000_cosebis_partial_control_null_replay_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == manifest["status"]
    assert summary["observed_branch"] == "positive_mask_mean"
    assert summary["null_draws"] == "1008"
    assert summary["partial_control_null_replay_executed"] == "true"
    assert summary["endpoint_scoring_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["uses_kids_data_vector_values_for_scoring"] == "true"
    assert summary["uses_kids_data_vector_values_for_source_selection"] == "false"
    assert summary["uses_posterior_chains"] == "false"
    assert summary["uses_posthoc_selection"] == "false"
    assert summary["claim_boundary"] == "partial_control_null_replay_not_endpoint_not_validation"
    assert summary["null_chi2_le_observed_count"] == "1"
    assert summary["null_aic_le_observed_count"] == "1"
    assert abs(float(summary["plus_one_tail_fraction_chi2_le_observed"]) - 0.001982160555) < 5e-13
    assert abs(float(summary["plus_one_tail_fraction_aic_le_observed"]) - 0.001982160555) < 5e-13
    with (
        ROOT / "data/derived/kids1000_cosebis_partial_control_null_replay_v1_grid.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 1008
    family_counts = {
        family: sum(row["control_family"] == family for row in rows)
        for family in {row["control_family"] for row in rows}
    }
    assert family_counts == {
        "sky_rotation": 4,
        "tomographic_pair_shuffle": 1000,
        "wrong_channel_activation": 2,
        "web_path_sign_flip": 2,
    }
    observed_chi2 = float(summary["observed_chi2"])
    observed_aic = float(summary["observed_aic"])
    chi2_le = sum(float(row["chi2"]) <= observed_chi2 + 1e-10 for row in rows)
    aic_le = sum(float(row["aic"]) <= observed_aic + 1e-10 for row in rows)
    assert chi2_le == int(summary["null_chi2_le_observed_count"])
    assert aic_le == int(summary["null_aic_le_observed_count"])
    assert abs(float(summary["plus_one_tail_fraction_chi2_le_observed"]) - ((chi2_le + 1) / (len(rows) + 1))) < 5e-13
    assert abs(float(summary["plus_one_tail_fraction_aic_le_observed"]) - ((aic_le + 1) / (len(rows) + 1))) < 5e-13
    best = min(rows, key=lambda row: float(row["chi2"]))
    assert summary["best_null_family"] == best["control_family"]
    assert summary["best_null_descriptor"] == best["control_descriptor"]
    assert float(summary["best_null_chi2"]) == float(best["chi2"])
    assert float(summary["best_null_chi2"]) < observed_chi2
    for row in rows:
        assert row["claim_boundary"] == summary["claim_boundary"]
        assert row["endpoint_scoring_allowed"] == "false"
        assert row["uses_kids_data_vector_values_for_scoring"] == "true"
        assert row["uses_kids_data_vector_values_for_source_selection"] == "false"
        assert row["uses_posterior_chains"] == "false"
        assert row["uses_posthoc_selection"] == "false"
        assert float(row["best_nonnegative_amplitude"]) >= 0


def test_kids1000_cosebis_partial_control_degeneracy_audit_blocks_endpoint() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_partial_control_degeneracy_audit_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert policy["status"] == "PARTIAL_CONTROL_DEGENERACY_AUDIT_NOT_ENDPOINT_VALIDATION"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert "kids_data_vector_values" in policy["forbidden_inputs"]
    assert "full_COVMAT_covariance_for_geometry_metric_only" in policy["allowed_inputs"]
    with (
        ROOT / "data/derived/kids1000_cosebis_partial_control_degeneracy_audit_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "PARTIAL_CONTROL_DEGENERACY_AUDIT_BUILT_NOT_ENDPOINT_VALIDATION"
    assert summary["positive_effective_rank_tol_1e_minus_8"] == "1"
    assert summary["branch_degeneracy_detected"] == "true"
    assert summary["endpoint_scoring_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["uses_kids_data_vector_values"] == "false"
    assert summary["uses_kids_covariance_for_metric_only"] == "true"
    assert summary["uses_posterior_chains"] == "false"
    assert summary["uses_posthoc_selection"] == "false"
    assert summary["claim_boundary"] == policy["claim_boundary"]
    assert float(summary["min_positive_abs_covariance_inverse_cosine"]) >= 0.999999999
    assert float(summary["max_positive_relative_shape_residual"]) <= 1e-9
    assert summary["positive_sign_flip_covariance_inverse_cosine"] == "-1"
    assert "non_degenerate_source_frozen_full_route" in summary["recommended_next_action"]
    with (
        ROOT / "data/derived/kids1000_cosebis_partial_control_degeneracy_audit_v1_pair_grid.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 10
    positive_pairs = [
        row
        for row in rows
        if row["branch_left"] in {"mask_sample_98", "mask_sample_195", "positive_mask_mean"}
        and row["branch_right"] in {"mask_sample_98", "mask_sample_195", "positive_mask_mean"}
    ]
    assert len(positive_pairs) == 3
    for row in rows:
        assert row["endpoint_scoring_allowed"] == "false"
        assert row["uses_kids_data_vector_values"] == "false"
        assert row["uses_kids_covariance_for_metric_only"] == "true"
        assert row["uses_posterior_chains"] == "false"
        assert row["uses_posthoc_selection"] == "false"
        assert row["claim_boundary"] == policy["claim_boundary"]
    for row in positive_pairs:
        assert abs(float(row["covariance_inverse_cosine"])) >= 0.999999999
        assert float(row["relative_shape_residual_left_on_right"]) <= 1e-9


def test_kids1000_cosebis_endpoint_family_geometry_audit_passes_without_scoring() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_endpoint_family_geometry_audit_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert policy["status"] == "KIDS1000_COSEBIS_ENDPOINT_FAMILY_GEOMETRY_AUDIT_POLICY_FROZEN_NOT_SCORED"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert policy["minimum_effective_rank"] == "2"
    for marker in [
        "kids_data_vector_values",
        "lensing_residuals",
        "fit_improvement_flags",
        "posthoc_weight_selection",
    ]:
        assert marker in policy["forbidden_inputs"]
    with (
        ROOT / "data/derived/kids1000_cosebis_endpoint_family_geometry_audit_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "KIDS1000_COSEBIS_ENDPOINT_FAMILY_GEOMETRY_AUDIT_BUILT_NOT_SCORED"
    assert summary["family_vector_count"] == "1009"
    assert summary["target_rows"] == "300"
    assert int(summary["raw_effective_rank_tol_1e_minus_8"]) >= 2
    assert int(summary["covariance_metric_effective_rank_tol_1e_minus_8"]) >= 2
    assert summary["endpoint_family_geometry_passed"] == "true"
    assert summary["contains_theory_vector"] == "true"
    assert summary["contains_control_scores"] == "false"
    assert summary["contains_predictions"] == "false"
    assert summary["contains_residuals"] == "false"
    assert summary["contains_fit_statistics"] == "false"
    assert summary["endpoint_scoring_allowed"] == "false"
    with (
        ROOT / "data/derived/kids1000_cosebis_endpoint_family_geometry_audit_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 1009
    assert sum(row["vector_family"] == "candidate" for row in rows) == 1
    assert {row["target_rows"] for row in rows} == {"300"}
    assert all(row["contains_control_scores"] == "false" for row in rows)
    assert all(row["contains_residuals"] == "false" for row in rows)
    assert all(row["uses_kids_data_vector_values"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)


def test_kids1000_cosebis_non_degenerate_mapping_promotion_gate_passes_not_scored() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_non_degenerate_mapping_promotion_gate_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert policy["status"] == "NON_DEGENERATE_MAPPING_PROMOTION_GATE_FROZEN_NOT_PASSED"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert "endpoint_candidate_family_must_not_be_effectively_rank_one" in policy["rank_threshold_policy"]
    for marker in [
        "kids_data_vector_values",
        "posterior_chains",
        "lensing_residuals",
        "posthoc_weight_selection",
        "posthoc_mask_subset_selection",
    ]:
        assert marker in policy["forbidden_inputs"]
    with (
        ROOT / "data/derived/kids1000_cosebis_non_degenerate_mapping_promotion_gate_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "NON_DEGENERATE_MAPPING_PROMOTION_GATE_PASSED_NOT_SCORED"
    assert summary["gate_count"] == "6"
    assert summary["passed_gate_count"] == "6"
    assert summary["blocking_gate_count"] == "0"
    assert summary["first_blocking_gate"] == "none"
    assert summary["non_degenerate_mapping_promotion_allowed"] == "true"
    assert summary["endpoint_scoring_allowed"] == "false"
    assert summary["scoring_executed"] == "false"
    assert summary["contains_theory_vector"] == "true"
    assert summary["contains_predictions"] == "false"
    assert summary["contains_residuals"] == "false"
    assert summary["contains_fit_statistics"] == "false"
    assert summary["uses_kids_data_vector_values"] == "false"
    assert summary["uses_posterior_chains"] == "false"
    assert summary["uses_posthoc_selection"] == "false"
    assert summary["claim_boundary"] == policy["claim_boundary"]
    with (
        ROOT / "data/derived/kids1000_cosebis_non_degenerate_mapping_promotion_gate_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    by_gate = {row["gate_id"]: row for row in rows}
    assert set(by_gate) == {
        "PROMOTE_01_F_OVERLAP_ENDPOINT_ROUTE",
        "PROMOTE_02_SOURCE_PREFLIGHT_MAPPING_READY",
        "PROMOTE_03_NON_DEGENERATE_BRANCH_GEOMETRY",
        "PROMOTE_04_THEORY_VECTOR_COMPUTED",
        "PROMOTE_05_NULL_CONTROLS_EXECUTED_AFTER_MAPPING",
        "PROMOTE_06_LEAKAGE_GUARDS",
    }
    assert by_gate["PROMOTE_01_F_OVERLAP_ENDPOINT_ROUTE"]["blocking_status"] == "not_blocking"
    assert by_gate["PROMOTE_01_F_OVERLAP_ENDPOINT_ROUTE"]["gate_passed"] == "true"
    assert by_gate["PROMOTE_04_THEORY_VECTOR_COMPUTED"]["blocking_status"] == "not_blocking"
    assert by_gate["PROMOTE_04_THEORY_VECTOR_COMPUTED"]["gate_passed"] == "true"
    assert by_gate["PROMOTE_02_SOURCE_PREFLIGHT_MAPPING_READY"]["blocking_status"] == "not_blocking"
    assert by_gate["PROMOTE_02_SOURCE_PREFLIGHT_MAPPING_READY"]["gate_passed"] == "true"
    assert by_gate["PROMOTE_03_NON_DEGENERATE_BRANCH_GEOMETRY"]["blocking_status"] == "not_blocking"
    assert by_gate["PROMOTE_03_NON_DEGENERATE_BRANCH_GEOMETRY"]["gate_passed"] == "true"
    assert "partial_positive_rank_1" in by_gate["PROMOTE_03_NON_DEGENERATE_BRANCH_GEOMETRY"]["current_state"]
    assert "endpoint_passed_true" in by_gate["PROMOTE_03_NON_DEGENERATE_BRANCH_GEOMETRY"]["current_state"]
    assert by_gate["PROMOTE_05_NULL_CONTROLS_EXECUTED_AFTER_MAPPING"]["blocking_status"] == "not_blocking"
    assert by_gate["PROMOTE_05_NULL_CONTROLS_EXECUTED_AFTER_MAPPING"]["gate_passed"] == "true"
    assert by_gate["PROMOTE_06_LEAKAGE_GUARDS"]["gate_passed"] == "true"
    for gate_id, row in by_gate.items():
        assert row["gate_passed"] == "true"
        assert row["endpoint_scoring_allowed"] == "false"
        assert row["scoring_executed"] == "false"
        assert row["uses_kids_data_vector_values"] == "false"
        assert row["uses_posterior_chains"] == "false"
        assert row["uses_posthoc_selection"] == "false"
        if gate_id == "PROMOTE_04_THEORY_VECTOR_COMPUTED":
            assert row["contains_theory_vector"] == "true"
        else:
            assert row["contains_theory_vector"] == "false"
        assert row["contains_predictions"] == "false"
        assert row["contains_residuals"] == "false"
        assert row["contains_fit_statistics"] == "false"
        assert row["claim_boundary"] == policy["claim_boundary"]


def test_kids1000_cosebis_f_overlap_execution_review_schema_is_not_execution() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_f_overlap_execution_review_schema_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert policy["status"] == "KIDS1000_COSEBIS_F_OVERLAP_EXECUTION_REVIEW_SCHEMA_DECLARED_NOT_EXECUTED"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert policy["current_execution_review_artifact_present"] == "false"
    assert policy["current_external_products_fetched"] == "false"
    assert policy["current_overlap_rule_computed"] == "false"
    with (
        ROOT / "data/derived/kids1000_cosebis_f_overlap_execution_review_schema_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "KIDS1000_COSEBIS_F_OVERLAP_EXECUTION_REVIEW_SCHEMA_BUILT_NOT_EXECUTED"
    assert summary["schema_column_count"] == "29"
    assert summary["forbidden_true_column_count"] == "13"
    assert summary["promotion_ready"] == "false"
    assert summary["current_execution_review_artifact_present"] == "false"
    assert summary["external_products_fetched"] == "false"
    assert summary["overlap_rule_computed"] == "false"
    assert summary["path_mapping_computed"] == "false"
    assert summary["contains_mapping_vector"] == "false"
    assert summary["contains_theory_vector"] == "false"
    assert summary["endpoint_scoring_allowed"] == "false"
    with (
        ROOT / "data/derived/kids1000_cosebis_f_overlap_execution_review_schema_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 29
    by_column = {row["column_name"]: row for row in rows}
    for column in [
        "batch_id",
        "tile_index_zero_based",
        "mask_product_url",
        "expected_cache_path",
        "fetch_status",
        "sha256",
        "review_artifact_status",
        "forbidden_inputs_used",
        "uses_kids_data_vector_values",
        "uses_posterior_chains",
        "uses_lensing_residuals",
        "uses_fit_improvement_flags",
        "uses_posthoc_tile_selection",
        "overlap_rule_computed",
        "path_mapping_computed",
        "contains_theory_vector",
        "contains_residuals",
        "endpoint_scoring_allowed",
        "claim_boundary",
    ]:
        assert column in by_column
    for column in [
        "uses_kids_data_vector_values",
        "uses_posterior_chains",
        "uses_lensing_residuals",
        "uses_fit_improvement_flags",
        "uses_posthoc_tile_selection",
        "overlap_rule_computed",
        "path_mapping_computed",
        "contains_mapping_vector",
        "contains_theory_vector",
        "contains_predictions",
        "contains_residuals",
        "contains_fit_statistics",
        "endpoint_scoring_allowed",
    ]:
        assert by_column[column]["forbidden_if_true"] == "true"
    assert all(row["external_products_fetched"] == "false" for row in rows)
    assert all(row["overlap_rule_computed"] == "false" for row in rows)
    assert all(row["path_mapping_computed"] == "false" for row in rows)
    assert all(row["contains_mapping_vector"] == "false" for row in rows)
    assert all(row["contains_theory_vector"] == "false" for row in rows)
    assert all(row["contains_predictions"] == "false" for row in rows)
    assert all(row["contains_residuals"] == "false" for row in rows)
    assert all(row["contains_fit_statistics"] == "false" for row in rows)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)


def test_kids1000_cosebis_f_overlap_execution_review_template_is_empty() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_f_overlap_execution_review_template_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert policy["status"] == "KIDS1000_COSEBIS_F_OVERLAP_EXECUTION_REVIEW_TEMPLATE_DECLARED_NOT_EXECUTED"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert policy["current_execution_review_artifact_present"] == "false"
    assert policy["current_external_products_fetched"] == "false"
    with (
        ROOT / "data/derived/kids1000_cosebis_f_overlap_execution_review_schema_v1.csv"
    ).open(newline="") as f:
        schema_rows = list(csv.DictReader(f))
    expected_columns = [row["column_name"] for row in sorted(schema_rows, key=lambda row: int(row["column_order"]))]
    with (
        ROOT / "data/derived/kids1000_cosebis_f_overlap_execution_review_template_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "KIDS1000_COSEBIS_F_OVERLAP_EXECUTION_REVIEW_TEMPLATE_BUILT_NOT_EXECUTED"
    assert summary["batch_id"] == "F_OVERLAP_FULL_MASK_BATCH_00"
    assert summary["template_row_count"] == "20"
    assert summary["schema_column_count"] == "29"
    assert summary["template_fetch_mode"] == "template_not_executed"
    assert summary["template_fetch_status"] == "template_not_fetched"
    assert summary["current_execution_review_artifact_present"] == "false"
    assert summary["external_products_fetched"] == "false"
    assert summary["overlap_rule_computed"] == "false"
    assert summary["path_mapping_computed"] == "false"
    assert summary["contains_mapping_vector"] == "false"
    assert summary["contains_theory_vector"] == "false"
    assert summary["endpoint_scoring_allowed"] == "false"
    with (
        ROOT / "data/derived/kids1000_cosebis_f_overlap_execution_review_template_v1.csv"
    ).open(newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert reader.fieldnames == expected_columns
    assert len(rows) == 20
    assert all(row["batch_id"] == "F_OVERLAP_FULL_MASK_BATCH_00" for row in rows)
    assert all(row["fetch_mode"] == "template_not_executed" for row in rows)
    assert all(row["fetch_status"] == "template_not_fetched" for row in rows)
    assert all(row["http_status"] == "" for row in rows)
    assert all(row["byte_count"] == "" for row in rows)
    assert all(row["sha256"] == "" for row in rows)
    assert all(row["fetched_at_utc"] == "" for row in rows)
    assert all(row["review_artifact_status"] == "template_pending_manual_execution_review" for row in rows)
    assert all(row["reviewer_id_or_role"] == "" for row in rows)
    for key in [
        "forbidden_inputs_used",
        "uses_kids_data_vector_values",
        "uses_posterior_chains",
        "uses_lensing_residuals",
        "uses_fit_improvement_flags",
        "uses_posthoc_tile_selection",
        "overlap_rule_computed",
        "path_mapping_computed",
        "contains_mapping_vector",
        "contains_theory_vector",
        "contains_predictions",
        "contains_residuals",
        "contains_fit_statistics",
        "endpoint_scoring_allowed",
    ]:
        assert all(row[key] == "false" for row in rows)


def test_kids1000_cosebis_path_mapping_source_preflight_has_source_mapping_only() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_path_mapping_source_preflight_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert policy["status"] == "KIDS1000_COSEBIS_PATH_MAPPING_SOURCE_PREFLIGHT_POLICY_FROZEN_NOT_SCORED"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert policy["current_path_mapping_computed"] == "false"
    assert policy["current_theory_vector_computed"] == "false"
    assert policy["preflight_rule"] == "component_level_source_availability_ledger_for_future_cosebis_path_mapping"
    for marker in [
        "kids_data_vector_values",
        "posterior_chains",
        "lensing_residuals",
        "fit_improvement_flags",
        "posthoc_path_projection_labels",
        "posthoc_sky_direction_selection",
        "posthoc_web_environment_labels",
    ]:
        assert marker in policy["forbidden_inputs"]
    with (
        ROOT / "data/derived/kids1000_cosebis_path_mapping_source_preflight_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "KIDS1000_COSEBIS_PATH_MAPPING_SOURCE_PREFLIGHT_BUILT_MAPPING_AND_NULL_REPLAY_AVAILABLE_NOT_SCORED"
    assert summary["component_count"] == "11"
    assert summary["available_component_count"] == "6"
    assert summary["partial_available_component_count"] == "1"
    assert summary["missing_component_count"] == "0"
    assert summary["declared_not_executed_component_count"] == "0"
    assert summary["declared_not_computed_component_count"] == "0"
    assert summary["target_rows"] == "300"
    assert summary["mapping_ready"] == "true"
    assert summary["endpoint_scoring_allowed"] == "false"
    assert summary["path_mapping_computed"] == "true"
    assert summary["contains_mapping_vector"] == "true"
    assert summary["contains_theory_vector"] == "false"
    assert summary["contains_predictions"] == "false"
    assert summary["contains_residuals"] == "false"
    assert summary["uses_kids_data_vector_values"] == "false"
    with (
        ROOT / "data/derived/kids1000_cosebis_path_mapping_source_preflight_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    by_component = {row["component_id"]: row for row in rows}
    assert set(by_component) == {
        "cosebis_target_rows",
        "redshift_kernel_inventory",
        "mask_observable_shell",
        "preferred_route_tile_inventory",
        "cosebis_path_mapping_design_skeleton",
        "cosebis_path_mapping_domain_skeleton",
        "path_weight_construction_rule",
        "source_frozen_mapping_vector",
        "full_path_depth_footprint_mapping",
        "web_environment_catalog",
        "null_control_theory_replay",
    }
    assert by_component["cosebis_target_rows"]["source_state"] == "available"
    assert by_component["redshift_kernel_inventory"]["source_state"] == "available"
    assert by_component["mask_observable_shell"]["source_state"] == "partial_available_control"
    assert by_component["mask_observable_shell"]["source_count"] == "3"
    assert by_component["preferred_route_tile_inventory"]["source_state"] == "available"
    assert by_component["preferred_route_tile_inventory"]["source_count"] == "196"
    assert by_component["cosebis_path_mapping_design_skeleton"]["source_state"] == "available"
    assert by_component["cosebis_path_mapping_design_skeleton"]["source_count"] == "300"
    assert by_component["cosebis_path_mapping_domain_skeleton"]["source_state"] == "available"
    assert by_component["cosebis_path_mapping_domain_skeleton"]["source_count"] == "58800"
    assert by_component["path_weight_construction_rule"]["source_state"] == "available_source_side_normalized_factor_rule"
    assert by_component["path_weight_construction_rule"]["source_count"] == "7"
    assert by_component["source_frozen_mapping_vector"]["source_state"] == "available"
    assert by_component["source_frozen_mapping_vector"]["source_count"] == "300"
    assert by_component["source_frozen_mapping_vector"]["blocking_status"] == "not_blocking"
    assert (
        by_component["full_path_depth_footprint_mapping"]["source_state"]
        == "available_caveated_mask_load_proxy"
    )
    assert by_component["full_path_depth_footprint_mapping"]["source_count"] == "196"
    assert by_component["full_path_depth_footprint_mapping"]["blocking_status"] == "not_blocking"
    assert by_component["web_environment_catalog"]["source_state"] == "available_uniform_null_web_control"
    assert by_component["web_environment_catalog"]["source_count"] == "196"
    assert by_component["web_environment_catalog"]["blocking_status"] == "not_blocking"
    assert by_component["null_control_theory_replay"]["source_state"] == "available_control_theory_replay_not_scored"
    assert by_component["null_control_theory_replay"]["source_count"] == "1008"
    assert by_component["null_control_theory_replay"]["blocking_status"] == "not_blocking"
    for row in rows:
        assert row["target_rows"] == "300"
        if row["component_id"] == "source_frozen_mapping_vector":
            assert row["path_mapping_computed"] == "true"
            assert row["contains_mapping_vector"] == "true"
        else:
            assert row["path_mapping_computed"] == "false"
            assert row["contains_mapping_vector"] == "false"
        assert row["contains_theory_vector"] == "false"
        assert row["contains_predictions"] == "false"
        assert row["contains_residuals"] == "false"
        assert row["uses_kids_data_vector_values"] == "false"
        assert row["endpoint_scoring_allowed"] == "false"


def test_kids1000_cosebis_endpoint_scoring_readiness_is_not_scoring() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_endpoint_scoring_readiness_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert policy["status"] == "KIDS1000_COSEBIS_ENDPOINT_SCORING_READINESS_POLICY_FROZEN_NOT_SCORED"
    assert policy["current_endpoint_scoring_allowed"] == "false"
    assert policy["current_scoring_executed"] == "false"
    assert policy["required_blocker_resolution"] == "F_overlap_before_D_path_E_web_C_norm_mapping_or_scoring"
    for marker in [
        "kids_data_vector_values_for_source_selection",
        "posterior_chains",
        "lensing_residuals",
        "posthoc_channel_activation",
        "posthoc_weight_selection",
    ]:
        assert marker in policy["forbidden_inputs"]

    with (
        ROOT / "data/derived/kids1000_cosebis_endpoint_scoring_readiness_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "KIDS1000_COSEBIS_ENDPOINT_SCORING_READINESS_BUILT_NOT_SCORED"
    assert summary["component_count"] == "12"
    assert summary["ready_component_count"] == "12"
    assert summary["blocking_component_count"] == "0"
    assert summary["first_blocker"] == "none"
    assert summary["next_action"] == "endpoint_scoring_protocol_can_be_run_after_explicit_user_approval"
    assert summary["endpoint_scoring_allowed"] == "false"
    assert summary["scoring_executed"] == "false"
    assert summary["contains_predictions"] == "false"
    assert summary["contains_residuals"] == "false"
    assert summary["contains_fit_statistics"] == "false"

    with (ROOT / "data/derived/kids1000_cosebis_endpoint_scoring_readiness_v1.csv").open(
        newline=""
    ) as f:
        rows = list(csv.DictReader(f))
    by_component = {row["component_id"]: row for row in rows}
    assert set(by_component) == {
        "data_vector_structure",
        "covariance_matrix",
        "covariance_solve_policy",
        "theory_vector_template",
        "mapping_template_join_contract",
        "theory_vector",
        "web_path_mapping",
        "source_preflight",
        "blocker_resolution_order",
        "f_overlap_resolution_decision",
        "null_controls",
        "endpoint_family_geometry_audit",
    }
    assert by_component["data_vector_structure"]["ready_for_scoring"] == "true"
    assert by_component["covariance_matrix"]["ready_for_scoring"] == "true"
    assert by_component["covariance_solve_policy"]["ready_for_scoring"] == "true"
    assert by_component["theory_vector_template"]["readiness_note"] == "300_row_interface_no_theory_values"
    assert (
        by_component["mapping_template_join_contract"]["readiness_note"]
        == "300_row_join_contract_no_mapping_values"
    )
    assert by_component["theory_vector"]["blocking_status"] == "not_blocking"
    assert by_component["theory_vector"]["ready_for_scoring"] == "true"
    assert (
        by_component["theory_vector"]["readiness_note"]
        == "300_row_source_frozen_theory_vector_no_endpoint_score"
    )
    assert by_component["web_path_mapping"]["blocking_status"] == "not_blocking"
    assert by_component["web_path_mapping"]["ready_for_scoring"] == "true"
    assert by_component["source_preflight"]["blocking_status"] == "not_blocking"
    assert by_component["source_preflight"]["ready_for_scoring"] == "true"
    assert by_component["blocker_resolution_order"]["readiness_note"] == "path_first_blocker_none"
    assert by_component["blocker_resolution_order"]["blocking_status"] == "not_blocking"
    assert (
        by_component["f_overlap_resolution_decision"]["readiness_note"]
        == "endpoint_true_control_true"
    )
    assert by_component["null_controls"]["blocking_status"] == "not_blocking"
    assert by_component["null_controls"]["ready_for_scoring"] == "true"
    assert "control_theory_replay_draws_1008" in by_component["null_controls"]["readiness_note"]
    assert by_component["endpoint_family_geometry_audit"]["blocking_status"] == "not_blocking"
    assert by_component["endpoint_family_geometry_audit"]["ready_for_scoring"] == "true"
    assert "partial_positive_rank_1" in by_component["endpoint_family_geometry_audit"]["readiness_note"]
    assert "endpoint_raw_rank_" in by_component["endpoint_family_geometry_audit"]["readiness_note"]
    for row in rows:
        assert row["endpoint_scoring_allowed"] == "false"
        assert row["scoring_executed"] == "false"
        assert row["contains_predictions"] == "false"
        assert row["contains_residuals"] == "false"
        assert row["contains_fit_statistics"] == "false"
        assert row["uses_posterior_chains"] == "false"
        assert row["uses_posthoc_selection"] == "false"


def test_kids1000_cosebis_endpoint_scoring_protocol_is_frozen_with_approved_run() -> None:
    with (ROOT / "data/source_manifest/kids1000_cosebis_endpoint_scoring_protocol_v1.csv").open(
        newline=""
    ) as f:
        protocol = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_endpoint_scoring_readiness_v1_summary.csv"
    ).open(newline="") as f:
        readiness = list(csv.DictReader(f))[0]
    assert protocol["status"] == "SCORING_PROTOCOL_FROZEN_NOT_RUN"
    assert protocol["scoring_allowed"] == "false"
    assert protocol["parent_readiness_policy"] == readiness["policy_id"]
    assert readiness["endpoint_scoring_allowed"] == "false"
    assert readiness["first_blocker"] == "none"
    assert readiness["blocking_component_count"] == "0"
    assert "chi2=" in protocol["primary_score"]
    for marker in [
        "baseline_only",
        "web_path_candidate",
        "wrong_channel_controls",
        "shuffled_or_rotated_nulls",
        "AIC_delta",
        "control_rank",
    ]:
        assert marker in protocol["comparison_outputs"]
    for marker in [
        "source-ready",
        "controls executed",
        "predeclared null controls",
        "endpoint leakage flags",
    ]:
        assert marker in protocol["pass_condition_shell"]
    for marker in [
        "kids_data_vector_values_for_source_selection",
        "posterior_chains",
        "fit_improvement_flags",
        "lensing_residuals",
        "posthoc_channel_activation",
        "posthoc_weight_selection",
    ]:
        assert marker in protocol["forbidden_inputs"]
    with (ROOT / "data/source_manifest/kids1000_cosebis_endpoint_scoring_run_v1.csv").open(
        newline=""
    ) as f:
        run = list(csv.DictReader(f))[0]
    assert run["parent_scoring_protocol"] == protocol["protocol_id"]
    assert run["status"] == "ENDPOINT_SCORING_APPROVED_RUN_V1"
    assert run["endpoint_scoring_allowed"] == "true"
    assert run["explicit_user_approval_recorded"] == "true"
    assert "kids_data_vector_values_for_source_selection" in run["forbidden_inputs_for_source_selection"]
    assert "retained_300_row_En_data_vector_for_scoring_only" in run["allowed_endpoint_inputs"]


def test_kids1000_cosebis_endpoint_scoring_run_is_control_ranked_not_validation() -> None:
    with (ROOT / "data/source_manifest/kids1000_cosebis_endpoint_scoring_run_v1.csv").open(
        newline=""
    ) as f:
        run = list(csv.DictReader(f))[0]
    with (ROOT / "data/derived/kids1000_cosebis_endpoint_scoring_v1_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    with (ROOT / "data/derived/kids1000_cosebis_endpoint_scoring_v1_results.csv").open(
        newline=""
    ) as f:
        result = list(csv.DictReader(f))[0]
    with (ROOT / "data/derived/kids1000_cosebis_endpoint_scoring_v1_residuals.csv").open(
        newline=""
    ) as f:
        residuals = list(csv.DictReader(f))
    with (ROOT / "data/derived/kids1000_cosebis_endpoint_scoring_v1_null_controls.csv").open(
        newline=""
    ) as f:
        nulls = list(csv.DictReader(f))
    with (ROOT / "data/derived/kids1000_cosebis_endpoint_scoring_v1_grid.csv").open(
        newline=""
    ) as f:
        grid = list(csv.DictReader(f))

    assert run["endpoint_scoring_allowed"] == "true"
    assert run["explicit_user_approval_recorded"] == "true"
    assert summary["status"] == "KIDS1000_COSEBIS_ENDPOINT_SCORING_RUN_V1_COMPLETE"
    assert summary["endpoint_scoring_executed"] == "true"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["uses_kids_data_vector_values_for_scoring"] == "true"
    assert summary["uses_kids_data_vector_values_for_source_selection"] == "false"
    assert summary["uses_posterior_chains"] == "false"
    assert summary["uses_posthoc_selection"] == "false"
    assert summary["claim_boundary"] == run["claim_boundary"]
    assert result["claim_boundary"] == run["claim_boundary"]
    assert result["null_control_count"] == "1008"
    assert result["candidate_rank_by_chi2"] == "3"
    assert result["candidate_rank_by_aic"] == "3"
    assert result["chi2_nulls_better_than_candidate"] == "2"
    assert result["aic_nulls_better_than_candidate"] == "2"
    assert abs(float(result["candidate_delta_chi2_vs_baseline"]) + 183.6152665217) < 1e-8
    assert abs(float(result["candidate_delta_aic_vs_baseline"]) + 181.6152665217) < 1e-8
    assert abs(float(result["plus_one_tail_fraction_chi2"]) - 0.002973240832507) < 1e-15
    assert abs(float(result["plus_one_tail_fraction_aic"]) - 0.002973240832507) < 1e-15
    assert len(residuals) == 300
    assert len(nulls) == 1008
    assert len(grid) == 2
    assert {row["branch_type"] for row in grid} == {"baseline", "candidate"}
    for row in [result, summary, *residuals, *nulls]:
        assert row["uses_kids_data_vector_values_for_scoring"] == "true"
        assert row["uses_kids_data_vector_values_for_source_selection"] == "false"
    for row in [result, summary]:
        assert row["uses_posterior_chains"] == "false"
        assert row["uses_posthoc_selection"] == "false"
        assert row["endpoint_validation_claimed"] == "false"


def test_kids1000_cosebis_endpoint_scoring_diagnostics_localize_null_caveat() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_endpoint_scoring_diagnostics_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_endpoint_scoring_diagnostics_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_endpoint_scoring_diagnostics_v1_family_summary.csv"
    ).open(newline="") as f:
        family_rows = list(csv.DictReader(f))
    with (
        ROOT / "data/derived/kids1000_cosebis_endpoint_scoring_diagnostics_v1_top_nulls.csv"
    ).open(newline="") as f:
        top_rows = list(csv.DictReader(f))

    assert policy["status"] == "ENDPOINT_SCORING_DIAGNOSTICS_POLICY_FROZEN"
    assert policy["endpoint_validation_claimed"] == "false"
    assert "posthoc_source_selection" in policy["forbidden_future_use"]
    assert summary["status"] == "KIDS1000_COSEBIS_ENDPOINT_SCORING_DIAGNOSTICS_BUILT"
    assert summary["families_with_better_than_candidate"] == "tomographic_pair_shuffle"
    assert (
        summary["diagnostic_verdict"]
        == "candidate_low_tail_but_not_absolute_winner_tomographic_shuffle_controls_dominate"
    )
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["uses_kids_data_vector_values_for_scoring"] == "true"
    assert summary["uses_kids_data_vector_values_for_source_selection"] == "false"
    by_family = {row["control_family"]: row for row in family_rows}
    assert set(by_family) == {
        "sky_rotation",
        "tomographic_pair_shuffle",
        "web_path_sign_flip",
        "wrong_channel_activation",
    }
    assert by_family["tomographic_pair_shuffle"]["controls_better_than_candidate_chi2"] == "2"
    assert by_family["tomographic_pair_shuffle"]["controls_better_than_candidate_aic"] == "2"
    for family_id in ["sky_rotation", "web_path_sign_flip", "wrong_channel_activation"]:
        assert by_family[family_id]["controls_better_than_candidate_chi2"] == "0"
        assert by_family[family_id]["controls_better_than_candidate_aic"] == "0"
    assert len(top_rows) == 25
    assert top_rows[0]["control_family"] == "tomographic_pair_shuffle"
    assert top_rows[0]["beats_candidate_chi2"] == "true"
    assert top_rows[0]["endpoint_validation_claimed"] == "false"


def test_kids1000_cosebis_tomographic_structure_robustness_preserves_low_tail() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_tomographic_structure_robustness_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_tomographic_structure_robustness_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_tomographic_structure_robustness_v1_family_summary.csv"
    ).open(newline="") as f:
        family_rows = list(csv.DictReader(f))
    with (
        ROOT / "data/derived/kids1000_cosebis_tomographic_structure_robustness_v1_controls.csv"
    ).open(newline="") as f:
        controls = list(csv.DictReader(f))
    with (
        ROOT / "data/derived/kids1000_cosebis_tomographic_structure_robustness_v1_top_controls.csv"
    ).open(newline="") as f:
        top_rows = list(csv.DictReader(f))

    assert policy["status"] == "TOMOGRAPHIC_STRUCTURE_ROBUSTNESS_POLICY_FROZEN"
    assert policy["endpoint_validation_claimed"] == "false"
    assert "bin_label_permutation" in policy["control_families"]
    assert "auto_cross_preserving_shuffle" in policy["control_families"]
    assert summary["status"] == "KIDS1000_COSEBIS_TOMOGRAPHIC_STRUCTURE_ROBUSTNESS_COMPLETE"
    assert summary["control_count"] == "1119"
    assert summary["candidate_rank_by_chi2"] == "4"
    assert summary["candidate_rank_by_aic"] == "4"
    assert summary["controls_better_than_candidate_chi2"] == "3"
    assert summary["controls_better_than_candidate_aic"] == "3"
    assert abs(float(summary["plus_one_tail_fraction_chi2"]) - 0.003571428571429) < 1e-15
    assert summary["families_with_better_than_candidate"] == "auto_cross_preserving_shuffle;bin_label_permutation"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["uses_kids_data_vector_values_for_scoring"] == "true"
    assert summary["uses_kids_data_vector_values_for_source_selection"] == "false"
    assert len(controls) == 1119
    assert len(top_rows) == 25
    by_family = {row["control_family"]: row for row in family_rows}
    assert by_family["bin_label_permutation"]["control_count"] == "119"
    assert by_family["bin_label_permutation"]["controls_better_than_candidate_chi2"] == "1"
    assert by_family["auto_cross_preserving_shuffle"]["control_count"] == "1000"
    assert by_family["auto_cross_preserving_shuffle"]["controls_better_than_candidate_chi2"] == "2"
    for row in [summary, *family_rows, *top_rows, *controls]:
        assert row["endpoint_validation_claimed"] == "false"
        assert row["claim_boundary"] == policy["claim_boundary"]


def test_kids1000_cosebis_tomographic_control_plausibility_audit_blocks_physical_alternative_promotion() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_tomographic_control_plausibility_audit_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_tomographic_control_plausibility_audit_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_tomographic_control_plausibility_audit_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))

    assert policy["status"] == "TOMOGRAPHIC_CONTROL_PLAUSIBILITY_AUDIT_POLICY_FROZEN"
    assert policy["computes_new_scores"] == "false"
    assert policy["endpoint_validation_claimed"] == "false"
    assert summary["status"] == "TOMOGRAPHIC_CONTROL_PLAUSIBILITY_AUDIT_BUILT"
    assert summary["audited_top_control_count"] == "25"
    assert summary["better_than_candidate_audited_count"] == "3"
    assert summary["better_control_only_count"] == "2"
    assert summary["better_conditional_source_systematic_count"] == "1"
    assert summary["accepted_physical_alternative_count"] == "0"
    assert summary["candidate_tomographic_caveat_active"] == "true"
    assert summary["tomographic_controls_refute_endpoint_signal"] == "false"
    assert summary["tomographic_controls_block_validation"] == "true"
    assert (
        summary["verdict"]
        == "better_tomographic_controls_are_control_only_or_source_systematic_candidates_not_physical_alternatives"
    )
    better = [row for row in rows if row["beats_candidate_chi2"] == "true"]
    assert len(better) == 3
    assert {row["physical_alternative_status"] for row in better} == {
        "CONTROL_ONLY",
        "CONDITIONAL_SOURCE_SYSTEMATIC",
    }
    assert any(row["is_global_bin_permutation"] == "true" for row in better)
    assert any(row["is_global_bin_permutation"] == "false" for row in better)
    for row in rows:
        assert row["computes_new_scores"] == "false"
        assert row["uses_kids_data_vector_values_for_source_selection"] == "false"
        assert row["endpoint_validation_claimed"] == "false"
        assert row["claim_boundary"] == policy["claim_boundary"]


def test_kids1000_cosebis_tomographic_holdout_calibration_gate_blocks_replay_until_source_freeze() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_tomographic_holdout_calibration_gate_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_tomographic_holdout_calibration_gate_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_tomographic_holdout_calibration_gate_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))

    assert policy["status"] == "TOMOGRAPHIC_HOLDOUT_CALIBRATION_GATE_POLICY_FROZEN"
    assert policy["computes_new_scores"] == "false"
    assert policy["endpoint_replay_allowed"] == "false"
    assert policy["endpoint_validation_claimed"] == "false"
    assert "endpoint_residuals" in policy["forbidden_endpoint_fields"]
    assert "delta_chi2" in policy["forbidden_endpoint_fields"]
    assert summary["status"] == "TOMOGRAPHIC_HOLDOUT_CALIBRATION_GATE_BUILT"
    assert summary["required_steps"] == "6"
    assert summary["completed_steps"] == "0"
    assert summary["requires_independent_photoz_or_tomographic_calibration"] == "true"
    assert summary["requires_holdout_partition_freeze"] == "true"
    assert summary["requires_leakage_validator_before_replay"] == "true"
    assert summary["tomographic_controls_block_validation"] == "true"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["verdict"] == "tomographic_holdout_required_before_endpoint_replay_or_validation"
    assert {row["step_id"] for row in rows} == {
        "H0_context",
        "H1_independent_tomographic_evidence",
        "H2_holdout_partition_freeze",
        "H3_tomographic_alternative_promotion_rule",
        "H4_replay_protocol_freeze",
        "H5_authorization_gate",
    }
    for row in rows:
        assert row["endpoint_replay_allowed_after_step"] == "false"
        assert "endpoint_residuals" in row["forbidden_inputs"]
        assert row["claim_boundary"] == policy["claim_boundary"]
    assert summary["claim_boundary"] == policy["claim_boundary"]


def test_kids1000_cosebis_source_frozen_tomographic_holdout_manifest_freezes_h2_only() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_source_frozen_tomographic_holdout_manifest_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_source_frozen_tomographic_holdout_manifest_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_source_frozen_tomographic_holdout_bins_v1.csv"
    ).open(newline="") as f:
        bins = list(csv.DictReader(f))
    with (
        ROOT / "data/derived/kids1000_cosebis_source_frozen_tomographic_holdout_pairs_v1.csv"
    ).open(newline="") as f:
        pairs = list(csv.DictReader(f))

    assert policy["status"] == "SOURCE_FROZEN_TOMOGRAPHIC_HOLDOUT_MANIFEST_POLICY_FROZEN"
    assert policy["computes_new_scores"] == "false"
    assert policy["endpoint_replay_allowed"] == "false"
    assert policy["endpoint_validation_claimed"] == "false"
    assert "endpoint_residuals" in policy["forbidden_endpoint_fields"]
    assert summary["status"] == "SOURCE_FROZEN_TOMOGRAPHIC_HOLDOUT_MANIFEST_BUILT"
    assert summary["source_bin_count"] == "5"
    assert summary["tomographic_pair_count"] == "15"
    assert summary["holdout_fold_count"] == "5"
    assert summary["holdout_pair_counts_by_fold"] == "1:5;2:5;3:5;4:5;5:5"
    assert summary["calibration_pair_counts_by_fold"] == "1:10;2:10;3:10;4:10;5:10"
    assert summary["source_native_nz_available"] == "true"
    assert summary["independent_external_photoz_calibration_attached"] == "false"
    assert summary["h1_independent_evidence_complete"] == "false"
    assert summary["h2_holdout_partition_frozen"] == "true"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert (
        summary["verdict"]
        == "holdout_partition_frozen_but_independent_photoz_calibration_still_open"
    )
    assert len(bins) == 5
    assert len(pairs) == 75
    for fold in range(1, 6):
        fold_rows = [row for row in pairs if row["held_out_source_bin"] == str(fold)]
        assert len(fold_rows) == 15
        holdout = [row for row in fold_rows if row["pair_role"] == "holdout_pair"]
        assert len(holdout) == 5
        for row in holdout:
            assert str(fold) in {row["bin_i"], row["bin_j"]}
    for row in [*bins, *pairs]:
        assert row["uses_kids_data_vector_values_for_source_selection"] == "false"
        assert row["uses_residuals"] == "false"
        assert row["uses_fit_statistics"] == "false"
        assert row["endpoint_replay_allowed"] == "false"
        assert row["endpoint_validation_claimed"] == "false"
        assert row["claim_boundary"] == policy["claim_boundary"]


def test_kids1000_cosebis_photoz_tomographic_calibration_evidence_keeps_h1_open() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_photoz_tomographic_calibration_evidence_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_photoz_tomographic_calibration_evidence_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_photoz_tomographic_calibration_evidence_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))

    assert policy["status"] == "PHOTOZ_TOMOGRAPHIC_CALIBRATION_EVIDENCE_POLICY_FROZEN"
    assert policy["computes_new_scores"] == "false"
    assert policy["endpoint_replay_allowed"] == "false"
    assert policy["endpoint_validation_claimed"] == "false"
    assert "endpoint_residuals" in policy["forbidden_endpoint_fields"]
    assert summary["status"] == "PHOTOZ_TOMOGRAPHIC_CALIBRATION_EVIDENCE_LEDGER_BUILT"
    assert summary["evidence_rows"] == "4"
    assert summary["source_native_product_frozen"] == "true"
    assert summary["cached_public_photoz_markers_present"] == "true"
    assert summary["source_native_nz_available"] == "true"
    assert summary["independent_external_photoz_calibration_attached"] == "false"
    assert summary["h1_independent_evidence_complete"] == "false"
    assert summary["h2_holdout_partition_frozen"] == "true"
    assert summary["computes_new_scores"] == "false"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert (
        summary["verdict"]
        == "partial_photoz_tomographic_evidence_available_but_h1_external_calibration_open"
    )
    by_id = {row["evidence_id"]: row for row in rows}
    assert set(by_id) == {
        "E0_kids_lensing_product",
        "E1_kids_landing_page_photoz_markers",
        "E2_nz_source_inventory",
        "E3_independent_external_calibration",
    }
    assert by_id["E3_independent_external_calibration"]["evidence_status"] == "OPEN_REQUIRED_BEFORE_REPLAY"
    for row in rows:
        assert row["endpoint_replay_allowed"] == "false"
        assert row["endpoint_validation_claimed"] == "false"
        assert row["claim_boundary"] == policy["claim_boundary"]
    assert summary["claim_boundary"] == policy["claim_boundary"]


def test_kids1000_cosebis_external_photoz_calibration_acquisition_plan_keeps_replay_forbidden() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_external_photoz_calibration_acquisition_plan_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_external_photoz_calibration_acquisition_plan_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_external_photoz_calibration_acquisition_plan_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))

    assert policy["status"] == "EXTERNAL_PHOTOZ_CALIBRATION_ACQUISITION_PLAN_FROZEN_NOT_ATTACHED"
    assert policy["current_external_calibration_manifest_attached"] == "false"
    assert policy["current_endpoint_replay_allowed"] == "false"
    assert policy["endpoint_validation_claimed"] == "false"
    assert "endpoint_residuals" in policy["forbidden_inputs"]
    assert summary["status"] == "EXTERNAL_PHOTOZ_CALIBRATION_ACQUISITION_PLAN_BUILT_NOT_ATTACHED"
    assert summary["required_routes"] == "4"
    assert summary["attached_routes"] == "0"
    assert summary["leakage_review_complete"] == "false"
    assert summary["h1_independent_evidence_complete"] == "false"
    assert summary["h2_holdout_partition_frozen"] == "true"
    assert summary["computes_new_scores"] == "false"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert (
        summary["verdict"]
        == "external_photoz_calibration_acquisition_plan_frozen_h1_still_open"
    )
    assert {row["route_id"] for row in rows} == {
        "R1_photoz_calibration_reference_manifest",
        "R2_som_gold_or_nz_validation_manifest",
        "R3_tomographic_bin_quality_manifest",
        "R4_leakage_review_for_attached_calibration",
    }
    for row in rows:
        assert row["forbidden_inputs_used"] == "false"
        assert row["endpoint_replay_allowed"] == "false"
        assert row["endpoint_validation_claimed"] == "false"
        assert row["claim_boundary"] == policy["claim_boundary"]
    assert summary["claim_boundary"] == policy["claim_boundary"]


def test_kids1000_cosebis_external_photoz_calibration_source_manifest_attaches_sources_pending_review() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_external_photoz_calibration_source_manifest_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_external_photoz_calibration_source_manifest_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_external_photoz_calibration_source_manifest_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))

    assert policy["status"] == "EXTERNAL_PHOTOZ_CALIBRATION_SOURCE_MANIFEST_POLICY_FROZEN_PENDING_REVIEW"
    assert policy["current_sources_cached"] == "true"
    assert policy["current_leakage_review_complete"] == "false"
    assert policy["current_endpoint_replay_allowed"] == "false"
    assert policy["endpoint_validation_claimed"] == "false"
    assert "endpoint_residuals" in policy["forbidden_inputs"]
    assert summary["status"] == "EXTERNAL_PHOTOZ_CALIBRATION_SOURCE_MANIFEST_BUILT_PENDING_REVIEW"
    assert summary["cached_source_count"] == "3"
    assert summary["r1_to_r3_source_artifacts_attached"] == "true"
    assert summary["r4_leakage_review_complete"] == "false"
    assert summary["h1_independent_evidence_complete"] == "false"
    assert summary["computes_new_scores"] == "false"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert (
        summary["verdict"]
        == "external_photoz_calibration_sources_attached_pending_leakage_review"
    )
    route_cover = {route for row in rows for route in row["route_ids"].split(";")}
    assert {
        "R1_photoz_calibration_reference_manifest",
        "R2_som_gold_or_nz_validation_manifest",
        "R3_tomographic_bin_quality_manifest",
    }.issubset(route_cover)
    assert {row["source_id"] for row in rows} == {
        "KIDS1000_PHOTOZ_CALIBRATION_AANDA",
        "KIDS1000_PHOTOZ_CALIBRATION_ARXIV",
        "KIDS1000_SOM_GOLD_CATALOGUE",
    }
    for row in rows:
        assert (ROOT / row["cache_path"]).exists()
        assert row["all_required_markers_present"] == "true"
        assert row["forbidden_inputs_used"] == "false"
        assert row["endpoint_replay_allowed"] == "false"
        assert row["endpoint_validation_claimed"] == "false"
        assert row["claim_boundary"] == policy["claim_boundary"]
    assert summary["claim_boundary"] == policy["claim_boundary"]


def test_kids1000_cosebis_external_photoz_calibration_leakage_review_preflight_keeps_reviewer_open() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_external_photoz_calibration_leakage_review_preflight_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_external_photoz_calibration_leakage_review_preflight_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_external_photoz_calibration_leakage_review_preflight_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))

    assert policy["status"] == "EXTERNAL_PHOTOZ_CALIBRATION_LEAKAGE_REVIEW_PREFLIGHT_POLICY_FROZEN"
    assert policy["automated_leakage_preflight_complete"] == "true"
    assert policy["independent_reviewer_attestation_complete"] == "false"
    assert policy["r4_leakage_review_complete"] == "false"
    assert policy["h1_independent_evidence_complete"] == "false"
    assert policy["current_endpoint_replay_allowed"] == "false"
    assert "endpoint_residuals" in policy["forbidden_inputs"]
    assert summary["status"] == "EXTERNAL_PHOTOZ_CALIBRATION_LEAKAGE_REVIEW_PREFLIGHT_BUILT"
    assert summary["check_count"] == "4"
    assert summary["passed_checks"] == "3"
    assert summary["failed_checks"] == "0"
    assert summary["open_checks"] == "1"
    assert summary["automated_leakage_preflight_complete"] == "true"
    assert summary["independent_reviewer_attestation_complete"] == "false"
    assert summary["r4_leakage_review_complete"] == "false"
    assert summary["h1_independent_evidence_complete"] == "false"
    assert summary["computes_new_scores"] == "false"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert (
        summary["verdict"]
        == "automated_leakage_preflight_passed_independent_reviewer_still_open"
    )
    by_check = {row["check_id"]: row for row in rows}
    assert by_check["L1_manifest_metadata_no_forbidden_inputs"]["check_status"] == "PASS"
    assert by_check["L2_cached_public_sources_present"]["check_status"] == "PASS"
    assert by_check["L3_source_manifest_builder_has_no_endpoint_dependencies"]["check_status"] == "PASS"
    assert by_check["L4_independent_reviewer_attestation"]["check_status"] == "OPEN"
    for row in rows:
        assert row["uses_endpoint_fields"] == "false"
        assert row["forbidden_inputs_used"] == "false"
        assert row["endpoint_replay_allowed"] == "false"
        assert row["endpoint_validation_claimed"] == "false"
        assert row["claim_boundary"] == policy["claim_boundary"]
    assert summary["claim_boundary"] == policy["claim_boundary"]


def test_kids1000_cosebis_external_photoz_calibration_reviewer_attestation_template_is_blank() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_external_photoz_calibration_reviewer_attestation_template_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_external_photoz_calibration_reviewer_attestation_template_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_external_photoz_calibration_reviewer_attestation_template_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))

    assert policy["status"] == "EXTERNAL_PHOTOZ_CALIBRATION_REVIEWER_ATTESTATION_TEMPLATE_POLICY_FROZEN"
    assert policy["current_template_built"] == "true"
    assert policy["independent_reviewer_attestation_complete"] == "false"
    assert policy["r4_leakage_review_complete"] == "false"
    assert policy["h1_independent_evidence_complete"] == "false"
    assert policy["current_endpoint_replay_allowed"] == "false"
    assert "endpoint_residuals" in policy["forbidden_inputs"]
    assert summary["status"] == "EXTERNAL_PHOTOZ_CALIBRATION_REVIEWER_ATTESTATION_TEMPLATE_BUILT_NOT_COMPLETED"
    assert summary["question_count"] == "4"
    assert summary["review_completed"] == "false"
    assert summary["independent_reviewer_attestation_complete"] == "false"
    assert summary["r4_leakage_review_complete"] == "false"
    assert summary["h1_independent_evidence_complete"] == "false"
    assert summary["computes_new_scores"] == "false"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["verdict"] == "reviewer_attestation_template_ready_not_completed"
    assert {row["question_id"] for row in rows} == {
        "Q1_source_identity",
        "Q2_no_endpoint_fields",
        "Q3_route_coverage",
        "Q4_r4_decision",
    }
    for row in rows:
        assert row["reviewer_response"] == ""
        assert row["reviewer_rationale"] == ""
        assert row["reviewer_id_or_role"] == ""
        assert row["review_completed"] == "false"
        assert row["forbidden_inputs_used"] == "false"
        assert row["endpoint_replay_allowed"] == "false"
        assert row["endpoint_validation_claimed"] == "false"
        assert row["claim_boundary"] == policy["claim_boundary"]
    assert summary["claim_boundary"] == policy["claim_boundary"]


def test_kids1000_cosebis_external_photoz_calibration_reviewer_handoff_package_is_source_side_only() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_external_photoz_calibration_reviewer_handoff_package_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_external_photoz_calibration_reviewer_handoff_package_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_external_photoz_calibration_reviewer_handoff_package_v1_manifest.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))

    assert policy["status"] == "EXTERNAL_PHOTOZ_CALIBRATION_REVIEWER_HANDOFF_PACKAGE_POLICY_FROZEN"
    assert policy["current_handoff_package_built"] == "true"
    assert policy["independent_reviewer_attestation_complete"] == "false"
    assert policy["r4_leakage_review_complete"] == "false"
    assert policy["h1_independent_evidence_complete"] == "false"
    assert policy["current_endpoint_replay_allowed"] == "false"
    assert summary["status"] == "EXTERNAL_PHOTOZ_CALIBRATION_REVIEWER_HANDOFF_PACKAGE_BUILT_NOT_COMPLETED"
    assert summary["package_file_count"] == "18"
    assert summary["review_completed"] == "false"
    assert summary["independent_reviewer_attestation_complete"] == "false"
    assert summary["r4_leakage_review_complete"] == "false"
    assert summary["h1_independent_evidence_complete"] == "false"
    assert summary["computes_new_scores"] == "false"
    assert summary["contains_endpoint_data"] == "false"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["verdict"] == "reviewer_handoff_package_ready_not_completed"
    zip_path = ROOT / summary["zip_path"]
    zip_sha256_path = ROOT / summary["zip_sha256_path"]
    assert zip_path.exists()
    assert zip_sha256_path.exists()
    assert zip_sha256_path.read_text().strip() == f"{summary['zip_sha256']}  {zip_path.name}"
    with zipfile.ZipFile(zip_path) as zf:
        names = set(zf.namelist())
    expected = {row["package_path"] for row in rows}
    expected.add("data/derived/kids1000_cosebis_external_photoz_calibration_reviewer_handoff_package_v1_manifest.csv")
    assert names == expected
    for row in rows:
        assert row["contains_endpoint_data"] == "false"
        assert row["endpoint_replay_allowed"] == "false"
        assert row["endpoint_validation_claimed"] == "false"
        assert row["claim_boundary"] == policy["claim_boundary"]
    assert summary["claim_boundary"] == policy["claim_boundary"]


def _completed_reviewer_response_rows() -> list[dict[str, str]]:
    with (
        ROOT / "data/derived/kids1000_cosebis_external_photoz_calibration_reviewer_attestation_template_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        row["reviewer_response"] = "yes"
        row["reviewer_rationale"] = "Reviewed source-side artifacts only; no endpoint fields inspected."
        row["reviewer_id_or_role"] = "independent_source_reviewer"
        row["review_completed"] = "true"
        row["forbidden_inputs_used"] = "false"
        row["endpoint_replay_allowed"] = "false"
        row["endpoint_validation_claimed"] = "false"
        if row["question_id"] == "Q4_r4_decision":
            row["reviewer_response"] = "ACCEPT_AS_CAVEATED_SOURCE_SIDE_REVIEW"
    return rows


def _write_completed_reviewer_response(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _completed_reviewer_response_validator_cmd(response: Path, summary: Path) -> list[str]:
    return [
        "python",
        str(ROOT / "scripts/validate_kids1000_cosebis_external_photoz_calibration_completed_reviewer_response_v1.py"),
        str(response),
        "--summary-out",
        str(summary),
    ]


def test_kids1000_cosebis_external_photoz_calibration_completed_reviewer_response_validator_accepts_source_side_only(
    tmp_path: Path,
) -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_external_photoz_calibration_completed_reviewer_response_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert policy["status"] == "EXTERNAL_PHOTOZ_CALIBRATION_COMPLETED_REVIEWER_RESPONSE_POLICY_FROZEN"
    assert policy["current_endpoint_replay_allowed"] == "false"
    assert policy["endpoint_validation_claimed"] == "false"

    rows = _completed_reviewer_response_rows()

    response = tmp_path / "completed_reviewer_response.csv"
    _write_completed_reviewer_response(response, rows)
    summary = tmp_path / "summary.csv"
    subprocess.run(
        _completed_reviewer_response_validator_cmd(response, summary),
        cwd=ROOT,
        check=True,
    )
    with summary.open(newline="") as f:
        accepted = list(csv.DictReader(f))[0]
    assert accepted["independent_reviewer_attestation_complete"] == "true"
    assert accepted["r4_leakage_review_complete"] == "true"
    assert accepted["h1_independent_evidence_complete"] == "true"
    assert accepted["computes_new_scores"] == "false"
    assert accepted["contains_endpoint_data"] == "false"
    assert accepted["endpoint_replay_allowed"] == "false"
    assert accepted["endpoint_validation_claimed"] == "false"
    assert (
        accepted["verdict"]
        == "completed_reviewer_response_accepted_source_side_only_endpoint_replay_still_forbidden"
    )


def test_kids1000_cosebis_external_photoz_calibration_completed_reviewer_response_is_imported_source_side_only() -> None:
    with (
        ROOT / "data/derived/kids1000_cosebis_external_photoz_calibration_completed_reviewer_response_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    with (
        ROOT / "data/derived/kids1000_cosebis_external_photoz_calibration_completed_reviewer_response_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]

    assert len(rows) == 4
    assert {row["question_id"] for row in rows} == {
        "Q1_source_identity",
        "Q2_no_endpoint_fields",
        "Q3_route_coverage",
        "Q4_r4_decision",
    }
    assert all(row["review_completed"] == "true" for row in rows)
    assert all(row["forbidden_inputs_used"] == "false" for row in rows)
    assert all(row["endpoint_replay_allowed"] == "false" for row in rows)
    assert all(row["endpoint_validation_claimed"] == "false" for row in rows)
    assert summary["response_path"] == (
        "data/derived/kids1000_cosebis_external_photoz_calibration_completed_reviewer_response_v1.csv"
    )
    assert summary["review_completed"] == "true"
    assert summary["independent_reviewer_attestation_complete"] == "true"
    assert summary["r4_leakage_review_complete"] == "true"
    assert summary["h1_independent_evidence_complete"] == "true"
    assert summary["computes_new_scores"] == "false"
    assert summary["contains_endpoint_data"] == "false"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert (
        summary["verdict"]
        == "completed_reviewer_response_accepted_source_side_only_endpoint_replay_still_forbidden"
    )


def test_kids1000_cosebis_external_photoz_calibration_completed_reviewer_response_validator_rejects_forbidden_inputs(
    tmp_path: Path,
) -> None:
    rows = _completed_reviewer_response_rows()
    rows[0]["forbidden_inputs_used"] = "true"
    response = tmp_path / "completed_reviewer_response_forbidden.csv"
    summary = tmp_path / "summary.csv"
    _write_completed_reviewer_response(response, rows)
    result = subprocess.run(
        _completed_reviewer_response_validator_cmd(response, summary),
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert result.returncode != 0
    assert "forbidden_inputs_used=false" in result.stderr
    assert not summary.exists()


def test_kids1000_cosebis_external_photoz_calibration_completed_reviewer_response_validator_rejects_endpoint_replay(
    tmp_path: Path,
) -> None:
    rows = _completed_reviewer_response_rows()
    rows[1]["endpoint_replay_allowed"] = "true"
    response = tmp_path / "completed_reviewer_response_replay.csv"
    summary = tmp_path / "summary.csv"
    _write_completed_reviewer_response(response, rows)
    result = subprocess.run(
        _completed_reviewer_response_validator_cmd(response, summary),
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert result.returncode != 0
    assert "must not authorize endpoint replay" in result.stderr
    assert not summary.exists()


def test_kids1000_cosebis_external_photoz_calibration_closure_ledger_closes_source_side_only() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_external_photoz_calibration_closure_ledger_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_external_photoz_calibration_closure_ledger_v1.csv"
    ).open(newline="") as f:
        row = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_external_photoz_calibration_closure_ledger_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]

    assert policy["status"] == "EXTERNAL_PHOTOZ_CALIBRATION_CLOSURE_LEDGER_POLICY_FROZEN"
    assert policy["current_endpoint_replay_allowed"] == "false"
    assert policy["endpoint_validation_claimed"] == "false"
    assert row["closure_status"] == "SOURCE_SIDE_COMPLETE"
    assert row["independent_reviewer_attestation_complete"] == "true"
    assert row["r4_leakage_review_complete"] == "true"
    assert row["h1_independent_evidence_complete"] == "true"
    assert summary["r4_leakage_review_complete"] == "true"
    assert summary["h1_independent_evidence_complete"] == "true"
    for key in ["computes_new_scores", "contains_endpoint_data", "endpoint_replay_allowed", "endpoint_validation_claimed"]:
        assert row[key] == "false"
        assert summary[key] == "false"
    assert (
        summary["verdict"]
        == "external_photoz_calibration_source_side_closed_endpoint_replay_still_forbidden"
    )
    assert row["claim_boundary"] == policy["claim_boundary"]
    assert summary["claim_boundary"] == policy["claim_boundary"]


def test_kids1000_cosebis_endpoint_jackknife_robustness_is_not_single_pair_localized() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_endpoint_jackknife_robustness_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_endpoint_jackknife_robustness_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_endpoint_jackknife_robustness_v1_grid.csv"
    ).open(newline="") as f:
        grid = list(csv.DictReader(f))

    assert policy["status"] == "ENDPOINT_JACKKNIFE_ROBUSTNESS_POLICY_FROZEN"
    assert policy["endpoint_validation_claimed"] == "false"
    assert policy["uses_kids_data_vector_values_for_source_selection"] == "false"
    assert policy["retunes_source_frozen_theory_vector"] == "false"
    assert summary["status"] == "KIDS1000_COSEBIS_ENDPOINT_JACKKNIFE_ROBUSTNESS_COMPLETE"
    assert summary["subset_count"] == "27"
    assert summary["leave_one_subset_count"] == "20"
    assert summary["mode_band_subset_count"] == "3"
    assert summary["leave_one_subsets_with_negative_delta_chi2"] == "20"
    assert summary["leave_one_subsets_with_negative_delta_aic"] == "20"
    assert summary["mode_band_subsets_with_negative_delta_chi2"] == "2"
    assert summary["mode_band_subsets_with_negative_delta_aic"] == "2"
    assert summary["localization_verdict"] == "not_single_source_bin_or_pair_under_leave_one_chi2"
    assert summary["worst_subset_id"] == "without_mode_band_low_1_5"
    assert float(summary["worst_subset_delta_chi2_vs_baseline"]) == 0.0
    assert abs(float(summary["full_reference_delta_chi2_vs_baseline"]) + 183.6152665217) < 1e-9
    assert len(grid) == 27
    assert sum(row["subset_family"] == "leave_one_source_bin" for row in grid) == 5
    assert sum(row["subset_family"] == "leave_one_tomographic_pair" for row in grid) == 15
    assert sum(row["subset_family"] == "mode_band" for row in grid) == 3
    assert sum(row["subset_family"] == "complement_mode_band" for row in grid) == 3
    for row in [summary, *grid]:
        assert row["endpoint_validation_claimed"] == "false"
        assert row["uses_kids_data_vector_values_for_scoring"] == "true"
        assert row["uses_kids_data_vector_values_for_source_selection"] == "false"
        assert row["claim_boundary"] == policy["claim_boundary"]


def test_kids1000_cosebis_endpoint_mode_localization_identifies_low_mode_dominance() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_endpoint_mode_localization_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_endpoint_mode_localization_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_endpoint_mode_localization_v1_grid.csv"
    ).open(newline="") as f:
        grid = list(csv.DictReader(f))

    assert policy["status"] == "ENDPOINT_MODE_LOCALIZATION_POLICY_FROZEN"
    assert policy["endpoint_validation_claimed"] == "false"
    assert policy["uses_kids_data_vector_values_for_source_selection"] == "false"
    assert policy["retunes_source_frozen_theory_vector"] == "false"
    assert summary["status"] == "KIDS1000_COSEBIS_ENDPOINT_MODE_LOCALIZATION_COMPLETE"
    assert summary["subset_count"] == "59"
    assert summary["single_mode_subset_count"] == "20"
    assert summary["cumulative_low_subset_count"] == "20"
    assert summary["without_low_subset_count"] == "19"
    assert summary["best_single_mode_subset_id"] == "single_mode_1"
    assert summary["best_cumulative_low_subset_id"] == "cumulative_low_modes_1_to_3"
    assert summary["first_without_low_non_improving_subset_id"] == "without_low_modes_1_to_5"
    assert summary["mode_localization_verdict"] == "low_modes_1_to_5_dominate_endpoint_signal"
    assert abs(float(summary["best_single_mode_delta_chi2_vs_baseline"]) + 101.5735188246) < 1e-9
    assert abs(float(summary["best_cumulative_low_delta_chi2_vs_baseline"]) + 237.1074068478) < 1e-9
    assert float(summary["first_without_low_non_improving_delta_chi2_vs_baseline"]) == 0.0
    assert len(grid) == 59
    by_subset = {row["subset_id"]: row for row in grid}
    assert by_subset["without_low_modes_1_to_5"]["candidate_amplitude"] == "0.000000000000e+00"
    assert by_subset["single_mode_20"]["candidate_amplitude"] == "0.000000000000e+00"
    for row in [summary, *grid]:
        assert row["endpoint_validation_claimed"] == "false"
        assert row["uses_kids_data_vector_values_for_scoring"] == "true"
        assert row["uses_kids_data_vector_values_for_source_selection"] == "false"
        assert row["claim_boundary"] == policy["claim_boundary"]


def test_kids1000_cosebis_endpoint_mode_shape_stress_preserves_claim_boundary() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_endpoint_mode_shape_stress_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_endpoint_mode_shape_stress_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_endpoint_mode_shape_stress_v1_grid.csv"
    ).open(newline="") as f:
        grid = list(csv.DictReader(f))

    assert policy["status"] == "ENDPOINT_MODE_SHAPE_STRESS_POLICY_FROZEN"
    assert policy["endpoint_validation_claimed"] == "false"
    assert policy["uses_kids_data_vector_values_for_source_selection"] == "false"
    assert policy["retunes_source_frozen_path_mapping"] == "false"
    assert summary["status"] == "KIDS1000_COSEBIS_ENDPOINT_MODE_SHAPE_STRESS_COMPLETE"
    assert summary["mode_shape_count"] == "7"
    assert summary["best_mode_shape_id"] == "n^-0.5_candidate"
    assert summary["candidate_beats_flat_chi2"] == "true"
    assert summary["high_mode_weighting_removes_signal"] == "true"
    assert (
        summary["mode_shape_stress_verdict"]
        == "low_weighted_carriers_preferred_but_flat_still_improves_high_weighting_fails"
    )
    assert abs(float(summary["candidate_mode_shape_delta_chi2_vs_baseline"]) + 183.6152665217) < 1e-9
    assert abs(float(summary["flat_mode_shape_delta_chi2_vs_baseline"]) + 136.5504934506) < 1e-9
    assert float(summary["high_n_mode_shape_delta_chi2_vs_baseline"]) == 0.0
    by_shape = {row["mode_shape_id"]: row for row in grid}
    assert set(by_shape) == {
        "flat",
        "n^-0.25",
        "n^-0.5_candidate",
        "n^-0.75",
        "n^-1.0",
        "high_sqrt_n",
        "high_n",
    }
    assert by_shape["flat"]["candidate_improves_chi2"] == "true"
    assert by_shape["high_n"]["candidate_improves_chi2"] == "false"
    for row in [summary, *grid]:
        assert row["endpoint_validation_claimed"] == "false"
        assert row["uses_kids_data_vector_values_for_scoring"] == "true"
        assert row["uses_kids_data_vector_values_for_source_selection"] == "false"
        assert row["claim_boundary"] == policy["claim_boundary"]


def test_kids1000_cosebis_endpoint_scoring_synthesis_ledger_keeps_endpoint_claim_caveated() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_endpoint_scoring_synthesis_ledger_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_endpoint_scoring_synthesis_ledger_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_endpoint_scoring_synthesis_ledger_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))

    assert policy["status"] == "ENDPOINT_SCORING_SYNTHESIS_LEDGER_POLICY_FROZEN"
    assert policy["computes_new_scores"] == "false"
    assert policy["endpoint_validation_claimed"] == "false"
    assert summary["status"] == "ENDPOINT_SCORING_SYNTHESIS_LEDGER_BUILT"
    assert summary["ledger_rows"] == "8"
    assert summary["diagnostic_endpoint_signal_present"] == "true"
    assert summary["candidate_low_tail"] == "true"
    assert summary["candidate_absolute_winner"] == "false"
    assert summary["tomographic_caveat_active"] == "true"
    assert summary["better_tomographic_controls_accepted_as_physical_alternatives"] == "false"
    assert summary["jackknife_supports_not_single_bin_or_pair"] == "true"
    assert summary["low_mode_localized"] == "true"
    assert summary["mode_shape_candidate_preferred"] == "true"
    assert summary["physical_promotion_ready"] == "false"
    assert summary["computes_new_scores"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert (
        summary["verdict"]
        == "endpoint_signal_low_tail_caveated_by_tomographic_controls_and_physical_promotion_blockers"
    )
    by_component = {row["component_id"]: row for row in rows}
    assert by_component["S0_endpoint_score"]["component_status"] == "DIAGNOSTIC_ENDPOINT_SIGNAL_PRESENT"
    assert by_component["S2_tomographic_structure_robustness"]["component_status"] == "TOMOGRAPHIC_CAVEAT_ACTIVE"
    assert (
        by_component["S2b_tomographic_control_plausibility"]["component_status"]
        == "BETTER_CONTROLS_NOT_ACCEPTED_AS_PHYSICAL_ALTERNATIVES"
    )
    assert by_component["S6_physical_promotion"]["component_status"] == "PHYSICAL_PROMOTION_BLOCKED"
    assert by_component["S6_physical_promotion"]["supports_endpoint_signal"] == "false"
    assert {row["claim_boundary"] for row in rows} == {policy["claim_boundary"]}
    assert summary["claim_boundary"] == policy["claim_boundary"]


def test_kids1000_cosebis_low_mode_carrier_source_grounding_keeps_open_blocker() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_low_mode_carrier_source_grounding_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_low_mode_carrier_source_grounding_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_low_mode_carrier_source_grounding_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))

    assert policy["status"] == "LOW_MODE_CARRIER_SOURCE_GROUNDING_POLICY_FROZEN"
    assert policy["uses_kids_data_vector_values_for_grounding"] == "false"
    assert policy["allows_endpoint_validation_claim"] == "false"
    assert summary["status"] == "LOW_MODE_CARRIER_SOURCE_GROUNDING_PARTIAL_COMPLETE"
    assert (
        summary["source_grounding_verdict"]
        == "partial_protocol_grounding_with_open_first_principles_derivation_blocker"
    )
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["uses_kids_data_vector_values_for_grounding"] == "false"
    assert summary["uses_kids_data_vector_values_for_scoring"] == "false"
    assert summary["open_blocker_count"] == "1"
    assert summary["supporting_diagnostic_count"] == "2"
    assert {row["criterion_id"] for row in rows} == {
        "source_independence",
        "coherent_path_readout_prior",
        "no_posthoc_mode_cut",
        "diagnostic_consistency_with_mode_localization",
        "mode_shape_stress_support",
        "missing_first_principles_mode_kernel_derivation",
    }
    assert {row["claim_boundary"] for row in rows} == {policy["claim_boundary"]}


def test_kids1000_cosebis_low_mode_kernel_envelope_derivation_is_conditional() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_low_mode_kernel_envelope_derivation_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_low_mode_kernel_envelope_derivation_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_low_mode_kernel_envelope_derivation_v1.csv"
    ).open(newline="") as f:
        ledger = list(csv.DictReader(f))
    with (
        ROOT / "data/derived/kids1000_cosebis_low_mode_kernel_envelope_derivation_v1_mode_weights.csv"
    ).open(newline="") as f:
        weights = list(csv.DictReader(f))

    assert policy["status"] == "LOW_MODE_KERNEL_ENVELOPE_DERIVATION_POLICY_FROZEN"
    assert policy["uses_kids_data_vector_values"] == "false"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert summary["status"] == "LOW_MODE_KERNEL_ENVELOPE_CONDITIONAL_DERIVATION_COMPLETE"
    assert (
        summary["derivation_verdict"]
        == "conditional_log_band_power_envelope_derives_n_minus_half_shape_but_covariant_kernel_blocker_remains"
    )
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["open_blocker_count"] == "1"
    assert summary["assumption_count"] == "2"
    assert summary["derived_conditional_count"] == "2"
    assert len(weights) == 20
    assert [row["mode"] for row in weights] == [str(i) for i in range(1, 21)]
    assert abs(float(summary["mean_unit_mode_weight"]) - 1.0) < 1e-12
    assert float(weights[0]["unit_mean_mode_weight"]) > float(weights[-1]["unit_mean_mode_weight"])
    assert {row["status"] for row in ledger} == {
        "ASSUMPTION",
        "DERIVED_CONDITIONAL",
        "DEFINITION",
        "LIMIT_CHECK",
        "OPEN_BLOCKER",
    }
    assert {row["claim_boundary"] for row in [*ledger, *weights]} == {policy["claim_boundary"]}


def test_kids1000_cosebis_log_band_prior_eligibility_gate_is_partial() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_log_band_prior_eligibility_gate_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_log_band_prior_eligibility_gate_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_log_band_prior_eligibility_gate_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))

    assert policy["status"] == "LOG_BAND_PRIOR_ELIGIBILITY_GATE_FROZEN"
    assert policy["uses_kids_data_vector_values"] == "false"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert summary["status"] == "LOG_BAND_PRIOR_ELIGIBILITY_GATE_PARTIAL_PASS"
    assert summary["eligibility_verdict"] == "protocol_eligible_for_conditional_envelope_but_not_full_kernel_validated"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["pass_count"] == "4"
    assert summary["assumption_not_source_proven_count"] == "1"
    assert summary["open_blocker_count"] == "1"
    by_condition = {row["condition_id"]: row for row in rows}
    assert set(by_condition) == {
        "C1_ordered_dimensionless_mode_domain",
        "C2_no_posthoc_mode_cut",
        "C3_source_side_path_mapping_exists",
        "C4_smooth_coherent_path_residual",
        "C5_no_high_frequency_only_source_claim",
        "C6_covariant_or_survey_native_kernel",
    }
    assert by_condition["C4_smooth_coherent_path_residual"]["status"] == "ASSUMPTION_NOT_SOURCE_PROVEN"
    assert by_condition["C6_covariant_or_survey_native_kernel"]["status"] == "OPEN_BLOCKER"
    assert {row["claim_boundary"] for row in rows} == {policy["claim_boundary"]}


def test_kids1000_cosebis_log_band_prior_mock_sanity_is_deterministic_not_validation() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_log_band_prior_mock_sanity_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_log_band_prior_mock_sanity_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_log_band_prior_mock_sanity_v1_grid.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))

    assert policy["status"] == "LOG_BAND_PRIOR_MOCK_SANITY_POLICY_FROZEN"
    assert policy["uses_kids_data_vector_values"] == "false"
    assert policy["uses_fit_statistics"] == "false"
    assert policy["uses_random_noise"] == "false"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert summary["status"] == "LOG_BAND_PRIOR_MOCK_SANITY_COMPLETE"
    assert summary["mock_sanity_verdict"] == "deterministic_template_recovery_pass_not_physical_mock_validation"
    assert summary["all_expected_templates_recovered"] == "true"
    assert summary["low_truth_best_template"] == "low_log_band_n^-0.5"
    assert summary["flat_truth_best_template"] == "flat_coherent"
    assert summary["high_truth_best_template"] == "high_mode_n"
    assert summary["oscillatory_truth_best_template"] == "oscillatory_alternating"
    assert summary["endpoint_validation_claimed"] == "false"
    assert len(rows) == 16
    assert {row["truth_recovered_expected_template"] for row in rows} == {"true"}
    assert {row["uses_kids_data_vector_values"] for row in rows} == {"false"}
    assert {row["uses_fit_statistics"] for row in rows} == {"false"}
    assert {row["uses_random_noise"] for row in rows} == {"false"}
    assert {row["endpoint_scoring_allowed"] for row in rows} == {"false"}
    assert {row["endpoint_validation_claimed"] for row in rows} == {"false"}
    assert {row["claim_boundary"] for row in rows} == {policy["claim_boundary"]}


def test_kids1000_cosebis_survey_native_path_kernel_gate_keeps_kernel_blockers_open() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_survey_native_path_kernel_derivation_gate_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_survey_native_path_kernel_derivation_gate_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_survey_native_path_kernel_derivation_gate_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))

    assert policy["status"] == "SURVEY_NATIVE_PATH_KERNEL_DERIVATION_GATE_FROZEN"
    assert policy["uses_kids_data_vector_values"] == "false"
    assert policy["uses_fit_statistics"] == "false"
    assert policy["uses_random_noise"] == "false"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert summary["status"] == "SURVEY_NATIVE_PATH_KERNEL_DERIVATION_GATE_PARTIAL"
    assert summary["survey_native_gate_verdict"] == (
        "survey_native_path_route_available_but_mode_response_and_covariant_kernel_derivation_blocked"
    )
    assert summary["route_support_conditions_passed"] == "true"
    assert summary["full_kernel_derivation_closed"] == "false"
    assert summary["pass_count"] == "4"
    assert summary["pass_caveated_count"] == "1"
    assert summary["open_blocker_count"] == "3"
    assert summary["fail_count"] == "0"
    assert summary["endpoint_validation_claimed"] == "false"
    by_condition = {row["condition_id"]: row for row in rows}
    assert by_condition["K2_full_route_path_observable"]["status"] == "PASS_CAVEATED"
    assert by_condition["K6_survey_native_mode_response_operator"]["status"] == "OPEN_BLOCKER"
    assert by_condition["K7_log_band_prior_from_kernel"]["status"] == "OPEN_BLOCKER"
    assert by_condition["K8_covariant_lensing_path_limit"]["status"] == "OPEN_BLOCKER"
    assert {row["claim_boundary"] for row in rows} == {policy["claim_boundary"]}
    assert all(row["dimension_check"] for row in rows)
    assert all(row["known_limit_check"] for row in rows)


def test_kids1000_cosebis_mode_response_operator_spec_is_frozen_not_derived() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_mode_response_operator_spec_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_mode_response_operator_spec_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_mode_response_operator_spec_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))

    assert policy["status"] == "MODE_RESPONSE_OPERATOR_SPEC_POLICY_FROZEN"
    assert policy["uses_kids_data_vector_values"] == "false"
    assert policy["uses_fit_statistics"] == "false"
    assert policy["uses_random_noise"] == "false"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert summary["status"] == "MODE_RESPONSE_OPERATOR_SPEC_COMPLETE_NOT_DERIVED"
    assert summary["operator_spec_verdict"] == "operator_requirements_frozen_but_survey_native_mode_response_not_derived"
    assert summary["mode_response_operator_derived"] == "false"
    assert summary["open_blocker_count"] == "2"
    assert summary["endpoint_validation_claimed"] == "false"
    by_requirement = {row["requirement_id"]: row for row in rows}
    assert by_requirement["R1_domain_path_observable"]["status"] == "SATISFIED_CAVEATED"
    assert by_requirement["R4_mode_response_from_source_operator"]["status"] == "OPEN_BLOCKER"
    assert by_requirement["R6_no_data_vector_or_fit_feedback"]["status"] == "SATISFIED"
    assert by_requirement["R7_gauge_or_mask_null_safety"]["status"] == "OPEN_BLOCKER"
    assert {row["claim_boundary"] for row in rows} == {policy["claim_boundary"]}
    assert all(row["dimension_check"] for row in rows)
    assert all(row["limit_check"] for row in rows)


def test_kids1000_cosebis_mode_response_spectrum_attempt_is_conditional() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_mode_response_spectrum_attempt_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_mode_response_spectrum_attempt_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_mode_response_spectrum_attempt_v1.csv"
    ).open(newline="") as f:
        ledger = list(csv.DictReader(f))
    with (
        ROOT / "data/derived/kids1000_cosebis_mode_response_spectrum_attempt_v1_spectra.csv"
    ).open(newline="") as f:
        spectra = list(csv.DictReader(f))

    assert policy["status"] == "MODE_RESPONSE_SPECTRUM_ATTEMPT_POLICY_FROZEN"
    assert policy["uses_kids_data_vector_values"] == "false"
    assert policy["uses_fit_statistics"] == "false"
    assert policy["uses_random_noise"] == "false"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert summary["status"] == "MODE_RESPONSE_SPECTRUM_ATTEMPT_CONDITIONAL_COMPLETE"
    assert summary["spectrum_attempt_verdict"] == (
        "conditional_source_spectrum_attempt_preserves_operator_and_null_safety_blockers"
    )
    assert summary["conditional_primary_spectrum"] == "log_band_neutral_candidate"
    assert summary["mode_response_operator_derived"] == "false"
    assert summary["open_blocker_count"] == "2"
    assert summary["high_mode_rejected_under_smooth_path_prior"] == "true"
    assert summary["oscillatory_rejected_under_smooth_path_prior"] == "true"
    by_step = {row["step_id"]: row for row in ledger}
    assert by_step["S2_log_band_power_prior"]["status"] == "ASSUMPTION_NOT_SOURCE_PROVEN"
    assert by_step["B1_operator_spectrum_blocker"]["status"] == "OPEN_BLOCKER"
    assert by_step["B2_gauge_null_safety_blocker"]["status"] == "OPEN_BLOCKER"
    assert len(spectra) == 80
    by_family = {row["spectrum_family"]: row["source_status"] for row in spectra if row["mode"] == "1"}
    assert by_family["log_band_neutral_candidate"] == "CONDITIONAL_PRIMARY"
    assert by_family["flat_boundary_control"] == "BOUNDARY_CONTROL"
    assert by_family["high_mode_rejected_under_smooth_path_prior"] == "REJECTED_BY_SMOOTH_PATH_PRIOR"
    assert by_family["oscillatory_rejected_under_smooth_path_prior"] == "REJECTED_BY_SMOOTH_PATH_PRIOR"
    assert {row["claim_boundary"] for row in ledger} == {policy["claim_boundary"]}
    assert {row["claim_boundary"] for row in spectra} == {policy["claim_boundary"]}
    assert all(row["dimension_check"] for row in ledger)
    assert all(row["limit_check"] for row in ledger)
    assert {row["uses_kids_data_vector_values"] for row in spectra} == {"false"}
    assert {row["uses_fit_statistics"] for row in spectra} == {"false"}
    assert {row["endpoint_scoring_allowed"] for row in spectra} == {"false"}
    assert {row["endpoint_validation_claimed"] for row in spectra} == {"false"}


def test_kids1000_cosebis_operator_null_safety_gate_is_blocked_not_derived() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_operator_null_safety_gate_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_operator_null_safety_gate_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_operator_null_safety_gate_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))

    assert policy["status"] == "OPERATOR_NULL_SAFETY_GATE_POLICY_FROZEN"
    assert policy["uses_kids_data_vector_values"] == "false"
    assert policy["uses_fit_statistics"] == "false"
    assert policy["uses_random_noise"] == "false"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert summary["status"] == "OPERATOR_NULL_SAFETY_GATE_BLOCKED_NOT_DERIVED"
    assert summary["verdict"] == "null_controls_exist_but_operator_level_null_safety_remains_blocked"
    assert summary["operator_null_safety_proven"] == "false"
    assert summary["mask_null_operator_proven"] == "false"
    assert summary["gauge_quotient_descent_proven"] == "false"
    assert summary["spectrum_null_coupling_proven"] == "false"
    assert summary["mode_response_operator_derived"] == "false"
    assert summary["open_blocker_count"] == "3"
    assert summary["endpoint_validation_claimed"] == "false"
    by_gate = {row["gate_id"]: row for row in rows}
    assert by_gate["N1_source_frozen_null_family_inventory"]["status"] == "SATISFIED"
    assert by_gate["N2_no_endpoint_feedback_in_null_replay"]["status"] == "SATISFIED"
    assert by_gate["N4_uniform_web_null_control"]["status"] == "SATISFIED_AS_NULL_CONTROL_ONLY"
    assert by_gate["N5_mask_null_operator_response"]["status"] == "OPEN_BLOCKER"
    assert by_gate["N6_gauge_quotient_descent"]["status"] == "OPEN_BLOCKER"
    assert by_gate["N7_spectrum_null_coupling"]["status"] == "OPEN_BLOCKER"
    assert {row["claim_boundary"] for row in rows} == {policy["claim_boundary"]}
    assert all(row["dimension_check"] for row in rows)
    assert all(row["limit_check"] for row in rows)


def test_kids1000_cosebis_pure_mask_response_gate_builds_basis_but_not_operator_proof() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_pure_mask_response_gate_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_pure_mask_response_gate_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_pure_mask_response_gate_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    with (
        ROOT / "data/derived/kids1000_cosebis_pure_mask_response_tile_basis_v1.csv"
    ).open(newline="") as f:
        tile_rows = list(csv.DictReader(f))
    with (
        ROOT / "data/derived/kids1000_cosebis_pure_mask_response_domain_basis_v1.csv"
    ).open(newline="") as f:
        domain_rows = list(csv.DictReader(f))

    assert policy["status"] == "PURE_MASK_RESPONSE_GATE_POLICY_FROZEN"
    assert policy["uses_kids_data_vector_values"] == "false"
    assert policy["uses_fit_statistics"] == "false"
    assert policy["uses_random_noise"] == "false"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert summary["status"] == "PURE_MASK_RESPONSE_GATE_BASIS_BUILT_OPERATOR_PROOF_BLOCKED"
    assert summary["verdict"] == (
        "pure_mask_basis_exists_but_quotient_triviality_and_mode_coupling_remain_blocked"
    )
    assert summary["tile_rows"] == "196"
    assert summary["domain_rows"] == "58800"
    assert summary["effective_centered_mask_basis_rank"] == "2"
    assert summary["pure_mask_basis_constructed"] == "true"
    assert summary["pure_mask_domain_lift_constructed"] == "true"
    assert summary["pure_mask_quotient_triviality_proven"] == "false"
    assert summary["pure_mask_mode_response_coupling_proven"] == "false"
    assert summary["mask_null_operator_response_proven"] == "false"
    assert summary["open_blocker_count"] == "2"
    assert len(tile_rows) == 196
    assert len(domain_rows) == 58800
    by_gate = {row["gate_id"]: row for row in rows}
    assert by_gate["P1_full_route_mask_sources_available"]["status"] == "SATISFIED"
    assert by_gate["P2_centered_pure_mask_basis_constructed"]["status"] == "SATISFIED"
    assert by_gate["P3_two_direction_mask_basis_non_degenerate"]["status"] == "SATISFIED_CAVEATED"
    assert by_gate["P6_quotient_triviality_not_proven"]["status"] == "OPEN_BLOCKER"
    assert by_gate["P7_mode_response_coupling_not_proven"]["status"] == "OPEN_BLOCKER"
    assert {row["claim_boundary"] for row in rows} == {policy["claim_boundary"]}
    assert all(row["dimension_check"] for row in rows)
    assert all(row["limit_check"] for row in rows)
    for row in tile_rows[:5] + domain_rows[:5]:
        assert row["contains_theory_vector"] == "false"
        assert row["contains_residuals"] == "false"
        assert row["contains_fit_statistics"] == "false"
        assert row["uses_kids_data_vector_values"] == "false"
        assert row["endpoint_scoring_allowed"] == "false"


def test_kids1000_cosebis_mask_mode_leakage_audit_records_risk_not_proof() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_mask_mode_leakage_audit_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_mask_mode_leakage_audit_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_mask_mode_leakage_audit_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    with (
        ROOT / "data/derived/kids1000_cosebis_mask_mode_leakage_audit_v1_grid.csv"
    ).open(newline="") as f:
        grid = list(csv.DictReader(f))

    assert policy["status"] == "MASK_MODE_LEAKAGE_AUDIT_POLICY_FROZEN"
    assert policy["uses_kids_data_vector_values"] == "false"
    assert policy["uses_fit_statistics"] == "false"
    assert policy["uses_random_noise"] == "false"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert summary["status"] == "MASK_MODE_LEAKAGE_AUDIT_SOURCE_SIDE_COMPLETE_OPERATOR_BLOCKED"
    assert summary["verdict"] == "uniform_mask_collapse_is_null_but_nonuniform_operator_leakage_remains_open"
    assert summary["basis_count"] == "3"
    assert summary["spectrum_family_count"] == "4"
    assert summary["grid_rows"] == "12"
    assert summary["uniform_collapse_all_null"] == "true"
    assert summary["leakage_risk_recorded"] == "true"
    assert summary["operator_level_leakage_theorem_proven"] == "false"
    assert summary["mode_response_operator_derived"] == "false"
    assert summary["open_blocker_count"] == "1"
    assert float(summary["max_uniform_collapse_norm"]) < 1.0e-10
    assert float(summary["max_low_mode_rms_envelope_norm"]) > 0.0
    by_gate = {row["gate_id"]: row for row in rows}
    assert by_gate["L1_centered_mask_uniform_collapse"]["status"] == "PASS"
    assert by_gate["L2_nonuniform_operator_leakage_risk"]["status"] == "RISK_RECORDED"
    assert by_gate["L4_operator_level_leakage_theorem"]["status"] == "OPEN_BLOCKER"
    assert {row["claim_boundary"] for row in rows} == {policy["claim_boundary"]}
    assert len(grid) == 12
    assert {row["uniform_collapse_is_null"] for row in grid} == {"true"}
    assert {row["leakage_risk_if_operator_uses_rms_or_abs_mask_load"] for row in grid} == {"true"}
    for row in grid:
        assert row["contains_theory_vector"] == "false"
        assert row["contains_residuals"] == "false"
        assert row["contains_fit_statistics"] == "false"
        assert row["uses_kids_data_vector_values"] == "false"
        assert row["endpoint_scoring_allowed"] == "false"
        assert row["endpoint_validation_claimed"] == "false"


def test_kids1000_cosebis_operator_leakage_theorem_requirements_are_frozen_not_proven() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_operator_leakage_theorem_requirements_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_operator_leakage_theorem_requirements_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_operator_leakage_theorem_requirements_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))

    assert policy["status"] == "OPERATOR_LEAKAGE_THEOREM_REQUIREMENTS_POLICY_FROZEN"
    assert policy["uses_kids_data_vector_values"] == "false"
    assert policy["uses_fit_statistics"] == "false"
    assert policy["uses_random_noise"] == "false"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert summary["status"] == "OPERATOR_LEAKAGE_THEOREM_REQUIREMENTS_FROZEN_NOT_PROVEN"
    assert summary["verdict"] == "requirements_frozen_for_operator_leakage_theorem_but_proof_remains_open"
    assert summary["requirement_rows"] == "7"
    assert summary["satisfied_count"] == "1"
    assert summary["satisfied_as_source_limit_count"] == "1"
    assert summary["risk_recorded_count"] == "1"
    assert summary["requirement_frozen_count"] == "2"
    assert summary["open_blocker_count"] == "2"
    assert summary["uniform_tile_null_limit_available"] == "true"
    assert summary["nonuniform_leakage_risk_recorded"] == "true"
    assert summary["pure_mask_rejection_requirement_frozen"] == "true"
    assert summary["mode_spectrum_coupling_requirement_frozen"] == "true"
    assert summary["operator_leakage_theorem_proven"] == "false"
    assert summary["gauge_quotient_descent_proven"] == "false"
    assert summary["mode_response_operator_derived"] == "false"
    by_req = {row["requirement_id"]: row for row in rows}
    assert by_req["T1_uniform_tile_null_limit"]["status"] == "SATISFIED_AS_SOURCE_LIMIT"
    assert by_req["T2_nonuniform_mask_leakage_risk"]["status"] == "RISK_RECORDED"
    assert by_req["T3_pure_mask_rejection_or_control_subspace"]["status"] == "REQUIREMENT_FROZEN"
    assert by_req["T4_mode_spectrum_coupling_requirement"]["status"] == "REQUIREMENT_FROZEN"
    assert by_req["T5_no_endpoint_feedback"]["status"] == "SATISFIED"
    assert by_req["T6_operator_leakage_theorem_not_proven"]["status"] == "OPEN_BLOCKER"
    assert by_req["T7_gauge_quotient_descent_not_proven"]["status"] == "OPEN_BLOCKER"
    assert {row["claim_boundary"] for row in rows} == {policy["claim_boundary"]}
    assert all(row["dimension_check"] for row in rows)
    assert all(row["known_limit_check"] for row in rows)
    for key in [
        "contains_theory_vector",
        "contains_predictions",
        "contains_residuals",
        "contains_fit_statistics",
        "uses_kids_data_vector_values",
        "uses_posterior_chains",
        "endpoint_scoring_allowed",
        "endpoint_validation_claimed",
    ]:
        assert summary[key] == "false"


def test_kids1000_cosebis_gauge_quotient_descent_gate_is_frozen_not_proven() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_gauge_quotient_descent_gate_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_gauge_quotient_descent_gate_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_gauge_quotient_descent_gate_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))

    assert policy["status"] == "GAUGE_QUOTIENT_DESCENT_GATE_POLICY_FROZEN"
    assert policy["uses_kids_data_vector_values"] == "false"
    assert policy["uses_fit_statistics"] == "false"
    assert policy["uses_random_noise"] == "false"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert summary["status"] == "GAUGE_QUOTIENT_DESCENT_REQUIREMENTS_FROZEN_NOT_PROVEN"
    assert summary["verdict"] == "gauge_quotient_descent_requirements_frozen_but_theorem_remains_open"
    assert summary["gate_rows"] == "8"
    assert summary["satisfied_count"] == "1"
    assert summary["satisfied_as_source_limit_count"] == "1"
    assert summary["requirement_frozen_count"] == "4"
    assert summary["open_blocker_count"] == "2"
    assert summary["equivalence_classes_declared"] == "true"
    assert summary["uniform_mask_offset_limit_available"] == "true"
    assert summary["normalization_invariance_proven"] == "false"
    assert summary["tile_relabeling_invariance_proven"] == "false"
    assert summary["pure_mask_control_compatibility_proven"] == "false"
    assert summary["gauge_quotient_descent_proven"] == "false"
    assert summary["survey_native_operator_constructed"] == "false"
    assert summary["operator_leakage_theorem_proven"] == "false"
    by_gate = {row["gate_id"]: row for row in rows}
    assert by_gate["Q1_equivalence_class_declared"]["status"] == "REQUIREMENT_FROZEN"
    assert by_gate["Q2_uniform_mask_offset_limit"]["status"] == "SATISFIED_AS_SOURCE_LIMIT"
    assert by_gate["Q3_normalization_representative_independence"]["status"] == "REQUIREMENT_FROZEN"
    assert by_gate["Q4_tile_relabeling_and_route_coordinate_invariance"]["status"] == "REQUIREMENT_FROZEN"
    assert by_gate["Q5_mask_pure_mode_control_compatibility"]["status"] == "REQUIREMENT_FROZEN"
    assert by_gate["Q6_no_endpoint_feedback"]["status"] == "SATISFIED"
    assert by_gate["Q7_gauge_quotient_descent_theorem_not_proven"]["status"] == "OPEN_BLOCKER"
    assert by_gate["Q8_survey_native_operator_not_constructed"]["status"] == "OPEN_BLOCKER"
    assert {row["claim_boundary"] for row in rows} == {policy["claim_boundary"]}
    assert all(row["dimension_check"] for row in rows)
    assert all(row["known_limit_check"] for row in rows)
    for key in [
        "contains_theory_vector",
        "contains_predictions",
        "contains_residuals",
        "contains_fit_statistics",
        "uses_kids_data_vector_values",
        "uses_posterior_chains",
        "uses_random_noise",
        "endpoint_scoring_allowed",
        "endpoint_validation_claimed",
    ]:
        assert summary[key] == "false"


def test_kids1000_cosebis_survey_native_operator_construction_attempt_is_skeleton_not_theorem() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_survey_native_operator_construction_attempt_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_survey_native_operator_construction_attempt_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_survey_native_operator_construction_attempt_v1_ledger.csv"
    ).open(newline="") as f:
        ledger = list(csv.DictReader(f))
    with (
        ROOT / "data/derived/kids1000_cosebis_survey_native_operator_construction_attempt_v1.csv"
    ).open(newline="") as f:
        operator_rows = list(csv.DictReader(f))

    assert policy["status"] == "SURVEY_NATIVE_OPERATOR_CONSTRUCTION_ATTEMPT_POLICY_FROZEN"
    assert policy["uses_kids_data_vector_values"] == "false"
    assert policy["uses_fit_statistics"] == "false"
    assert policy["uses_random_noise"] == "false"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert summary["status"] == "SURVEY_NATIVE_OPERATOR_SKELETON_CONSTRUCTED_THEOREM_OPEN"
    assert summary["verdict"] == "factorized_source_side_operator_skeleton_exists_but_operator_theorem_remains_open"
    assert summary["operator_rows"] == "300"
    assert summary["ledger_rows"] == "6"
    assert summary["satisfied_count"] == "1"
    assert summary["satisfied_caveated_count"] == "2"
    assert summary["open_blocker_count"] == "3"
    assert summary["operator_skeleton_constructed"] == "true"
    assert summary["contains_theory_vector"] == "true"
    for key in [
        "survey_native_operator_constructed",
        "operator_theorem_proven",
        "operator_leakage_theorem_proven",
        "mask_leakage_theorem_proven",
        "gauge_quotient_descent_proven",
        "physical_operator_units_derived",
        "mode_response_operator_derived",
        "contains_predictions",
        "contains_residuals",
        "contains_fit_statistics",
        "uses_kids_data_vector_values",
        "uses_posterior_chains",
        "uses_random_noise",
        "endpoint_scoring_allowed",
        "endpoint_validation_claimed",
    ]:
        assert summary[key] == "false"
    assert len(operator_rows) == 300
    for row in operator_rows[:10] + operator_rows[-10:]:
        assert row["operator_skeleton_constructed"] == "true"
        assert row["operator_theorem_proven"] == "false"
        assert row["mask_leakage_theorem_proven"] == "false"
        assert row["gauge_quotient_descent_proven"] == "false"
        assert row["contains_predictions"] == "false"
        assert row["contains_residuals"] == "false"
        assert row["contains_fit_statistics"] == "false"
        assert row["uses_kids_data_vector_values"] == "false"
        assert row["endpoint_scoring_allowed"] == "false"
        assert abs(
            float(row["operator_kernel_value"])
            - float(row["source_mapping_component"]) * float(row["mode_response_component"])
        ) < 1.0e-10
    by_gate = {row["gate_id"]: row for row in ledger}
    assert by_gate["O1_domain_codomain_available"]["status"] == "SATISFIED_CAVEATED"
    assert by_gate["O2_factorized_operator_skeleton_constructed"]["status"] == "SATISFIED_CAVEATED"
    assert by_gate["O3_mask_leakage_theorem_open"]["status"] == "OPEN_BLOCKER"
    assert by_gate["O4_gauge_quotient_descent_open"]["status"] == "OPEN_BLOCKER"
    assert by_gate["O5_no_endpoint_feedback"]["status"] == "SATISFIED"
    assert by_gate["O6_physical_operator_units_open"]["status"] == "OPEN_BLOCKER"
    assert {row["claim_boundary"] for row in ledger} == {policy["claim_boundary"]}
    assert all(row["dimension_check"] for row in ledger)
    assert all(row["known_limit_check"] for row in ledger)


def test_kids1000_cosebis_physical_operator_units_gate_freezes_units_blockers() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_physical_operator_units_gate_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_physical_operator_units_gate_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_physical_operator_units_gate_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))

    assert policy["status"] == "PHYSICAL_OPERATOR_UNITS_GATE_POLICY_FROZEN"
    assert policy["uses_kids_data_vector_values"] == "false"
    assert policy["uses_fit_statistics"] == "false"
    assert policy["uses_random_noise"] == "false"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert summary["status"] == "PHYSICAL_OPERATOR_UNITS_REQUIREMENTS_FROZEN_NOT_DERIVED"
    assert summary["verdict"] == "dimensionless_operator_kernel_identified_but_physical_units_and_amplitude_remain_open"
    assert summary["gate_rows"] == "6"
    assert summary["satisfied_count"] == "1"
    assert summary["satisfied_as_source_limit_count"] == "1"
    assert summary["requirement_frozen_count"] == "2"
    assert summary["open_blocker_count"] == "2"
    assert summary["dimensionless_source_kernel_identified"] == "true"
    assert summary["covariance_metric_available"] == "true"
    for key in [
        "physical_operator_units_derived",
        "source_side_amplitude_map_derived",
        "standard_lensing_null_normalization_proven",
        "covariance_metric_used_as_units_derivation",
        "contains_theory_vector",
        "contains_predictions",
        "contains_residuals",
        "contains_fit_statistics",
        "uses_kids_data_vector_values",
        "uses_posterior_chains",
        "uses_random_noise",
        "endpoint_scoring_allowed",
        "endpoint_validation_claimed",
    ]:
        assert summary[key] == "false"
    by_gate = {row["gate_id"]: row for row in rows}
    assert by_gate["U1_dimensionless_source_kernel_identified"]["status"] == "SATISFIED_AS_SOURCE_LIMIT"
    assert by_gate["U2_cosebis_response_units_need_derivation"]["status"] == "REQUIREMENT_FROZEN"
    assert by_gate["U3_amplitude_map_not_derived"]["status"] == "OPEN_BLOCKER"
    assert by_gate["U4_standard_lensing_null_normalization_open"]["status"] == "OPEN_BLOCKER"
    assert by_gate["U5_covariance_metric_not_units_derivation"]["status"] == "REQUIREMENT_FROZEN"
    assert by_gate["U6_no_endpoint_feedback"]["status"] == "SATISFIED"
    assert {row["claim_boundary"] for row in rows} == {policy["claim_boundary"]}
    assert all(row["dimension_check"] for row in rows)
    assert all(row["known_limit_check"] for row in rows)


def test_kids1000_cosebis_source_side_amplitude_map_attempt_freezes_dimensionless_source_amplitude() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_source_side_amplitude_map_attempt_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_source_side_amplitude_map_attempt_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_source_side_amplitude_map_attempt_v1.csv"
    ).open(newline="") as f:
        amplitude_rows = list(csv.DictReader(f))
    with (
        ROOT / "data/derived/kids1000_cosebis_source_side_amplitude_map_attempt_v1_ledger.csv"
    ).open(newline="") as f:
        ledger_rows = list(csv.DictReader(f))

    assert policy["status"] == "SOURCE_SIDE_AMPLITUDE_MAP_ATTEMPT_POLICY_FROZEN"
    assert policy["uses_kids_data_vector_values"] == "false"
    assert policy["uses_fit_statistics"] == "false"
    assert policy["uses_random_noise"] == "false"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert summary["status"] == "DIMENSIONLESS_SOURCE_SIDE_AMPLITUDE_MAP_CONSTRUCTED_PHYSICAL_AMPLITUDE_OPEN"
    assert summary["verdict"] == "dimensionless_source_amplitude_map_exists_but_physical_amplitude_remains_open"
    assert summary["amplitude_rows"] == "1"
    assert summary["ledger_rows"] == "5"
    assert summary["satisfied_count"] == "1"
    assert summary["satisfied_as_source_limit_count"] == "1"
    assert summary["satisfied_caveated_count"] == "1"
    assert summary["open_blocker_count"] == "2"
    assert summary["dimensionless_source_side_amplitude_map_constructed"] == "true"
    assert summary["source_side_amplitude_map_derived"] == "true"
    assert summary["dimensionless_amplitude_value"] == "1.000000000000e+00"
    for key in [
        "physical_amplitude_units_derived",
        "physical_operator_units_derived",
        "endpoint_calibrated_amplitude",
        "standard_lensing_null_amplitude_proven",
        "contains_predictions",
        "contains_residuals",
        "contains_fit_statistics",
        "uses_kids_data_vector_values",
        "uses_posterior_chains",
        "uses_random_noise",
        "endpoint_scoring_allowed",
        "endpoint_validation_claimed",
    ]:
        assert summary[key] == "false"

    row = amplitude_rows[0]
    assert row["amplitude_id"] == "A_src_unit_mean_dimensionless"
    assert row["amplitude_value"] == "1.000000000000e+00"
    assert row["amplitude_units"] == "dimensionless"
    assert row["physical_units_derived"] == "false"
    assert row["endpoint_calibrated"] == "false"
    assert row["uses_kids_data_vector_values"] == "false"
    assert row["contains_residuals"] == "false"
    assert row["contains_fit_statistics"] == "false"
    assert row["uses_posterior_chains"] == "false"
    assert row["uses_random_noise"] == "false"

    by_gate = {row["gate_id"]: row for row in ledger_rows}
    assert by_gate["A1_unit_mean_source_normalization_available"]["status"] == "SATISFIED_AS_SOURCE_LIMIT"
    assert by_gate["A2_dimensionless_amplitude_map_constructed"]["status"] == "SATISFIED_CAVEATED"
    assert by_gate["A3_no_endpoint_feedback"]["status"] == "SATISFIED"
    assert by_gate["A4_physical_amplitude_units_not_derived"]["status"] == "OPEN_BLOCKER"
    assert by_gate["A5_standard_lensing_null_amplitude_open"]["status"] == "OPEN_BLOCKER"
    assert {row["claim_boundary"] for row in ledger_rows} == {policy["claim_boundary"]}
    assert all(row["dimension_check"] for row in ledger_rows)
    assert all(row["known_limit_check"] for row in ledger_rows)


def test_kids1000_cosebis_physical_amplitude_requirements_gate_keeps_physical_amplitude_open() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_physical_amplitude_requirements_gate_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_physical_amplitude_requirements_gate_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_physical_amplitude_requirements_gate_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))

    assert policy["status"] == "PHYSICAL_AMPLITUDE_REQUIREMENTS_GATE_POLICY_FROZEN"
    assert policy["uses_kids_data_vector_values"] == "false"
    assert policy["uses_fit_statistics"] == "false"
    assert policy["uses_random_noise"] == "false"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert summary["status"] == "PHYSICAL_AMPLITUDE_REQUIREMENTS_FROZEN_NOT_DERIVED"
    assert summary["verdict"] == "dimensionless_source_amplitude_available_but_physical_response_amplitude_remains_open"
    assert summary["gate_rows"] == "5"
    assert summary["satisfied_count"] == "1"
    assert summary["satisfied_as_source_limit_count"] == "1"
    assert summary["requirement_frozen_count"] == "1"
    assert summary["open_blocker_count"] == "2"
    assert summary["dimensionless_source_amplitude_available"] == "true"
    assert summary["dimensionless_amplitude_value"] == "1.000000000000e+00"
    for key in [
        "physical_amplitude_units_derived",
        "response_unit_normalization_derived",
        "standard_lensing_null_amplitude_proven",
        "covariance_metric_used_as_amplitude_derivation",
        "contains_predictions",
        "contains_residuals",
        "contains_fit_statistics",
        "uses_kids_data_vector_values",
        "uses_posterior_chains",
        "uses_random_noise",
        "endpoint_scoring_allowed",
        "endpoint_validation_claimed",
    ]:
        assert summary[key] == "false"
    by_gate = {row["gate_id"]: row for row in rows}
    assert by_gate["P1_dimensionless_source_amplitude_available"]["status"] == "SATISFIED_AS_SOURCE_LIMIT"
    assert by_gate["P2_response_unit_normalization_required"]["status"] == "OPEN_BLOCKER"
    assert by_gate["P3_standard_lensing_null_amplitude_required"]["status"] == "OPEN_BLOCKER"
    assert by_gate["P4_covariance_metric_not_amplitude_derivation"]["status"] == "REQUIREMENT_FROZEN"
    assert by_gate["P5_no_endpoint_feedback"]["status"] == "SATISFIED"
    assert {row["claim_boundary"] for row in rows} == {policy["claim_boundary"]}
    assert all(row["dimension_check"] for row in rows)
    assert all(row["known_limit_check"] for row in rows)


def test_kids1000_cosebis_response_unit_normalization_requirements_keep_units_open() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_response_unit_normalization_requirements_gate_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_response_unit_normalization_requirements_gate_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_response_unit_normalization_requirements_gate_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))

    assert policy["status"] == "RESPONSE_UNIT_NORMALIZATION_REQUIREMENTS_GATE_POLICY_FROZEN"
    assert policy["uses_kids_data_vector_values"] == "false"
    assert policy["uses_fit_statistics"] == "false"
    assert policy["uses_random_noise"] == "false"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert summary["status"] == "RESPONSE_UNIT_NORMALIZATION_REQUIREMENTS_FROZEN_NOT_DERIVED"
    assert summary["verdict"] == "cosebis_response_unit_requirements_frozen_but_normalization_remains_open"
    assert summary["gate_rows"] == "6"
    assert summary["satisfied_count"] == "1"
    assert summary["satisfied_as_domain_limit_count"] == "1"
    assert summary["satisfied_as_source_limit_count"] == "1"
    assert summary["requirement_frozen_count"] == "1"
    assert summary["open_blocker_count"] == "2"
    for key in [
        "cosebis_row_domain_available",
        "dimensionless_kernel_and_source_amplitude_available",
        "covariance_metric_available",
    ]:
        assert summary[key] == "true"
    for key in [
        "covariance_metric_used_as_units_derivation",
        "response_unit_normalization_derived",
        "physical_amplitude_units_derived",
        "standard_lensing_null_compatibility_proven",
        "contains_predictions",
        "contains_residuals",
        "contains_fit_statistics",
        "uses_kids_data_vector_values",
        "uses_posterior_chains",
        "uses_random_noise",
        "endpoint_scoring_allowed",
        "endpoint_validation_claimed",
    ]:
        assert summary[key] == "false"
    by_gate = {row["gate_id"]: row for row in rows}
    assert by_gate["R1_cosebis_row_domain_available"]["status"] == "SATISFIED_AS_DOMAIN_LIMIT"
    assert by_gate["R2_dimensionless_kernel_and_source_amplitude_available"]["status"] == "SATISFIED_AS_SOURCE_LIMIT"
    assert by_gate["R3_covariance_metric_available_not_units"]["status"] == "REQUIREMENT_FROZEN"
    assert by_gate["R4_response_unit_map_not_derived"]["status"] == "OPEN_BLOCKER"
    assert by_gate["R5_standard_lensing_null_compatibility_required"]["status"] == "OPEN_BLOCKER"
    assert by_gate["R6_no_endpoint_feedback"]["status"] == "SATISFIED"
    assert {row["claim_boundary"] for row in rows} == {policy["claim_boundary"]}
    assert all(row["dimension_check"] for row in rows)
    assert all(row["known_limit_check"] for row in rows)


def test_kids1000_cosebis_standard_lensing_null_amplitude_requirements_keep_theorem_open() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_standard_lensing_null_amplitude_theorem_requirements_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_standard_lensing_null_amplitude_theorem_requirements_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_standard_lensing_null_amplitude_theorem_requirements_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))

    assert policy["status"] == "STANDARD_LENSING_NULL_AMPLITUDE_THEOREM_REQUIREMENTS_POLICY_FROZEN"
    assert policy["uses_kids_data_vector_values"] == "false"
    assert policy["uses_fit_statistics"] == "false"
    assert policy["uses_random_noise"] == "false"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert summary["status"] == "STANDARD_LENSING_NULL_AMPLITUDE_THEOREM_REQUIREMENTS_FROZEN_NOT_PROVEN"
    assert summary["verdict"] == "standard_lensing_null_amplitude_requirements_frozen_but_theorem_remains_open"
    assert summary["requirement_rows"] == "6"
    assert summary["satisfied_count"] == "1"
    assert summary["satisfied_as_control_limit_count"] == "1"
    assert summary["specified_not_derived_count"] == "1"
    assert summary["open_blocker_count"] == "3"
    assert summary["null_controls_available_as_control_limit"] == "true"
    assert summary["zero_tau_source_amplitude_statement_specified"] == "true"
    for key in [
        "standard_lensing_null_amplitude_proven",
        "operator_null_safety_proven",
        "gauge_quotient_descent_proven",
        "operator_leakage_theorem_proven",
        "physical_amplitude_units_derived",
        "contains_predictions",
        "contains_residuals",
        "contains_fit_statistics",
        "uses_kids_data_vector_values",
        "uses_posterior_chains",
        "uses_random_noise",
        "endpoint_scoring_allowed",
        "endpoint_validation_claimed",
    ]:
        assert summary[key] == "false"
    by_req = {row["requirement_id"]: row for row in rows}
    assert by_req["Z1_source_replayed_null_controls_available"]["status"] == "SATISFIED_AS_CONTROL_LIMIT"
    assert by_req["Z2_zero_tau_source_amplitude_statement"]["status"] == "SPECIFIED_NOT_DERIVED"
    assert by_req["Z3_operator_null_safety_required"]["status"] == "OPEN_BLOCKER"
    assert by_req["Z4_gauge_quotient_descent_required"]["status"] == "OPEN_BLOCKER"
    assert by_req["Z5_leakage_theorem_required"]["status"] == "OPEN_BLOCKER"
    assert by_req["Z6_no_endpoint_feedback"]["status"] == "SATISFIED"
    assert {row["claim_boundary"] for row in rows} == {policy["claim_boundary"]}
    assert all(row["dimension_check"] for row in rows)
    assert all(row["known_limit_check"] for row in rows)


def test_kids1000_cosebis_physical_promotion_blocker_ledger_separates_diagnostic_from_physical() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_physical_promotion_blocker_ledger_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_physical_promotion_blocker_ledger_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/kids1000_cosebis_physical_promotion_blocker_ledger_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))

    assert policy["status"] == "PHYSICAL_PROMOTION_BLOCKER_LEDGER_POLICY_FROZEN"
    assert policy["uses_kids_data_vector_values"] == "false"
    assert policy["uses_fit_statistics"] == "false"
    assert policy["uses_random_noise"] == "false"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert summary["status"] == "PHYSICAL_PROMOTION_BLOCKER_LEDGER_BUILT_NOT_CLOSED"
    assert summary["verdict"] == "diagnostic_endpoint_ready_but_physical_promotion_blocked_by_five_open_requirements"
    assert summary["ledger_rows"] == "6"
    assert summary["diagnostic_ready_not_physical_count"] == "1"
    assert summary["open_blocker_count"] == "5"
    assert summary["diagnostic_endpoint_pipeline_ready"] == "true"
    for key in [
        "physical_promotion_ready",
        "survey_native_operator_theorem_proven",
        "operator_leakage_theorem_proven",
        "gauge_quotient_descent_proven",
        "response_unit_normalization_derived",
        "standard_lensing_null_amplitude_proven",
        "contains_predictions",
        "contains_residuals",
        "contains_fit_statistics",
        "uses_kids_data_vector_values",
        "uses_posterior_chains",
        "uses_random_noise",
        "endpoint_scoring_allowed",
        "endpoint_validation_claimed",
    ]:
        assert summary[key] == "false"
    by_blocker = {row["blocker_id"]: row for row in rows}
    assert by_blocker["G0_diagnostic_endpoint_pipeline_ready_not_physical_promotion"]["status"] == "DIAGNOSTIC_READY_NOT_PHYSICAL"
    assert by_blocker["B1_survey_native_operator_theorem_open"]["status"] == "OPEN_BLOCKER"
    assert by_blocker["B2_operator_leakage_theorem_open"]["status"] == "OPEN_BLOCKER"
    assert by_blocker["B3_gauge_quotient_descent_open"]["status"] == "OPEN_BLOCKER"
    assert by_blocker["B4_response_unit_normalization_open"]["status"] == "OPEN_BLOCKER"
    assert by_blocker["B5_standard_lensing_null_amplitude_theorem_open"]["status"] == "OPEN_BLOCKER"
    assert {row["claim_boundary"] for row in rows} == {policy["claim_boundary"]}
    assert all(row["dimension_check"] for row in rows)
    assert all(row["known_limit_check"] for row in rows)


def test_kids1000_cosebis_null_control_policy_is_declared_not_run() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_null_control_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert policy["status"] == "KIDS1000_COSEBIS_NULL_CONTROL_POLICY_DECLARED_NOT_RUN"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert policy["current_controls_executed"] == "false"
    assert policy["control_family_count"] == "4"
    for marker in [
        "sky_rotation",
        "tomographic_pair_shuffle",
        "wrong_channel_activation",
        "web_path_sign_flip",
    ]:
        assert marker in policy["control_families"]
    for marker in [
        "posthoc_control_selection",
        "posthoc_control_multiplicity",
        "kids_data_vector_values",
    ]:
        assert marker in policy["forbidden_inputs"]
    with (
        ROOT / "data/derived/kids1000_cosebis_null_control_readiness_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "KIDS1000_COSEBIS_NULL_CONTROL_READINESS_BUILT_THEORY_REPLAY_NOT_SCORED"
    assert summary["endpoint_scoring_allowed"] == "false"
    assert summary["current_controls_executed"] == "true"
    assert summary["contains_theory_vector"] == "true"
    assert summary["contains_control_scores"] == "false"
    assert summary["contains_predictions"] == "false"
    assert summary["contains_residuals"] == "false"
    assert summary["contains_fit_statistics"] == "false"
    assert summary["uses_kids_data_vector_values"] == "false"
    assert summary["uses_posterior_chains"] == "false"
    assert summary["uses_posthoc_control_selection"] == "false"
    assert summary["target_rows"] == "300"
    assert summary["control_family_count"] == "4"
    assert summary["control_draw_count"] == "1008"
    with (
        ROOT / "data/derived/kids1000_cosebis_null_control_readiness_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert {row["control_family"] for row in rows} == {
        "sky_rotation",
        "tomographic_pair_shuffle",
        "wrong_channel_activation",
        "web_path_sign_flip",
    }
    assert {row["control_status"] for row in rows} == {"THEORY_REPLAY_EXECUTED_NOT_SCORED"}
    assert {row["current_control_executed"] for row in rows} == {"true"}
    assert {row["contains_theory_vector"] for row in rows} == {"true"}
    assert {row["requires_seed_policy"] for row in rows} == {"true"}
    assert {row["contains_control_scores"] for row in rows} == {"false"}


def test_kids1000_cosebis_null_control_theory_replay_is_not_scoring() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_null_control_theory_replay_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert policy["status"] == "KIDS1000_COSEBIS_NULL_CONTROL_THEORY_REPLAY_POLICY_FROZEN_NOT_SCORED"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert policy["current_control_theory_replay_executed"] == "true"
    assert policy["current_control_scores_computed"] == "false"
    for marker in [
        "posthoc_control_selection",
        "posthoc_control_multiplicity",
        "kids_data_vector_values",
        "lensing_residuals",
    ]:
        assert marker in policy["forbidden_inputs"]
    with (
        ROOT / "data/derived/kids1000_cosebis_null_control_theory_replay_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "KIDS1000_COSEBIS_NULL_CONTROL_THEORY_REPLAY_BUILT_NOT_SCORED"
    assert summary["control_draw_count"] == "1008"
    assert summary["target_rows_per_control"] == "300"
    assert int(summary["unique_control_digest_count"]) >= 900
    assert summary["contains_theory_vector"] == "true"
    assert summary["contains_control_scores"] == "false"
    assert summary["contains_predictions"] == "false"
    assert summary["contains_residuals"] == "false"
    assert summary["contains_fit_statistics"] == "false"
    assert summary["endpoint_scoring_allowed"] == "false"
    with (
        ROOT / "data/derived/kids1000_cosebis_null_control_theory_replay_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 1008
    counts = {}
    for row in rows:
        counts[row["control_family"]] = counts.get(row["control_family"], 0) + 1
        assert row["target_rows"] == "300"
        assert len(row["vector_sha256"]) == 64
        assert row["contains_theory_vector"] == "true"
        assert row["contains_control_scores"] == "false"
        assert row["contains_predictions"] == "false"
        assert row["contains_residuals"] == "false"
        assert row["endpoint_scoring_allowed"] == "false"
    assert counts == {
        "sky_rotation": 4,
        "tomographic_pair_shuffle": 1000,
        "wrong_channel_activation": 2,
        "web_path_sign_flip": 2,
    }


def test_kids1000_cosebis_null_control_seed_policy_is_frozen_not_run() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_null_control_seed_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert policy["status"] == "KIDS1000_COSEBIS_NULL_CONTROL_SEED_POLICY_FROZEN_NOT_RUN"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert policy["current_seed_policy_frozen"] == "true"
    assert policy["current_controls_executed"] == "false"
    assert policy["seed_policy"] == "deterministic_family_seed_table"
    assert policy["multiplicity_policy"] == "fixed_family_multiplicity_table"
    for marker in [
        "posthoc_seed_selection",
        "posthoc_control_multiplicity",
        "kids_data_vector_values",
    ]:
        assert marker in policy["forbidden_inputs"]
    with (
        ROOT / "data/derived/kids1000_cosebis_null_control_seed_inventory_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "KIDS1000_COSEBIS_NULL_CONTROL_SEED_INVENTORY_BUILT_NOT_RUN"
    assert summary["endpoint_scoring_allowed"] == "false"
    assert summary["current_seed_policy_frozen"] == "true"
    assert summary["current_controls_executed"] == "false"
    assert summary["contains_control_scores"] == "false"
    assert summary["contains_predictions"] == "false"
    assert summary["contains_residuals"] == "false"
    assert summary["contains_fit_statistics"] == "false"
    assert summary["uses_kids_data_vector_values"] == "false"
    assert summary["uses_posthoc_seed_selection"] == "false"
    assert summary["uses_posthoc_control_multiplicity"] == "false"
    assert summary["control_family_count"] == "4"
    assert summary["total_declared_control_draws"] == "1008"
    with (
        ROOT / "data/derived/kids1000_cosebis_null_control_seed_inventory_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    expected = {
        "sky_rotation": ("601001", "4"),
        "tomographic_pair_shuffle": ("601002", "1000"),
        "wrong_channel_activation": ("601003", "2"),
        "web_path_sign_flip": ("601004", "2"),
    }
    assert {row["control_family"] for row in rows} == set(expected)
    for row in rows:
        assert (row["seed"], row["multiplicity"]) == expected[row["control_family"]]
        assert row["current_control_executed"] == "false"
        assert row["contains_control_scores"] == "false"
        assert row["contains_predictions"] == "false"
        assert row["contains_residuals"] == "false"
        assert row["uses_kids_data_vector_values"] == "false"
        assert row["uses_posthoc_seed_selection"] == "false"
        assert row["uses_posthoc_control_multiplicity"] == "false"


def test_pilot_products_are_frozen_but_not_endpoint_enabled() -> None:
    with (ROOT / "data/source_manifest/pilot_frozen_product_manifest.csv").open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 3
    assert {row["status"] for row in rows} == {"PILOT_PRODUCT_FETCHED_FROZEN"}
    assert {row["endpoint_allowed"] for row in rows} == {"false"}
    for row in rows:
        path = ROOT / row["local_path"]
        assert path.exists(), row["pilot_product_id"]
        assert int(row["byte_count"]) > 0
        assert row["sha256"]
        assert row["endpoint_blocker"]
    ids = {row["pilot_product_id"] for row in rows}
    assert "PANTHEON_PLUS_SH0ES_STAT_SYS_COV" in ids


def test_pantheon_scope_v1_is_frozen_not_scored() -> None:
    with (ROOT / "data/derived/pantheon_scope_v1_summary.csv").open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 1
    row = rows[0]
    assert row["status"] == "SCOPE_FROZEN_NOT_SCORED"
    assert row["endpoint_scoring_allowed"] == "false"
    assert int(row["total_rows"]) == 1701
    assert int(row["included_rows"]) == 1371
    assert int(row["covariance_dimension"]) == 1701
    forbidden = row["forbidden_inputs_checked"]
    assert "Tau_residual_parameters" in forbidden
    assert "late_time_activation_fit" in forbidden


def test_pantheon_scoring_protocol_is_frozen_not_run() -> None:
    with (ROOT / "data/source_manifest/pantheon_scoring_protocol_v1.csv").open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 1
    row = rows[0]
    assert row["status"] == "SCORING_PROTOCOL_FROZEN_NOT_RUN"
    assert row["scoring_allowed"] == "false"
    assert row["parent_scope_id"] == "PANTHEON_DISTANCE_SCOPE_V1"
    assert "flat_LCDM" in row["baseline_family"]
    assert "W_tau" in row["tau_activation_family"]
    forbidden = row["forbidden_inputs"]
    assert "distance_residuals" in forbidden
    assert "posthoc_row_masks" in forbidden
    assert not (ROOT / "data/derived/pantheon_scoring_v1_results.csv").exists()


def test_pantheon_design_matrix_is_not_a_score_artifact() -> None:
    with (ROOT / "data/derived/pantheon_design_matrix_v1_summary.csv").open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 1
    row = rows[0]
    assert row["status"] == "DESIGN_MATRIX_FROZEN_NOT_SCORED"
    assert row["endpoint_scoring_allowed"] == "false"
    assert int(row["rows"]) == 1371
    assert row["contains_model_predictions"] == "false"
    assert row["contains_residuals"] == "false"
    assert row["contains_fit_statistics"] == "false"
    with (ROOT / "data/derived/pantheon_design_matrix_v1.csv").open(newline="") as f:
        columns = set(csv.DictReader(f).fieldnames or [])
    assert "model_mu" not in columns
    assert "distance_residuals" not in columns
    assert "chi2" not in columns
    assert "W_void_proxy_basis" in columns
    assert "W_web_proxy_basis" in columns


def test_pantheon_pilot_scoring_is_a_nonvalidation_smoke_test() -> None:
    with (ROOT / "data/source_manifest/pantheon_pilot_scoring_v1.csv").open(newline="") as f:
        manifest_rows = list(csv.DictReader(f))
    with (ROOT / "data/derived/pantheon_pilot_scoring_v1_summary.csv").open(newline="") as f:
        summary_rows = list(csv.DictReader(f))
    with (ROOT / "data/derived/pantheon_pilot_scoring_v1_grid.csv").open(newline="") as f:
        grid_rows = list(csv.DictReader(f))
    assert len(manifest_rows) == 1
    assert len(summary_rows) == 1
    manifest = manifest_rows[0]
    summary = summary_rows[0]
    assert manifest["status"] == "PILOT_SCORING_NOT_VALIDATION"
    assert summary["status"] == "PILOT_SCORING_NOT_VALIDATION"
    assert summary["claim_boundary"] == "pilot_scoring_not_validation"
    assert int(summary["n_rows"]) == 1371


def test_void_web_proxy_full_cov_pilot_is_nonvalidation() -> None:
    with (ROOT / "data/source_manifest/pantheon_void_web_proxy_full_cov_pilot_v1.csv").open(
        newline=""
    ) as f:
        manifest_rows = list(csv.DictReader(f))
    with (ROOT / "data/derived/pantheon_void_web_proxy_full_cov_pilot_v1_summary.csv").open(
        newline=""
    ) as f:
        summary_rows = list(csv.DictReader(f))
    with (ROOT / "data/derived/pantheon_void_web_proxy_full_cov_pilot_v1_grid.csv").open(
        newline=""
    ) as f:
        grid_rows = list(csv.DictReader(f))
    assert len(manifest_rows) == 1
    assert len(summary_rows) == 1
    manifest = manifest_rows[0]
    summary = summary_rows[0]
    assert manifest["status"] == "VOID_WEB_PROXY_FULL_COV_PILOT_NOT_VALIDATION"
    assert summary["status"] == "VOID_WEB_PROXY_FULL_COV_PILOT_NOT_VALIDATION"
    assert summary["claim_boundary"] == "void_web_proxy_full_cov_pilot_not_validation"
    assert "W_VOID_MATURITY" in summary["active_channels"]
    assert "W_WEB_ANISOTROPY" in summary["active_channels"]
    assert "W_PATH_PROJECTION" in summary["disabled_channels"]
    assert "W_TIME_READOUT" in summary["disabled_channels"]
    branches = {row["branch"] for row in grid_rows}
    assert {
        "baseline_only",
        "void_web_proxy_shell",
        "void_only",
        "web_only",
        "wrong_web_sign",
        "deterministic_shuffled_void_web",
    } <= branches
    forbidden = manifest["forbidden_inputs"]
    assert "distance_residuals" in forbidden
    assert "posthoc_environment_labels" in forbidden
    assert "cholesky" in manifest["covariance_policy"]
    assert summary["covariance_regularization"] == "none_positive_definite_cholesky"
    for key in [
        "baseline_best_chi2",
        "void_web_best_chi2",
        "void_only_best_chi2",
        "web_only_best_chi2",
        "wrong_web_sign_best_chi2",
        "shuffled_best_chi2",
        "delta_aic_void_web_minus_baseline",
    ]:
        assert float(summary[key]) == float(summary[key])


def test_pantheon_full_cov_pilot_scoring_is_not_validation() -> None:
    with (ROOT / "data/source_manifest/pantheon_full_cov_pilot_scoring_v1.csv").open(newline="") as f:
        manifest_rows = list(csv.DictReader(f))
    with (ROOT / "data/derived/pantheon_full_cov_pilot_scoring_v1_summary.csv").open(newline="") as f:
        summary_rows = list(csv.DictReader(f))
    with (ROOT / "data/derived/pantheon_full_cov_pilot_scoring_v1_grid.csv").open(newline="") as f:
        grid_rows = list(csv.DictReader(f))
    assert len(manifest_rows) == 1
    assert len(summary_rows) == 1
    manifest = manifest_rows[0]
    summary = summary_rows[0]
    assert manifest["status"] == "FULL_COV_PILOT_SCORING_NOT_VALIDATION"
    assert summary["status"] == "FULL_COV_PILOT_SCORING_NOT_VALIDATION"
    assert summary["claim_boundary"] == "full_cov_pilot_scoring_not_validation"
    assert int(summary["n_rows"]) == 1371
    assert "cholesky" in manifest["covariance_policy"]
    assert summary["covariance_regularization"] == "none_positive_definite_cholesky"
    assert float(summary["covariance_min_eigenvalue"]) > 0
    assert float(summary["covariance_condition_number"]) > 0
    branches = {row["branch"] for row in grid_rows}
    assert {
        "baseline_only",
        "tau_shell",
        "wrong_activation",
        "deterministic_shuffled_activation",
    } <= branches
    for key in [
        "baseline_best_chi2",
        "tau_best_chi2",
        "wrong_best_chi2",
        "shuffled_best_chi2",
        "delta_aic_tau_minus_baseline",
    ]:
        assert float(summary[key]) == float(summary[key])


def test_kids1000_cosebis_f_overlap_filled_review_validator_accepts_template_mode() -> None:
    result = subprocess.run(
        [
            "python",
            "scripts/validate_kids1000_cosebis_f_overlap_filled_execution_review_artifact_v1.py",
            "--input",
            "data/derived/kids1000_cosebis_f_overlap_execution_review_template_v1.csv",
            "--mode",
            "template",
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "mode=template" in result.stdout
    assert "endpoint_allowed=false" in result.stdout


def test_kids1000_cosebis_endpoint_replay_authorization_is_permission_only() -> None:
    response = ROOT / "data/derived/kids1000_cosebis_endpoint_replay_authorization_review_response_v1.csv"
    summary_out = ROOT / "data/derived/kids1000_cosebis_endpoint_replay_authorization_review_response_v1_summary.csv"
    result = subprocess.run(
        [
            "python",
            "scripts/validate_kids1000_cosebis_endpoint_replay_authorization_review_response_v1.py",
            str(response),
            "--summary-out",
            str(summary_out),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "endpoint_replay_authorized_permission_only_not_validation" in result.stdout
    with summary_out.open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 1
    summary = rows[0]
    assert summary["endpoint_replay_allowed"] == "true"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["forbidden_inputs_used"] == "false"
    assert (
        summary["authorization_scope"]
        == "single_predeclared_endpoint_replay_under_existing_frozen_source_side_state_permission_only_not_validation"
    )


def test_kids1000_cosebis_authorized_endpoint_replay_is_not_validation() -> None:
    subprocess.run(
        ["python", "scripts/validate_kids1000_cosebis_authorized_endpoint_replay_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with (ROOT / "data/derived/kids1000_cosebis_authorized_endpoint_replay_v1_summary.csv").open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 1
    summary = rows[0]
    assert summary["status"] == "AUTHORIZED_ENDPOINT_REPLAY_COMPLETE_PERMISSION_ONLY"
    assert summary["endpoint_replay_executed"] == "true"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["forbidden_inputs_used_for_source_selection"] == "false"
    assert summary["verdict"] == "authorized_endpoint_replay_low_tail_signal_not_validation"
    assert summary["candidate_rank_by_chi2"] == "3"
    assert summary["null_control_count"] == "1008"


def test_kids1000_cosebis_tomographic_control_disambiguation_blocks_validation_only() -> None:
    subprocess.run(
        ["python", "scripts/build_kids1000_cosebis_tomographic_control_disambiguation_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/validate_kids1000_cosebis_tomographic_control_disambiguation_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with (ROOT / "data/derived/kids1000_cosebis_tomographic_control_disambiguation_v1_summary.csv").open(
        newline=""
    ) as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 1
    summary = rows[0]
    assert summary["status"] == "TOMOGRAPHIC_CONTROL_DISAMBIGUATION_COMPLETE"
    assert summary["better_tomographic_control_count"] == "3"
    assert summary["better_control_only_count"] == "2"
    assert summary["better_conditional_source_systematic_count"] == "1"
    assert summary["accepted_physical_alternative_count"] == "0"
    assert summary["tomographic_controls_refute_endpoint_signal"] == "false"
    assert summary["tomographic_controls_block_validation"] == "true"
    assert summary["computes_new_scores"] == "false"
    assert summary["uses_kids_data_vector_values_for_source_selection"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["verdict"] == "tomographic_controls_block_validation_but_do_not_refute_endpoint_signal"


def test_kids1000_cosebis_tomographic_holdout_replay_preserves_signal_without_validation() -> None:
    subprocess.run(
        ["python", "scripts/run_kids1000_cosebis_tomographic_holdout_replay_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/validate_kids1000_cosebis_tomographic_holdout_replay_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with (ROOT / "data/derived/kids1000_cosebis_tomographic_holdout_replay_v1_summary.csv").open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 1
    summary = rows[0]
    assert summary["status"] == "TOMOGRAPHIC_HOLDOUT_REPLAY_COMPLETE"
    assert summary["fold_count"] == "5"
    assert summary["comparison_branch_count"] == "4"
    assert summary["candidate_holdout_improved_fold_count"] == "4"
    assert summary["candidate_rank_by_total_holdout_delta_chi2"] == "2"
    assert summary["candidate_beating_control_count"] == "1"
    assert summary["holdout_replay_refutes_endpoint_signal"] == "false"
    assert summary["tomographic_controls_block_validation"] == "true"
    assert summary["computes_new_labels"] == "false"
    assert summary["uses_kids_data_vector_values_for_source_selection"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["verdict"] == "holdout_replay_preserves_signal_but_tomographic_control_caveat_remains"


def test_kids1000_cosebis_best_tomographic_control_source_evidence_gate_keeps_control_only() -> None:
    subprocess.run(
        ["python", "scripts/build_kids1000_cosebis_best_tomographic_control_source_evidence_gate_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/validate_kids1000_cosebis_best_tomographic_control_source_evidence_gate_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with (
        ROOT / "data/derived/kids1000_cosebis_best_tomographic_control_source_evidence_gate_v1_summary.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 1
    summary = rows[0]
    assert summary["status"] == "CONTROL_ONLY_NO_SOURCE_EVIDENCE_FOR_PHYSICAL_PROMOTION"
    assert summary["target_operator"] == "seeded_auto_cross_shuffle_702759"
    assert summary["target_control_family"] == "auto_cross_preserving_shuffle"
    assert summary["target_is_global_source_bin_relabel"] == "false"
    assert summary["target_has_independent_source_evidence"] == "false"
    assert summary["accepted_physical_alternative_count"] == "0"
    assert summary["source_systematic_candidate_count"] == "0"
    assert summary["control_only_count"] == "1"
    assert summary["best_control_refutes_endpoint_signal"] == "false"
    assert summary["best_control_blocks_validation"] == "true"
    assert summary["computes_new_scores"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["verdict"] == "best_holdout_control_is_control_only_not_physical_alternative"


def test_kids1000_cosebis_validation_readiness_ledger_keeps_validation_blocked() -> None:
    subprocess.run(
        ["python", "scripts/build_kids1000_cosebis_validation_readiness_ledger_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/validate_kids1000_cosebis_validation_readiness_ledger_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with (ROOT / "data/derived/kids1000_cosebis_validation_readiness_ledger_v1_summary.csv").open(
        newline=""
    ) as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 1
    summary = rows[0]
    assert summary["status"] == "VALIDATION_READINESS_LEDGER_BUILT_NOT_VALIDATION"
    assert summary["ledger_rows"] == "5"
    assert summary["low_tail_endpoint_signal_present"] == "true"
    assert summary["tomographic_controls_refute_endpoint_signal"] == "false"
    assert summary["tomographic_control_concern_reduced"] == "true"
    assert summary["source_bin_holdout_signal_survives"] == "true"
    assert summary["candidate_holdout_improved_fold_count"] == "4"
    assert summary["best_holdout_control_physical_alternative"] == "false"
    assert summary["tomographic_caveat_active"] == "true"
    assert summary["physical_promotion_ready"] == "false"
    assert summary["validation_ready"] == "false"
    assert (
        summary["allowed_current_claim"]
        == "diagnostic_low_tail_signal_with_reduced_tomographic_control_concern_not_validation"
    )
    assert (
        summary["next_required_gate"]
        == "independent_tomographic_or_photoz_holdout_and_physical_promotion_blocker_resolution"
    )
    assert summary["computes_new_scores"] == "false"
    assert summary["uses_kids_data_vector_values_for_source_selection"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert (
        summary["verdict"]
        == "diagnostic_signal_survives_with_reduced_tomographic_concern_but_validation_blocked"
    )

    with (ROOT / "data/derived/kids1000_cosebis_validation_readiness_ledger_v1.csv").open(
        newline=""
    ) as f:
        ledger = {row["component_id"]: row for row in csv.DictReader(f)}
    assert ledger["R0_authorized_endpoint_replay"]["component_status"] == "LOW_TAIL_SIGNAL_PRESENT_NOT_VALIDATION"
    assert (
        ledger["R1_tomographic_control_disambiguation"]["component_status"]
        == "CONTROLS_BLOCK_VALIDATION_BUT_DO_NOT_REFUTE"
    )
    assert ledger["R2_source_bin_holdout_replay"]["component_status"] == "HOLDS_OUT_DIAGNOSTICALLY_WITH_CAVEAT"
    assert (
        ledger["R3_best_holdout_control_source_evidence"]["component_status"]
        == "BEST_CONTROL_CONTROL_ONLY_NOT_PHYSICAL"
    )
    assert ledger["R4_physical_promotion_blockers"]["component_status"] == "PHYSICAL_PROMOTION_BLOCKED"
    assert ledger["R4_physical_promotion_blockers"]["supports_signal_survival"] == "false"


def test_kids1000_cosebis_tomographic_photoz_closure_status_reduces_caveat_without_validation() -> None:
    subprocess.run(
        ["python", "scripts/build_kids1000_cosebis_tomographic_photoz_closure_status_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/validate_kids1000_cosebis_tomographic_photoz_closure_status_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with (ROOT / "data/derived/kids1000_cosebis_tomographic_photoz_closure_status_v1_summary.csv").open(
        newline=""
    ) as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 1
    summary = rows[0]
    assert summary["status"] == "TOMOGRAPHIC_PHOTOZ_CLOSURE_STATUS_BUILT_NOT_VALIDATION"
    assert summary["ledger_rows"] == "4"
    assert summary["external_photoz_source_side_closed"] == "true"
    assert summary["source_bin_holdout_signal_survives"] == "true"
    assert summary["candidate_holdout_improved_fold_count"] == "4"
    assert summary["best_holdout_control_physical_alternative"] == "false"
    assert summary["tomographic_control_concern_reduced"] == "true"
    assert summary["tomographic_caveat_active"] == "true"
    assert summary["physical_promotion_ready"] == "false"
    assert summary["validation_ready"] == "false"
    assert (
        summary["allowed_current_claim"]
        == "source_side_photoz_closed_and_holdout_signal_survives_but_validation_blocked"
    )
    assert summary["next_required_gate"] == "physical_promotion_blocker_resolution_before_validation_claim"
    assert summary["computes_new_scores"] == "false"
    assert summary["uses_kids_data_vector_values_for_source_selection"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert summary["verdict"] == "photoz_source_side_closed_tomographic_concern_reduced_but_validation_blocked"

    with (ROOT / "data/derived/kids1000_cosebis_tomographic_photoz_closure_status_v1.csv").open(
        newline=""
    ) as f:
        ledger = {row["component_id"]: row for row in csv.DictReader(f)}
    assert (
        ledger["C0_external_photoz_source_side_closure"]["component_status"]
        == "SOURCE_SIDE_PHOTOZ_CLOSURE_COMPLETE"
    )
    assert ledger["C3_validation_readiness"]["component_status"] == "VALIDATION_STILL_BLOCKED"
    assert ledger["C3_validation_readiness"]["blocks_validation"] == "true"


def test_kids1000_cosebis_physical_promotion_dependency_order_keeps_leakage_and_gauge_next() -> None:
    subprocess.run(
        ["python", "scripts/build_kids1000_cosebis_physical_promotion_dependency_order_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/validate_kids1000_cosebis_physical_promotion_dependency_order_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with (ROOT / "data/derived/kids1000_cosebis_physical_promotion_dependency_order_v1_summary.csv").open(
        newline=""
    ) as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 1
    summary = rows[0]
    assert summary["status"] == "PHYSICAL_PROMOTION_DEPENDENCY_ORDER_BUILT_NOT_PROOF"
    assert summary["dependency_rows"] == "5"
    assert summary["open_physical_blocker_count"] == "5"
    assert summary["next_primary_proof_gate"] == "B2_operator_leakage_theorem_open"
    assert summary["next_parallel_proof_gate"] == "B3_gauge_quotient_descent_open"
    assert (
        summary["unit_normalization_waits_for"]
        == "B2_operator_leakage_theorem_open;B3_gauge_quotient_descent_open"
    )
    assert (
        summary["standard_null_waits_for"]
        == "B2_operator_leakage_theorem_open;B3_gauge_quotient_descent_open;B4_response_unit_normalization_open"
    )
    assert summary["physical_promotion_ready"] == "false"
    assert summary["validation_ready"] == "false"
    assert summary["computes_new_scores"] == "false"
    assert summary["uses_kids_data_vector_values_for_source_selection"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert summary["verdict"] == "physical_promotion_ordered_leakage_and_gauge_are_next_not_validation"

    with (ROOT / "data/derived/kids1000_cosebis_physical_promotion_dependency_order_v1.csv").open(
        newline=""
    ) as f:
        dependency_rows = {row["blocker_id"]: row for row in csv.DictReader(f)}
    assert dependency_rows["B2_operator_leakage_theorem_open"]["dependency_status"] == "NEXT_PRIMARY_PROOF_GATE"
    assert dependency_rows["B3_gauge_quotient_descent_open"]["dependency_status"] == "NEXT_PARALLEL_PROOF_GATE"
    assert dependency_rows["B1_survey_native_operator_theorem_open"]["dependency_status"] == "FINAL_SYNTHESIS_PROOF_GATE"


def test_kids1000_cosebis_operator_leakage_proof_plan_freezes_exit_conditions_not_theorem() -> None:
    subprocess.run(
        ["python", "scripts/build_kids1000_cosebis_operator_leakage_proof_plan_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/validate_kids1000_cosebis_operator_leakage_proof_plan_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with (ROOT / "data/derived/kids1000_cosebis_operator_leakage_proof_plan_v1_summary.csv").open(
        newline=""
    ) as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 1
    summary = rows[0]
    assert summary["status"] == "OPERATOR_LEAKAGE_PROOF_PLAN_BUILT_NOT_PROOF"
    assert summary["proof_plan_rows"] == "5"
    assert summary["anchor_available_count"] == "1"
    assert summary["guard_satisfied_count"] == "1"
    assert summary["open_proof_step_count"] == "3"
    assert summary["operator_leakage_theorem_proven"] == "false"
    assert summary["physical_promotion_ready"] == "false"
    assert summary["validation_ready"] == "false"
    assert summary["computes_new_scores"] == "false"
    assert summary["uses_kids_data_vector_values_for_source_selection"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert summary["verdict"] == "B2_operator_leakage_exit_conditions_frozen_but_theorem_open"

    with (ROOT / "data/derived/kids1000_cosebis_operator_leakage_proof_plan_v1.csv").open(newline="") as f:
        plan = {row["step_id"]: row for row in csv.DictReader(f)}
    assert plan["P1_uniform_null_limit_anchor"]["step_status"] == "ANCHOR_AVAILABLE"
    assert plan["P2_nonuniform_leakage_projection"]["step_status"] == "PRIMARY_OPEN_PROOF_STEP"
    assert plan["P3_pure_mask_quotient_or_control"]["step_status"] == "PRIMARY_OPEN_PROOF_STEP"
    assert plan["P4_single_operator_coupling"]["step_status"] == "COUPLING_OPEN_PROOF_STEP"
    assert plan["P5_no_endpoint_feedback_guard"]["step_status"] == "GUARD_SATISFIED"


def test_kids1000_cosebis_operator_leakage_domain_decomposition_is_bookkeeping_only() -> None:
    subprocess.run(
        ["python", "scripts/build_kids1000_cosebis_operator_leakage_domain_decomposition_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/validate_kids1000_cosebis_operator_leakage_domain_decomposition_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with (ROOT / "data/derived/kids1000_cosebis_operator_leakage_domain_decomposition_v1_summary.csv").open(
        newline=""
    ) as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 1
    summary = rows[0]
    assert summary["status"] == "OPERATOR_LEAKAGE_DOMAIN_DECOMPOSITION_DECLARED_NOT_PROJECTION_PROOF"
    assert summary["component_rows"] == "5"
    assert summary["domain_decomposition_declared"] == "true"
    assert summary["candidate_physical_component_declared"] == "true"
    assert summary["mask_component_declared"] == "true"
    assert summary["control_or_null_component_declared"] == "true"
    assert summary["no_endpoint_feedback_guard_satisfied"] == "true"
    assert summary["components_pairwise_orthogonality_proven"] == "false"
    assert summary["mask_component_quotient_triviality_proven"] == "false"
    assert summary["operator_projection_condition_proven"] == "false"
    assert summary["control_routing_condition_proven"] == "false"
    assert summary["single_operator_consistency_proven"] == "false"
    assert summary["operator_leakage_theorem_proven"] == "false"
    assert summary["p2_nonuniform_leakage_closed"] == "false"
    assert summary["physical_promotion_ready"] == "false"
    assert summary["validation_ready"] == "false"
    assert summary["computes_new_scores"] == "false"
    assert summary["uses_kids_data_vector_values_for_source_selection"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert summary["verdict"] == "domain_decomposition_declared_but_projection_and_leakage_theorem_remain_open"

    with (ROOT / "data/derived/kids1000_cosebis_operator_leakage_domain_decomposition_v1.csv").open(
        newline=""
    ) as f:
        components = {row["component_id"]: row for row in csv.DictReader(f)}
    assert components["V_phys_candidate"]["component_status"] == "DECLARED_CANDIDATE_NOT_PHYSICAL_PROOF"
    assert components["V_mask"]["component_status"] == "DECLARED_MASK_ONLY_BASIS_NOT_NULL_PROVEN"
    assert components["V_control_or_null"]["component_status"] == "DECLARED_CONTROL_OR_NULL_NOT_SIGNAL"
    assert components["decomposition_status"]["component_status"] == "DECLARED_BOOKKEEPING_NOT_PROJECTION_PROOF"


def test_kids1000_cosebis_operator_leakage_projection_criterion_is_not_a_proof() -> None:
    subprocess.run(
        ["python", "scripts/build_kids1000_cosebis_operator_leakage_domain_decomposition_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/build_kids1000_cosebis_operator_leakage_projection_criterion_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/validate_kids1000_cosebis_operator_leakage_projection_criterion_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with (ROOT / "data/derived/kids1000_cosebis_operator_leakage_projection_criterion_v1_summary.csv").open(
        newline=""
    ) as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 1
    summary = rows[0]
    assert summary["status"] == "OPERATOR_LEAKAGE_PROJECTION_CRITERION_BUILT_NOT_PROVEN"
    assert summary["criterion_rows"] == "5"
    assert summary["sufficient_projection_criterion_frozen"] == "true"
    assert summary["domain_decomposition_declared"] == "true"
    assert summary["null_projection_condition_proven"] == "false"
    assert summary["control_routing_condition_proven"] == "false"
    assert summary["single_operator_consistency_proven"] == "false"
    assert summary["operator_leakage_theorem_proven"] == "false"
    assert summary["p2_nonuniform_leakage_closed"] == "false"
    assert summary["physical_promotion_ready"] == "false"
    assert summary["validation_ready"] == "false"
    assert summary["computes_new_scores"] == "false"
    assert summary["uses_kids_data_vector_values_for_source_selection"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert summary["verdict"] == "nonuniform_leakage_projection_criterion_frozen_but_not_proven"

    with (ROOT / "data/derived/kids1000_cosebis_operator_leakage_projection_criterion_v1.csv").open(
        newline=""
    ) as f:
        criteria = {row["criterion_id"]: row for row in csv.DictReader(f)}
    assert criteria["C1_domain_decomposition"]["criterion_status"] == "DECLARED_NOT_PROJECTION_PROOF"
    assert criteria["C2_null_projection_condition"]["criterion_status"] == "SUFFICIENT_CONDITION_FROZEN_NOT_PROVEN"
    assert (
        criteria["C3_control_routing_alternative"]["criterion_status"]
        == "ALTERNATIVE_SUFFICIENT_CONDITION_FROZEN_NOT_PROVEN"
    )
    assert criteria["C5_theorem_status"]["criterion_status"] == "OPEN_NOT_PROVEN"


def test_act_dr6_lensing_acquisition_manifest_is_source_side_only() -> None:
    subprocess.run(
        ["python", "scripts/build_act_dr6_lensing_product_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/validate_act_dr6_lensing_product_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with (ROOT / "data/source_manifest/act_dr6_lensing_product_v1.csv").open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 1
    row = rows[0]
    assert row["artifact_id"] == "ACT_DR6_LENSING_PRODUCT_V1"
    assert row["provider"] == "NASA_LAMBDA_ACT_DR6"
    assert row["expected_byte_count"] == "1371472486"
    assert row["endpoint_replay_allowed"] == "false"
    assert row["endpoint_validation_claimed"] == "false"
    assert row["physical_lensing_path_weight_claimed"] == "false"
    assert row["contains_distance_residuals"] == "false"
    assert row["contains_fit_statistics"] == "false"
    if row["download_complete"] == "true":
        assert row["local_byte_count"] == row["expected_byte_count"]
        assert row["sha256"]
    else:
        assert row["metric_lensing_numeric_product_available_for_source"] == "false"


def test_act_dr6_lensing_inventory_has_science_and_null_control_variants() -> None:
    subprocess.run(
        ["python", "scripts/build_act_dr6_lensing_inventory_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/validate_act_dr6_lensing_inventory_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with (ROOT / "data/derived/act_dr6_lensing_inventory_v1_summary.csv").open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 1
    summary = rows[0]
    assert summary["status"] == "SOURCE_INVENTORY_BUILT_NOT_ENDPOINT"
    assert summary["variant_count"] == "13"
    assert summary["kappa_alm_products"] == "13"
    assert summary["mask_products"] == "13"
    assert summary["recommended_science_variant_available"] == "true"
    assert summary["null_control_variants_available"] == "true"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_lensing_path_weight_claimed"] == "false"


def test_act_dr6_lensing_low_z_sampling_pilot_is_source_side_only() -> None:
    subprocess.run(
        ["python", "scripts/build_act_dr6_lensing_low_z_sampling_pilot_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/validate_act_dr6_lensing_low_z_sampling_pilot_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with (ROOT / "data/derived/act_dr6_lensing_low_z_sampling_pilot_v1_summary.csv").open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 1
    summary = rows[0]
    assert summary["status"] == "SOURCE_SIDE_SAMPLING_PILOT_BUILT_NOT_ENDPOINT"
    assert summary["source_rows"] == "424"
    assert summary["nside_map"] == "512"
    assert summary["lmax_out"] == "1024"
    assert summary["variants_sampled"] == "baseline;curl;diff_f150_f090"
    assert summary["baseline_sample_finite_count"] == summary["source_rows"]
    assert summary["curl_sample_finite_count"] == summary["source_rows"]
    assert summary["diff_f150_f090_sample_finite_count"] == summary["source_rows"]
    assert int(summary["mask_positive_count"]) + int(summary["mask_zero_count"]) == int(summary["source_rows"])
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_lensing_path_weight_claimed"] == "false"
    assert summary["contains_distance_residuals"] == "false"
    assert summary["contains_fit_statistics"] == "false"


def test_act_dr6_lensing_path_weight_candidate_is_review_ready_not_endpoint() -> None:
    for command in [
        ["python", "scripts/build_act_dr6_lensing_low_z_sampling_pilot_v1.py"],
        ["python", "scripts/validate_act_dr6_lensing_low_z_sampling_pilot_v1.py"],
        ["python", "scripts/build_act_dr6_lensing_path_weight_candidate_v1.py"],
        ["python", "scripts/validate_act_dr6_lensing_path_weight_candidate_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/act_dr6_lensing_path_weight_candidate_v1_summary.csv").open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 1
    summary = rows[0]
    assert summary["status"] == "SOURCE_SIDE_PATH_WEIGHT_CANDIDATE_BUILT_NOT_ENDPOINT"
    assert summary["source_rows"] == "424"
    assert summary["mask_positive_rows"] == "168"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_lensing_path_weight_claimed"] == "false"
    assert summary["contains_distance_residuals"] == "false"
    assert summary["contains_fit_statistics"] == "false"
    assert summary["verdict"] == "act_dr6_source_side_path_weight_candidate_ready_for_review_not_endpoint"


def test_act_dr6_lensing_path_weight_authorization_package_is_not_completed() -> None:
    for command in [
        ["python", "scripts/build_act_dr6_lensing_path_weight_replay_authorization_review_package_v1.py"],
        ["python", "scripts/validate_act_dr6_lensing_path_weight_replay_authorization_review_package_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (
        ROOT / "data/derived/act_dr6_lensing_path_weight_replay_authorization_review_package_v1_summary.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 1
    summary = rows[0]
    assert summary["status"] == "ACT_DR6_LENSING_PATH_WEIGHT_REPLAY_AUTHORIZATION_PACKAGE_BUILT_NOT_COMPLETED"
    assert summary["review_completed"] == "false"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["contains_endpoint_residuals"] == "false"
    assert summary["contains_endpoint_scores"] == "false"
    assert summary["contains_fit_statistics"] == "false"
    assert summary["physical_lensing_path_weight_claimed"] == "false"
    assert summary["verdict"] == "act_dr6_lensing_path_weight_authorization_package_ready_not_completed"


def test_act_dr6_lensing_path_weight_completed_response_validator_is_permission_only(
    tmp_path: Path,
) -> None:
    template = ROOT / "data/derived/act_dr6_lensing_path_weight_replay_authorization_review_response_template_v1.csv"
    if not template.exists():
        subprocess.run(
            ["python", "scripts/build_act_dr6_lensing_path_weight_replay_authorization_review_package_v1.py"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    with template.open(newline="") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        row["reviewer_answer"] = (
            "authorize_replay_as_caveated_candidate"
            if row["question_id"] == "Q5_replay_permission"
            else "accept_with_caveat"
        )
        row["reviewer_notes"] = "pytest smoke response based only on package contents"
    response = tmp_path / "act_response.csv"
    with response.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    summary_out = tmp_path / "act_response_summary.csv"
    subprocess.run(
        [
            "python",
            "scripts/validate_act_dr6_lensing_path_weight_replay_authorization_review_response_v1.py",
            str(response),
            "--summary-out",
            str(summary_out),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with summary_out.open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["review_completed"] == "true"
    assert summary["permission_only_replay_authorized"] == "true"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_lensing_path_weight_claimed"] == "false"
    assert summary["verdict"] == "act_dr6_lensing_path_weight_caveated_replay_authorized_not_validation"


def test_act_dr6_lensing_path_weight_replay_run_template_requires_authorization() -> None:
    for command in [
        ["python", "scripts/build_act_dr6_lensing_path_weight_replay_run_template_v1.py"],
        ["python", "scripts/validate_act_dr6_lensing_path_weight_replay_run_template_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/act_dr6_lensing_path_weight_replay_run_template_v1_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "ACT_DR6_LENSING_PATH_WEIGHT_REPLAY_PREPARED_AUTH_REQUIRED_NOT_VALIDATION"
    assert summary["control_branch_count"] == "6"
    assert summary["forbidden_input_count"] == "11"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_lensing_path_weight_claimed"] == "false"
    assert summary["physical_validation_claimed"] == "false"
    assert summary["verdict"] == "act_dr6_lensing_path_weight_replay_template_ready_auth_required_not_validation"


def test_act_dr6_lensing_path_weight_authorized_replay_blocks_without_authorization(
    tmp_path: Path,
) -> None:
    for command in [
        ["python", "scripts/build_act_dr6_lensing_path_weight_replay_run_template_v1.py"],
        ["python", "scripts/validate_act_dr6_lensing_path_weight_replay_run_template_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    env = {
        **os.environ,
        "ACT_DR6_LENSING_PATH_WEIGHT_AUTH_SUMMARY": str(tmp_path / "missing_authorization_summary.csv"),
    }
    result = subprocess.run(
        ["python", "scripts/run_act_dr6_lensing_path_weight_authorized_replay_v1.py"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )
    combined_output = result.stdout + result.stderr
    assert result.returncode != 0
    assert "missing required input" in combined_output


def test_act_dr6_lensing_path_weight_authorized_replay_is_control_dominated() -> None:
    subprocess.run(
        ["python", "scripts/validate_act_dr6_lensing_path_weight_authorized_replay_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with (ROOT / "data/derived/act_dr6_lensing_path_weight_authorized_replay_v1_summary.csv").open(
        newline=""
    ) as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "ACT_DR6_LENSING_PATH_WEIGHT_AUTHORIZED_REPLAY_PERMISSION_ONLY_NOT_VALIDATION"
    assert summary["authorization_verdict"] == "act_dr6_lensing_path_weight_caveated_replay_authorized_not_validation"
    assert summary["best_control_branch"] == "curl_null"
    assert summary["controls_better_than_candidate"] == "4"
    assert summary["family_survives_controls"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_lensing_path_weight_claimed"] == "false"
    assert (
        summary["verdict"]
        == "act_dr6_lensing_path_weight_candidate_not_control_resistant_permission_only_not_validation"
    )


def test_act_dr6_lensing_path_weight_control_dominance_diagnostic_preserves_negative_result() -> None:
    for command in [
        ["python", "scripts/build_act_dr6_lensing_path_weight_control_dominance_diagnostic_v1.py"],
        ["python", "scripts/validate_act_dr6_lensing_path_weight_control_dominance_diagnostic_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (
        ROOT / "data/derived/act_dr6_lensing_path_weight_control_dominance_diagnostic_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "CONTROL_DOMINANCE_DIAGNOSTIC_BUILT_NOT_VALIDATION"
    assert summary["best_control_branch"] == "curl_null"
    assert summary["controls_better_than_candidate"] == "4"
    assert float(summary["candidate_delta_chi2_vs_baseline"]) < 0
    assert float(summary["candidate_delta_chi2_vs_best_control"]) > 0
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_lensing_path_weight_claimed"] == "false"
    assert summary["verdict"] == "ACT_PATH_WEIGHT_WEAK_NON_SPECIFIC_SIGNAL_CONTROL_DOMINATED"


def test_act_dr6_lensing_path_weight_paper11_control_veto_gate_blocks_family_verdict() -> None:
    for command in [
        ["python", "scripts/build_act_dr6_lensing_path_weight_paper11_control_veto_gate_v1.py"],
        ["python", "scripts/validate_act_dr6_lensing_path_weight_paper11_control_veto_gate_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (
        ROOT / "data/derived/act_dr6_lensing_path_weight_paper11_control_veto_gate_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["status"] == "PAPER11_STYLE_CONTROL_VETO_GATE_BUILT_NOT_VALIDATION"
    assert summary["best_control_branch"] == "curl_null"
    assert summary["controls_better_than_candidate"] == "4"
    assert summary["family_survives_controls"] == "false"
    assert summary["m0_or_m1_source_structure_claim_allowed"] == "false"
    assert summary["m2_dark_sector_inference_allowed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_lensing_path_weight_claimed"] == "false"
    assert (
        summary["verdict"]
        == "PAPER11_CONTROL_VETO_ACT_PATH_WEIGHT_NOT_FAMILY_VERDICT_ELIGIBLE"
    )


def test_act_dr6_lensing_path_weight_source_basis_gate_demotes_current_basis() -> None:
    for command in [
        ["python", "scripts/build_act_dr6_lensing_observer_path_source_object_v1.py"],
        ["python", "scripts/validate_act_dr6_lensing_observer_path_source_object_v1.py"],
        ["python", "scripts/build_act_dr6_lensing_e_mode_route_v1.py"],
        ["python", "scripts/validate_act_dr6_lensing_e_mode_route_v1.py"],
        ["python", "scripts/build_act_dr6_lensing_curl_null_policy_v1.py"],
        ["python", "scripts/validate_act_dr6_lensing_curl_null_policy_v1.py"],
        ["python", "scripts/build_act_dr6_lensing_mask_coverage_policy_v1.py"],
        ["python", "scripts/validate_act_dr6_lensing_mask_coverage_policy_v1.py"],
        ["python", "scripts/build_act_dr6_lensing_units_normalization_policy_v1.py"],
        ["python", "scripts/validate_act_dr6_lensing_units_normalization_policy_v1.py"],
        ["python", "scripts/build_act_dr6_lensing_channel_handoff_policy_v1.py"],
        ["python", "scripts/validate_act_dr6_lensing_channel_handoff_policy_v1.py"],
        ["python", "scripts/build_act_dr6_lensing_control_suite_policy_v1.py"],
        ["python", "scripts/validate_act_dr6_lensing_control_suite_policy_v1.py"],
        ["python", "scripts/build_act_dr6_lensing_path_weight_source_basis_freeze_or_demote_gate_v1.py"],
        ["python", "scripts/validate_act_dr6_lensing_path_weight_source_basis_freeze_or_demote_gate_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (
        ROOT / "data/derived/act_dr6_lensing_path_weight_source_basis_freeze_or_demote_gate_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/act_dr6_lensing_path_weight_source_basis_freeze_or_demote_gate_v1_checklist.csv"
    ).open(newline="") as f:
        checklist = list(csv.DictReader(f))
    assert summary["decision"] == "DEMOTE_CURRENT_UNITLESS_ACT_PATH_WEIGHT_BASIS"
    assert summary["current_basis_replay_allowed_now"] == "false"
    assert summary["reopen_allowed_with_new_source_freeze"] == "true"
    assert summary["source_object_defined_source_side"] == "true"
    assert summary["e_mode_route_defined_source_side"] == "true"
    assert summary["curl_null_policy_frozen_source_side"] == "true"
    assert summary["curl_current_branch_vetoed"] == "true"
    assert summary["mask_coverage_policy_frozen_source_side"] == "true"
    assert summary["units_normalization_policy_frozen_source_side"] == "true"
    assert summary["physical_normalization_blocker_open"] == "true"
    assert summary["channel_handoff_policy_frozen_source_side"] == "true"
    assert summary["channel_handoff_source_diagnostic_only"] == "true"
    assert summary["control_suite_policy_frozen_source_side"] == "true"
    assert summary["control_suite_replay_disabled"] == "true"
    assert summary["dark_sector_inference_allowed"] == "false"
    assert summary["verdict"] == "ACT_SOURCE_BASIS_DEMOTED_REOPEN_ONLY_WITH_NEW_SOURCE_FREEZE"
    assert {row["current_status"] for row in checklist} >= {
        "DEFINED_SOURCE_SIDE",
        "FROZEN_SOURCE_SIDE",
        "FROZEN_SOURCE_SIDE_VETO_ACTIVE",
        "PROXY_FROZEN_PHYSICAL_BLOCKER_OPEN",
        "SOURCE_DIAGNOSTIC_ONLY_NOT_PHYSICAL_K_PATH",
        "FROZEN_CURRENT_BRANCH_REPLAY_STILL_DISABLED",
    }
    assert all(row["required_for_reopen"] == "true" for row in checklist)
    assert any(
        row["requirement_id"] == "ACT_REOPEN_01_SOURCE_OBJECT"
        and row["current_status"] == "DEFINED_SOURCE_SIDE"
        for row in checklist
    )
    assert any(
        row["requirement_id"] == "ACT_REOPEN_06_CHANNEL_HANDOFF"
        and row["current_status"] == "SOURCE_DIAGNOSTIC_ONLY_NOT_PHYSICAL_K_PATH"
        for row in checklist
    )
    assert any(
        row["requirement_id"] == "ACT_REOPEN_07_CONTROL_SUITE"
        and row["current_status"] == "FROZEN_CURRENT_BRANCH_REPLAY_STILL_DISABLED"
        for row in checklist
    )
    assert any(
        row["requirement_id"] == "ACT_REOPEN_05_UNITS_AND_NORMALIZATION"
        and row["current_status"] == "PROXY_FROZEN_PHYSICAL_BLOCKER_OPEN"
        for row in checklist
    )
    assert any(
        row["requirement_id"] == "ACT_REOPEN_02_E_MODE_ROUTE"
        and row["current_status"] == "DEFINED_SOURCE_SIDE"
        for row in checklist
    )
    assert any(
        row["requirement_id"] == "ACT_REOPEN_03_CURL_NULL_POLICY"
        and row["current_status"] == "FROZEN_SOURCE_SIDE_VETO_ACTIVE"
        for row in checklist
    )
    assert any(
        row["requirement_id"] == "ACT_REOPEN_04_MASK_AND_COVERAGE_POLICY"
        and row["current_status"] == "FROZEN_SOURCE_SIDE"
        for row in checklist
    )


def test_act_dr6_lensing_observer_path_source_object_is_source_side_only() -> None:
    for command in [
        ["python", "scripts/build_act_dr6_lensing_observer_path_source_object_v1.py"],
        ["python", "scripts/validate_act_dr6_lensing_observer_path_source_object_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (
        ROOT / "data/source_manifest/act_dr6_lensing_observer_path_source_object_v1.csv"
    ).open(newline="") as f:
        source_object = list(csv.DictReader(f))[0]
    assert source_object["status"] == "SOURCE_OBJECT_DEFINED_SOURCE_SIDE_NOT_ENDPOINT"
    assert source_object["endpoint_replay_allowed"] == "false"
    assert source_object["physical_lensing_path_weight_claimed"] == "false"
    assert source_object["dark_sector_inference_allowed"] == "false"
    assert "convergence reconstruction samples" in source_object["source_object_definition"]
    assert "not a metric/lensing path integral" in source_object["what_it_is_not"]
    assert "remaining source-basis requirements" in source_object["claim_boundary"]


def test_act_dr6_lensing_e_mode_route_is_source_route_only() -> None:
    for command in [
        ["python", "scripts/build_act_dr6_lensing_observer_path_source_object_v1.py"],
        ["python", "scripts/validate_act_dr6_lensing_observer_path_source_object_v1.py"],
        ["python", "scripts/build_act_dr6_lensing_e_mode_route_v1.py"],
        ["python", "scripts/validate_act_dr6_lensing_e_mode_route_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/source_manifest/act_dr6_lensing_e_mode_route_v1.csv").open(newline="") as f:
        route = list(csv.DictReader(f))[0]
    assert route["status"] == "E_MODE_ROUTE_DEFINED_SOURCE_SIDE_NOT_PHYSICAL_KERNEL"
    assert route["candidate_variant"] == "baseline"
    assert route["candidate_variant_role"] == "recommended_science_variant"
    assert route["baseline_has_kappa_alm_modes"] == "true"
    assert route["endpoint_replay_allowed"] == "false"
    assert route["physical_lensing_path_weight_claimed"] == "false"
    assert "does not prove a physical E/B theorem" in route["what_this_does_not_define"]


def test_act_dr6_lensing_curl_null_policy_vetoes_current_branch() -> None:
    for command in [
        ["python", "scripts/build_act_dr6_lensing_curl_null_policy_v1.py"],
        ["python", "scripts/validate_act_dr6_lensing_curl_null_policy_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/source_manifest/act_dr6_lensing_curl_null_policy_v1.csv").open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert policy["status"] == "CURL_NULL_POLICY_FROZEN_SOURCE_SIDE_NOT_THEOREM"
    assert policy["curl_is_predeclared_null_control"] == "true"
    assert policy["observed_control_status"] == "curl_null_best_control"
    assert policy["curl_as_positive_channel_allowed"] == "false"
    assert policy["endpoint_replay_allowed"] == "false"
    assert policy["physical_lensing_path_weight_claimed"] == "false"
    assert policy["verdict"] == "ACT_REOPEN_03_CURL_NULL_POLICY_FROZEN_AND_CURRENT_BRANCH_VETOED"


def test_act_dr6_lensing_mask_coverage_policy_freezes_rows_without_selection() -> None:
    for command in [
        ["python", "scripts/build_act_dr6_lensing_mask_coverage_policy_v1.py"],
        ["python", "scripts/validate_act_dr6_lensing_mask_coverage_policy_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/source_manifest/act_dr6_lensing_mask_coverage_policy_v1.csv").open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert policy["status"] == "MASK_COVERAGE_POLICY_FROZEN_SOURCE_SIDE_NOT_REPLAY"
    assert policy["source_rows"] == "424"
    assert policy["mask_positive_rows"] == "168"
    assert policy["mask_zero_rows"] == "256"
    assert policy["outside_mask_policy"] == "assign_zero_weight_keep_rows_in_scope"
    assert policy["row_selection_policy"] == "no_endpoint_row_drop_or_posthoc_selection"
    assert policy["endpoint_replay_allowed"] == "false"
    assert "does not authorize dropping rows" in policy["what_this_does_not_define"]


def test_act_dr6_lensing_units_normalization_policy_freezes_proxy_only() -> None:
    for command in [
        ["python", "scripts/build_act_dr6_lensing_units_normalization_policy_v1.py"],
        ["python", "scripts/validate_act_dr6_lensing_units_normalization_policy_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (
        ROOT / "data/source_manifest/act_dr6_lensing_units_normalization_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert policy["status"] == "UNITLESS_PROXY_NORMALIZATION_FROZEN_PHYSICAL_NORMALIZATION_MISSING"
    assert policy["current_normalization_rule"] == "mask_positive_only_median_center_mad_scale_else_zero"
    assert policy["normalization_domain"] == "mask_positive_rows_only"
    assert policy["current_units_status"] == "dimensionless_standardized_proxy"
    assert policy["physical_units_available"] == "false"
    assert policy["physical_normalization_allowed_now"] == "false"
    assert policy["proxy_normalization_allowed_for_source_diagnostics"] == "true"
    assert policy["endpoint_replay_allowed"] == "false"
    assert policy["physical_lensing_path_weight_claimed"] == "false"
    assert "theorem-bounded mapping" in policy["required_for_physical_reopen"]
    assert "does not define physical path-weight units" in policy["what_this_does_not_define"]
    assert policy["verdict"] == "ACT_REOPEN_05_UNITS_NORMALIZATION_PROXY_FROZEN_PHYSICAL_BLOCKER_OPEN"


def test_act_dr6_lensing_channel_handoff_policy_demotes_to_source_diagnostic() -> None:
    for command in [
        ["python", "scripts/build_act_dr6_lensing_observer_path_source_object_v1.py"],
        ["python", "scripts/build_act_dr6_lensing_e_mode_route_v1.py"],
        ["python", "scripts/build_act_dr6_lensing_curl_null_policy_v1.py"],
        ["python", "scripts/build_act_dr6_lensing_units_normalization_policy_v1.py"],
        ["python", "scripts/build_act_dr6_lensing_channel_handoff_policy_v1.py"],
        ["python", "scripts/validate_act_dr6_lensing_channel_handoff_policy_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (
        ROOT / "data/source_manifest/act_dr6_lensing_channel_handoff_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert policy["status"] == "CHANNEL_HANDOFF_FROZEN_AS_SOURCE_DIAGNOSTIC_NOT_PHYSICAL_K_PATH"
    assert policy["candidate_tau_channel_requested"] == "K_path_observer_path"
    assert policy["current_tau_channel_status"] == "K_path_candidate_source_diagnostic_only"
    assert policy["positive_k_path_promotion_allowed"] == "false"
    assert policy["k_closure_handoff_allowed"] == "false"
    assert policy["k_null_handoff_allowed_for_curl"] == "true"
    assert policy["source_diagnostic_handoff_allowed"] == "true"
    assert policy["endpoint_replay_allowed"] == "false"
    assert policy["family_verdict_allowed"] == "false"
    assert "physical units are missing" in policy["why_not_positive_k_path"]
    assert "curl_null as the best control" in policy["why_not_positive_k_path"]
    assert "no closure equation" in policy["why_not_k_closure"]
    assert policy["verdict"] == "ACT_REOPEN_06_CHANNEL_HANDOFF_SOURCE_DIAGNOSTIC_ONLY"


def test_act_dr6_lensing_control_suite_policy_freezes_current_controls() -> None:
    for command in [
        ["python", "scripts/build_act_dr6_lensing_control_suite_policy_v1.py"],
        ["python", "scripts/validate_act_dr6_lensing_control_suite_policy_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (
        ROOT / "data/source_manifest/act_dr6_lensing_control_suite_policy_v1.csv"
    ).open(newline="") as f:
        controls = list(csv.DictReader(f))
    with (
        ROOT / "data/derived/act_dr6_lensing_control_suite_policy_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert {row["control_id"] for row in controls} == {
        "off",
        "baseline_only",
        "curl_null",
        "diff_f150_f090_null",
        "wrong_sign",
        "deterministic_shuffle",
        "rank_reverse",
        "source_basis_recenter_stress",
    }
    assert {row["control_channel"] for row in controls} == {"K_null"}
    assert any(
        row["control_id"] == "curl_null"
        and row["current_status"] == "FROZEN_SCORED_CONTROL_VETO_ACTIVE"
        for row in controls
    )
    assert any(
        row["control_id"] == "source_basis_recenter_stress"
        and row["scored_in_current_replay"] == "false"
        for row in controls
    )
    assert summary["status"] == "CURRENT_CONTROL_SUITE_FROZEN_VALIDATION_REOPEN_STRESS_DECLARED"
    assert summary["scored_control_count"] == "7"
    assert summary["declared_control_count"] == "8"
    assert summary["missing_scored_controls"] == "none"
    assert summary["curl_veto_active"] == "true"
    assert summary["current_suite_replay_allowed"] == "false"
    assert summary["verdict"] == "ACT_REOPEN_07_CONTROL_SUITE_FROZEN_CURRENT_BRANCH_REPLAY_STILL_DISABLED"


def test_act_dr6_lensing_reopen_closure_ledger_quarantines_current_branch() -> None:
    for command in [
        ["python", "scripts/build_act_dr6_lensing_observer_path_source_object_v1.py"],
        ["python", "scripts/build_act_dr6_lensing_e_mode_route_v1.py"],
        ["python", "scripts/build_act_dr6_lensing_curl_null_policy_v1.py"],
        ["python", "scripts/build_act_dr6_lensing_mask_coverage_policy_v1.py"],
        ["python", "scripts/build_act_dr6_lensing_units_normalization_policy_v1.py"],
        ["python", "scripts/build_act_dr6_lensing_channel_handoff_policy_v1.py"],
        ["python", "scripts/build_act_dr6_lensing_control_suite_policy_v1.py"],
        ["python", "scripts/build_act_dr6_lensing_path_weight_source_basis_freeze_or_demote_gate_v1.py"],
        ["python", "scripts/build_act_dr6_lensing_reopen_closure_ledger_v1.py"],
        ["python", "scripts/validate_act_dr6_lensing_reopen_closure_ledger_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (ROOT / "data/derived/act_dr6_lensing_reopen_closure_ledger_v1.csv").open(newline="") as f:
        rows = list(csv.DictReader(f))
    with (
        ROOT / "data/derived/act_dr6_lensing_reopen_closure_ledger_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert {row["requirement_id"] for row in rows} == {
        "ACT_REOPEN_01_SOURCE_OBJECT",
        "ACT_REOPEN_02_E_MODE_ROUTE",
        "ACT_REOPEN_03_CURL_NULL_POLICY",
        "ACT_REOPEN_04_MASK_AND_COVERAGE_POLICY",
        "ACT_REOPEN_05_UNITS_AND_NORMALIZATION",
        "ACT_REOPEN_06_CHANNEL_HANDOFF",
        "ACT_REOPEN_07_CONTROL_SUITE",
    }
    assert {row["endpoint_replay_allowed"] for row in rows} == {"false"}
    assert summary["all_reopen_gates_accounted"] == "true"
    assert summary["all_reopen_gates_closed_or_frozen"] == "true"
    assert summary["current_branch_control_dominated"] == "true"
    assert summary["current_branch_endpoint_replay_allowed"] == "false"
    assert summary["best_control_branch"] == "curl_null"
    assert summary["verdict"] == "ACT_REOPEN_CLOSED_CURRENT_BRANCH_QUARANTINED_NOT_VALIDATION"


def test_act_dr6_lensing_next_source_basis_design_scaffold_blocks_replay() -> None:
    for command in [
        ["python", "scripts/build_act_dr6_lensing_next_source_basis_design_scaffold_v1.py"],
        ["python", "scripts/validate_act_dr6_lensing_next_source_basis_design_scaffold_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (
        ROOT / "data/source_manifest/act_dr6_lensing_next_source_basis_design_scaffold_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    with (
        ROOT / "data/derived/act_dr6_lensing_next_source_basis_design_scaffold_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert {row["design_requirement_id"] for row in rows} == {
        "ACT_NEXT_BASIS_01_PHYSICAL_K_PATH_MAPPING",
        "ACT_NEXT_BASIS_02_OPERATOR_QUOTIENT_DESCENT",
        "ACT_NEXT_BASIS_03_MASK_COVERAGE_POPULATION_POLICY",
        "ACT_NEXT_BASIS_04_SOURCE_BASIS_RECENTER_STRESS",
        "ACT_NEXT_BASIS_05_CONTROL_SUITE_PRECOMMIT",
        "ACT_NEXT_BASIS_06_CHANNEL_HANDOFF_DECISION",
        "ACT_NEXT_BASIS_07_FORBIDDEN_ENDPOINT_FIELDS",
    }
    assert {row["endpoint_replay_allowed"] for row in rows} == {"false"}
    assert {row["endpoint_validation_claimed"] for row in rows} == {"false"}
    assert summary["requirements_count"] == "7"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["current_branch_status"] == "previous_ACT_branch_quarantined_control_dominated"
    assert summary["verdict"] == "ACT_NEXT_SOURCE_BASIS_DESIGN_SCAFFOLD_FROZEN_NOT_REPLAY"


def test_act_dr6_lensing_caveated_kpath_source_design_requires_review() -> None:
    for command in [
        ["python", "scripts/build_act_dr6_lensing_product_v1.py"],
        ["python", "scripts/build_act_dr6_lensing_path_weight_candidate_v1.py"],
        ["python", "scripts/build_act_dr6_lensing_path_weight_source_basis_freeze_or_demote_gate_v1.py"],
        ["python", "scripts/build_act_dr6_lensing_reopen_closure_ledger_v1.py"],
        ["python", "scripts/build_act_dr6_lensing_next_source_basis_design_scaffold_v1.py"],
        ["python", "scripts/build_act_dr6_lensing_caveated_kpath_source_design_v1.py"],
        ["python", "scripts/validate_act_dr6_lensing_caveated_kpath_source_design_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (
        ROOT / "data/source_manifest/act_dr6_lensing_caveated_kpath_source_design_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    with (
        ROOT / "data/derived/act_dr6_lensing_caveated_kpath_source_design_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert {row["design_item_id"] for row in rows} == {
        "CKPATH_01_SOURCE_PRODUCT",
        "CKPATH_02_PROXY_MAPPING",
        "CKPATH_03_NULL_QUOTIENT_RULE",
        "CKPATH_04_COVERAGE_SCOPE",
        "CKPATH_05_REPLAY_PRECONDITIONS",
    }
    assert {row["endpoint_replay_allowed"] for row in rows} == {"false"}
    assert {row["physical_path_weight_claimed"] for row in rows} == {"false"}
    assert summary["mapping_status"] == "dimensionless_shape_proxy_only"
    assert summary["external_review_required_before_replay"] == "true"
    assert summary["endpoint_replay_allowed"] == "false"
    assert "curl_null" in summary["control_suite_required"]
    assert summary["verdict"] == "ACT_CAVEATED_KPATH_SOURCE_DESIGN_REVIEW_READY_NOT_REPLAY"


def test_act_dr6_lensing_caveated_kpath_source_design_review_package_ready() -> None:
    for command in [
        ["python", "scripts/build_act_dr6_lensing_caveated_kpath_source_design_review_package_v1.py"],
        ["python", "scripts/validate_act_dr6_lensing_caveated_kpath_source_design_review_package_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    package = ROOT / "data/derived/act_dr6_lensing_caveated_kpath_source_design_review_package_v1.zip"
    assert package.exists()
    with (
        ROOT / "data/derived/act_dr6_lensing_caveated_kpath_source_design_review_package_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/act_dr6_lensing_caveated_kpath_source_design_review_response_template_v1.csv"
    ).open(newline="") as f:
        template_rows = list(csv.DictReader(f))
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["physical_lensing_path_weight_claimed"] == "false"
    assert summary["verdict"] == "ACT_CAVEATED_KPATH_SOURCE_DESIGN_REVIEW_PACKAGE_READY"
    assert {row["review_item"] for row in template_rows} == {
        "source_product_status",
        "proxy_mapping_status",
        "null_control_status",
        "leakage_status",
        "overall_verdict",
    }


def test_act_dr6_lensing_caveated_kpath_source_design_review_response_is_narrow() -> None:
    subprocess.run(
        ["python", "scripts/validate_act_dr6_lensing_caveated_kpath_source_design_review_response_v1.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    with (
        ROOT / "data/derived/act_dr6_lensing_caveated_kpath_source_design_review_completed_summary_v1.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["decision"] == "ACCEPT_CAVEATED_KPATH_SOURCE_DESIGN_FOR_REVIEW_ONLY"
    assert summary["future_permission_only_replay_review_preparation_allowed"] == "true"
    assert summary["current_replay_authorized_by_this_review"] == "false"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["physical_lensing_path_weight_claimed"] == "false"


def test_act_dr6_lensing_caveated_kpath_replay_authorization_package_pending() -> None:
    for command in [
        ["python", "scripts/build_act_dr6_lensing_caveated_kpath_replay_authorization_review_package_v1.py"],
        ["python", "scripts/validate_act_dr6_lensing_caveated_kpath_replay_authorization_review_package_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (
        ROOT / "data/derived/act_dr6_lensing_caveated_kpath_replay_authorization_review_package_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with (
        ROOT / "data/derived/act_dr6_lensing_caveated_kpath_replay_authorization_review_response_template_v1.csv"
    ).open(newline="") as f:
        template_rows = list(csv.DictReader(f))
    assert summary["source_design_review_decision"] == "ACCEPT_CAVEATED_KPATH_SOURCE_DESIGN_FOR_REVIEW_ONLY"
    assert summary["review_completed"] == "false"
    assert summary["endpoint_replay_allowed"] == "false"
    assert summary["future_permission_only_replay_package_authorization_pending"] == "true"
    assert summary["verdict"] == "ACT_CAVEATED_KPATH_REPLAY_AUTHORIZATION_PACKAGE_READY_NOT_COMPLETED"
    assert {row["question_id"] for row in template_rows} == {
        "Q1_source_design_acceptance",
        "Q2_controls_required",
        "Q3_old_branch_quarantine",
        "Q4_forbidden_inputs",
        "Q5_permission_only_replay",
    }


def test_act_dr6_lensing_caveated_kpath_guarded_replay_package_ready_not_executed() -> None:
    for command in [
        ["python", "scripts/validate_act_dr6_lensing_caveated_kpath_replay_authorization_review_response_v1.py"],
        ["python", "scripts/build_act_dr6_lensing_caveated_kpath_guarded_replay_package_v1.py"],
        ["python", "scripts/validate_act_dr6_lensing_caveated_kpath_guarded_replay_package_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (
        ROOT / "data/derived/act_dr6_lensing_caveated_kpath_guarded_replay_package_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["authorization_verdict"] == "ACT_CAVEATED_KPATH_REPLAY_PACKAGE_PREPARATION_ALLOWED_NOT_SCORING"
    assert summary["endpoint_replay_executed"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["physical_lensing_path_weight_claimed"] == "false"
    assert summary["verdict"] == "ACT_CAVEATED_KPATH_GUARDED_REPLAY_PACKAGE_READY_NOT_EXECUTED"


def test_act_dr6_lensing_caveated_kpath_guarded_replay_preserves_negative_result() -> None:
    for command in [
        ["python", "scripts/run_act_dr6_lensing_caveated_kpath_guarded_replay_v1.py"],
        ["python", "scripts/validate_act_dr6_lensing_caveated_kpath_guarded_replay_v1.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    with (
        ROOT / "data/derived/act_dr6_lensing_caveated_kpath_guarded_replay_v1_summary.csv"
    ).open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    assert summary["candidate_best_chi2_act_path"] == "380.575996101"
    assert summary["baseline_best_chi2_act_path"] == "381.794196616"
    assert summary["best_control_branch"] == "curl_null"
    assert summary["controls_better_than_candidate"] == "4"
    assert summary["family_survives_controls"] == "false"
    assert summary["endpoint_validation_claimed"] == "false"
    assert summary["verdict"] == "ACT_CAVEATED_KPATH_GUARDED_REPLAY_CONTROL_DOMINATED_PERMISSION_ONLY_NOT_VALIDATION"
