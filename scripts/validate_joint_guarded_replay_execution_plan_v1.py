#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "data/source_manifest/joint_guarded_replay_execution_plan_v1.csv"
SUMMARY = ROOT / "data/derived/joint_guarded_replay_execution_plan_v1_summary.csv"
DOC = ROOT / "docs/joint_guarded_replay_execution_plan_v1.md"
CLAIM_BOUNDARY = "joint_guarded_replay_execution_plan_not_run_not_scoring_not_validation"
REQUIRED_CONTROLS = {
    "shuffled_channel_labels",
    "wrong_channel_assignment",
    "sign_flip",
    "block_drop",
    "null_readout",
    "leakage_audit",
    "shared_statistic_control",
    "covariance_binding_control",
}
REQUIRED_CAVEATS = {
    "no_source_native_cross_probe_covariance_product",
    "block_diagonal_independence_caveated",
    "shared_sky_overlap_caveat",
    "shared_mask_selection_caveat",
    "shared_redshift_kernel_caveat",
    "shared_cosmology_nuisance_caveat",
    "shared_calibration_population_caveat",
}


def read_one(path: Path) -> dict[str, str]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    plan = read_one(PLAN)
    summary = read_one(SUMMARY)
    require(plan["status"] == "JOINT_GUARDED_REPLAY_EXECUTION_PLAN_READY_NOT_RUN", "bad plan status")
    require(summary["status"] == plan["status"], "summary status mismatch")
    require(plan["claim_boundary"] == CLAIM_BOUNDARY, "plan claim boundary mismatch")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    require(plan["execution_plan_only"] == "true", "plan must remain plan-only")
    require(summary["execution_plan_only"] == "true", "summary must remain plan-only")
    require(plan["runner_exists"] == "false", "runner must not exist yet")
    require(summary["runner_exists"] == "false", "summary runner flag mismatch")
    for row, label in [(plan, "plan"), (summary, "summary")]:
        for key in [
            "direct_execution_allowed",
            "endpoint_scoring_allowed",
            "endpoint_validation_claimed",
            "cosmological_validation_claimed",
        ]:
            require(row[key] == "false", f"{label}: {key} must be false")
    require("same_frozen_block_diagonal_statistic" in plan["statistic_rule"], "statistic rule mismatch")
    require("same_frozen_block_weights" in plan["block_weight_rule"], "block-weight rule mismatch")
    require("same_declared_block_covariance" in plan["covariance_rule"], "covariance rule mismatch")
    require(REQUIRED_CONTROLS.issubset(set(plan["required_controls"].split(";"))), "missing required controls")
    require(REQUIRED_CAVEATS.issubset(set(plan["required_caveats"].split(";"))), "missing required caveats")
    require(plan["future_runner_script"].endswith("run_joint_guarded_replay_permission_only_v1.py"), "future runner name mismatch")
    require(plan["future_validator_script"].endswith("validate_joint_guarded_replay_permission_only_v1.py"), "future validator name mismatch")
    for rel_path in plan["future_outputs"].split(";"):
        require(rel_path.startswith(("data/derived/", "docs/")), f"future output path outside derived/docs: {rel_path}")
    require(
        summary["verdict"] == "joint_guarded_replay_execution_plan_ready_not_run_not_scoring_not_validation",
        "unexpected summary verdict",
    )
    text = DOC.read_text()
    for marker in [
        "not an executable replay",
        "no endpoint scores",
        "separate execution authorization",
        CLAIM_BOUNDARY,
    ]:
        require(marker in text, f"doc missing marker: {marker}")
    print("JOINT_GUARDED_REPLAY_EXECUTION_PLAN_V1_VALIDATED status=ready_not_run")


if __name__ == "__main__":
    main()
