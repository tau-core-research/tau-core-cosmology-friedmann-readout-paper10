#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_best_tomographic_control_source_evidence_gate_policy_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_best_tomographic_control_source_evidence_gate_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_best_tomographic_control_source_evidence_gate_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    policy = read_one(POLICY)
    row = read_one(OUT)
    summary = read_one(SUMMARY)
    require(policy["computes_new_scores"] == "false", "policy must forbid new scores")
    require(policy["endpoint_validation_claimed"] == "false", "policy must not claim validation")
    require(summary["status"] == "CONTROL_ONLY_NO_SOURCE_EVIDENCE_FOR_PHYSICAL_PROMOTION", "unexpected summary status")
    require(summary["target_operator"] == "seeded_auto_cross_shuffle_702759", "unexpected target control")
    require(summary["target_control_family"] == "auto_cross_preserving_shuffle", "unexpected target control family")
    require(summary["target_is_global_source_bin_relabel"] == "false", "target must not be a global source-bin relabel")
    require(summary["target_has_independent_source_evidence"] == "false", "target must not have independent source evidence")
    require(summary["accepted_physical_alternative_count"] == "0", "target must not be accepted as physical alternative")
    require(summary["source_systematic_candidate_count"] == "0", "target must not be promoted to source-systematic candidate")
    require(summary["control_only_count"] == "1", "target must remain control-only")
    require(summary["best_control_refutes_endpoint_signal"] == "false", "target must not refute endpoint signal")
    require(summary["best_control_blocks_validation"] == "true", "target must keep validation blocked")
    require(summary["computes_new_scores"] == "false", "summary must not compute scores")
    require(summary["uses_endpoint_residual_shape_for_source_evidence"] == "false", "no endpoint residual-shape evidence allowed")
    require(summary["endpoint_validation_claimed"] == "false", "summary must not claim validation")
    require(summary["verdict"] == "best_holdout_control_is_control_only_not_physical_alternative", "unexpected verdict")
    require(row["is_global_source_bin_relabel"] == "false", "row must not be global source-bin relabel")
    require("1-2_expected_2-3_observed_1-5" in row["global_relabel_contradictions"], "expected contradiction missing")
    require(row["accepted_as_physical_alternative"] == "false", "row must not promote physical alternative")
    require(row["endpoint_validation_claimed"] == "false", "row must not claim validation")
    print(
        "PAPER10_KIDS1000_COSEBIS_BEST_TOMOGRAPHIC_CONTROL_SOURCE_EVIDENCE_GATE_V1_VALIDATED "
        f"target={summary['target_operator']} verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()
