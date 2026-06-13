#!/usr/bin/env python3
"""Validate the ACT DR6 next-source-basis design scaffold."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "source_manifest" / "act_dr6_lensing_next_source_basis_design_scaffold_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "act_dr6_lensing_next_source_basis_design_scaffold_v1_summary.csv"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    rows = read_rows(MANIFEST)
    summary_rows = read_rows(SUMMARY)
    if len(rows) != 7:
        raise SystemExit(f"expected seven design requirements, found {len(rows)}")
    if len(summary_rows) != 1:
        raise SystemExit(f"expected one summary row, found {len(summary_rows)}")

    expected_ids = {
        "ACT_NEXT_BASIS_01_PHYSICAL_K_PATH_MAPPING",
        "ACT_NEXT_BASIS_02_OPERATOR_QUOTIENT_DESCENT",
        "ACT_NEXT_BASIS_03_MASK_COVERAGE_POPULATION_POLICY",
        "ACT_NEXT_BASIS_04_SOURCE_BASIS_RECENTER_STRESS",
        "ACT_NEXT_BASIS_05_CONTROL_SUITE_PRECOMMIT",
        "ACT_NEXT_BASIS_06_CHANNEL_HANDOFF_DECISION",
        "ACT_NEXT_BASIS_07_FORBIDDEN_ENDPOINT_FIELDS",
    }
    if {row["design_requirement_id"] for row in rows} != expected_ids:
        raise SystemExit("unexpected next-source-basis requirement set")
    if any(row["artifact_id"] != "ACT_DR6_LENSING_NEXT_SOURCE_BASIS_DESIGN_SCAFFOLD_V1" for row in rows):
        raise SystemExit("unexpected artifact_id in scaffold rows")
    if any(row["endpoint_replay_allowed"] != "false" for row in rows):
        raise SystemExit("next-source-basis scaffold rows must not authorize replay")
    if any(row["endpoint_validation_claimed"] != "false" for row in rows):
        raise SystemExit("next-source-basis scaffold rows must not claim validation")
    if any("endpoint" not in row["forbidden_inputs"] for row in rows):
        raise SystemExit("each row must list endpoint-side forbidden inputs")

    summary = summary_rows[0]
    expected_summary = {
        "artifact_id": "ACT_DR6_LENSING_NEXT_SOURCE_BASIS_DESIGN_SCAFFOLD_V1",
        "status": "NEXT_SOURCE_BASIS_DESIGN_SCAFFOLD_FROZEN",
        "requirements_count": "7",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_lensing_path_weight_claimed": "false",
        "family_verdict_allowed": "false",
        "current_branch_status": "previous_ACT_branch_quarantined_control_dominated",
        "next_branch_allowed_action": "source_basis_design_and_external_review_before_any_replay",
        "verdict": "ACT_NEXT_SOURCE_BASIS_DESIGN_SCAFFOLD_FROZEN_NOT_REPLAY",
    }
    for key, expected in expected_summary.items():
        if summary.get(key) != expected:
            raise SystemExit(f"{key}: expected {expected!r}, got {summary.get(key)!r}")
    if "not replay authorization" not in summary["claim_boundary"]:
        raise SystemExit("claim boundary must say this is not replay authorization")
    if "reuse_current_endpoint_scores" not in summary["forbidden_action"]:
        raise SystemExit("forbidden actions must block reuse of current endpoint scores")


if __name__ == "__main__":
    main()
