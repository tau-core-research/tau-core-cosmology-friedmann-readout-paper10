from __future__ import annotations

import csv
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
        "data/source_manifest/kids1000_cosebis_web_path_mapping_policy_v1.csv",
        "data/derived/kids1000_cosebis_web_path_mapping_readiness_v1.csv",
        "data/derived/kids1000_cosebis_web_path_mapping_readiness_v1_summary.csv",
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
        "data/source_manifest/kids1000_cosebis_path_mapping_source_preflight_policy_v1.csv",
        "data/derived/kids1000_cosebis_path_mapping_source_preflight_v1.csv",
        "data/derived/kids1000_cosebis_path_mapping_source_preflight_v1_summary.csv",
        "data/source_manifest/kids1000_cosebis_null_control_policy_v1.csv",
        "data/derived/kids1000_cosebis_null_control_readiness_v1.csv",
        "data/derived/kids1000_cosebis_null_control_readiness_v1_summary.csv",
        "data/source_manifest/kids1000_cosebis_null_control_seed_policy_v1.csv",
        "data/derived/kids1000_cosebis_null_control_seed_inventory_v1.csv",
        "data/derived/kids1000_cosebis_null_control_seed_inventory_v1_summary.csv",
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
        "docs/kids1000_cosebis_web_path_mapping_policy_v1.md",
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
        "docs/kids1000_cosebis_path_mapping_source_preflight_policy_v1.md",
        "docs/kids1000_cosebis_null_control_policy_v1.md",
        "docs/kids1000_cosebis_null_control_seed_policy_v1.md",
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
        "scripts/build_kids1000_cosebis_web_path_mapping_readiness_v1.py",
        "scripts/validate_kids1000_cosebis_web_path_mapping_readiness_v1.py",
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
        "scripts/build_kids1000_cosebis_path_mapping_source_preflight_v1.py",
        "scripts/validate_kids1000_cosebis_path_mapping_source_preflight_v1.py",
        "scripts/build_kids1000_cosebis_null_control_readiness_v1.py",
        "scripts/validate_kids1000_cosebis_null_control_readiness_v1.py",
        "scripts/build_kids1000_cosebis_null_control_seed_inventory_v1.py",
        "scripts/validate_kids1000_cosebis_null_control_seed_inventory_v1.py",
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
    assert summary["status"] == "KIDS1000_COSEBIS_THEORY_VECTOR_READINESS_BUILT_NOT_COMPUTED"
    assert summary["endpoint_scoring_allowed"] == "false"
    assert summary["current_theory_vector_computed"] == "false"
    assert summary["contains_theory_vector"] == "false"
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
    assert rows[0]["contains_theory_vector"] == "false"
    assert rows[0]["uses_kids_data_vector_values"] == "false"


def test_kids1000_cosebis_web_path_mapping_policy_is_declared_not_computed() -> None:
    with (
        ROOT / "data/source_manifest/kids1000_cosebis_web_path_mapping_policy_v1.csv"
    ).open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    assert policy["status"] == "KIDS1000_COSEBIS_WEB_PATH_MAPPING_POLICY_DECLARED_NOT_COMPUTED"
    assert policy["endpoint_scoring_allowed"] == "false"
    assert policy["current_mapping_computed"] == "false"
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
    assert summary["current_mapping_computed"] == "false"
    assert summary["contains_mapping_vector"] == "false"
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
    with (
        ROOT / "data/derived/kids1000_cosebis_web_path_mapping_readiness_v1.csv"
    ).open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 1
    assert rows[0]["contains_mapping_vector"] == "false"
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


def test_kids1000_cosebis_path_weight_construction_rule_is_not_computable() -> None:
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
    assert summary["available_factor_count"] == "2"
    assert summary["partial_available_factor_count"] == "1"
    assert summary["missing_factor_count"] == "2"
    assert summary["declared_not_computed_factor_count"] == "1"
    assert summary["declared_not_executed_factor_count"] == "1"
    assert summary["domain_rows"] == "58800"
    assert summary["path_weight_rule_computable"] == "false"
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
    assert by_factor["F_overlap"]["source_state"] == "missing"
    assert by_factor["D_path"]["source_state"] == "partial_available"
    assert by_factor["D_path"]["source_count"] == "3"
    assert by_factor["E_web"]["source_state"] == "missing"
    assert by_factor["C_norm"]["source_state"] == "declared_not_computed"
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
    assert summary["blocking_requirement_count"] == "4"
    assert summary["nonblocking_requirement_count"] == "3"
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
    assert by_req["REQ_F_OVERLAP_SOURCE"]["blocks_weight_computation"] == "true"
    assert by_req["REQ_D_PATH_SOURCE"]["blocks_weight_computation"] == "true"
    assert by_req["REQ_E_WEB_SOURCE"]["blocks_weight_computation"] == "true"
    assert by_req["REQ_C_NORM_RULE"]["blocks_weight_computation"] == "true"
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


