from __future__ import annotations

import csv
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
        "paper10_submission_source/refs.bib",
        "paper10_submission_source/main.pdf",
        "arxiv_submission_source.zip",
        "data/derived/audit_gate_inventory.csv",
        "data/source_manifest/paper10_source_freeze_manifest.csv",
        "data/source_manifest/cosmology_channel_manifest_v1.csv",
        "data/source_manifest/cosmology_activation_rule_manifest_v1.csv",
        "data/source_manifest/cosmology_activation_parameter_freeze_plan_v1.csv",
        "data/source_manifest/cosmology_source_grounding_gate_v1.csv",
        "docs/cosmology_channel_manifest_v1.md",
        "docs/cosmology_activation_rule_manifest_v1.md",
        "docs/cosmology_activation_parameter_freeze_plan_v1.md",
        "docs/cosmology_source_grounding_gate_v1.md",
        "docs/source_freeze_protocol.md",
        "docs/source_selection_audit_001.md",
        "scripts/validate_source_freeze.py",
        "scripts/validate_cosmology_channel_manifest_v1.py",
        "scripts/validate_cosmology_activation_rule_manifest_v1.py",
        "scripts/validate_cosmology_activation_parameter_freeze_plan_v1.py",
        "scripts/validate_cosmology_source_grounding_gate_v1.py",
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
        "scripts/run_pantheon_full_cov_pilot_scoring_v1.py",
        "scripts/validate_pantheon_full_cov_pilot_scoring_v1.py",
        "scripts/run_pantheon_void_web_proxy_full_cov_pilot_v1.py",
        "scripts/validate_pantheon_void_web_proxy_full_cov_pilot_v1.py",
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
    assert "Lambda-like distance behavior" in text
    assert "web/environment-dependent growth or lensing residual" in text
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
