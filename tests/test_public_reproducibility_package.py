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
        "docs/source_freeze_protocol.md",
        "docs/source_selection_audit_001.md",
        "scripts/validate_source_freeze.py",
        "scripts/acquire_source_pages.py",
        "scripts/validate_cached_source_pages.py",
        "data/source_manifest/source_page_cache_manifest.csv",
        "data/source_manifest/paper10_product_freeze_plan.csv",
        "docs/product_freeze_plan.md",
        "scripts/validate_product_freeze_plan.py",
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
        "scripts/build_figures.py",
        "figures/fig_pantheon_pilot_branch_diagnostics.pdf",
        "paper10_submission_source/figures/fig_pantheon_pilot_branch_diagnostics.pdf",
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
    assert "figures/fig_pantheon_pilot_branch_diagnostics.pdf" in names
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
    assert "diagonal" in manifest["covariance_policy"]
    assert "diagonal_variance" in summary["covariance_regularization"]
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
