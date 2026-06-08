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