def test_kids1000_cosebis_path_mapping_source_preflight_is_not_mapping() -> None:
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
    assert summary["status"] == "KIDS1000_COSEBIS_PATH_MAPPING_SOURCE_PREFLIGHT_BUILT_NOT_MAPPED"
    assert summary["component_count"] == "10"
    assert summary["available_component_count"] == "5"
    assert summary["partial_available_component_count"] == "1"
    assert summary["missing_component_count"] == "2"
    assert summary["declared_not_executed_component_count"] == "1"
    assert summary["declared_not_computed_component_count"] == "1"
    assert summary["target_rows"] == "300"
    assert summary["mapping_ready"] == "false"
    assert summary["endpoint_scoring_allowed"] == "false"
    assert summary["path_mapping_computed"] == "false"
    assert summary["contains_mapping_vector"] == "false"
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
        "full_path_depth_footprint_mapping",
        "web_environment_catalog",
        "null_control_seed_policy",
    }
    assert by_component["cosebis_target_rows"]["source_state"] == "available"
    assert by_component["redshift_kernel_inventory"]["source_state"] == "available"
    assert by_component["mask_observable_shell"]["source_state"] == "partial_available"
    assert by_component["mask_observable_shell"]["source_count"] == "3"
    assert by_component["preferred_route_tile_inventory"]["source_state"] == "available"
    assert by_component["preferred_route_tile_inventory"]["source_count"] == "196"
    assert by_component["cosebis_path_mapping_design_skeleton"]["source_state"] == "available"
    assert by_component["cosebis_path_mapping_design_skeleton"]["source_count"] == "300"
    assert by_component["cosebis_path_mapping_domain_skeleton"]["source_state"] == "available"
    assert by_component["cosebis_path_mapping_domain_skeleton"]["source_count"] == "58800"
    assert by_component["path_weight_construction_rule"]["source_state"] == "declared_not_computed"
    assert by_component["path_weight_construction_rule"]["source_count"] == "7"
    assert by_component["full_path_depth_footprint_mapping"]["source_state"] == "missing"
    assert by_component["full_path_depth_footprint_mapping"]["blocking_status"] == "blocking"
    assert by_component["web_environment_catalog"]["source_state"] == "missing"
    assert by_component["web_environment_catalog"]["blocking_status"] == "blocking"
    assert by_component["null_control_seed_policy"]["source_state"] == "declared_not_executed"
    assert by_component["null_control_seed_policy"]["source_count"] == "1008"
    for row in rows:
        assert row["target_rows"] == "300"
        assert row["path_mapping_computed"] == "false"
        assert row["contains_mapping_vector"] == "false"
        assert row["contains_theory_vector"] == "false"
        assert row["contains_predictions"] == "false"
        assert row["contains_residuals"] == "false"
        assert row["uses_kids_data_vector_values"] == "false"
        assert row["endpoint_scoring_allowed"] == "false"


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
    assert summary["status"] == "KIDS1000_COSEBIS_NULL_CONTROL_READINESS_BUILT_NOT_RUN"
    assert summary["endpoint_scoring_allowed"] == "false"
    assert summary["current_controls_executed"] == "false"
    assert summary["contains_control_scores"] == "false"
    assert summary["contains_predictions"] == "false"
    assert summary["contains_residuals"] == "false"
    assert summary["contains_fit_statistics"] == "false"
    assert summary["uses_kids_data_vector_values"] == "false"
    assert summary["uses_posterior_chains"] == "false"
    assert summary["uses_posthoc_control_selection"] == "false"
    assert summary["target_rows"] == "300"
    assert summary["control_family_count"] == "4"
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
    assert {row["control_status"] for row in rows} == {"DECLARED_NOT_RUN"}
    assert {row["requires_seed_policy"] for row in rows} == {"true"}
    assert {row["contains_control_scores"] for row in rows} == {"false"}


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
