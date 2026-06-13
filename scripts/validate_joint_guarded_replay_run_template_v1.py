#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "data/source_manifest/joint_guarded_replay_run_template_v1.csv"
SUMMARY = ROOT / "data/derived/joint_guarded_replay_run_template_v1_summary.csv"
DOC = ROOT / "docs/joint_guarded_replay_run_template_v1.md"
CLAIM_BOUNDARY = "joint_guarded_replay_run_template_not_execution_not_scoring_not_validation"
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
REQUIRED_FORBIDDEN = {
    "endpoint_residuals",
    "new_endpoint_scores",
    "fit_improvements",
    "posterior_chains",
    "post_score_control_ranks",
    "posthoc_channel_selection",
    "posthoc_block_weight_tuning",
    "posthoc_covariance_reweighting",
    "cosmological_validation_claims",
}


def read_one(path: Path) -> dict[str, str]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def require_false(row: dict[str, str], key: str, label: str) -> None:
    if row[key] != "false":
        raise SystemExit(f"{label}: {key} must remain false")


def main() -> None:
    template = read_one(TEMPLATE)
    summary = read_one(SUMMARY)

    if template["status"] != "JOINT_GUARDED_REPLAY_RUN_TEMPLATE_READY_NOT_EXECUTED":
        raise SystemExit("unexpected template status")
    if summary["status"] != template["status"]:
        raise SystemExit("summary/template status mismatch")
    if template["claim_boundary"] != CLAIM_BOUNDARY or summary["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("claim boundary mismatch")
    if template["run_template_only"] != "true" or summary["run_template_only"] != "true":
        raise SystemExit("run_template_only must remain true")
    for row, label in [(template, "template"), (summary, "summary")]:
        for key in [
            "direct_execution_allowed",
            "endpoint_scoring_allowed",
            "endpoint_validation_claimed",
            "cosmological_validation_claimed",
        ]:
            require_false(row, key, label)

    if "same_frozen_block_diagonal_statistic" not in template["statistic_rule"]:
        raise SystemExit("statistic rule must bind the same frozen statistic")
    if "same_frozen_block_weights" not in template["block_weight_rule"]:
        raise SystemExit("block-weight rule must bind the same frozen weights")
    if "same_declared_block_covariance" not in template["covariance_rule"]:
        raise SystemExit("covariance rule must bind same covariance conditions")

    controls = set(template["required_controls"].split(";"))
    caveats = set(template["required_caveats"].split(";"))
    forbidden = set(template["forbidden_inputs"].split(";"))
    if not REQUIRED_CONTROLS.issubset(controls):
        raise SystemExit("missing mandatory controls")
    if not REQUIRED_CAVEATS.issubset(caveats):
        raise SystemExit("missing mandatory caveats")
    if not REQUIRED_FORBIDDEN.issubset(forbidden):
        raise SystemExit("missing forbidden-input markers")

    for rel_path in template["dependency_summaries"].split(";"):
        if not (ROOT / rel_path).exists():
            raise SystemExit(f"missing dependency summary: {rel_path}")

    text = DOC.read_text()
    for marker in [
        "not an executable replay",
        "not endpoint scoring",
        "not cosmological validation",
        "Candidate and controls must be evaluated",
        CLAIM_BOUNDARY,
    ]:
        if marker not in text:
            raise SystemExit(f"doc missing marker: {marker}")
    if summary["verdict"] != "joint_guarded_replay_run_template_ready_not_executed_not_scoring_not_validation":
        raise SystemExit("unexpected summary verdict")

    print("JOINT_GUARDED_REPLAY_RUN_TEMPLATE_V1_VALIDATED not_executed=true")


if __name__ == "__main__":
    main()
