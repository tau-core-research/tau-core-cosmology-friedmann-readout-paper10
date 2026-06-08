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
    run(["python", "scripts/validate_cached_source_pages.py"])
    run(["python", "scripts/validate_product_freeze_plan.py"])
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
    run(["python", "scripts/build_figures.py"])
    print("+ tectonic paper10_submission_source/main.tex")
    subprocess.run(["tectonic", PAPER.name], cwd=PAPER.parent, env=env, check=True)
    run(["python", "scripts/build_arxiv_source.py"])
    run(["python", "-m", "pytest", "-q"])
    print("PAPER10_REPRODUCTION_COMPLETE")


if __name__ == "__main__":
    main()
