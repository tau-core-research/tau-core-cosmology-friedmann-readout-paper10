#!/usr/bin/env python3
from __future__ import annotations

import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper10_submission_source" / "main.tex"


def run(cmd: list[str], cwd: Path = ROOT) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, cwd=cwd, check=True)


def main() -> None:
    env = os.environ.copy()
    env.setdefault("SOURCE_DATE_EPOCH", "1780876800")
    run(["python", "scripts/validate_source_freeze.py"])
    run(["python", "scripts/validate_cosmology_channel_manifest_v1.py"])
    run(["python", "scripts/validate_cosmology_activation_rule_manifest_v1.py"])
    run(["python", "scripts/validate_cosmology_activation_parameter_freeze_plan_v1.py"])
    run(["python", "scripts/validate_cosmology_source_grounding_gate_v1.py"])
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
    run(["python", "scripts/build_figures.py"])
    print("+ tectonic paper10_submission_source/main.tex")
    subprocess.run(["tectonic", PAPER.name], cwd=PAPER.parent, env=env, check=True)
    run(["python", "scripts/build_arxiv_source.py"])
    run(["python", "-m", "pytest", "-q"])
    print("PAPER10_REPRODUCTION_COMPLETE")


if __name__ == "__main__":
    main()
